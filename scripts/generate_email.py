"""
生成邮件 HTML 内容
从环境变量中读取测试结果信息，生成格式化的 HTML 邮件正文
"""
import os
import html

def get_env(key, default=''):
    """安全获取环境变量"""
    return os.environ.get(key, default)


def generate_email_html():
    """生成邮件 HTML 内容"""
    # 读取环境变量
    branch = get_env('BRANCH')
    commit_hash = get_env('COMMIT_HASH', 'unknown')[:8]
    commit_author = get_env('COMMIT_AUTHOR')
    commit_msg = get_env('COMMIT_MSG')
    test_status = get_env('TEST_STATUS', 'UNKNOWN')
    test_time = get_env('TEST_TIME')
    github_repository = get_env('GITHUB_REPOSITORY')
    github_server_url = get_env('GITHUB_SERVER_URL', 'https://github.com')
    github_run_id = get_env('GITHUB_RUN_ID')

    # 构建报告链接
    report_url = f"{github_server_url}/{github_repository}/actions/runs/{github_run_id}"

    # 根据测试状态设置颜色
    if test_status == 'COMPLETED':
        status_color = '#28a745'
        status_text = '✅ 通过'
    elif test_status == 'FAILED':
        status_color = '#dc3545'
        status_text = '❌ 失败'
    else:
        status_color = '#ffc107'
        status_text = '⚠️ 未知'

    # 构建 HTML 内容
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #f6f8fa;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .header {{
            background-color: {status_color};
            color: #ffffff;
            padding: 24px 32px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 22px;
            font-weight: 600;
        }}
        .header p {{
            margin: 8px 0 0;
            font-size: 14px;
            opacity: 0.9;
        }}
        .body {{
            padding: 24px 32px;
        }}
        .status-badge {{
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            background-color: {status_color};
            margin-bottom: 20px;
        }}
        .info-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        .info-table th,
        .info-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #e1e4e8;
            text-align: left;
            font-size: 14px;
        }}
        .info-table th {{
            width: 100px;
            color: #586069;
            font-weight: 500;
        }}
        .info-table td {{
            color: #24292e;
        }}
        .commit-msg {{
            background-color: #f6f8fa;
            border-radius: 6px;
            padding: 12px 16px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 13px;
            color: #24292e;
            margin-bottom: 20px;
            word-break: break-all;
        }}
        .footer {{
            padding: 16px 32px;
            text-align: center;
            font-size: 12px;
            color: #586069;
            border-top: 1px solid #e1e4e8;
        }}
        .btn {{
            display: inline-block;
            padding: 10px 24px;
            background-color: #0366d6;
            color: #ffffff;
            text-decoration: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            margin-top: 16px;
        }}
        .btn:hover {{
            background-color: #0256b9;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CRMEB UI 自动化测试报告</h1>
            <p>{test_time}</p>
        </div>
        <div class="body">
            <div class="status-badge">{status_text}</div>

            <table class="info-table">
                <tr>
                    <th>分支</th>
                    <td>{html.escape(branch)}</td>
                </tr>
                <tr>
                    <th>提交</th>
                    <td><code>{html.escape(commit_hash)}</code></td>
                </tr>
                <tr>
                    <th>触发者</th>
                    <td>{html.escape(commit_author)}</td>
                </tr>
                <tr>
                    <th>测试时间</th>
                    <td>{html.escape(test_time)}</td>
                </tr>
            </table>

            <div style="font-size:14px;font-weight:500;margin-bottom:8px;color:#24292e;">提交信息</div>
            <div class="commit-msg">{html.escape(commit_msg)}</div>

            <div style="text-align:center;">
                <a href="{report_url}" class="btn" target="_blank">查看详细报告</a>
            </div>
        </div>
        <div class="footer">
            <p>此邮件由 CRMEB UI 自动化测试 CI 自动生成</p>
        </div>
    </div>
</body>
</html>
"""
    return html_content


def main():
    """主函数：生成邮件 HTML 并写入文件"""
    html_content = generate_email_html()

    output_path = 'email_body.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f">>> [OK] 邮件 HTML 已生成: {output_path}")
    print(f">>> 文件大小: {len(html_content)} 字节")


if __name__ == '__main__':
    main()
