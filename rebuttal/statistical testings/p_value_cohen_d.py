from tabulate import tabulate
from utils import get_baselines_list, get_our_list, get_p_value

types = ['unit', 'static', 'fuzz']
compare_list = ['OriginalLLM', 'LLM-Agent', 'AutoSafeCoder']
llm_list = ['qwen-max', 'deepseek-chat',
            'qwen-coder-plus', 'claude-3-5-sonnet', 'gemini-1.5-pro', 'gpt-4o']


SIGNIFICANCE_LEVEL = 0.05


def format_p_value(p_val):
    if p_val == 'Error':
        return 'Error'

    # 检查是否为显著差异
    is_significant = p_val < SIGNIFICANCE_LEVEL

    # 格式化数值显示
    if p_val < 0.0001:  # 非常小的值使用科学计数法
        formatted_val = f"{p_val:.2e}"
    elif p_val < 0.01:  # 较小值保留4位小数
        formatted_val = f"{p_val:.4f}"
    else:  # 其他值保留2位小数
        formatted_val = f"{p_val:.2f}"

    # 添加显著性标记
    symbol = "✅" if is_significant else "❌"
    return f"{symbol} {formatted_val}"


results = {what_type: [] for what_type in types}
size_results = {what_type: [] for what_type in types}

for what_type in types:
    for llm in llm_list:
        row = [llm]  # 每行的第一列是LLM名称
        size_row = [llm]  # 效应量表格行
        for compare in compare_list:
            print(
                f'---------- LLM: {llm}, Compare: {compare}, Type: {what_type} ----------')
            # 从指定文件路径读取fail_list, 该文件内容形如83,87,130,132,145,162，需要识别字符串并转换成list
            with open(f'S²CG-Agent-025/{llm}-{what_type}', 'r') as f:
                fail_list = f.read().strip().split(',')
                fail_list = [int(i) for i in fail_list]
            our_list = get_our_list(
                f'S²CG-Agent-025/{llm}.json', fail_list, what_type)
            baseline_list = get_baselines_list(
                f'{compare}/{llm}.json', what_type)
            p_value, size = get_p_value(our_list, baseline_list)
            print(f'p-value: {p_value}\n')
            row.append(format_p_value(p_value))  # 保留4位小数
            size_row.append(f"{size:.4f}")  # 直接保留4位小数
        results[what_type].append(row)
        size_results[what_type].append(size_row)


for what_type in types:
    print(
        f"\n S²CG-Agent vs. Baselines: P-Values On {what_type.upper()} TEST")

    # 创建表头
    headers = ["LLM"] + compare_list

    # 使用tabulate美化打印
    table = tabulate(results[what_type],
                     headers=headers,
                     tablefmt='pretty',
                     floatfmt=".4f")

    # 添加解释说明
    print(table)
    print()
    print(f"Note: ✅ p < {SIGNIFICANCE_LEVEL} (significant difference)")
    print(f"      ❌ p ≥ {SIGNIFICANCE_LEVEL} (no significant difference)")

    # 打印效应量表格
    print(f"\n Cohen's d")
    headers = ["LLM"] + compare_list
    print(tabulate(size_results[what_type], headers=headers, tablefmt='grid'))

# 添加整体解释说明
print("\n" + "="*80)
print("Analysis Notes:")
print("1. p-value represents the statistical significance between S²CG-Agent and the comparison method")
print("2. ✅ indicates statistically significant difference (p < 0.05)")
print("3. For very small values (<0.0001), scientific notation is used")
print("4. Errors may occur due to missing data files or calculation issues")
