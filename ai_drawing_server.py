"""
AI 画图 MCP Server
使用即梦 Seedream 4.0 模型 API 进行图像生成

参考文档：https://www.volcengine.com/docs/82379/1541523
"""

from fastmcp import FastMCP
import requests
import json
import os
from typing import Optional

# 创建 MCP 服务实例
mcp = FastMCP("AI Drawing Server - Seedream 4.0")

# ============================================
# 工具定义（Tools）
# ============================================

@mcp.tool()
def generate_image(
    prompt: str,
    negative_prompt: Optional[str] = None,
    width: int = 1024,
    height: int = 1024,
    seed: Optional[int] = None,
    steps: int = 30,
    guidance_scale: float = 7.5,
    api_key: Optional[str] = None
) -> str:
    """
    使用即梦 Seedream 4.0 模型生成图像
    
    参数：
        prompt: 图像生成的提示词（必填）
        negative_prompt: 负面提示词，描述不希望出现在图像中的内容（可选）
        width: 图像宽度，默认 1024
        height: 图像高度，默认 1024
        seed: 随机种子，用于生成可重复的图像（可选）
        steps: 生成步数，默认 30
        guidance_scale: 引导强度，默认 7.5
        api_key: API 密钥，如果未提供则从环境变量 SEEDREAM_API_KEY 读取
    
    返回：
        图像生成的 URL 或错误信息
    
    参考：https://www.volcengine.com/docs/82379/1541523
    """
    # 获取 API 密钥
    if not api_key:
        api_key = os.getenv("SEEDREAM_API_KEY")
        if not api_key:
            return "错误：未提供 API 密钥，请设置环境变量 SEEDREAM_API_KEY 或在调用时提供 api_key 参数"
    
    # 即梦 API 端点（根据火山引擎文档）
    # 参考: https://www.volcengine.com/docs/82379/1541523
    # 正确的端点是 ark.cn-beijing.volces.com
    api_url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    
    # 构建请求头
    # 火山引擎 API 可能使用不同的认证方式
    headers = {
        "Content-Type": "application/json"
    }
    
    # 尝试不同的认证方式
    # 方式1: Bearer Token
    if api_key.startswith("Bearer "):
        headers["Authorization"] = api_key
    elif len(api_key) > 50:  # 可能是 Token
        headers["Authorization"] = f"Bearer {api_key}"
    else:  # 可能是 AccessKey，需要配合 SecretKey 使用签名
        headers["X-Access-Key"] = api_key
    
    # 构建请求体（根据即梦 API 文档格式）
    # 根据测试，Seedream-4.0 (首字母大写) 返回 500 而不是 404，说明格式可能接近
    # 使用 Seedream-4.0 作为主要模型名称
    payload = {
        "model": "Seedream-4.0",
        "prompt": prompt,
        "width": width,
        "height": height
    }
    
    # 添加可选参数（如果 API 支持）
    if steps > 0:
        payload["steps"] = steps
    if guidance_scale > 0:
        payload["guidance_scale"] = guidance_scale
    
    # 如果 width 和 height 都是 1024，也可以尝试使用 size 参数
    # 但根据测试，使用 width/height 更可靠
    
    # 添加可选参数
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    
    if seed is not None:
        payload["seed"] = seed
    
    try:
        # 发送请求
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=120  # 图像生成可能需要较长时间
        )
        
        # 记录请求信息用于调试
        debug_info = f"""
请求 URL: {api_url}
请求头: {json.dumps(dict(headers), indent=2, ensure_ascii=False)}
请求体: {json.dumps(payload, indent=2, ensure_ascii=False)}
响应状态码: {response.status_code}
"""
        
        # 如果返回 500 错误，可能是参数问题或服务问题
        # 如果返回 404 错误，尝试其他模型名称
        if response.status_code in [404, 500]:
            error_data = response.json() if response.text else {}
            error_code = error_data.get("error", {}).get("code", "")
            
            # 如果是 404，尝试其他模型名称
            if response.status_code == 404 and "InvalidEndpointOrModel" in str(error_data):
                alternative_models = ["seedream-4.0", "seedream_v4.0", "Seedream4.0"]
                for model_name in alternative_models:
                    payload["model"] = model_name
                    response = requests.post(
                        api_url,
                        headers=headers,
                        json=payload,
                        timeout=120
                    )
                    if response.status_code == 200:
                        break
            
            # 如果是 500，尝试简化参数
            elif response.status_code == 500:
                # 尝试最小参数集
                minimal_payload = {
                    "model": payload["model"],
                    "prompt": payload["prompt"]
                }
                if "width" in payload and "height" in payload:
                    minimal_payload["width"] = payload["width"]
                    minimal_payload["height"] = payload["height"]
                
                response = requests.post(
                    api_url,
                    headers=headers,
                    json=minimal_payload,
                    timeout=120
        )
        
        # 检查响应状态
        if response.status_code == 200:
            result = response.json()
            
            # 根据即梦 API 响应格式解析（可能的结构）
            # 方式1: 直接返回 image_url
            if "image_url" in result:
                return f"✅ 图像生成成功！\n🖼️  图像 URL: {result['image_url']}"
            
            # 方式2: 嵌套在 data 字段中
            elif "data" in result:
                data = result["data"]
                if isinstance(data, list) and len(data) > 0:
                    # 数组格式
                    first_item = data[0]
                    if "image_url" in first_item:
                        return f"✅ 图像生成成功！\n🖼️  图像 URL: {first_item['image_url']}"
                    elif "url" in first_item:
                        return f"✅ 图像生成成功！\n🖼️  图像 URL: {first_item['url']}"
                    elif "image" in first_item:
                        # 可能返回 base64 编码的图片
                        return f"✅ 图像生成成功！\n📸 图像数据已返回（base64 编码）"
                elif isinstance(data, dict):
                    # 对象格式
                    if "image_url" in data:
                        return f"✅ 图像生成成功！\n🖼️  图像 URL: {data['image_url']}"
                    elif "url" in data:
                        return f"✅ 图像生成成功！\n🖼️  图像 URL: {data['url']}"
            
            # 方式3: 直接返回 url
            elif "url" in result:
                return f"✅ 图像生成成功！\n🖼️  图像 URL: {result['url']}"
            
            # 如果都不匹配，返回完整响应以便调试
            else:
                return f"⚠️  图像生成成功，但响应格式未识别：\n{json.dumps(result, indent=2, ensure_ascii=False)}\n\n请检查 API 响应格式，可能需要调整代码。"
        else:
            error_msg = f"❌ API 请求失败 (状态码: {response.status_code})"
            
            # 尝试解析错误响应
            try:
                error_detail = response.json()
                error_msg += f"\n\n📋 错误详情:\n{json.dumps(error_detail, indent=2, ensure_ascii=False)}"
                
                # 检查是否有 logid 或具体的错误信息
                if "logid" in error_detail:
                    error_msg += f"\n\n🔍 Log ID: {error_detail.get('logid')}"
                if "error" in error_detail:
                    error_msg += f"\n\n⚠️  错误信息: {error_detail.get('error')}"
                if "message" in error_detail:
                    error_msg += f"\n\n📝 消息: {error_detail.get('message')}"
                    
            except:
                error_msg += f"\n\n📄 响应内容: {response.text[:500]}"
            
            # 添加调试信息
            error_msg += f"\n\n🔧 调试信息:{debug_info}"
            error_msg += "\n\n💡 排查建议："
            
            if response.status_code == 500:
                error_msg += "\n1. ⚠️  500 内部错误通常表示："
                error_msg += "\n   - API Key 可能没有权限访问该模型"
                error_msg += "\n   - 需要在火山引擎控制台开通即梦服务"
                error_msg += "\n   - 模型名称可能正确，但服务配置有问题"
                error_msg += "\n   - 建议联系火山引擎技术支持，提供 logid"
            elif response.status_code == 404:
                error_msg += "\n1. ⚠️  404 错误表示模型不存在或无权访问"
                error_msg += "\n   - 检查模型名称是否正确"
                error_msg += "\n   - 确认 API Key 是否有权限访问该模型"
            else:
                error_msg += "\n1. 检查 API Key 是否正确"
                error_msg += "\n2. 确认 API URL 是否正确（当前: ark.cn-beijing.volces.com）"
                error_msg += "\n3. 检查请求参数格式是否符合 API 文档要求"
                error_msg += "\n4. 确认是否需要使用签名认证（火山引擎通常需要 AccessKey + SecretKey）"
            
            error_msg += "\n\n📚 参考文档："
            error_msg += "\n- https://www.volcengine.com/docs/82379/1541523"
            error_msg += "\n- https://www.volcengine.com/docs/82379/1824121"
            
            return error_msg
            
    except requests.exceptions.Timeout:
        return "错误：请求超时，图像生成可能需要更长时间"
    except requests.exceptions.RequestException as e:
        return f"错误：网络请求失败 - {str(e)}"
    except Exception as e:
        return f"错误：处理请求时发生异常 - {str(e)}"


@mcp.tool()
def generate_image_simple(prompt: str) -> str:
    """
    简化版图像生成工具（使用默认参数）
    
    参数：
        prompt: 图像生成的提示词
    
    返回：
        图像生成的 URL 或错误信息
    """
    return generate_image(prompt=prompt)


# ============================================
# 启动服务
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("AI 画图 MCP Server - Seedream 4.0")
    print("=" * 60)
    print("提示：请确保已设置环境变量 SEEDREAM_API_KEY")
    print("或在调用时提供 api_key 参数")
    print("=" * 60)
    
    # 运行 MCP 服务器
    mcp.run()

