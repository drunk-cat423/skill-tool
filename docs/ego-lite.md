# Ego Lite：安装与使用

## 安装

官方入口：https://lite.ego.app/ 。官方使用指南由本机 `ego-browser skill` 返回；它比仓库中的旧命令样例更接近当前版本。

Windows 从官网下载对应安装器，运行并打开浏览器。完成首次引导，再打开新终端执行：

```powershell
Get-Command ego-browser
ego-browser nodejs -e "console.log('ego-browser ready')"
ego-browser skill
```

如果旧进程没有刷新 PATH，检查用户目录的 `.local/share/ego/active_version_dir/ego-browser.exe`。不要复制旧电脑的版本子目录。当前没有在此维护 Windows 静默安装参数。

macOS 从官方入口下载对应架构的应用并完成引导。检查 `command -v ego-browser`；必要时在新终端检查 `~/.local/bin` 是否在 PATH。系统权限由用户按官方安装提示处理，本仓库不自动删除 quarantine 或改安全策略。

Linux 先查官网是否提供当前系统构建；没有则明确记录 Ego 不可用，不能把别的浏览器冒充 Ego。

## 在 agent 中使用

恢复器安装一个轻量的 `ego-browser` 入口。若已有供应商 Skill，保留并优先使用其匹配版本；不同内容造成恢复冲突时不要直接覆盖。

联网搜索、原始网页阅读、页面交互及网页验收使用 Ego。原生文件选择框、系统窗口使用 Cua Driver。

Windows PowerShell 推荐先创建 UTF-8 文件 `smoke.mjs`：

```javascript
const task = await taskSpace('ego-restore-smoke');
console.log({spaceId: task.spaceId});
const page = task.page('p1');
await page.goto('https://example.com');
console.log(await page.snapshot());
await task.finish({keep: []});
```

再以实际绝对路径导入：

```powershell
ego-browser nodejs -e "await import('file:///C:/your-work/skill-tool/.local/smoke.mjs')"
```

`C:/your-work/...` 是示例，必须换成本机实际文件位置。不要把多行脚本或带复杂引号的代码直接传入 Windows PowerShell 的 `-e`。

一次目标只用一个 TaskSpace，后续恢复同一 ID。任务成功后 `finish({keep:[]})` 必须等待成功；如果错误暂停、用户接管或需要验证码，按当前 guide 交接，不强制关闭。只保留用户要求的页面。

## 迁移边界

恢复规则不会导入浏览器 profile、cookie、登录态或旧 Space。首次引导、网站登录和扩展授权在新机器完成。旧机器的“恢复上次标签页”“内存节省”“中文 UI”等浏览器偏好需要按新版本设置，不能用旧 profile 强灌。
