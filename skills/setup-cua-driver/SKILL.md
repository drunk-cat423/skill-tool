---
name: setup-cua-driver
description: 安装或修复 cua.ai Cua Driver 的 agent 接入，设置后台桌面操作并处理与 agent-desktop 的默认路由冲突。不是日常 GUI 操作 Skill；操作时读取官方 cua-driver Skill。
---

# Set up Cua Driver

官方安装：https://cua.ai/docs/how-to-guides/driver/install 。官方接入：https://cua.ai/docs/how-to-guides/driver/connect-your-agent 。先阅读与当前系统匹配的说明，再执行安装。

- Windows 下载并检查官方 `https://cua.ai/driver/install.ps1`，安装时可用 `-NoConnect -NoTest -NoAutoStart`，先避免接入无关 agent、自动测试输入或注册高权限自启。仅接入用户指定的宿主，例如 `cua-driver connect --client codex --dry-run --json`，确认后执行去掉 --dry-run 的命令。
- 若 connect 在 Windows 误找到 npm 的无扩展名 codex 脚本而报 os error 193，查明实际 Codex 原生 exe，并仅在当前安装命令的 PATH 前置该 exe 的目录后重试；不删除或覆盖用户的 CLI shim。
- 使用 `skills status` 核实官方 Skill，再读其 SKILL.md 与当前平台指引。MCP 在 Windows/Linux 可以自行持有运行时；CLI 一次性调用通常需要 serve。以当前版本帮助为准，不为此无条件注册管理员任务。
- 按宿主支持的方法停用旧 agent-desktop Skill 的默认发现，保留程序与回滚路径，更新规则中的默认工具。不要移除 Codex 内置 Computer Use 的运行时文件。
- `doctor` 后用独立测试窗口验收，例如 Calculator 的 6 × 7，必须从新快照读到 42。观察前台是否切换，区分用户移动鼠标与工具输入；不能仅凭计算正确宣称不抢鼠标。
- 用同一 session 标签进行多次 CLI 操作；Windows 明确使用 background，不设 foreground_fallback。出现后台拒绝，先查其他后台路径；前台动作须用户明确授权。
- 清理用 end_session，不停止共享服务、不杀 ApplicationFrameHost 等共享宿主。若 Driver 拒绝终止 UWP 内部进程，报告并保留，不能改用 taskkill 绕过。

标准权限模式先保持默认；它与 Codex 本身的审批策略是两层设置，不因任务受阻而切 unrestricted。
