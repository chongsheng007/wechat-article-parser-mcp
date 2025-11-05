# 快速开始指南

## 第一步：安装依赖

```bash
cd src/wechat_article_parser
uv sync
```

## 第二步：测试服务器

```bash
# 使用 fastmcp dev 启动开发服务器
uv run fastmcp dev server.py
```

访问 http://localhost:6274 打开 MCP Inspector

## 第三步：测试工具

在 MCP Inspector 中测试工具：

### 测试 parse_wechat_article

```json
{
  "url": "https://mp.weixin.qq.com/s/your-article-url",
  "format": "markdown"
}
```

### 测试 extract_article_metadata

```json
{
  "url": "https://mp.weixin.qq.com/s/your-article-url"
}
```

### 测试 extract_article_images

```json
{
  "url": "https://mp.weixin.qq.com/s/your-article-url",
  "include_cover": true
}
```

## 第四步：在 Cursor 中使用

1. 配置 MCP Server（在 Cursor 设置中）
2. 重启 Cursor
3. 在聊天中使用：
   - "解析这篇文章: https://mp.weixin.qq.com/s/..."

## GitHub 工作流程

详细说明请参考：`.cursor/specs/wechat-article-parser/GITHUB_WORKFLOW.md`

### 快速提交代码

```bash
# 1. 初始化 Git（如果还没有）
git init
git remote add origin https://github.com/your-username/wechat-article-parser-mcp.git

# 2. 添加文件
git add .

# 3. 提交
git commit -m "feat: 初始项目结构"

# 4. 推送
git push -u origin main
```

