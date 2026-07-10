"""
从 pytest 输出日志中提取用例统计信息
用于 CI 工作流中替代脆弱的 sed 正则解析

用法: python mes/parse_test_stats.py <test_output.log> <output_file>

特性:
- 优先解析 pytest summary 行 (如 "= 1 failed, 7 passed, 1 rerun in 162.94s =")
- 如果 summary 行不存在，回退到按行统计 PASSED/FAILED/SKIPPED/ERROR 关键字
- 日志文件不存在时静默退出（不报错）
"""
import re
import sys
from pathlib import Path


def find_int(pattern, text):
    """从文本中提取第一个匹配的数字，未匹配返回 0"""
    m = re.search(pattern, text)
    if m:
        return int(m.group(1))
    return 0


def parse_test_stats(log_path: str) -> dict:
    """从 pytest 输出日志中提取用例统计"""
    log_file = Path(log_path)
    if not log_file.exists():
        print(f'>>> [WARNING] 日志文件不存在: {log_path}')
        return {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0, 'errors': 0}

    text = log_file.read_text(encoding='utf-8', errors='ignore')

    # 方法1: 解析 pytest summary 行
    # 格式: "= 1 failed, 7 passed, 1 rerun in 162.94s (0:02:42) ="
    # 注意: 使用 [ \t]+ 而非 \s+，防止跨行匹配（如 "12345678\nPASSED"）
    passed = find_int(r'(\d+)[ \t]+passed', text)
    failed = find_int(r'(\d+)[ \t]+failed', text)
    skipped = find_int(r'(\d+)[ \t]+skipped', text)
    errors = find_int(r'(\d+)[ \t]+error', text)  # 匹配 error 和 errors

    # 如果 summary 行解析到数据，直接返回
    if passed + failed + skipped + errors > 0:
        total = passed + failed + skipped + errors
        print(f'>>> 用例统计(summary): 总计={total}, 通过={passed}, 失败={failed}, 跳过={skipped}, 错误={errors}')
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'errors': errors,
        }

    # 方法2: 回退到按行统计关键字
    passed = len(re.findall(r'(^|\s)PASSED($|\s)', text, flags=re.M))
    failed = len(re.findall(r'(^|\s)FAILED($|\s)', text, flags=re.M))
    skipped = len(re.findall(r'(^|\s)SKIPPED($|\s)', text, flags=re.M))
    errors = len(re.findall(r'(^|\s)ERROR($|\s)', text, flags=re.M))

    total = passed + failed + skipped + errors
    print(f'>>> 用例统计(行数): 总计={total}, 通过={passed}, 失败={failed}, 跳过={skipped}, 错误={errors}')
    return {
        'total': total,
        'passed': passed,
        'failed': failed,
        'skipped': skipped,
        'errors': errors,
    }


def main():
    if len(sys.argv) < 3:
        print('用法: python mes/parse_test_stats.py <test_output.log> <output_file>')
        sys.exit(1)

    log_path = sys.argv[1]
    output_path = sys.argv[2]

    stats = parse_test_stats(log_path)

    # 输出到文件（追加模式，兼容 GITHUB_OUTPUT）
    with open(output_path, 'a', encoding='utf-8') as f:
        f.write(f'total={stats["total"]}\n')
        f.write(f'passed={stats["passed"]}\n')
        f.write(f'failed={stats["failed"]}\n')
        f.write(f'skipped={stats["skipped"]}\n')
        f.write(f'errors={stats["errors"]}\n')

    print(f'>>> 统计结果已写入: {output_path}')


if __name__ == '__main__':
    main()
