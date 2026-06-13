#!/usr/bin/env python3
"""
发送测试报告邮件的脚本
供 GitHub Actions 工作流调用

需要的环境变量（由 GitHub Secrets 传入）:
  HOST_QQ     - SMTP 服务器地址（如 smtp.qq.com）
  PORT_QQ     - SMTP 服务器端口（如 465）
  USERNAME_QQ - QQ 邮箱地址（如 123456@qq.com）
  PASSWORD_QQ - QQ 邮箱 SMTP 授权码
  MAIL_TO     - 收件人地址（可选，默认发给自己）
  BRANCH      - 分支名（可选，用于邮件主题）
  COMMIT_HASH - 提交哈希（可选，用于邮件主题）

依赖:
  Python 标准库 smtplib / email，无需额外安装
"""

import os
import smtplib
import socket
import ssl
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime


def get_env_or(key: str, default: str = "") -> str:
    """安全获取环境变量"""
    return os.environ.get(key, default)


def load_html_body(file_path: str = "email_body.html") -> str:
    """加载由 generate_email.py 生成的 HTML 邮件内容"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"""
        <html>
        <body>
        <h2>CRMEB UI 自动化测试报告</h2>
        <p>生成时间: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        <p>详细报告请查看 GitHub Actions 运行结果。</p>
        </body>
        </html>
        """
    except Exception as e:
        print(f"[ERROR] 加载邮件模板失败: {e}")
        return "<html><body><p>报告内容加载失败</p></body></html>"


def get_test_summary(html_body: str) -> str:
    """从 HTML 中提取测试概要作为邮件主题的一部分"""
    import re
    status_match = re.search(
        r'status_text["\']?\s*[:=]\s*["\']?([^"\'<]+)', html_body
    )
    return status_match.group(1).strip() if status_match else "测试完成"


def try_connect(method: str, smtp_host: str, smtp_port: int,
                smtp_user: str, smtp_pass: str, mail_to: str,
                msg) -> bool:
    """
    尝试用指定方式连接并发送邮件
    method: 'ssl' 或 'tls'
    """
    timeout = 15  # 统一使用 15 秒超时，避免长时间卡住
    print(f"[INFO] 尝试 {method.upper()} 连接 {smtp_host}:{smtp_port} (超时 {timeout}s)...")

    try:
        if method == "ssl":
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=timeout, context=context)
        elif method == "tls":
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=timeout)
            server.ehlo()
            server.starttls()
            server.ehlo()
        else:
            print(f"[WARN] {method.upper()} 不支持的连接方式")
            return False

        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, mail_to.split(","), msg.as_string())
        server.quit()
        print(f"[SUCCESS] {method.upper()} 发送成功 -> {mail_to}")
        return True

    except smtplib.SMTPAuthenticationError:
        print(f"[ERROR] {method.upper()} 认证失败，请检查 USERNAME_QQ 和 PASSWORD_QQ")
        print("  - 对于 QQ 邮箱，PASSWORD_QQ 应使用 SMTP 授权码，而非登录密码")
        print("  - 授权码获取: QQ邮箱 → 设置 → 账户 → POP3/SMTP服务 → 生成授权码")
        return False
    except (socket.timeout, smtplib.SMTPConnectError, ConnectionRefusedError,
            OSError, TimeoutError, TimeoutError) as e:
        print(f"[WARN] {method.upper()} 连接失败 ({type(e).__name__})，跳过此策略")
        return False
    except Exception as e:
        print(f"[WARN] {method.upper()} 错误: {type(e).__name__}: {e}")
        return False


def send_email() -> None:
    """主函数: 读取环境变量并发送邮件"""

    # ========== 读取配置 ==========
    smtp_host = get_env_or("HOST_QQ", "smtp.qq.com")
    smtp_port_str = get_env_or("PORT_QQ", "465")
    smtp_user = get_env_or("USERNAME_QQ", "")
    smtp_pass = get_env_or("PASSWORD_QQ", "")
    mail_to = get_env_or("MAIL_TO", smtp_user)

    # ========== 参数校验 ==========
    if not smtp_user or not smtp_pass:
        print("[WARNING] 邮箱配置不完整 (USERNAME_QQ 或 PASSWORD_QQ 为空)，跳过邮件发送")
        return

    try:
        smtp_port = int(smtp_port_str)
    except ValueError:
        print(f"[ERROR] PORT_QQ 格式错误: {smtp_port_str}，使用默认端口 465")
        smtp_port = 465

    # ========== 构建邮件 ==========
    html_body = load_html_body()
    test_status = get_test_summary(html_body)

    branch = get_env_or("BRANCH", "unknown")
    commit_hash = get_env_or("COMMIT_HASH", "unknown")[:8]

    msg = MIMEMultipart("alternative")
    msg["From"] = f"CRMEB 自动化测试 <{smtp_user}>"
    msg["To"] = mail_to
    subject = (
        f"[CRMEB UI Test] {test_status}"
        f" - {branch} ({commit_hash})"
        f" - {datetime.now().strftime('%m-%d %H:%M')}"
    )
    msg["Subject"] = Header(subject, "utf-8")
    msg["X-Priority"] = "3"

    html_part = MIMEText(html_body, "html", "utf-8")
    msg.attach(html_part)

    # ========== 打印配置 ==========
    print("=" * 60)
    print("邮件发送配置:")
    print(f"  服务器: {smtp_host}")
    print(f"  配置端口: {smtp_port}")
    print(f"  发件人: {smtp_user}")
    print(f"  收件人: {mail_to}")
    print(f"  主题: {subject}")
    print("=" * 60)

    # ========== 多策略自动回退 ==========
    # 只尝试主流的 SSL 465 和 TLS 587 端口
    # 25 端口在云环境（GitHub Actions）中几乎都被屏蔽，跳过以避免长时间卡住
    config_method = "ssl" if smtp_port == 465 else "tls"
    strategies = [
        (config_method, smtp_port),  # 使用配置的端口
    ]
    # 如果配置的端口不是标准端口，补充标准端口尝试
    if smtp_port != 465:
        strategies.append(("ssl", 465))
    if smtp_port != 587:
        strategies.append(("tls", 587))

    # 去重: 跳过已尝试过的 (method, port) 组合
    tried = set()

    print(f"\n>>> 开始尝试发送邮件，共 {len(strategies)} 种策略...")
    for idx, (method, port) in enumerate(strategies, 1):
        key = (method, port)
        if key in tried:
            continue
        tried.add(key)

        print(f">>> 策略 {idx}/{len(strategies)}: {method.upper()} {smtp_host}:{port}")
        time.sleep(0.5)  # 避免触发限流
        if try_connect(method, smtp_host, port, smtp_user, smtp_pass, mail_to, msg):
            print(f"\n{'=' * 60}")
            print("✅ 邮件发送成功！")
            print(f"{'=' * 60}")
            return

    # ========== 全部失败 ==========
    print(f"\n{'=' * 60}")
    print("❌ 所有发送策略均失败")
    print(f"{'=' * 60}")
    print("")
    print("可能的原因和解决方法:")
    print("1. 网络环境限制：GitHub Actions 无法连接 QQ 邮箱 SMTP")
    print("   - 这是常见问题，建议换用其他邮件服务:")
    print("     • SendGrid: HOST_QQ=smtp.sendgrid.net, PORT_QQ=465, PASSWORD_QQ=API Key")
    print("     • Mailgun:  HOST_QQ=smtp.mailgun.org, PORT_QQ=465")
    print("     • 阿里云邮件推送: HOST_QQ=smtpdm.aliyun.com, PORT_QQ=465")
    print("2. 端口被屏蔽")
    print("   - 检查 PORT_QQ 是否可访问 (QQ 邮箱推荐 465 SSL)")
    print("3. 认证信息错误")
    print("   - PASSWORD_QQ 必须为 SMTP 授权码（非邮箱登录密码）")


if __name__ == "__main__":
    send_email()
