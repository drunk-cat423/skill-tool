# Cua Driver：安装、接入与冲突处理

这里是 cua.ai 的 Cua Driver，不是 Codex 内置 Computer Use，也不是 Vercel agent-desktop。

官方来源：

- https://cua.ai/docs/how-to-guides/driver/install
- https://cua.ai/docs/how-to-guides/driver/connect-your-agent
- https://github.com/trycua/cua

## Windows

下载官方脚本到工作目录并阅读，再执行。以下步骤由 agent 按授权范围执行，不建议把未经检查的网络响应直接送入 iex。

```powershell
New-Item -ItemType Directory -Force .local | Out-Null
Invoke-WebRequest https://cua.ai/driver/install.ps1 -OutFile .local/cua-install.ps1
# 阅读脚本，核实版本、安装范围和当前参数后：
& .local/cua-install.ps1 -NoConnect -NoTest -NoAutoStart
```

参数以下载版本为准；本机验证版本为 0.47.13，不代表以后永远最新。安装器会下载官方二进制、校验发布校验和及 Windows 签名。不要自行关闭签名校验。

默认稳定入口是 `%LOCALAPPDATA%/Programs/Cua/cua-driver/bin/cua-driver.exe`，实际版本在用户 `.cua-driver` 目录，通过 junction 指向，不复制版本目录。

```powershell
cua-driver --version
cua-driver doctor --json
cua-driver connect --client codex --dry-run --json
cua-driver connect --client codex --json
cua-driver skills status
```

只指定本次使用的 client，避免默认 connect 修改其他 agent。Windows 若报 `os error 193`，通常是找到了 npm 的无扩展名 codex 脚本。先找到已安装 Codex 的原生 exe，只为这次连接命令临时前置其目录到 PATH。不要硬编码本仓库作者机器上的 app 版本，也不要删除 shim。

MCP 注册结果应指向本机实际二进制，形状类似：

```toml
[mcp_servers.cua-driver]
command = "C:/Users/YOUR_USER/AppData/Local/Programs/Cua/cua-driver/bin/cua-driver.exe"
args = ["mcp"]
```

使用 connect 生成真实路径，不把示例原样粘贴到新机器。重启 agent 后加载 MCP。

## macOS / Linux

打开官方 Quickstart，选择本机系统并按当前安装步骤执行。macOS 需要实际批准辅助功能和屏幕录制；Linux 需要对应桌面会话及图形协议支持。不要把 Windows 脚本当作通用安装器。本仓库尚未在这些平台实机验收。

连接 agent 的原则相同：先 `connect --client ... --dry-run --json`，再执行实际接入并检查 `skills status`。不因配置恢复自动开启所有应用的系统权限或 unrestricted。

## 常驻与权限

Windows/Linux 的裸 `cua-driver mcp` 可以自己持有运行时，所以 Codex 的 MCP 接入不要求另设常驻窗口或管理员自启任务。单次 CLI 调用通常需要 `serve`；先查 status 与当前 Skill，不盲目启动第二个服务。

如确实需要 CLI 常驻，再审阅 `autostart` 的当前行为和权限。`standard`、`bounded`、`unrestricted` 是 CUA 自己的权限层，与 Codex 完全访问不同。恢复器不会切换它们。

## 与旧工具的冲突

旧程序通常不会仅因安装就与 CUA 抢桌面；主要冲突是 agent 同时看见多个 Skill，或全局规则仍要求 agent-desktop。处理顺序：

1. 将用户规则中的默认桌面工具改为 Cua Driver，Ego 继续负责网页。
2. 在 Codex 中，检查旧 Skill 的实际位置，再使用支持的 `[[skills.config]]` 设置 `enabled = false`。不要照搬其他用户的绝对路径。
3. 其他 agent 按其支持的技能禁用机制操作；没有机制时明确规则并避免同时使用，不自动删目录。
4. 不卸载旧二进制，不删除 Codex 内置 Computer Use，不停止其他任务的服务。

恢复脚本只安装规则，不自动编辑 `config.toml`；这一步由恢复 agent 按实际位置有针对性处理并备份。

## 后台使用与清理

阅读官方 `cua-driver` Skill 和 `WINDOWS.md` 等平台指引。优先快照语义元素，输入显式 background，foreground_fallback 保持 false。后台不支持的 app 可能必须前台，届时先向用户说明并获得授权。

CLI 多次调用使用同一非空 session。结束用 end_session，别停止共享服务。UWP 的 UI 宿主可能是 ApplicationFrameHost，不能因为它承载测试计算器就终止整个宿主。Driver 若拒绝终止内部进程，保留并报告，不改用 taskkill 绕过。
