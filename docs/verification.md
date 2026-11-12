# 恢复后的最小验收

按层次报告，避免“命令存在”等同于“任务能完成”。

1. **文件恢复**：先 dry-run，再 apply，再次 dry-run 应全是 unchanged。原配置不同时不应直接覆盖，替换必须有备份。不要在生产用户目录练习 --overwrite。
2. **Ego 运行时**：CLI 能执行 `skill` 并输出到 guide 结尾。运行一个 TaskSpace 打开 example.com，读取标题/正文，最后 finish({keep:[]}) 成功。系统引导或验证码未完成就报告待用户处理。
3. **CUA 系统能力**：--version、doctor、skills status；再检查 MCP 是否连接并能列出 list_apps/get_window_state/run_steps。doctor 的零退出码不代表 GUI 验收通过，必须看每项报告。
4. **CUA 实际操作**：确认没有占用用户已有计算器；按官方 Skill 打开测试计算器，读取快照，用后台语义动作算 6 × 7，再从新快照读到 42。不能凭模型自己知道答案就通过。检查是否切换前台；用户在同时移动鼠标时，不能把光标变化直接归因于工具。
5. **路由**：新开 agent 聊天，检查 Ego、cua-driver Skill 和 MCP 已被发现，旧 agent-desktop 不再默认选用。临时网页/Space 和本次 session 清理完，不关闭其他任务页面或共享服务。
6. **模型限制**：若恢复 pstack，角色继承项和宿主默认覆盖分别检查。Astra 上限既保留规则，也在实际调用时检查所传参数；未实际调用就不要声称模型路由已实测。

本仓库恢复器测试：

```sh
python -m unittest discover -s tests -v
```

这些测试在临时目录验证文件行为，不启动 GUI、不下载二进制、不发模型请求。真实系统安装仍需逐项验收。
