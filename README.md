# Job Hunter AI — AI 求职助理（每日搜岗 → 按 JD 改简历 → 自动记账）

一个"半自动"求职助手：每天自动搜索国内岗位，**按你可配置的行业/岗位优先级**排序，基于你的真实经历按 JD 改写简历，并把投递记录（公司、岗位、链接、账号密码、用了哪份简历）写进一张台账表。真正的"提交"由你人工确认——**不自动提交、不自动建账号**，合规不封号。

## 特点

- 🔧 **优先级完全可配置**：改一个 JSON 文件即可换行业/岗位偏好，不用改代码
- 🤖 **每日自动化**：搜岗 → 内部打分排序 → 取 Top N → 写台账（状态=待确认）
- 📝 **按 JD 改写简历**：基于你的真实经历（resume_material）逐岗生成适配摘要，不编造
- 📊 **投递台账**：13 列记录一切，含官网自建账号的账号/密码、所用简历版本
- ✅ **半自动确认制**：AI 只做搜索/改写/记录，提交永远是你点头后人工完成
- 🔓 **ATS 适配知识库**：主流校招系统（飞书/Moka/北森等）登录方式与自动化可行性速查，判断"能不能自动/要配合什么"
- 🤖 **飞书系两阶段投递法**：登录后可无人值守批量投递（拿职位 ID 与提交分离，绕过登录态精简视图）
- 🧭 **方向硬校验 + 防海投**：只投配置方向+沾边岗位，同公司≤2-3个，宁缺毋滥（写在每日 prompt 第 0 条最高红线）
- 👥 **双模式协作**：用户在线直接要验证码；用户不在线干不了的直接跳过，不阻塞流程

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
  "exclude_keywords": ["关键词示例A", "关键词示例B"],  // 命中的岗位直接排除
  "industry_priority": [                 // 行业阶梯：level 越小越优先
    { "level": 1, "name": "行业A", "match_keywords": ["关键词A1", "关键词A2"] },
    { "level": 2, "name": "行业B", "match_keywords": ["关键词B1", "关键词B2"] }
    // ... 其他行业，level 越大越靠后
  ],
  "role_priority": [                     // 岗位阶梯
    { "level": 1, "name": "岗位A", "match_keywords": ["关键词A1", "关键词A2"] },
    { "level": 2, "name": "岗位B", "match_keywords": ["关键词B1", "关键词B2"] }
    // ...
  ]
}
```

> 以上为**演示结构**，`priority_config.example.json` 中的行业/岗位名称均为占位示例，请替换成你自己的偏好。

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
├── docs/
│   ├── feishu-auto-apply.md       # 飞书系无人值守投递流程（两阶段投递法）
│   └── ats-adaptation-guide.md    # 主流校招 ATS 系统适配知识库
└── scripts/
    ├── generate_tracker.py        # 由配置生成投递台账 xlsx
    └── upload_repo.py             # 发布/更新本仓库（GitHub Contents API，git 通道受限时用）
```

## 安全与合规

- **不自动提交 / 不自动建账号**：主流招聘平台（Boss直聘/猎聘/官网网申）反爬与 ToS 约束下，可靠的"一键自动提交"不可行且违规风险高。本项目采用**半自动确认制**。
- **台账密码为明文**：仅本地保存，勿公开/外发，建议配合密码管理器。
- **简历不编造**：AI 只做翻译/提炼/量化，素材必须是真实经历。

## License

[MIT](./LICENSE)
