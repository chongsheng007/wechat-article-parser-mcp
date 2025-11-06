# API 格式更新说明

## 已根据文档更新代码

根据提供的文档，我已经更新了代码以匹配文档中的格式：

### 1. 参数格式更新

**之前：**
- 使用 `width` 和 `height` 参数
- 包含 `steps` 和 `guidance_scale`
- 包含 `watermark` 参数

**现在（根据文档）：**
- 使用 `size` 参数（如 "1K", "2K", "2048x2048"）
- 添加 `response_format` 参数（默认 "url"）
- 添加 `optimize_prompt` 参数（默认 True）
- 移除了 `steps`, `guidance_scale`, `watermark` 参数

### 2. 代码更新位置

- `src/seedream_image_generator/utils/api_client.py`
  - `make_api_request()` 函数已更新
  - 支持 `size` 参数
  - 支持 `response_format` 和 `optimize_prompt`

### 3. 测试结果

即使使用文档格式，仍然返回 500 InternalServiceError。

**结论：** 问题不在代码格式，而在 API Key 权限或服务配置。

## 可能的解决方案

### 方案 1: 检查 API Key

1. **确认老师的 API Key 是否与你相同**
   - 如果不同，请使用老师的 API Key 测试

2. **检查 API Key 权限**
   - 登录火山引擎控制台
   - 确认 API Key 是否有 Seedream 4.0 的权限
   - 检查服务是否已开通

### 方案 2: 对比代码差异

请提供：
1. 老师使用的完整请求示例
2. 老师使用的 API Key（如果不同）
3. 老师使用的模型名称（如果不同）

### 方案 3: 联系技术支持

如果 API Key 权限正确但仍报错，联系火山引擎技术支持，提供：
- Request ID: `021762261368621134a33f22921f0bc01c0430890f5ffa36d8a79`
- 错误代码: `InternalServiceError`
- API Key（前几位用于验证）

## 当前代码状态

✅ 代码已更新为符合文档格式
✅ 支持 `size` 参数（1K, 2K, 2048x2048 等）
✅ 支持 `response_format` 和 `optimize_prompt`
✅ 移除了可能不支持的参数
✅ 错误处理完善

## 下一步

1. **重启 MCP Inspector** 测试更新后的代码
2. **如果仍报错**，请提供老师的成功示例以便对比
3. **检查控制台** 确认服务开通状态


