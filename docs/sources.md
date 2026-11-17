# 来源与验证范围

整理日期：2026-11-12；pstack 分工更新于 2026-11-17。安装命令、支持系统及工具 schema 会更新；使用前读取安装版本的帮助和官方指南。

- Ego Lite 官网：https://lite.ego.app/ 。本仓库的入口依据本机 Ego Browser Skill 2.2.0 与 `ego-browser skill` 运行指南整理，未复制其供应商安装脚本。
- Cua Driver 安装：https://cua.ai/docs/how-to-guides/driver/install 。接入：https://cua.ai/docs/how-to-guides/driver/connect-your-agent 。源代码：https://github.com/trycua/cua 。Windows 本机安装并验证 0.47.13，MCP 初始化与工具枚举通过，后台计算器从新快照读到 42；期间前台窗口未切换。光标期间有变化，未据此宣称零真实鼠标移动。
- pstack Codex port：https://github.com/pstack-ports/codex-pstack 。2026-11-17 核对本机安装 0.15.43；模型偏好通过个人配置与本仓库入口维护，不修改上游缓存。
- pstack Arena 原文：https://github.com/cursor/plugins/blob/2f87c854fe3e2fcda44ca86b46ede35aad3c46b7/pstack/skills/arena/SKILL.md 。支持多模型执行席，交叉裁判必须与父模型来自不同厂商；未指定必须采用 DeepSeek。
- 社区分工实例：https://github.com/breko861-hash/sol-luna-codex-orchestrator 。参考其 Sol 保留判断、Luna High 执行明确任务及按收益委派的思路；不采用其超出个人限制的 Astra High。
- 官方分工示例：https://openai.com/zh-Hans-CN/index/advancing-the-price-performance-frontier-with-gpt-5-6/ 。其中 Sol 制定计划、Luna 实施明确修改的示例针对 GPT-5.6，不将旧版本成绩、价格比例视为当前模型实测。
- Codex Skill：https://developers.openai.com/codex/build-skills 。子 Agent 覆盖与继承：https://developers.openai.com/codex/agent-configuration/subagents 。配置：https://developers.openai.com/codex/config-file/config-reference 。不同版本或宿主可能有不同字段，应以当前安装为准。

这些不是完整系统镜像。官方工具与 Skill 仍由原作者授权和分发，本仓库只保存个人编写的恢复材料；不包含公司内部飞书内容、凭证或浏览器数据。
