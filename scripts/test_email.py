"""
临时测试脚本：验证 generate_email.py 是否能正确生成邮件 HTML
"""
import os
import sys
import pathlib

# 切换到项目根目录
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置测试环境变量
os.environ['BRANCH'] = 'main'
os.environ['COMMIT_HASH'] = 'abc123def456'
os.environ['COMMIT_AUTHOR'] = 'testuser'
os.environ['COMMIT_MSG'] = 'test commit msg'
os.environ['TEST_STATUS'] = 'COMPLETED'
os.environ['TEST_TIME'] = '2024-01-01 12:00:00'
os.environ['GITHUB_REPOSITORY'] = 'test/repo'
os.environ['GITHUB_SERVER_URL'] = 'https://github.com'
os.environ['GITHUB_RUN_ID'] = '123456'

results = []

# 执行 generate_email.py
try:
    exec(open('scripts/generate_email.py').read())
    results.append('generate_email.py 执行成功')
except Exception as e:
    results.append(f'generate_email.py 执行失败: {e}')

# 验证文件是否生成
p = pathlib.Path('email_body.html')
if p.exists():
    results.append(f'email_body.html 已生成，大小: {p.stat().st_size} 字节')
    content = p.read_text(encoding='utf-8')
    results.append(f'包含 DOCTYPE: {"<!DOCTYPE html>" in content}')
    results.append(f'包含状态: {"✅ 通过" in content}')
    results.append(f'包含分支: {"main" in content}')
    results.append(f'包含报告链接: {"https://github.com/test/repo/actions/runs/123456" in content}')
    # 清理
    p.unlink()
    results.append('临时文件已清理')
else:
    results.append('错误: email_body.html 未生成')

# 写结果到文件
with open('test_verify_result.txt', 'w', encoding='utf-8') as f:
    for r in results:
        f.write(r + '\n')
    f.write('ALL CHECKS COMPLETED\n')
