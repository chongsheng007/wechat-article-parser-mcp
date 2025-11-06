# MCP Inspector 连接问题 - 完整总结

## 问题概述

在配置和使用微信公众号文章解析 MCP Server 时，遇到了 MCP Inspector 连接问题，经过多次尝试最终成功解决。

---

## 遇到的问题

### 问题 1: 导入错误（ImportError）

**错误信息**:
```
ImportError: attempted relative import with no known parent package
```

**原因**:
- `server.py` 使用相对导入（`from .tools.xxx`）
- `fastmcp dev` 直接运行文件时，Python 不知道包的上下文

**解决方案**:
- ✅ 创建了 `wechat_server.py` 作为入口文件
- ✅ 使用绝对导入替代相对导入
- ✅ 正确设置 `sys.path` 以支持包导入

**关键代码**:
```python
# wechat_server.py
import sys
from pathlib import Path

project_root = Path(__file__).parent
src_root = project_root.parent
sys.path.insert(0, str(src_root))

# 使用绝对导入
from wechat_article_parser.tools.parse_article import register_parse_article_tool
```

---

### 问题 2: 端口占用

**错误信息**:
```
❌ Proxy Server PORT IS IN USE at port 6277 ❌
```

**原因**:
- 之前的 MCP Inspector 进程没有正确关闭
- 端口 6277 被占用

**解决方案**:
- ✅ 停止占用端口的进程：`kill -9 <PID>`
- ✅ 或使用清理命令：`pkill -f "fastmcp"`

**成功方法**:
```bash
# 查找并停止进程
lsof -i :6277
kill -9 <PID>
```

---

### 问题 3: Session Token 配置

**错误信息**:
```
Connection Error - Did you add the proxy session token in Configuration?
```

**原因**:
- `fastmcp dev` 会生成 session token
- 需要在 MCP Inspector 配置中正确填写 token
- 需要区分两个端口：6274（Web UI）和 6277（Proxy API）

**关键理解**:
- **端口 6274**: MCP Inspector 的 Web 界面（在浏览器中访问）
- **端口 6277**: Proxy 服务器的 API 端点（不在浏览器中打开，只在配置中填写）

**最终成功的配置**:
```
Transport Type: STDIO
Command: uv
Arguments: run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python wechat_server.py
Inspector Proxy Address: http://localhost:6277
Proxy Session Token: 06a33a9ad3a12ee339c352a25f66f510463a597e184b361160d25f2d41e0e017
```

**重要细节**:
- Arguments 中 `run` 和 `--directory` 之间必须有空格
- 使用 `wechat_server.py` 而不是 `server.py`
- Inspector Proxy Address 填写 `http://localhost:6277`（不是 6274）
- 这个地址不在浏览器中打开，只在配置字段中填写

---

### 问题 4: 连接错误

**错误信息**:
```
Connection Error - Check if your MCP server is running and proxy token is correct
```

**尝试的解决方案**:
1. ❌ 在浏览器中打开 `http://localhost:6277`（错误 - 这是 API 端点，不是 Web 页面）
2. ❌ 使用错误的 Arguments 格式（缺少空格）
3. ❌ 使用 `server.py` 而不是 `wechat_server.py`
4. ❌ Inspector Proxy Address 填写错误的端口（6274 而不是 6277）

---

## ✅ 最终成功的解决方案

### 关键步骤

1. **使用正确的入口文件**:
   - 使用 `wechat_server.py` 而不是 `server.py`

2. **正确的启动命令**:
   ```bash
   cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
   uv run fastmcp dev wechat_server.py
   ```

3. **获取 Session Token**:
   - 服务器启动后会显示 token 和完整 URL
   - 例如：`http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=06a33a9ad3a12ee339c352a25f66f510463a597e184b361160d25f2d41e0e017`

4. **在浏览器中访问**:
   - 使用带 token 的完整 URL 访问端口 6274

5. **在 MCP Inspector 中配置**:
   - Transport Type: `STDIO`
   - Command: `uv`
   - Arguments: `run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python wechat_server.py`
   - Inspector Proxy Address: `http://localhost:6277`
   - Proxy Session Token: `（从服务器输出中复制）`

6. **点击 Connect**

---

## ❌ 没有成功的尝试

### 1. 直接使用 `server.py`

**尝试**: 使用 `fastmcp dev server.py`

**结果**: 失败 - 相对导入错误

**原因**: `server.py` 使用相对导入，无法直接运行

---

