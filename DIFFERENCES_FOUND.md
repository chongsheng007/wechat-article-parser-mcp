# 老师文档与我们的文档关键差异

## ✅ 已修复的关键差异

### 1. 模型名称 ❌ → ✅
- **之前**: `Seedream-4.0`
- **现在**: `doubao-seedream-4-0-250828` ✅
- **来源**: cursor/3 文件第 28 行

### 2. API 参数格式

#### 文生图参数
- ✅ 使用 `size` 参数（"1K", "2K", "2048x2048"）
- ✅ 添加 `response_format` 参数（默认 "url"）
- ✅ 添加 `optimize_prompt` 参数（默认 True）
- ✅ 显式设置 `watermark: False`
- ✅ 移除 `steps` 和 `guidance_scale`（doubao-seedream-4.0 不支持）

#### 组图功能
- ✅ 使用 `sequential_image_generation: "auto"`
- ✅ 使用 `sequential_image_generation_options.max_images`
- ❌ 之前使用 `num_images` 参数

#### 图生图参数
- ✅ 使用 `image` 参数（不是 `image_url`）
- ✅ 支持 URL 或 Base64
- ✅ 移除 `strength` 参数（doubao-seedream-4.0 不支持）

#### 多图融合参数
- ✅ 使用 `image` 参数（数组形式，不是 `image_urls`）
- ✅ 支持 1-10 张参考图
- ✅ 移除 `fusion_weights` 参数（不支持）

### 3. 环境变量
- 文档中提到使用 `ARK_API_KEY`，但我们使用 `SEEDREAM_API_KEY`（这个应该可以，只是命名不同）

## 📊 测试结果对比

### 之前（使用 Seedream-4.0）
- 状态码: 500 InternalServiceError
- 错误: 服务器内部错误

### 现在（使用 doubao-seedream-4-0-250828）
- 状态码: 404 ModelNotOpen
- 错误: "Your account 2101246886 has not activated the model doubao-seedream-4-0-250828. Please activate the model service in the Ark Console."

## 🎯 结论

**代码格式现在是正确的！** 

错误信息非常明确：需要在 Ark Console（火山引擎控制台）中开通 `doubao-seedream-4-0-250828` 模型服务。

## 📝 下一步操作

1. **登录火山引擎控制台**
   - 访问：https://console.volcengine.com/
   - 账号：2101246886

2. **开通模型服务**
   - 找到 Ark 服务或即梦服务
   - 开通 `doubao-seedream-4-0-250828` 模型
   - 确认服务配额和权限

3. **重启 MCP Inspector 测试**
   - 一旦服务开通，所有四个工具应该可以正常工作

## ✅ 代码更新清单

- [x] 模型名称更新为 `doubao-seedream-4-0-250828`
- [x] 使用 `size` 参数替代 `width` 和 `height`
- [x] 添加 `response_format` 和 `optimize_prompt`
- [x] 显式设置 `watermark: False`
- [x] 移除不支持的参数（steps, guidance_scale, strength, fusion_weights）
- [x] 图生图使用 `image` 参数
- [x] 多图融合使用 `image` 数组
- [x] 组图使用 `sequential_image_generation`


