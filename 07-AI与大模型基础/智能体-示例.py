# -*- coding: utf-8 -*-
"""智能体（Agent）示例脚本
演示 Agent 的三大要素：目标（任务）+ 工具（add/mul/sub）+ 循环（思考→行动→观察）。
这个"大脑"用简单规则模拟大模型的决策过程，重点展现 Agent 的结构而非智能本身。
运行方式：python -X utf8 "智能体-示例.py"
"""
import re

# --------------------------------------------------
# 1. 工具层：Agent 的"手脚"，只会做三件小事
# --------------------------------------------------
def tool_add(a, b):
    return a + b

def tool_mul(a, b):
    return a * b

def tool_sub(a, b):
    return a - b

TOOLS = {"+": tool_add, "*": tool_mul, "-": tool_sub}
OP_NAME = {"+": "加法", "*": "乘法", "-": "减法"}


# --------------------------------------------------
# 2. 大脑层：每一步先观察环境，再决定调用哪个工具、传什么参数
# --------------------------------------------------
def think(expr):
    """观察表达式，返回下一步决策 (a, 运算符, b, 位置说明)；无处可算则返回 None。"""
    m = re.search(r"\((\d+)([+\-*])(\d+)\)", expr)  # 优先算最内层括号
    if m:
        a, op, b = m.groups()
        return a, op, b, "括号内发现"
    m = re.search(r"(\d+)([+\-*])(\d+)", expr)      # 没有括号则从左往右
    if m:
        a, op, b = m.groups()
        return a, op, b, "表达式中发现"
    return None


# --------------------------------------------------
# 3. 循环层：感知 → 思考 → 行动 → 观察，直到任务完成
# --------------------------------------------------
def run_agent(goal):
    expr = goal
    steps = 0
    print(f"目标: 计算 {goal}")
    print("-" * 52)
    while not expr.isdigit():
        steps += 1
        decision = think(expr)
        if decision is None:
            print("[失败] 无法解析表达式，任务终止")
            return None
        a, op, b, where = decision
        a, b = int(a), int(b)
        print(f"[第{steps}步·思考] {where} {a}{op}{b}，选用{OP_NAME[op]}工具")
        print(f"[第{steps}步·行动] 调用 tool({'a=' + str(a)}, {'b=' + str(b)})")
        value = TOOLS[op](a, b)
        old = f"({a}{op}{b})" if where == "括号内发现" else f"{a}{op}{b}"
        expr = expr.replace(old, str(value), 1)
        print(f"[第{steps}步·观察] 工具返回 {value}，表达式变为 {expr}")
        print("-" * 52)
    print(f"任务完成！共执行 {steps} 步，最终答案 = {expr}")
    return int(expr)


if __name__ == "__main__":
    run_agent("(23+17)*2-8")
