# 跨 agent 迁移

可迁移的是个人偏好和工具协议，不是 Codex 的进程、运行时路径和账号权限。

| 内容 | Codex | Claude Code | 其他 agent |
|---|---|---|---|
| 个人规则 | Codex home / AGENTS.md | ~/.claude/CLAUDE.md | 先确认宿主实际规则位置，再用 --rules-file |
| 本仓库通用 Skill | ~/.agents/skills | ~/.claude/skills | --skills-dir 显式指定 |
| Ego | CLI + 当前 guide | CLI + 当前 guide | 有本机 shell 和 Ego 才可用 |
| CUA | connect --client codex | connect --client claude | 查官方 connect / mcp-config 支持 |
| pstack-auto | 可选 | 不安装此 Codex 专用入口 | 使用对应 port 或手动工作流 |

恢复脚本的 `--home` 用于显式目标目录及隔离测试，不更改系统 HOME。Codex home 在正常运行时尊重 CODEX_HOME；技能目录默认仍位于用户 ~/.agents/skills。定制路径可用 --rules-file 和 --skills-dir。

Cursor 的规则可能需要 `.mdc` 文件及 `alwaysApply` frontmatter；恢复器不自动生成未经确认的宿主格式。请让 agent 读取 templates/AGENTS.md，将其内容转换成当前宿主支持的形式，保持偏好和 Astra 上限，不照搬 Codex 字段。

对于不支持 MCP 的宿主，Cua Driver 可通过 CLI 操作，但需按官方 Skill 管理服务与 session。没有本机 shell、桌面或浏览器连接能力的云端 agent，不能仅靠复制 Skill 控制另一台电脑；需要该平台支持的远程连接。不要因此开放公网端口或共享浏览器调试端口。

模型名、推理强度、预算和审批概念可能不兼容。Astra 不可用时不用猜模型；如实报告。没有强度覆盖能力时不能宣称已技术强制封顶。任何宿主都不因导入规则而获得额外权限。
