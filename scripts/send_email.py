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

依赖:
  Python 标准库 smtplib / email，无需额外安装
"""

import os
import smtplib
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
        # 如果没有邮件模板，生成一个简单的纯文本报告
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
    # 尝试提取测试状态
    status_match = re.search(
        r'status_text["\']?\s*[:=]\s*["\']?([^"\'<]+)', html_body
    )
    status = status_match.group(1).strip() if status_match else "测试完成"
    return status


def send_email() -> None:
    """主函数: 读取环境变量并发送邮件"""

    # ========== 读取配置 ==========
    smtp_host = get_env_or("HOST_QQ", "smtp.qq.com")
    smtp_port_str = get_env_or("PORT_QQ", "465")
    smtp_user = get_env_or("USERNAME_QQ", "")
    smtp_pass = get_env_or("PASSWORD_QQ", "")
    mail_to = get_env_or("MAIL_TO", smtp_user)  # 默认发送给自己

    # ========== 参数校验 ==========
    if not smtp_user or not smtp_pass:
        print("[WARNING] 邮箱配置不完整 (USERNAME_QQ 或 PASSWORD_QQ 为空)，跳过邮件发送")
        print(f"  HOST_QQ={smtp_host}, PORT_QQ={smtp_port_str}, USERNAME_QQ={'*' * max(0, len(smtp_user) - 4) + smtp_user[-4:] if smtp_user else '(空)'}")
        return

    try:
        smtp_port = int(smtp_port_str)
    except ValueError:
        print(f"[ERROR] PORT_QQ 格式错误: {smtp_port_str}，使用默认端口 465")
        smtp_port = 465

    # ========== 构建邮件 ==========
    html_body = load_html_body()
    test_status = get_test_summary(html_body)

    # 获取提交信息用于邮件主题
    branch = get_env_or("BRANCH", "unknown")
    commit_hash = get_env_or("COMMIT_HASH", "unknown")[:8]

    # 创建 multipart 邮件对象
    msg = MIMEMultipart("alternative")
    msg["From"] = f"CRMEB 自动化测试 <{smtp_user}>"
    msg["To"] = mail_to
    subject = f"[CRMEB UI Test] {test_status} - {branch} ({commit_hash}) - {datetime.utcnow().strftime('%m-%d %H:%M')}"
    msg["Subject"] = Header(subject, "utf-8")
    msg["X-Priority"] = "3"  # 正常优先级

    # 添加 HTML 正文
    html_part = MIMEText(html_body, "html", "utf-8")
    msg.attach(html_part)

    # ========== 发送邮件 ==========
    print("=" * 60)
    print("邮件发送配置:")
    print(f"  服务器: {smtp_host}:{smtp_port}")
    print(f"  发件人: {smtp_user}")
    print(f"  收件人: {mail_to}")
    print(f"  主题: {subject}")
    print("=" * 60)

    try:
        if smtp_port == 465:
            # SSL 方式 (QQ 邮箱推荐)
            print("[INFO] 使用 SSL 方式连接...")
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, mail_to.split(","), msg.as_string())
        else:
            # TLS 方式 (587 或其它端口)
            print(f"[INFO] 使用 TLS 方式连接 (端口 {smtp_port})...")
            with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, mail_to.split(","), msg.as_string())

        print(f"[SUCCESS] 邮件发送成功 -> {mail_to}")

    except smtplib.SMTPAuthenticationError:
        print("[ERROR] SMTP 认证失败，请检查 USERNAME_QQ 和 PASSWORD_QQ")
        print("  - 对于 QQ 邮箱，PASSWORD_QQ 应使用 SMTP 授权码，而非登录密码")
        print("  - 授权码获取方式: QQ邮箱 -> 设置 -> 账户 -> 生成授权码")
    except smtplib.SMTPConnectError:
        print(f"[ERROR] 无法连接到 SMTP 服务器 {smtp_host}:{smtp_port}")
        print("  - 请检查 HOST_QQ 和 PORT_QQ 是否正确")
    except smtplib.SMTPSenderRefused:
        print(f"[ERROR] 发件人被拒绝: {smtp_user}")
    except smtplib.SMTPRecipientsRefused:
        print(f"[ERROR] 收件人被拒绝: {mail_to}")
    except smtplib.SMTPException as e:
        print(f"[ERROR] SMTP 错误: {e}")
    except Exception as e:
        print(f"[ERROR] 未知错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    send_email()
