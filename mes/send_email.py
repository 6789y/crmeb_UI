"""
发送测试报告邮件
从环境变量中读取邮箱配置和邮件 HTML 内容，通过 SMTP 发送邮件
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def get_env(key, default=''):
    """安全获取环境变量"""
    return os.environ.get(key, default)


def send_email():
    """发送测试报告邮件"""
    # 读取邮箱配置（从环境变量）
    mail_username = get_env('MAIL_USERNAME')
    mail_password = get_env('MAIL_PASSWORD')
    mail_to = get_env('MAIL_TO', mail_username)  # 默认发送给自己

    # 读取邮件 HTML 内容
    email_body_path = 'email_body.html'
    if not os.path.exists(email_body_path):
        print(f">>> [ERROR] 邮件 HTML 文件不存在: {email_body_path}")
        print(">>> 请先执行 generate_email.py 生成邮件内容")
        return False

    with open(email_body_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 读取其他信息
    branch = get_env('BRANCH', 'unknown')
    test_status = get_env('TEST_STATUS', 'UNKNOWN')
    test_total = get_env('TEST_TOTAL', '0')
    test_passed = get_env('TEST_PASSED', '0')

    # 计算通过率
    total_int = int(test_total) if test_total.isdigit() else 0
    passed_int = int(test_passed) if test_passed.isdigit() else 0
    if total_int > 0:
        pass_rate = (passed_int / total_int) * 100
        pass_rate_str = f'{pass_rate:.1f}%'
    else:
        pass_rate_str = 'N/A'

    # 构建邮件主题
    if test_status == 'COMPLETED':
        subject_prefix = '✅ 通过'
    elif test_status == 'FAILED':
        subject_prefix = '❌ 失败'
    else:
        subject_prefix = '⚠️ 报告'

    subject = f'{subject_prefix} CRMEB UI 自动化测试报告 - {branch} ({test_passed}/{test_total} {pass_rate_str})'

    # 构建邮件
    msg = MIMEMultipart('alternative')
    msg['From'] = mail_username
    msg['To'] = mail_to
    msg['Subject'] = Header(subject, 'utf-8')

    # 添加 HTML 内容
    html_part = MIMEText(html_content, 'html', 'utf-8')
    msg.attach(html_part)

    # 发送邮件
    try:
        # 自动识别邮箱类型并设置 SMTP 服务器
        if 'qq.com' in mail_username:
            smtp_host = 'smtp.qq.com'
            smtp_port = 465
            use_ssl = True
        elif '163.com' in mail_username:
            smtp_host = 'smtp.163.com'
            smtp_port = 465
            use_ssl = True
        elif 'gmail.com' in mail_username:
            smtp_host = 'smtp.gmail.com'
            smtp_port = 587
            use_ssl = False
        elif 'outlook.com' in mail_username or 'hotmail.com' in mail_username:
            smtp_host = 'smtp.office365.com'
            smtp_port = 587
            use_ssl = False
        else:
            # 默认使用 QQ 邮箱 SMTP
            smtp_host = 'smtp.qq.com'
            smtp_port = 465
            use_ssl = True

        print(f">>> [INFO] SMTP 服务器: {smtp_host}:{smtp_port} (SSL: {use_ssl})")
        print(f">>> [INFO] 发件人: {mail_username}")
        print(f">>> [INFO] 收件人: {mail_to}")

        if use_ssl:
            # SSL 方式连接（端口 465）
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
                server.login(mail_username, mail_password)
                server.sendmail(mail_username, [mail_to], msg.as_string())
        else:
            # STARTTLS 方式连接（端口 587）
            with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
                server.starttls()
                server.login(mail_username, mail_password)
                server.sendmail(mail_username, [mail_to], msg.as_string())

        print(f">>> [OK] 邮件发送成功!")
        print(f">>> 收件人: {mail_to}")
        return True

    except smtplib.SMTPAuthenticationError:
        print(f">>> [ERROR] SMTP 认证失败，请检查邮箱地址和授权码是否正确")
        print(f">>> 提示: 对于 QQ 邮箱，请在邮箱设置中生成 SMTP 授权码，而非使用登录密码")
        return False
    except smtplib.SMTPException as e:
        print(f">>> [ERROR] SMTP 发送失败: {e}")
        return False
    except Exception as e:
        print(f">>> [ERROR] 发送邮件时发生未知错误: {e}")
        return False


def main():
    """主函数"""
    print(">>> [INFO] 开始发送测试报告邮件...")
    success = send_email()
    if success:
        print(">>> [DONE] 邮件发送流程完成")
    else:
        print(">>> [FAILED] 邮件发送失败")
        exit(1)


if __name__ == '__main__':
    main()