# -*- coding: utf-8 -*-
"""
第 1 周练习：计算描述性统计量
使用 Python 标准库 statistics（无需安装第三方包）

运行方式：
    python week01-练习.py
"""

import csv
import statistics
from pathlib import Path

# 数据文件路径（相对于本脚本）
DATA_FILE = Path(__file__).parent.parent / "datasets" / "student_scores.csv"


def load_scores(path: Path) -> list[float]:
    """从 CSV 文件读取学生成绩"""
    scores = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scores.append(float(row["成绩"]))
    return scores


def quartiles(data: list[float]):
    """计算四分位数 Q1 / Q2 / Q3（线性插值法，与 NumPy 默认一致）"""
    s = sorted(data)
    n = len(s)

    def percentile(p):
        k = (n - 1) * p / 100
        f = int(k)
        c = min(f + 1, n - 1)
        return s[f] + (s[c] - s[f]) * (k - f)

    return percentile(25), percentile(50), percentile(75)


def describe(data: list[float]) -> dict:
    """返回一组数据的常用描述统计量"""
    q1, q2, q3 = quartiles(data)
    iqr = q3 - q1
    return {
        "样本量": len(data),
        "最小值": min(data),
        "最大值": max(data),
        "均值": statistics.mean(data),
        "中位数": statistics.median(data),
        "众数": statistics.mode(data),
        "方差(样本)": statistics.variance(data),
        "标准差(样本)": statistics.stdev(data),
        "Q1": q1,
        "Q2(中位数)": q2,
        "Q3": q3,
        "IQR": iqr,
        "异常值下界": q1 - 1.5 * iqr,
        "异常值上界": q3 + 1.5 * iqr,
    }


def main():
    scores = load_scores(DATA_FILE)

    stats = describe(scores)

    print("=" * 46)
    print(" 学生成绩描述性统计")
    print("=" * 46)
    for name, value in stats.items():
        if isinstance(value, float):
            print(f" {name:<14} {value:>10.2f}")
        else:
            print(f" {name:<14} {value:>10}")

    # 找出疑似异常值（1.5×IQR 法则）
    lower = stats["异常值下界"]
    upper = stats["异常值上界"]
    outliers = [x for x in scores if x < lower or x > upper]

    print("-" * 46)
    if outliers:
        print(f" 疑似异常值: {outliers}")
    else:
        print(" 未发现疑似异常值")


if __name__ == "__main__":
    main()
