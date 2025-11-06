# Seedream 4.0 MCP Server 开发指南

## 🚀 快速开始

### 1. 启动 MCP Inspector（开发模式）

使用以下命令启动 MCP Inspector 来测试和开发：

```bash
cd /Users/changjp/my-first-mcp-server
export SEEDREAM_API_KEY="2b9a2920-1636-4549-bfb0-e1af92206aa2"
npx @modelcontextprotocol/inspector --transport stdio -- uv run python seedream_server.py
```

MCP Inspector 会自动在浏览器中打开，或者你可以手动访问显示的 URL。

### 2. 在 Cursor 中使用

服务器已经在 `~/.cursor/mcp.json` 中配置为 `seedream-image-generator`。

在 Cursor 中：
1. 重启 Cursor 或重新加载 MCP 配置
2. 在聊天中可以直接使用四个工具：
   - `generate_image` - 文生图
   - `generate_image_group` - 生成组图
   - `generate_image_from_image` - 图生图
   - `generate_image_fusion` - 多图融合

## 🛠️ 开发工具

### 四个已实现的工具

#### 1. generate_image（文生图）
```python
# 使用示例
generate_image(
    prompt="一只可爱的小猫",
    width=1024,
    height=1024,
    steps=30,
    guidance_scale=7.5
)
```

#### 2. generate_image_group（生成组图）
```python
# 使用示例
generate_image_group(
    prompt="美丽的风景",
    num_images=3,
    width=1024,
    height=1024
)
```

#### 3. generate_image_from_image（图生图）
```python
# 使用示例
generate_image_from_image(
    prompt="一只可爱的小猫",
    image_url="https://example.com/reference.jpg",
    strength=0.8,
    width=1024,
    height=1024
)
```

#### 4. generate_image_fusion（多图融合）
```python
# 使用示例
generate_image_fusion(
    prompt="融合两张图像的特征",
    image_urls=[
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ],
    fusion_weights=[0.5, 0.5],
    width=1024,
    height=1024
)
```

## 📁 项目结构

```
src/seedream_image_generator/
├── server.py                          # 主服务器（注册所有工具）
├── tools/
│   ├── generate_image.py              # 文生图工具
│   ├── generate_image_group.py        # 生成组图工具
│   ├── generate_image_from_image.py   # 图生图工具
│   └── generate_image_fusion.py       # 多图融合工具
└── utils/
    ├── api_client.py                  # API 客户端（所有请求函数）
    ├── errors.py                      # 错误处理
    └── formatters.py                  # 响应格式化
```

## 🔧 API 端点

- **文生图/生成组图**: `https://ark.cn-beijing.volces.com/api/v3/images/generations`
- **图生图**: `https://ark.cn-beijing.volces.com/api/v3/images/img2img`
- **多图融合**: `https://ark.cn-beijing.volces.com/api/v3/images/fusion`

## ✅ 开发检查清单

- [x] 四个工具全部实现
- [x] API 客户端支持所有请求类型
- [x] 错误处理完善
- [x] 响应格式化统一
- [x] 水印统一设置为 false
- [x] stdio 传输方式
- [ ] 测试所有工具功能
- [ ] 验证 API 响应格式
- [ ] 优化错误消息

## 🐛 调试技巧

### 查看日志

服务器输出会显示在终端中，包括：
- API 请求详情
- 错误信息
- 调试信息

### 测试单个工具

在 MCP Inspector 中：
1. 切换到 "Tools" 标签
2. 选择要测试的工具
3. 填写参数
4. 点击 "Call Tool" 执行

### 常见问题

1. **API Key 错误**: 确保环境变量 `SEEDREAM_API_KEY` 已设置
2. **404 错误**: 检查 API 端点是否正确
3. **500 错误**: 检查模型名称和参数格式

## 📝 下一步

1. 在 MCP Inspector 中测试所有工具
2. 根据实际 API 响应调整代码
3. 优化错误处理和用户体验
4. 添加更多测试用例


