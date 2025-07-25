import numpy as np
import scipy.stats as stats


def get_our_list(path, fail_list, what_type):
    # 加载jsonl文件
    import json

    # 设置你的 .jsonl 文件路径
    file_path = path

    # 读取所有样本
    samples = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            sample = json.loads(line.strip())
            samples.append(sample)

    samples = samples[:164]
    results = []
    # 0 for fail
    RESULT = ['success', 'fixed, round: 1',
              'fixed, round: 2', 'fixed, round: 3']
    for i, sample in enumerate(samples):
        if what_type == 'unit':
            a = sample['unit_test_status']
        elif what_type == 'static':
            a = sample['static_analysis_status']
        elif what_type == 'fuzz':
            a = sample['fuzzing_test_status']
        if a not in RESULT:
            if i not in fail_list:
                results.append(1)
            else:
                results.append(0)
        else:
            results.append(RESULT.index(a) + 1)
    # print(results)
    return results


def get_baselines_list(path, what_type):
    # 加载jsonl文件
    import json

    # 设置你的 .jsonl 文件路径
    file_path = path

    # 读取所有样本
    samples = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            sample = json.loads(line.strip())
            samples.append(sample)

    samples = samples[:164]
    results = []
    RESULT = ['success', 'fixed, round: 1',
              'fixed, round: 2', 'fixed, round: 3']
    for i, sample in enumerate(samples):
        if what_type == 'unit':
            a = sample['unit_test_status']
        elif what_type == 'static':
            a = sample['static_analysis_status']
        elif what_type == 'fuzz':
            a = sample['fuzzing_test_status']

        if a not in RESULT:
            results.append(0)
        else:
            results.append(RESULT.index(a) + 1)
    # print(results)
    return results


def get_p_value(group1, group2):
    def cohen_d(x, y):
        """
        计算两个独立样本的 Cohen's d。
        d = (mean(x) - mean(y)) / s_pooled
        其中 s_pooled = sqrt(((n_x-1)*s_x^2 + (n_y-1)*s_y^2) / (n_x + n_y - 2))
        """
        nx, ny = len(x), len(y)
        mx, my = np.mean(x), np.mean(y)
        sx2, sy2 = np.var(x, ddof=1), np.var(y, ddof=1)
        s_pooled = np.sqrt(((nx - 1)*sx2 + (ny - 1)*sy2) / (nx + ny - 2))
        return (mx - my) / s_pooled

    # 1. 计算 t 检验
    t_statistic, p_value = stats.ttest_ind(group1, group2)

    # 2. 计算 Cohen's d
    d_value = cohen_d(group1, group2)

    # 3. 输出结果
    print(f"T-statistic: {t_statistic:.4f}")
    print(f"P-value:    {p_value:.4f}")
    print(f"Cohen's d:  {d_value:.4f}")

    # 4. 判断显著性与效应量解读
    alpha = 0.05
    if p_value < alpha:
        print("\n结论：两组数据之间存在显著差异 (p < 0.05)。")
    else:
        print("\n结论：两组数据之间没有显著差异 (p ≥ 0.05)。")

    # 常用的 Cohen's d 效应量阈值：
    # |d| < 0.2   微小效应
    # |d| ≈ 0.2–0.5 小至中等效应
    # |d| ≈ 0.5–0.8 中等效应
    # |d| > 0.8   较大效应

    if abs(d_value) < 0.2:
        size = "微小效应"
    elif abs(d_value) < 0.5:
        size = "小效应"
    elif abs(d_value) < 0.8:
        size = "中等效应"
    else:
        size = "大效应"
    print(f"效应量解读：{size}")

    return p_value, abs(d_value)
