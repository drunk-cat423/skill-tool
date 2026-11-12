# Repository instructions

本仓库保存个人开发环境的恢复方法，不保存整机配置转储、凭证、浏览器数据或公司内部文档。

- 入口为 README.md。可安装 Skill 位于 skills/，用户全局规则模板位于 templates/；不要把仓库自身的 AGENTS.md 当作用户规则模板安装。
- scripts/restore.py 默认只预览，仅 --apply 写入；已有差异必须拒绝，只有显式 --overwrite 才备份后替换。不自动修改 config.toml、权限、登录态、代理或其他 agent 的配置。
- 脚本使用 Python 3.11+ 标准库。修改恢复行为后运行 python -m unittest discover -s tests -v，所有恢复测试使用临时目录。
- 官方二进制及官方 Skill 从供应商获取，不打包浏览器、CUA 二进制或插件缓存。操作参数以安装版本的 skill/help/describe 为准。
- 发布前检查文件中是否含用户名绝对路径、账号、密钥、会话、私有地址；不包含此类实际数据。
