# Cursor MCP 配置指南

## 快速配置

### 步骤 1: 复制配置文件

从项目根目录复制 `cursor-mcp-config.json` 的内容，或直接使用以下配置：

```json
{
  "mcpServers": {
    "wechat-article-parser": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/Users/changjp/my-first-mcp-server/src/wechat_article_parser",
        "python",
        "/Users/changjp/my-first-mcp-server/src/wechat_article_parser/wechat_server.py"
      ]
    }
  }
}
```

**重要**: 将 `/Users/changjp/my-first-mcp-server` 替换为你的实际项目路径！

### 步骤 2: 编辑 Cursor 配置文件

#### macOS/Linux

```bash
# 创建配置目录（如果不存在）
mkdir -p ~/.cursor

# 编辑配置文件
nano ~/.cursor/mcp.json
# 或使用其他编辑器
code ~/.cursor/mcp.json
```

#### Windows

```bash
# 配置文件位置
%APPDATA%\Cursor\User\mcp.json
```

### 步骤 3: 添加配置

如果 `mcp.json` 文件已存在其他配置，在 `mcpServers` 对象中添加：

```json
{
  "mcpServers": {
    "existing-server": {
      ...
    },
    "wechat-article-parser": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/your/project/src/wechat_article_parser",
        "python",
        "/path/to/your/project/src/wechat_article_parser/wechat_server.py"
      ]
    }
  }
}
```

### 步骤 4: 修改路径

**重要**: 将配置中的路径替换为你的实际路径：

- 查找: `/Users/changjp/my-first-mcp-server`
- 替换为: 你的项目实际路径

例如：
- `/Users/yourname/my-first-mcp-server`
- `/home/yourname/my-first-mcp-server`
- `C:\Users\yourname\my-first-mcp-server` (Windows)

### 步骤 5: 保存并重启 Cursor

1. 保存配置文件（`Ctrl+O`, `Enter`, `Ctrl+X` 如果使用 nano）
2. **完全退出 Cursor**（Cmd+Q / Ctrl+Q）
3. 重新启动 Cursor

### 步骤 6: 验证配置

重启后，在 Cursor 聊天中问：
"你能看到 wechat-article-parser 的工具吗？"

如果配置正确，AI 会告诉你它可以使用的工具：
- `parse_wechat_article`
- `extract_article_metadata`
- `extract_article_images`

## 使用工具

配置成功后，在 Cursor 聊天中直接使用：

### 解析完整文章

```
解析这篇文章: https://mp.weixin.qq.com/s/...
```

### 提取元数据

```
提取这篇文章的元数据: https://mp.weixin.qq.com/s/...
```

### 提取图片

```
提取这篇文章的所有图片: https://mp.weixin.qq.com/s/...
```

## 配置示例（完整版）

如果这是你唯一的 MCP 服务器：

```json
{
  "mcpServers": {
    "wechat-article-parser": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/your/project/src/wechat_article_parser",
        "python",
        "/path/to/your/project/src/wechat_article_parser/wechat_server.py"
      ]
    }
  }
}
```

如果已有其他 MCP 服务器：

```json
{
  "mcpServers": {
    "existing-server-1": {
      "command": "...",
      "args": [...]
    },
    "wechat-article-parser": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/your/project/src/wechat_article_parser",
        "python",
        "/path/to/your/project/src/wechat_article_parser/wechat_server.py"
      ]
    }
  }
}
```

## 路径说明

### macOS/Linux 路径格式

```json
"/Users/yourname/my-first-mcp-server/src/wechat_article_parser"
```

### Windows 路径格式

```json
"C:\\Users\\yourname\\my-first-mcp-server\\src\\wechat_article_parser"
```

**注意**: Windows 路径中的反斜杠需要转义（`\\`）

## 故障排除

### 问题：工具不可用

**检查**:
1. 配置文件路径是否正确
2. 项目路径是否正确
3. 是否已重启 Cursor

### 问题：路径错误

**解决**:
```bash
# 获取项目绝对路径
cd /path/to/your/project
pwd
```

然后使用输出的路径更新配置。

### 问题：找不到 uv 命令

**解决**: 确保已安装 `uv`：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 快速安装脚本

你也可以创建一个安装脚本来自动配置：

```bash
#!/bin/bash
# install_cursor_mcp.sh

PROJECT_PATH=$(pwd)
CONFIG_DIR="$HOME/.cursor"
CONFIG_FILE="$CONFIG_DIR/mcp.json"

# 创建配置目录
mkdir -p "$CONFIG_DIR"

# 创建或更新配置文件
cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "wechat-article-parser": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "$PROJECT_PATH/src/wechat_article_parser",
        "python",
        "$PROJECT_PATH/src/wechat_article_parser/wechat_server.py"
      ]
    }
  }
}
EOF

echo "✅ 配置已添加到 $CONFIG_FILE"
echo "请重启 Cursor 以生效"
```

## 参考

- 项目 README: `README.md`
- 快速开始: `QUICK_START.md`
- Cursor 配置: `CURSOR_CONFIG.md`

