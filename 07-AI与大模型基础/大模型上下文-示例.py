# -*- coding: utf-8 -*-
"""大模型上下文（Context）示例脚本
演示两件事：
  1) 上下文窗口容量有限，装满后旧消息会被"挤出"（滑动窗口遗忘）
  2) 注意力机制的计算量随上下文长度呈平方增长（O(N^2)）
运行方式：python -X utf8 "大模型上下文-示例.py"
"""


# --------------------------------------------------
# 1. 极简上下文窗口：容量固定，装不下就丢弃最旧的对话消息
# --------------------------------------------------
class ContextWindow:
    def __init__(self, capacity):
        self.capacity = capacity          # 窗口容量（token 数）
        self.messages = []                # [角色, 内容, token数]
        self.dropped = []                 # 被挤出窗口的"遗忘区"

    def used(self):
        return sum(t for _, _, t in self.messages)

    def add(self, role, content, tokens):
        self.messages.append([role, content, tokens])
        victims = []
        # 保护 system 消息（首条），从第二条开始淘汰最旧的
        while self.used() > self.capacity and len(self.messages) > 1:
            victim = self.messages.pop(1)
            self.dropped.append(victim)
            victims.append(victim[1])
        note = f"挤出旧消息: {'、'.join(victims)}" if victims else "正常"
        print(f"  [{len(self.messages)}条在窗] {self.used():>2}/{self.capacity} tokens | {note}")

    def current(self):
        return " + ".join(f"{c}" for _, c, _ in self.messages)


# --------------------------------------------------
# 2. 模拟一场对话：窗口容量 30 tokens
# --------------------------------------------------
print("=" * 60)
print("实验一：滑动窗口遗忘（容量 30 tokens）")
print("=" * 60)
win = ContextWindow(capacity=30)
conversation = [
    ("system", "系统提示", 6),
    ("user",   "提问1", 8),
    ("assistant", "回答1", 7),
    ("user",   "提问2", 9),
    ("user",   "提问3", 8),
    ("assistant", "回答3", 10),
]
for role, content, tokens in conversation:
    print(f"新增 [{role}] {content}（{tokens} tokens）")
    win.add(role, content, tokens)

print(f"\n最终窗口内: {win.current()}")
print(f"被遗忘的: {'、'.join(c for _, c, _ in win.dropped)}")
print("结论：Agent 每轮对话都要重读窗口内的全部内容，装不下的等于没发生。")

# --------------------------------------------------
# 3. 注意力计算量：每个 token 都要"看"其他所有 token
# --------------------------------------------------
print()
print("=" * 60)
print("实验二：注意力计算量随上下文长度平方增长")
print("=" * 60)
print(f"{'上下文长度N':>10} | {'token 两两配对数 N(N-1)/2':>22} | {'相对 N=128':>12}")
print("-" * 60)
base = 128 * 127 // 2
for n in [128, 512, 2048, 8192, 32768, 131072]:
    pairs = n * (n - 1) // 2
    print(f"{n:>12,} | {pairs:>26,} | {pairs / base:>11,.0f}x")
print("结论：窗口扩大 1024 倍，计算量约扩大 100 万倍——这就是长上下文又贵又慢的原因。")
