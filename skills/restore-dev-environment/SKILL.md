---
name: restore-dev-environment
description: 在新电脑或新的 agent 环境恢复此仓库中的 Ego Lite、Cua Driver 和个人开发规则。适用于换机、迁移或明确要求恢复开发环境；不用于日常浏览和普通桌面操作。
---

# Restore the development environment

从这个入口所在位置找到仓库根目录的 README.md。若此 Skill 已复制到用户技能目录，先要求定位仓库 checkout；没有文件时从 https://github.com/drunk-cat423/skill-tool 获取，而不是假定相对路径仍存在。

1. 检测操作系统、当前 agent、真实用户目录、Python、Git、已有 Ego/CUA 安装以及相关规则。只读取有关配置，不打印密钥或完整环境变量。
2. 阅读根 README.md 及当前需要的 docs/ego-lite.md、docs/cua-driver.md。非 Codex 宿主再读 docs/other-agents.md。Windows 安装经验不能当作 macOS/Linux 实测。
3. 运行 `scripts/restore.py` 预览。默认目标是 Codex；Claude 或其他宿主须选对参数。现有文件不同时先展示差异并合并，不能为追求一键成功覆盖它。只有明确允许替换时使用 --overwrite。
4. 在用户授权的恢复范围内，用 --apply 安装个人规则和本仓库 Skill。二进制及官方 Skill 按供应商指引获取；只接入本次指定的 agent。首次引导、登录和系统权限交给用户，不复制旧机器的登录态。
5. 用 docs/verification.md 验收。网页通过 Ego Lite，桌面通过官方 Cua Driver。后台失败不自动切 foreground、不使用真实鼠标回退；清理只涉及本次页面、会话及明确拥有的测试窗口。
6. 报告实际安装和写入位置、备份、验证结果以及尚需用户完成的步骤。重启宿主以加载新 MCP。工具可执行、能列出工具与实际 GUI 任务成功分别报告。

不迁移完整 config.toml，不放宽权限，不自动改代理、部署、发送消息或安装未请求的第三方工具。pstack 只在需要恢复 Codex 工程工作流时启用 --with-pstack，并按 docs/pstack.md 接入。
