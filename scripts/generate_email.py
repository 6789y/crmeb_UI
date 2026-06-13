#!/usr/bin/env python3
"""
生成 HTML 邮件内容的脚本
供 GitHub Actions 工作流调用
"""
import json
import os
from html import escape
from datetime import datetime


def get_env_or(key, default=""):
    """安全获取环境变量"""
    return os.environ.get(key, default)


def count_status_in_report(report_dir: str):
    """
    从 Allure 原始报告目录中统计测试结果
    返回 (total, passed, failed, broken)
    """
    total = 0
    passed = 0
    failed = 0
    broken = 0

    if not os.path.isdir(report_dir):
        return total, passed, failed, broken

    for root, dirs, files in os.walk(report_dir):
        for f in files:
            if not f.endswith('.json'):
                continue
            filepath = os.path.join(root, f)
            try:
                with open(filepath, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                    total += content.count('"status"')
                    passed += content.count('"status":"passed"')
                    failed += content.count('"status":"failed"')
                    broken += content.count('"status":"broken"')
            except Exception:
                pass

    return total, passed, failed, broken


def build_html_email():
    """构建 HTML 邮件内容"""

    # ========== 从环境变量获取数据 ==========
    branch = get_env_or('BRANCH', 'unknown')
    commit_hash = get_env_or('COMMIT_HASH', 'unknown')
    commit_author = get_env_or('COMMIT_AUTHOR', 'unknown')
    commit_msg = get_env_or('COMMIT_MSG', 'No commit message')
    test_status = get_env_or('TEST_STATUS', 'FAILED')
    test_time = get_env_or('TEST_TIME', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'))
    github_repo = get_env_or('GITHUB_REPOSITORY', 'unknown')
    github_server = get_env_or('GITHUB_SERVER_URL', 'https://github.com')
    github_run_id = get_env_or('GITHUB_RUN_ID', '0')

    # ========== 统计测试结果 ==========
    total, passed, failed, broken = count_status_in_report('raw-report')

    # ========== 状态判断 ==========
    if test_status == 'COMPLETED':
        status_icon = '&#9989;'
        status_text = '测试完成'
        status_color = '#28a745'
        status_msg = '所有测试用例已执行完毕'
    else:
        status_icon = '&#10060;'
        status_text = '测试异常'
        status_color = '#dc3545'
        status_msg = '测试执行过程中出现异常，请查看详细日志'

    # ========== 生成 HTML ==========
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CRMEB 自动化测试报告</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, 'Segoe UI', Arial, 'Microsoft YaHei', sans-serif; margin: 0; padding: 0; background-color: #f5f5f5; }}
    .container {{ max-width: 700px; margin: 20px auto; background: #ffffff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); overflow: hidden; }}
    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px 40px; text-align: center; }}
    .header h2 {{ color: #fff; margin: 0; font-size: 24px; letter-spacing: 1px; }}
    .header p {{ color: rgba(255,255,255,0.85); margin: 8px 0 0 0; font-size: 14px; }}
    .body-content {{ padding: 30px 40px; }}
    .section {{ margin-bottom: 25px; }}
    .section-title {{ font-size: 16px; font-weight: 600; color: #333; border-bottom: 2px solid #f0f0f0; padding-bottom: 8px; margin-bottom: 15px; }}
    .status-badge {{ display: inline-block; padding: 6px 20px; border-radius: 20px; font-size: 14px; font-weight: 600; color: #fff; }}
    .status-msg {{ font-size: 13px; color: #888; margin-top: 8px; }}
    table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
    th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #eee; font-size: 14px; }}
    th {{ background-color: #f8f9fa; font-weight: 600; color: #555; width: 120px; }}
    td {{ color: #333; }}
    tr:last-child td {{ border-bottom: none; }}
    .stats-grid {{ display: flex; gap: 15px; margin: 15px 0; flex-wrap: wrap; }}
    .stat-card {{ flex: 1; min-width: 100px; padding: 15px; border-radius: 8px; text-align: center; background: #f8f9fa; }}
    .stat-card .number {{ font-size: 28px; font-weight: 700; margin: 5px 0; }}
    .stat-card .label {{ font-size: 12px; color: #888; }}
    .stat-card.total {{ border-top: 3px solid #667eea; }}
    .stat-card.passed {{ border-top: 3px solid #28a745; }}
    .stat-card.passed .number {{ color: #28a745; }}
    .stat-card.failed {{ border-top: 3px solid #dc3545; }}
    .stat-card.failed .number {{ color: #dc3545; }}
    .stat-card.broken {{ border-top: 3px solid #ffc107; }}
    .stat-card.broken .number {{ color: #ffc107; }}
    .btn-link {{ display: inline-block; padding: 10px 24px; background: #667eea; color: #fff; text-decoration: none; border-radius: 6px; font-size: 14px; }}
    .btn-link:hover {{ background: #5a6fd6; }}
    .footer {{ text-align: center; padding: 20px 40px; background: #f8f9fa; color: #999; font-size: 12px; border-top: 1px solid #eee; }}
    .footer a {{ color: #667eea; text-decoration: none; }}
    code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 13px; color: #d63384; }}
    .env-grid {{ display: flex; gap: 10px; margin: 10px 0; flex-wrap: wrap; }}
    .env-tag {{ display: inline-block; padding: 4px 12px; background: #e8f0fe; color: #1a73e8; border-radius: 4px; font-size: 12px; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h2>&#129514; CRMEB UI 自动化测试报告</h2>
      <p>{escape(github_repo)}</p>
    </div>
    <div class="body-content">
      <!-- 提交信息 -->
      <div class="section">
        <div class="section-title">&#128221; 提交信息</div>
        <table>
          <tr><th>分支</th><td><code>{escape(branch)}</code></td></tr>
          <tr><th>提交 ID</th><td><code>{escape(commit_hash)}</code></td></tr>
          <tr><th>作者</th><td>{escape(commit_author)}</td></tr>
          <tr><th>提交信息</th><td style="max-width:300px;word-break:break-all;">{escape(commit_msg)}</td></tr>
        </table>
      </div>

      <!-- 测试执行结果 -->
      <div class="section">
        <div class="section-title">&#128202; 测试执行结果</div>
        <div style="display:flex;align-items:center;gap:15px;margin-bottom:15px;">
          <span class="status-badge" style="background:{status_color};">{status_icon} {status_text}</span>
          <span style="color:#888;font-size:14px;">{escape(test_time)}</span>
        </div>
        <div class="status-msg">{status_msg}</div>
        <div class="stats-grid">
          <div class="stat-card total">
            <div class="label">总计</div>
            <div class="number">{total}</div>
          </div>
          <div class="stat-card passed">
            <div class="label">通过</div>
            <div class="number">{passed}</div>
          </div>
          <div class="stat-card failed">
            <div class="label">失败</div>
            <div class="number">{failed}</div>
          </div>
          <div class="stat-card broken">
            <div class="label">中断</div>
            <div class="number">{broken}</div>
          </div>
        </div>
        <div class="env-grid">
          <span class="env-tag">Playwright</span>
          <span class="env-tag">pytest</span>
          <span class="env-tag">Allure</span>
          <span class="env-tag">Python 3.10</span>
        </div>
      </div>

      <!-- 相关链接 -->
      <div class="section">
        <div class="section-title">&#128279; 相关链接</div>
        <a class="btn-link" href="{github_server}/{github_repo}/actions/runs/{github_run_id}" target="_blank">
          查看 GitHub Actions 运行详情 &rarr;
        </a>
        <p style="margin-top:12px;font-size:13px;color:#888;">
          Allure 测试报告已作为 Artifact 上传，请在工作流运行页面下载
          <code>allure-report-3.10</code> 查看详细报告。
        </p>
      </div>
    </div>
    <div class="footer">
      <p>此邮件由 <a href="{github_server}/{github_repo}/actions">GitHub Actions</a> 自动生成</p>
      <p>CRMEB UI 自动化测试项目 &middot; Powered by Playwright + pytest + Allure</p>
    </div>
  </div>
</body>
</html>'''

    # ========== 写入文件 ==========
    output_path = 'email_body.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"邮件内容已生成: {output_path}")
    return output_path


if __name__ == '__main__':
    build_html_email()
