# 我的 Agent 开发环境恢复包

换电脑或换 agent 时，用这个仓库恢复工具选择、个人规则和可复用的操作方法。Windows 是已实测的平台；macOS 有官方安装路径与配置说明，但本仓库尚未在 macOS 实机验证。Linux 可使用 Cua Driver；Ego Lite 是否有对应构建必须先看官网，不承诺可用。

## 给新 agent 的第一句话

克隆此仓库后，在仓库目录开启聊天，发送：

> 阅读 skills/restore-dev-environment/SKILL.md，帮我恢复这套开发环境。先检测系统和 agent，预览计划并保留已有配置。网页默认 Ego Lite，原生桌面默认 cua.ai Cua Driver；不要抢真实鼠标和焦点，Astra 最高 Medium。按本机实际能力验证，不迁移凭证或浏览器登录态。

这个入口可以由任意具备文件和命令行能力的 agent 直接读取，不要求先有 Skill 安装器。

## 自己操作：Windows + Codex

需要 Git、Python 3.11+、Codex。下列命令都在克隆后的仓库根目录运行。

```powershell
git clone https://github.com/drunk-cat423/skill-tool.git
cd skill-tool
python scripts/restore.py --with-pstack
python scripts/restore.py --with-pstack --apply
```

第一条 Python 命令只展示写入计划；第二条才写入。相同内容重复执行不写文件。遇到不同的已有文件会整体拒绝；请让 agent 合并，或审阅差异后明确加 `--overwrite`，它会先备份。不会整份复制或改写现有 `config.toml`。

如果目标 Skill 或其父目录是 symlink/junction，脚本会拒绝通过链接写入，即使加 --overwrite 也不会绕过。已有官方 Ego Skill 的机器可能遇到这一情况，应保留官方 Skill 并由 agent 单独合并其余规则，不把供应商目录替换成本仓库入口。

然后完成工具安装和接入：

1. [安装 Ego Lite 并完成首次引导](docs/ego-lite.md)。Windows 从官网下载并安装，没有在此伪造一键安装脚本。
2. [安装 Cua Driver，并仅接入要使用的 agent](docs/cua-driver.md)。官方 `connect --client codex` 会安装其正式 Skill 并注册 MCP。
3. 如果要恢复 pstack，按 [pstack 设置](docs/pstack.md)安装插件。恢复脚本中的 `--with-pstack` 只安装个人入口和角色偏好，不等于已经安装插件。
4. 重启 agent，执行 [验收清单](docs/verification.md)。官方工具的提示、帮助和权限要求优先于本文的历史样例。

## 换成 Claude Code 或其他 agent

恢复脚本也支持 Claude Code 的规则和 Skill 位置：

```sh
python scripts/restore.py --agent claude
python scripts/restore.py --agent claude --apply
```

其他 agent 使用其文档确认过的路径，显式传入，不猜配置目录：

```sh
python scripts/restore.py --agent generic --rules-file /absolute/path/to/agent-rules.md --skills-dir /absolute/path/to/skills
```

确认计划后加 `--apply`。Cursor 的 `.mdc` 头、其他 agent 的指令注册、模型路由及 MCP 注册仍按对应宿主执行，见 [跨 agent 适配](docs/other-agents.md)。`--with-pstack` 仅支持 Codex，其他版本使用各自 port 与 setup。

## 默认分工

| 用途 | 默认工具 |
|---|---|
| 搜索、打开原始网页、页面交互 | Ego Lite / ego-browser |
| Windows/macOS/Linux 原生应用、系统窗口、文件选择框 | cua.ai Cua Driver |
| 非琐碎工程任务 | 可选 pstack，通过本地 pstack-auto 加载；Luna 执行明确任务，Sol 处理常规与复杂开发，百炼 DS 独立审核 |
| 桌面输入 | 先精确窗口、语义元素、background；禁止自动前台回退 |
| Astra | 默认及最高 Medium，不通过其他角色或接口绕过 |

Cua Driver 与 Codex 内置 Computer Use 不是同一产品。Vercel agent-desktop 保留为可选旧工具，不再默认选用；不要让两个控制器同时操作同一桌面。

## 包含什么

- `skills/restore-dev-environment/`：恢复入口。
- `skills/ego-browser/`：本仓库编写的轻量入口，实际 API 指引由安装版本的 `ego-browser skill` 提供；不冒充供应商完整 Skill。
- `skills/setup-cua-driver/`：安装、接入、冲突处理和验收指引。实际操作使用官方安装的 `cua-driver` Skill。
- `skills/pstack-auto/`：Codex 可选自动入口，不修改上游插件缓存。
- `templates/AGENTS.md`：可移植的个人约定。
- `templates/pstack-models.md`：Sol / Luna / 百炼 DS 分工、预算换算、T3 路由与 Astra 上限；详见 [pstack 设置](docs/pstack.md)。
- `scripts/restore.py`：有预览、冲突检查和备份的文件恢复器。
- `scripts/doctor.py`：只读检查工具是否存在及 Codex 覆盖项，不输出凭证，不启动 GUI。

本仓库不保存 auth.json、完整 config.toml、MCP 令牌、浏览器 profile、cookie、代理订阅、GUI 主题或 Codex 内置运行时路径。账号登录和系统授权在新机器上重新完成。

## 检查恢复状态

```sh
python scripts/doctor.py
python -m unittest discover -s tests -v
```

doctor 的成功仅表示发现了命令或文件；真实网页及桌面操作必须按验收清单另测。来源及本机实测范围见 [sources.md](docs/sources.md)。
