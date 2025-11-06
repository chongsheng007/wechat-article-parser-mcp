# MCP Inspector 输入格式说明

## 错误格式

❌ **函数调用格式**（错误）:
```
parse_wechat_article_tool(url="https://mp.weixin.qq.com/s/nEJhdxGea-KLZA_IGw9R5A", format="markdown")
```

## ✅ 正确格式

MCP Inspector 需要 **JSON 格式**的输入：

### 格式 1: 完整 JSON 对象

```json
{
  "url": "https://mp.weixin.qq.com/s/nEJhdxGea-KLZA_IGw9R5A",
  "format": "markdown"
}
```

### 格式 2: 简化格式（只填写参数）

在 MCP Inspector 的输入框中，直接填写：

```json
{
  "url": "https://mp.weixin.qq.com/s/nEJhdxGea-KLZA_IGw9R5A",
  "format": "markdown"
}
```

## 工具参数说明

### parse_wechat_article（解析文章）

**完整参数示例**:
```json
{
  "url": "https://mp.weixin.qq.com/s/nEJhdxGea-KLZA_IGw9R5A",
  "format": "markdown",
  "include_images": true,
  "include_links": true
}
```

**简化示例**（只填必填参数）:
```json
{
  "url": "https://mp.weixin.qq.com/s/nEJhdxGea-KLZA_IGw9R5A"
}
```

**参数说明**:
- `url`: 文章 URL（必填）
- `format`: 输出格式，可选值：`markdown`（默认）、`text`、`html`
- `include_images`: 是否包含图片信息（默认：true）
- `include_links`: 是否包含链接信息（默认：true）

### extract_article_metadata（提取元数据）

```json
{
  "url": "https://mp.weixin.qq.com/s/nEJhdxGea-KLZA_IGw9R5A"
}
```

### extract_article_images（提取图片）

```json
{
  "url": "https://mp.weixin.qq.com/s/nEJhdxGea-KLZA_IGw9R5A",
  "include_cover": true
}
```

## 在 MCP Inspector 中使用步骤

1. **选择工具**: 在 Tools 列表中选择 `parse_wechat_article`
2. **填写参数**: 在输入框中输入 JSON 格式的参数
3. **点击调用**: 点击 "Call Tool" 或 "调用工具" 按钮

## 示例

### 示例 1: 解析文章（Markdown 格式）

```json
{
  "url": "https://mp.weixin.qq.com/s/nEJhdxGea-KLZA_IGw9R5A",
  "format": "markdown"
}
```

### 示例 2: 解析文章（纯文本格式）

```json
{
  "url": "https://mp.weixin.qq.com/s/nEJhdxGea-KLZA_IGw9R5A",
  "format": "text"
}
```

### 示例 3: 解析文章（不包含图片）

```json
{
  "url": "https://mp.weixin.qq.com/s/nEJhdxGea-KLZA_IGw9R5A",
  "format": "markdown",
  "include_images": false
}
```

## 常见错误

### ❌ 错误 1: 使用函数调用格式
```
parse_wechat_article_tool(url="...", format="markdown")
```

### ❌ 错误 2: 缺少引号
```json
{
  url: "https://...",
  format: "markdown"
}
```

### ✅ 正确格式
```json
{
  "url": "https://...",
  "format": "markdown"
}
```

## 快速复制

对于你的 URL，直接复制这个：

```json
{
  "url": "https://mp.weixin.qq.com/s/nEJhdxGea-KLZA_IGw9R5A",
  "format": "markdown"
}
```