### 2. 在浏览器中打开端口 6277

**尝试**: 在浏览器中访问 `http://localhost:6277`

**结果**: 失败 - 无法打开

**原因**: 端口 6277 是 API 端点，不是 Web 页面，不应该在浏览器中打开

---

### 3. 使用错误的 Arguments 格式

**尝试**: `run--directory ...`（缺少空格）

**结果**: 失败 - 命令解析错误

**原因**: `run` 和 `--directory` 之间必须有空格

---

### 4. 使用错误的 Inspector Proxy Address

**尝试**: 填写 `http://localhost:6274`

**结果**: 失败 - 连接错误

**原因**: 应该填写 `http://localhost:6277`（proxy 服务器端口）

---

### 5. 使用 `fastmcp dev` 但不配置 proxy

**尝试**: 启动服务器但不填写 proxy 配置

**结果**: 失败 - 连接错误

**原因**: `fastmcp dev` 需要 proxy 配置才能工作

---

## 📚 学到的经验

### 1. 端口理解

- **6274**: Web UI，在浏览器中访问
- **6277**: Proxy API，不在浏览器中打开，只在配置中填写

### 2. 导入问题

- 相对导入（`from .tools.xxx`）在直接运行文件时会有问题
- 需要创建入口文件，使用绝对导入或正确设置路径

### 3. 配置细节

- Arguments 中的空格很重要
- 使用正确的入口文件（`wechat_server.py`）
- Session Token 必须从服务器输出中获取

### 4. 替代方案

如果 `fastmcp dev` 一直有问题，可以：
- 使用标准 MCP Inspector（`npx @modelcontextprotocol/inspector`）
- 直接在 Cursor 中配置使用（最推荐）

---

## ✅ 替代方案：使用标准 MCP Inspector（不需要 Proxy）

如果 `fastmcp dev` 的 proxy 配置一直有问题，可以使用标准 MCP Inspector，这种方式**不需要 proxy 和 token**。

### 启动步骤

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
./start_inspector.sh
```

或者手动启动：

```bash
cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser
npx @modelcontextprotocol/inspector --transport stdio -- uv run python wechat_server.py
```

### 配置说明

在打开的 MCP Inspector 页面中配置：

- **Transport Type**: `STDIO` ✅
- **Command**: `uv` ✅
- **Arguments**: `run --directory /Users/changjp/my-first-mcp-server/src/wechat_article_parser python wechat_server.py` ✅
- **不需要** Inspector Proxy Address（留空或删除）
- **不需要** Proxy Session Token（留空或删除）

**直接点击 Connect 即可！**

### 优势

- ✅ 不需要处理 proxy 配置
- ✅ 不需要 session token
- ✅ 更简单直接
- ✅ 使用 stdio 传输，更稳定

### 与 fastmcp dev 的区别

| 特性 | fastmcp dev | 标准 MCP Inspector |
|------|-------------|-------------------|
| 需要 Proxy | ✅ 是 | ❌ 否 |
| 需要 Token | ✅ 是 | ❌ 否 |
| 配置复杂度 | 较高 | 较低 |
| 端口 | 6274 (Web) + 6277 (Proxy) | 5173 (Web) |
| 稳定性 | 可能有问题 | 更稳定 |

---

## 🎯 推荐的工作流程

### 开发/测试阶段

1. 使用 `fastmcp dev wechat_server.py` 启动
2. 复制完整 URL（带 token）到浏览器
3. 在 MCP Inspector 中配置并测试工具

### 日常使用阶段

**直接在 Cursor 中配置使用**：

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

这样就不需要 MCP Inspector 了，直接在聊天中使用工具。

---

## 📝 关键文件

- `wechat_server.py` - 入口文件（解决导入问题）
- `server.py` - 原始服务器文件（使用相对导入）
- `start_inspector.sh` - 标准 MCP Inspector 启动脚本

---

## ✅ 成功的关键因素

1. **正确的入口文件**: `wechat_server.py` 使用绝对导入
2. **正确的 Arguments 格式**: 注意空格和文件路径
3. **正确的端口理解**: 6274 用于 Web，6277 用于 API
4. **正确的 Token 配置**: 从服务器输出中获取并填写

---

## 🎉 最终状态

✅ 服务器成功启动  
✅ MCP Inspector 成功连接  
✅ 工具可以正常测试和使用  

---

**总结**: 通过创建正确的入口文件、理解端口用途、正确配置 Arguments 和 Token，最终成功解决了所有连接问题。

