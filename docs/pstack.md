# 可选：恢复 pstack

Codex 版上游：https://github.com/pstack-ports/codex-pstack 。以下是已验证版本的安装入口；新环境先用 CLI help 核实支持。

```sh
codex plugin marketplace add pstack-ports/codex-pstack
codex plugin add pstack@codex-pstack
codex plugin list --marketplace codex-pstack --json
```

`restore.py --with-pstack --apply` 会安装个人 pstack-auto 及 `~/.agents/pstack-models.md`。它不下载插件，不复制上游缓存，也不选择收费模型。

当前偏好：pstack budget 为 medium，17 项角色均 inherit-parent。budget medium 对显式模型选择表示 High；inherit-parent 同时继承父会话模型和强度，不会被 budget 固定为 High。

宿主仍可能通过 `[agents].default_subagent_model`、`default_subagent_reasoning_effort` 或具名角色 TOML 覆盖继承。先用 doctor 检查，再让 agent 定点删除不需要的默认覆盖。恢复器不会自动改写已有 config.toml。选择具名角色前也要核实是否与当前继承选择一致。

若要重新选模型，运行 `$pstack:setup-pstack`，按本机实际可用模型走流程，不照抄旧角色分工。Astra 最高 Medium 的限制始终保留；自然语言约定不是全局技术硬锁。

上游 poteto-mode 默认显式调用。本仓库提供个人 pstack-auto 加上全局规则，让非琐碎工程任务自动读取已安装入口。实际匹配仍由宿主和模型执行，不能保证每次自动触发；第一次可明确选择 `$pstack:poteto-mode` 验证。不要直接修改插件缓存中的 allow_implicit_invocation。

Claude Code、Cursor 等宿主使用各自 port 和 setup，不安装本仓库的 Codex 专用 pstack-auto。新的项目仍需自己的启动、测试和真实行为验证方法。
