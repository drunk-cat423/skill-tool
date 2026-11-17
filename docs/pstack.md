# 可选：恢复 pstack

Codex 版上游：https://github.com/pstack-ports/codex-pstack 。以下是已验证版本的安装入口；新环境先用 CLI help 核实支持。

```sh
codex plugin marketplace add pstack-ports/codex-pstack
codex plugin add pstack@codex-pstack
codex plugin list --marketplace codex-pstack --json
```

`restore.py --with-pstack --apply` 会安装个人 pstack-auto 及 `~/.agents/pstack-models.md`。它复制下面的模型偏好，但不下载插件、不复制上游缓存、不创建提供方、不迁移凭证，也不发起模型调用。执行前按预览审阅现有文件差异。

## 当前模型分工

以已安装的 pstack 0.15.43 格式维护 9 个现行角色；旧版的 8 个失效角色已移除，不再把全部子任务交给父模型。以下强度均为预算换算后的实际目标。

| 工作 | 模型与强度 | 边界 |
|---|---|---|
| 代码定位、边界明确的实现、机械修改、重复验证 | GPT-6 Luna High | 先有明确验收条件；枚举文件、校验和及执行测试直接用工具 |
| 常规功能、重构、一般 Bug 修复、综合判断 | GPT-6.1 Sol Medium | 主 Agent 保留产品决策与最终集成 |
| 模糊排查、并发、数据一致性、跨模块复杂修改、关键审查 | GPT-6.1 Sol High | 常规角色遇到这些风险时提升一级，不将 High 用于所有任务 |
| 独立方案意见、需求对照、阶段审核、跨厂商裁判 | 百炼 DeepSeek-V4.1-Flash-1017 | 默认只读；不虚构 Codex 风格的推理强度 |
| 重大架构、系统边界或实质审查争议 | GPT-6 Astra Medium | 仅只读，最高 Medium；无法表达上限时不启动 |

Terra 不再作为默认开发或审查席。Sol 已是主模型时，可直接处理复杂任务，不为复刻主会话再开同模型子 Agent。委派按实际收益使用，不强制每个任务开一轮多模型评审；用户明确要求的阶段审核和人工关卡始终优先。

角色配置中，功能、Bug、优化和综合判断使用 Sol；swarm 使用 Luna；Arena 执行席为 Sol + DS，交叉裁判池为 DS；interrogate 审查席为 Sol High + DS。Arena 的裁判必须与父模型来自不同厂商；如果父模型本身是 DS，当前只有 DS 的裁判池就没有合格席位，须说明并按工作流跳过或先取得有效配置，不能冒称独立跨厂商判断。

### 预算换算

模板保留 `# budget: medium`，按当前 setup-pstack 规则，显式起始强度降低一级：角色行中的 `high` 实际为 Medium，`xhigh` 实际为 High。只换算一次，不把起始值直接传给子 Agent。DS 行不填 effort，调用时使用提供方自身默认，不继承 Codex 的 reasoningEffort。模型名称与强度是两个字段，不拼接模型 slug。

项目 `.agents/pstack-models.md` 优先于个人配置。宿主的默认项和具名角色 TOML 也可能覆盖选择，需核对实际调用参数。恢复器不修改 config.toml 或具名角色配置；这里的模型优化也不改变主会话模型。个人规则模板仍按恢复器的预览、冲突检查和显式替换规则处理。

## T3 中的跨提供方路由

GPT 使用官方 Codex；百炼 DS 使用 T3 的 `delegate_task`，不把 DS slug 传给只支持 GPT 的原生 spawn。当前路由偏好为：

```json
{"providerInstanceId":"bailian","driverKind":"claudeAgent","model":"deepseek-v4.1-flash-1017","options":{}}
```

`options: {}` 用于清除继承的 Codex 专用参数。驱动名 `claudeAgent` 表示传输适配器，实际模型仍是 DeepSeek；判断模型厂商时不能把它算作 Claude。首次委派前按 T3 规则读取 `orchestrator_capabilities`，核实提供方、模型和选项，不反复发现或轮询正在运行的任务。新审核和复审都建立新的 delegate_task，遵从返回的 next，子 Agent 不再委派，不另开顶层 thread。

新机器不一定存在 `bailian` 这个提供方别名。缺失时明确报告，保留配置并暂停该席位，不静默改走 deepseek_official 或继承父模型。其他宿主先发现其授权的跨提供方能力，不照搬 T3 参数或安装新路由。能力目录可见、实际调用成功与审核质量是不同的验证层次；配置文件不是强制执行的路由器。

若要重新选模型，运行 `$pstack:setup-pstack`，按本机实际可用模型走流程，不照抄旧角色分工。Astra 最高 Medium 的限制始终保留；自然语言约定不是全局技术硬锁。

上游 poteto-mode 默认显式调用。本仓库提供个人 pstack-auto 加上全局规则，让非琐碎工程任务自动读取已安装入口。实际匹配仍由宿主和模型执行，不能保证每次自动触发；第一次可明确选择 `$pstack:poteto-mode` 验证。不要直接修改插件缓存中的 allow_implicit_invocation。

Claude Code、Cursor 等宿主使用各自 port 和 setup，不安装本仓库的 Codex 专用 pstack-auto。新的项目仍需自己的启动、测试和真实行为验证方法。
