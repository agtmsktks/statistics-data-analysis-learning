# -*- coding: utf-8 -*-
"""智能体技能（Skill）示例脚本
演示技能的核心机制：平时只让"技能描述"常驻上下文（几十 token），
触发时才加载技能正文（上千 token），从而节省宝贵的上下文容量。
运行方式：python -X utf8 "智能体技能-示例.py"
"""

# --------------------------------------------------
# 1. 技能注册表：每个技能 = 描述（常驻）+ 关键词（触发）+ 正文（按需加载）
# --------------------------------------------------
SKILLS = {
    "concept-learning-material": {
        "description": "为统计/数据分析概念生成标准化学习资料（笔记+示例+练习）",
        "keywords": ["生成", "学习资料", "笔记", "练习"],
        "body_tokens": 1800,
    },
    "data-visualization": {
        "description": "绘制统计图表：直方图、箱线图、散点图",
        "keywords": ["画", "图表", "直方图", "可视化"],
        "body_tokens": 1500,
    },
    "github-push-api": {
        "description": "网络阻断时通过 GitHub API 通道推送代码",
        "keywords": ["github", "推送", "push"],
        "body_tokens": 1200,
    },
}

# 描述常驻成本：3 个技能的 description 合计约 60 tokens
METADATA_TOKENS = 60
ALL_BODY_TOKENS = sum(s["body_tokens"] for s in SKILLS.values())


# --------------------------------------------------
# 2. 触发逻辑：用请求与关键词的命中数挑选技能（模拟大模型的判断）
# --------------------------------------------------
def match_skill(query):
    best, best_hits, hit_words = None, 0, []
    for name, s in SKILLS.items():
        hits = [k for k in s["keywords"] if k in query]
        if len(hits) > best_hits:
            best, best_hits, hit_words = name, len(hits), hits
    return best, hit_words


# --------------------------------------------------
# 3. 对比：按需加载 vs 全部常驻
# --------------------------------------------------
def demo(query):
    print(f"用户请求: {query}")
    skill, hit_words = match_skill(query)
    if skill is None:
        print(f"  未命中任何技能 -> 加载 0（技能描述仍常驻 {METADATA_TOKENS} tokens）\n")
        return ALL_BODY_TOKENS - 0
    body = SKILLS[skill]["body_tokens"]
    cost = METADATA_TOKENS + body
    print(f"  命中技能: {skill}（关键词: {'、'.join(hit_words)}）")
    print(f"  本次加载: 描述常驻 {METADATA_TOKENS} + 正文 {body} = {cost} tokens")
    print(f"  对比全部正文常驻 {ALL_BODY_TOKENS} tokens，本次节省 {ALL_BODY_TOKENS - cost}\n")
    return ALL_BODY_TOKENS - cost


if __name__ == "__main__":
    print("=" * 60)
    print(f"技能共 3 个，全部正文常驻需 {ALL_BODY_TOKENS} tokens/轮")
    print("=" * 60 + "\n")
    queries = [
        "帮我生成假设检验的学习资料",
        "给我画一个成绩分布的直方图",
        "github 推送失败，帮我推上去",
        "今天天气怎么样？",
    ]
    total_saved = sum(demo(q) for q in queries)
    print("=" * 60)
    print(f"4 轮请求累计节省: {total_saved} tokens")
    print("结论：技能 = 按需加载的专项手册，让 Agent 用小窗口办大事。")
