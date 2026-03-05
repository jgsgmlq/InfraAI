# Skills 已迁移

Skills 文件已迁移到分层结构：

| 位置 | 用途 |
|------|------|
| `core/.agent/skills/` | 框架核心 skills（可移植） |
| `project/.agent/skills/` | 项目自定义 skills |
| `project/.agent/external/` | 外部导入的 skills |

此目录保留用于后向兼容，不再存放实际 skill 文件。
