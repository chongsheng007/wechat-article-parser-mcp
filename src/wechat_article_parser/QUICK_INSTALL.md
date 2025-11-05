# 快速安装指南

## 一键配置到 Cursor

### 方式 1: 使用安装脚本（推荐）

```bash
# 克隆项目后
cd src/wechat_article_parser
./install_cursor_mcp.sh
```

脚本会自动：
- 检测项目路径
- 创建 Cursor 配置文件
- 添加 MCP Server 配置

### 方式 2: 手动配置

1. **复制配置文件内容**

   打开 `cursor-mcp-config.json`，复制配置内容。

2. **编辑 Cursor 配置文件**

   - macOS/Linux: `~/.cursor/mcp.json`
   - Windows: `%APPDATA%\Cursor\User\mcp.json`

3. **修改路径**

   将配置中的路径替换为你的实际项目路径：
   ```json
   "/path/to/your/project/src/wechat_article_parser"
   ```

4. **重启 Cursor**

   完全退出并重新启动 Cursor。

## 验证安装

重启 Cursor 后，在聊天中问：
"你能看到 wechat-article-parser 的工具吗？"

如果配置正确，AI 会告诉你它可以使用的工具。

## 开始使用

```
解析这篇文章: https://mp.weixin.qq.com/s/...
```

## 详细文档

- [CURSOR_SETUP.md](CURSOR_SETUP.md) - 完整配置指南
- [README.md](README.md) - 项目说明

