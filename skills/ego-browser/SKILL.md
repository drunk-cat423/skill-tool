---
name: ego-browser
description: 通过 Ego Lite 浏览器进行联网检索、读取原始网页、页面交互和网页验收。优先用于用户未指定其他工具的浏览任务；不是原生桌面控制工具。
---

# Ego Lite entry

这是个人配置的轻量入口。实际 API 以安装版本输出为准，不复制固定版本的操作手册。

1. 从 PATH 查找 `ego-browser`。Windows 当前进程找不到时，检查当前用户目录下 `.local/share/ego/active_version_dir/ego-browser.exe`；不要固定版本目录。macOS 检查 `~/.local/bin` 是否在 PATH。
2. 先运行 `ego-browser skill`，完整读取到 `end of guide`。输出截断则保存后分段读取。命令不存在时访问 https://lite.ego.app/，按系统下载安装并完成首次引导，刷新 shell 后再检查；不静默改用其他浏览器。
3. 按该指引使用 TaskSpace、Page 和当前可用 API，不假设它等于 Playwright。PowerShell 使用 UTF-8 `.mjs` 文件，配合 ASCII 单行 import，避免多行 -e 和本地 shell 引号损坏。
4. 每个用户目标使用一个 TaskSpace，后续恢复同一 ID，不为恢复超时另开 Space。检索打开原始来源并保留链接；遇到验证码或权限限制说明原因，不绕过。
5. 完成时调用并等待 `await task.finish({ keep: [] })`。只有用户要求时保留结果页，不关闭原有或其他任务页面。交接、失去控制或错误暂停时按当前指引处理，不强行关闭。

首次引导必须由用户完成。浏览器扩展、已登录账号、cookie 和 profile 不是本 Skill 的迁移内容。原生系统窗口和文件选择使用 Cua Driver。
