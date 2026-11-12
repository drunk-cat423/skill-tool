---
name: pstack-auto
description: 为复杂开发、Bug 修复、重构、架构、性能和工程验证加载已安装的 pstack。普通问答、网页摘要、翻译、媒体处理及简单局部修改不触发。
---

# Personal pstack entry for Codex

先确认用户没有指定其他工作流。从当前技能目录定位 `pstack:poteto-mode` 的入口；若未列出，用 `codex plugin list --marketplace codex-pstack --json` 确认启用版本，再在本机 Codex home 的 `plugins/cache/codex-pstack/pstack/<version>/` 核对 manifest 和入口。不得固定版本目录或使用临时源码。

完整读取 poteto-mode 与其 Codex adapter，在当前主线程执行匹配 playbook。模型配置先读项目 `.agents/pstack-models.md`，没有时读用户 `~/.agents/pstack-models.md`。默认继承父会话，不套用旧的固定角色分工；检查宿主 `[agents]` 默认项和具名角色是否覆盖了继承。

网页继续 Ego Lite，原生桌面使用 Cua Driver；pstack 不授权改用真实鼠标、前台输入或静默换工具。任务的范围、权限、个人限制优先，不自动部署、合并、发消息或付费。

Astra 默认及最高 Medium，继承到更高强度时也必须显式封顶；工具不能表达该限制就不启动相应 Astra 子 Agent。不通过角色、CLI/API 或再委派规避。遵守当前宿主的并发和嵌套上限，不声称不同上下文就是不同模型。

插件缺失时说明并继续能做的常规工作，不声称 pstack 已启用，不自行安装或改全局模型。非 Codex 环境应使用相应 port，不直接安装此入口。
