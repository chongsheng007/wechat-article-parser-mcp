# 导入错误修复说明

## 问题

使用 `fastmcp dev server.py` 时出现：
```
ImportError: attempted relative import with no known parent package
```

## 原因

`server.py` 使用相对导入（`from .tools.xxx`），当 `fastmcp dev` 直接运行时，Python 不知道包的上下文。

## 解决方案

已创建 `wechat_server.py` 作为入口文件，使用绝对导入：

```python
# 添加 src 目录到 sys.path
sys.path.insert(0, str(src_root))

# 使用绝对导入
from wechat_article_parser.tools.parse_article import register_parse_article_tool
from wechat_article_parser.tools.extract_metadata import register_extract_metadata_tool
from wechat_article_parser.tools.extract_images import register_extract_images_tool
```

## 正确的启动命令

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
uv run fastmcp dev wechat_server.py
```

## 验证

服务器模块已成功加载：
```
✅ 服务器模块加载成功: WeChat Article Parser
```

## 如果还有问题

### 使用标准 MCP Inspector（不需要 fastmcp dev）

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

### 直接在 Cursor 中使用（最推荐）

编辑 `~/.cursor/mcp.json`，使用 `wechat_server.py` 作为入口文件。

