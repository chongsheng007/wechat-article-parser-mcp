# 快速开始指南

## 一分钟快速测试

### 1. 设置环境变量

```bash
export SEEDREAM_API_KEY="2b9a2920-1636-4549-bfb0-e1af92206aa2"
export API_BASE_URL="https://ark.cn-beijing.volces.com"
export REQUEST_TIMEOUT="60"
```

### 2. 同步依赖

```bash
uv sync
```

### 3. 测试图像生成

```bash
uv run python test_generate_image.py
```

## 启动开发服务器

### 方式 1: 使用启动脚本（推荐）

```bash
./start_dev.sh
```

然后访问：http://localhost:6274

### 方式 2: 手动启动

```bash
uv run fastmcp dev src/seedream_image_generator/server.py
```

## 在 Cursor 中使用

1. **配置 MCP 服务器**（如果还未配置）

编辑 `~/.cursor/mcp.json` 或 `~/.config/cursor/mcp.json`:

```json
{
  "mcpServers": {
    "seedream-image-generator": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "/Users/changjp/my-first-mcp-server/seedream_server.py"
      ],
      "env": {
        "SEEDREAM_API_KEY": "2b9a2920-1636-4549-bfb0-e1af92206aa2",
        "API_BASE_URL": "https://ark.cn-beijing.volces.com",
        "REQUEST_TIMEOUT": "60"
      }
    }
  }
}
```

2. **重启 Cursor**

3. **在聊天中使用**

直接在 Cursor 聊天中说：
- "使用即梦生成一只小猫的图片"
- "帮我生成一张风景画"
- "创建一个卡通风格的动物图片"

## 常见问题

### Q: 遇到 `ModelNotOpen` 错误？

**A:** 需要先在火山引擎 Ark Console 激活模型：

1. 访问：https://console.volcengine.com/ark/
2. 激活模型：`doubao-seedream-4-0-250828`
3. 等待 5-30 分钟生效

### Q: 如何查看所有可用的工具？

**A:** 在 MCP Inspector 中：
1. 访问 http://localhost:6274
2. 点击左侧 "Tools" 菜单
3. 查看所有已注册的工具

### Q: 如何测试不同的工具？

**A:** 使用 MCP Inspector：

1. 启动开发服务器：`./start_dev.sh`
2. 访问 http://localhost:6274
3. 选择 "Tools" → 选择工具 → 输入参数 → "Call Tool"

## 工具使用示例

### 文生图 (generate_image)

```json
{
  "prompt": "一只可爱的小猫",
  "size": "1024x1024"
}
```

### 生成组图 (generate_image_group)

```json
{
  "prompt": "美丽的日落",
  "num_images": 4,
  "size": "1024x1024"
}
```

### 图生图 (generate_image_from_image)

```json
{
  "prompt": "将这张图片变成卡通风格",
  "image_url": "https://example.com/image.jpg",
  "size": "1024x1024"
}
```

### 多图融合 (generate_image_fusion)

```json
{
  "prompt": "融合这两张图片",
  "image_urls": [
    "https://example.com/image1.jpg",
    "https://example.com/image2.jpg"
  ],
  "size": "1024x1024"
}
```

