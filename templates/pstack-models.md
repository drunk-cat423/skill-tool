# Personal pstack model configuration
# budget: medium

feature, refactoring: inherit-parent
bug-fix: inherit-parent
perf-issue: inherit-parent
hillclimb: inherit-parent
judgment and prose: inherit-parent
hardest tasks: inherit-parent
how explorer: inherit-parent
how explainer: inherit-parent
why investigators: inherit-parent
why synthesizer: inherit-parent
reflect tooling: inherit-parent
reflect judgment, divergent, synthesizer: inherit-parent
arena runners: inherit-parent, inherit-parent
arena cross-judge pool: inherit-parent, inherit-parent
swarm workers: inherit-parent
architect runners: inherit-parent, inherit-parent
interrogate reviewers: inherit-parent, inherit-parent

所有角色先继承父会话模型和推理强度。medium 预算对显式模型条目使用 High，但不把 inherit-parent 固定为 High。面板为两个独立上下文，不宣称跨模型；Arena 的继承项不能作为异模型裁判。

Astra 默认及最高 Medium。即使父会话 Astra 强度更高，也应在子 Agent 显式封顶；无法表达时不启动。只读且只用于高不确定性架构、重大系统边界或实质审查争议，不通过角色、CLI/API 或再委派绕过。

项目配置优先于此文件的角色选择，但不能绕过全局 Astra 上限。宿主默认子 Agent 和具名角色也可能覆盖继承，必须核实实际路由。
