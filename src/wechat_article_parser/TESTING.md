# 测试指南

## MCP 服务器已启动

如果服务器正在运行，你可以：

### 1. 访问 MCP Inspector

打开浏览器访问：
**http://localhost:6274**

### 2. 测试工具

在 MCP Inspector 中，你可以测试以下工具：

#### 工具 1: parse_wechat_article
解析完整的微信公众号文章

**测试参数**:
```json
{
  "url": "https://mp.weixin.qq.com/s/your-article-url",
  "format": "markdown",
  "include_images": true,
  "include_links": true
}
```

#### 工具 2: extract_article_metadata
快速提取文章元数据

**测试参数**:
```json
{
  "url": "https://mp.weixin.qq.com/s/your-article-url"
}
```

#### 工具 3: extract_article_images
提取文章中的所有图片

**测试参数**:
```json
{
  "url": "https://mp.weixin.qq.com/s/your-article-url",
  "include_cover": true
}
```

## 测试真实文章

你可以使用真实的微信公众号文章 URL 进行测试：

1. 打开一篇微信公众号文章
2. 复制文章 URL
3. 在 MCP Inspector 中使用该 URL 测试工具

## 停止服务器

按 `Ctrl+C` 停止服务器

## 故障排除

### 问题：无法访问 MCP Inspector

**解决方案**:
1. 确认服务器正在运行
2. 检查端口 6274 是否被占用
3. 尝试重启服务器

### 问题：工具调用失败

**可能原因**:
- URL 格式不正确
- 文章需要登录访问
- 网络连接问题

**解决方案**:
- 检查 URL 格式是否为有效的微信公众号文章 URL
- 尝试在浏览器中打开该 URL 确认可以访问
- 检查网络连接

## 在 Cursor 中使用

配置 MCP Server 到 Cursor 后，可以在聊天中直接使用：

- "解析这篇文章: https://mp.weixin.qq.com/s/..."
- "提取这篇文章的元数据: https://mp.weixin.qq.com/s/..."
- "提取这篇文章的图片: https://mp.weixin.qq.com/s/..."

