# 微信公众号文章解析 MCP Server

一个基于 FastMCP 的 MCP Server，用于解析微信公众号文章，提取文章内容、元数据、图片和链接。

## 功能特性

- ✅ **文章解析**: 完整解析微信公众号文章内容
- ✅ **元数据提取**: 快速提取标题、作者、发布时间等信息
- ✅ **图片提取**: 提取文章中的所有图片
- ✅ **格式转换**: 支持 Markdown、Text、HTML 格式输出
- ✅ **链接提取**: 提取文章中的外部链接

## 安装

### 使用 uv（推荐）

```bash
# 安装依赖
cd src/wechat_article_parser
uv sync
```

### 使用 pip

```bash
pip install -r requirements.txt
```

## 使用方法

### 方式 1: 在 Cursor 中使用（推荐）

#### 快速配置

1. **复制配置文件**

   编辑 `~/.cursor/mcp.json`（macOS/Linux）或 `%APPDATA%\Cursor\User\mcp.json`（Windows），添加以下配置：

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

   **重要**: 将 `/path/to/your/project` 替换为你的实际项目路径！

2. **重启 Cursor**

   完全退出并重新启动 Cursor。

3. **使用工具**

   在 Cursor 聊天中直接说：
   - "解析这篇文章: https://mp.weixin.qq.com/s/..."
   - "提取这篇文章的元数据: https://mp.weixin.qq.com/s/..."
   - "提取这篇文章的图片: https://mp.weixin.qq.com/s/..."

#### 详细配置说明

查看 [CURSOR_SETUP.md](CURSOR_SETUP.md) 获取完整配置指南。

### 方式 2: 使用 MCP Inspector（开发/测试）

```bash
# 使用 fastmcp dev（开发模式）
cd src/wechat_article_parser
uv run fastmcp dev wechat_server.py

# 访问 http://localhost:6274（使用带 token 的 URL）
```

### 方式 3: 使用标准 MCP Inspector

```bash
cd src/wechat_article_parser
./start_inspector.sh
```

## 工具说明

### 1. parse_wechat_article

解析完整的微信公众号文章。

**参数**:
- `url`: 文章 URL（必填）
- `format`: 输出格式（可选，默认 "markdown"）
- `include_images`: 是否包含图片（默认 true）
- `include_links`: 是否包含链接（默认 true）

### 2. extract_article_metadata

快速提取文章元数据（不解析全文）。

**参数**:
- `url`: 文章 URL（必填）

### 3. extract_article_images

提取文章中的所有图片。

**参数**:
- `url`: 文章 URL（必填）
- `include_cover`: 是否包含封面图（默认 true）
- `image_format`: 图片格式过滤（可选）

## 项目结构

```
src/wechat_article_parser/
├── server.py              # MCP 服务器主文件
├── tools/                 # 工具实现
│   ├── parse_article.py
│   ├── extract_metadata.py
│   └── extract_images.py
└── utils/                 # 工具函数
    ├── parser.py          # 解析核心逻辑
    ├── html_extractor.py  # HTML 提取
    ├── formatters.py      # 格式化工具
    └── errors.py          # 错误处理
```

## 开发

### 运行测试

```bash
# 运行测试脚本
uv run python test_parse_article.py
```

### 代码规范

- 遵循 PEP 8
- 使用类型提示
- 编写文档字符串

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

详见 [CHANGELOG.md](../../CHANGELOG.md)

