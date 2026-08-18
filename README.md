# Job Hunter AI — AI 求职助理（每日搜岗 → 按 JD 改简历 → 自动记账）

一个"半自动"求职助手：每天自动搜索国内岗位，**按你可配置的行业/岗位优先级**排序，基于你的真实经历按 JD 改写简历，并把投递记录（公司、岗位、链接、账号密码、用了哪份简历）写进一张台账表。真正的"提交"由你人工确认——**不自动提交、不自动建账号**，合规不封号。

## 特点

- 🔧 **优先级完全可配置**：改一个 JSON 文件即可换行业/岗位偏好，不用改代码
- 🤖 **每日自动化**：搜岗 → 内部打分排序 → 取 Top N → 写台账（状态=待确认）
- 📝 **按 JD 改写简历**：基于你的真实经历（resume_material）逐岗生成适配摘要，不编造
- 📊 **投递台账**：13 列记录一切，含官网自建账号的账号/密码、所用简历版本
- ✅ **半自动确认制**：AI 只做搜索/改写/记录，提交永远是你点头后人工完成

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/<你的用户名>/job-hunter-ai.git
cd job-hunter-ai

# 2. 配置优先级（复制示例并修改）
cp priority_config.example.json priority_config.json

# 3. 填简历素材（真实经历，改简历的原料）
cp resume_material.example.md resume_material.md

# 4. 生成台账模板（需要 python3 + openpyxl）
pip install openpyxl
python scripts/generate_tracker.py --config priority_config.json --output 求职投递台账.xlsx
```

之后把 `automation_prompt.md` 里的 prompt 填进你的 WorkBuddy 每日定时任务（或任何 Agent 平台），替换 `{WORKSPACE}` 为你的工作目录即可。

## 优先级配置说明（priority_config.json）

```jsonc
{
  "max_batch": 20,                       // 每日最多写入的候选数
  "weights": { "industry": 10, "role": 5 },  // 行业/岗位打分权重
  "exclude_keywords": ["销售代表", "客服", "纯硬件"],  // 命中的岗位直接排除
  "industry_priority": [                 // 行业阶梯：level 越小越优先
    { "level": 1, "name": "具身智能", "match_keywords": ["机器人", "embodied"] },
    { "level": 2, "name": "具身智能上游(AI)", "match_keywords": ["大模型", "机器视觉", "传感器"] }
    // ... 其他行业，level 越大越靠后
  ],
  "role_priority": [                     // 岗位阶梯
    { "level": 1, "name": "出海岗(GTM,不含销售)", "match_keywords": ["出海", "GTM", "海外"] },
    { "level": 2, "name": "产品经理", "match_keywords": ["产品经理", "AI产品"] }
    // ...
  ]
}
```

- **打分**：行业得分 = (最大行业层级 + 1 − 层级) × 行业权重；岗位得分同理。综合分 = 两者之和，越高越优先。
- **改优先级**：编辑 `priority_config.json`，重新生成台账 / 让自动化重新读取即可，零代码。

## 目录结构

```
job-hunter-ai/
├── README.md
├── LICENSE
├── priority_config.example.json   # 优先级配置示例（可配置核心）
├── resume_material.example.md     # 简历素材库模板（真实经历原料）
├── automation_prompt.md           # 每日自动化 prompt 模板
└── scripts/
    └── generate_tracker.py        # 由配置生成投递台账 xlsx
```

## 安全与合规

- **不自动提交 / 不自动建账号**：主流招聘平台（Boss直聘/猎聘/官网网申）反爬与 ToS 约束下，可靠的"一键自动提交"不可行且违规风险高。本项目采用**半自动确认制**。
- **台账密码为明文**：仅本地保存，勿公开/外发，建议配合密码管理器。
- **简历不编造**：AI 只做翻译/提炼/量化，素材必须是真实经历。

## License

[MIT](./LICENSE)
