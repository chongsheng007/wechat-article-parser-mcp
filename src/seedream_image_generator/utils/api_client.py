"""API 请求客户端"""

import requests
import os
from typing import Any, Dict, Optional
from .errors import APIKeyError, handle_api_error, MCPError

# API 端点配置
# 从环境变量读取基础 URL，默认使用 https://ark.cn-beijing.volces.com
def get_api_base_url() -> str:
    """获取 API 基础 URL"""
    base_url = os.getenv("API_BASE_URL", "https://ark.cn-beijing.volces.com")
    # 确保 URL 不以 / 结尾
    if base_url.endswith("/"):
        base_url = base_url.rstrip("/")
    return base_url

# 生成完整的端点 URL
def get_images_generations_url() -> str:
    """获取图像生成端点 URL"""
    return f"{get_api_base_url()}/api/v3/images/generations"

API_BASE_URL = get_images_generations_url()  # 文生图和生成组图
API_IMG2IMG_URL = get_images_generations_url()  # 图生图（使用同一个端点）
API_FUSION_URL = get_images_generations_url()  # 多图融合（使用同一个端点）


def make_api_request(
    api_key: str,
    model: str,
    prompt: str,
    width: int = 1024,
    height: int = 1024,
    steps: int = 30,
    guidance_scale: float = 7.5,
    negative_prompt: Optional[str] = None,
    seed: Optional[int] = None,
    num_images: int = 1,
    size: Optional[str] = None,  # 支持直接传入 size 字符串
    response_format: str = "url"  # 根据文档添加
) -> Dict[str, Any]:
    """
    发起图像生成 API 请求

    Args:
        api_key: API 密钥
        model: 模型标识符
        prompt: 图像生成提示词
        width: 图像宽度
        height: 图像高度
        steps: 生成步数
        guidance_scale: 引导强度
        negative_prompt: 负面提示词
        seed: 随机种子
        num_images: 生成图像数量（用于批量生成）

    Returns:
        API 响应数据

    Raises:
        MCPError: 当 API 请求失败时
    """
    if not api_key:
        raise APIKeyError()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 根据文档，优先使用 size 参数
    # 如果提供了 size，使用它；否则从 width 和 height 生成
    if size:
        size_str = size
    else:
        # 将 width x height 转换为 size 格式
        # 根据文档，支持 "2048x2048", "1K", "2K" 等格式
        if width == 1024 and height == 1024:
            size_str = "1K"
        elif width == 2048 and height == 2048:
            size_str = "2K"
        else:
            size_str = f"{width}x{height}"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size_str,
        "sequential_image_generation": "disabled" if num_images == 1 else "auto",  # 单图时 disabled
        "stream": False,  # 根据示例添加
        "response_format": response_format,
        "watermark": False  # 根据需求，设置为 false（不带水印）
        # 注意：根据实际 API 示例，不包含 optimize_prompt 参数
    }
    
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    
    if seed is not None:
        payload["seed"] = seed
    
    # 如果 num_images > 1，使用 sequential_image_generation_options（组图功能）
    if num_images > 1:
        payload["sequential_image_generation"] = "auto"
        payload["sequential_image_generation_options"] = {
            "max_images": num_images
        }
    
    # 从环境变量读取超时时间，默认 60 秒
    timeout = int(os.getenv("REQUEST_TIMEOUT", "60"))
    
    # 动态获取端点 URL（支持环境变量配置）
    api_url = get_images_generations_url()
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=timeout
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            # 在错误时输出详细的调试信息
            print(f"\n🔍 调试信息 - API 请求错误:")
            print(f"请求 URL: {api_url}")
            print(f"API 基础 URL: {get_api_base_url()}")
            print(f"模型: {model}")
            print(f"请求头: {headers}")
            print(f"请求体: {payload}")
            print(f"响应状态码: {response.status_code}")
            try:
                print(f"响应内容: {response.json()}")
            except:
                print(f"响应文本: {response.text[:500]}")
            print()
            raise handle_api_error(response)
            
    except requests.exceptions.Timeout:
        raise MCPError(
            message="请求超时",
            suggestion="图像生成可能需要更长时间，请稍后重试或减少生成步数"
        )
    except requests.exceptions.RequestException as e:
        raise MCPError(
            message=f"网络请求失败: {str(e)}",
            suggestion="请检查网络连接或稍后重试"
        )
    except MCPError:
        raise  # 重新抛出 MCPError
    except Exception as e:
        raise MCPError(
            message=f"处理请求时发生异常: {str(e)}",
            suggestion="请检查请求参数，如果问题持续存在，请联系技术支持"
        )


def make_img2img_request(
    api_key: str,
    model: str,
    prompt: str,
    image_url: str,
    strength: float = 0.8,
    width: int = 1024,
    height: int = 1024,
    steps: int = 30,
    guidance_scale: float = 7.5,
    negative_prompt: Optional[str] = None,
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    发起图生图 API 请求

    Args:
        api_key: API 密钥
        model: 模型标识符
        prompt: 图像生成提示词
        image_url: 参考图像 URL
        strength: 参考图像影响强度（0.0-1.0）
        width: 图像宽度
        height: 图像高度
        steps: 生成步数
        guidance_scale: 引导强度
        negative_prompt: 负面提示词
        seed: 随机种子

    Returns:
        API 响应数据

    Raises:
        MCPError: 当 API 请求失败时
    """
    if not api_key:
        raise APIKeyError()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 根据文档，图生图使用 image 参数（支持 URL 或 Base64）
    size_str = f"{width}x{height}"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "image": image_url,  # 使用 image 参数，支持 URL
        "size": size_str,
        "response_format": "url",
        "watermark": False
        # 注意：doubao-seedream-4.0 不支持 strength, steps, guidance_scale 参数
    }
    
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    
    if seed is not None:
        payload["seed"] = seed
    
    # 从环境变量读取超时时间，默认 60 秒
    timeout = int(os.getenv("REQUEST_TIMEOUT", "60"))
    
    # 动态获取端点 URL（支持环境变量配置）
    api_url = get_images_generations_url()
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=timeout
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            # 在错误时输出详细的调试信息
            print(f"\n🔍 调试信息 - 图生图 API 请求错误:")
            print(f"请求 URL: {api_url}")
            print(f"API 基础 URL: {get_api_base_url()}")
            print(f"模型: {model}")
            print(f"请求体: {payload}")
            print(f"响应状态码: {response.status_code}")
            try:
                print(f"响应内容: {response.json()}")
            except:
                print(f"响应文本: {response.text[:500]}")
            print()
            raise handle_api_error(response)
            
    except requests.exceptions.Timeout:
        raise MCPError(
            message="请求超时",
            suggestion="图像生成可能需要更长时间，请稍后重试或减少生成步数"
        )
    except requests.exceptions.RequestException as e:
        raise MCPError(
            message=f"网络请求失败: {str(e)}",
            suggestion="请检查网络连接或稍后重试"
        )
    except MCPError:
        raise
    except Exception as e:
        raise MCPError(
            message=f"处理请求时发生异常: {str(e)}",
            suggestion="请检查请求参数，如果问题持续存在，请联系技术支持"
        )


def make_fusion_request(
    api_key: str,
    model: str,
    prompt: str,
    image_urls: list,
    fusion_weights: Optional[list] = None,
    width: int = 1024,
    height: int = 1024,
    steps: int = 30,
    guidance_scale: float = 7.5,
    negative_prompt: Optional[str] = None,
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    发起多图融合 API 请求

    Args:
        api_key: API 密钥
        model: 模型标识符
        prompt: 图像生成提示词
        image_urls: 参考图像 URL 数组（至少2张）
        fusion_weights: 各图像的融合权重（可选）
        width: 图像宽度
        height: 图像高度
        steps: 生成步数
        guidance_scale: 引导强度
        negative_prompt: 负面提示词
        seed: 随机种子

    Returns:
        API 响应数据

    Raises:
        MCPError: 当 API 请求失败时
    """
    if not api_key:
        raise APIKeyError()
    
    if not image_urls or len(image_urls) < 2:
        raise MCPError(
            message="多图融合需要至少2张参考图像",
            suggestion="请提供至少2张图像的 URL"
        )
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 根据文档，多图融合使用 image 参数（数组形式）
    size_str = f"{width}x{height}"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "image": image_urls,  # 使用 image 参数，支持数组（1-10张）
        "size": size_str,
        "response_format": "url",
        "watermark": False
        # 注意：doubao-seedream-4.0 不支持 fusion_weights, steps, guidance_scale 参数
    }
    
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
    
    if seed is not None:
        payload["seed"] = seed
    
    # 从环境变量读取超时时间，默认 60 秒
    timeout = int(os.getenv("REQUEST_TIMEOUT", "60"))
    
    # 动态获取端点 URL（支持环境变量配置）
    api_url = get_images_generations_url()
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=timeout
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            # 在错误时输出详细的调试信息
            print(f"\n🔍 调试信息 - 多图融合 API 请求错误:")
            print(f"请求 URL: {api_url}")
            print(f"API 基础 URL: {get_api_base_url()}")
            print(f"模型: {model}")
            print(f"请求体: {payload}")
            print(f"响应状态码: {response.status_code}")
            try:
                print(f"响应内容: {response.json()}")
            except:
                print(f"响应文本: {response.text[:500]}")
            print()
            raise handle_api_error(response)
            
    except requests.exceptions.Timeout:
        raise MCPError(
            message="请求超时",
            suggestion="图像生成可能需要更长时间，请稍后重试或减少生成步数"
        )
    except requests.exceptions.RequestException as e:
        raise MCPError(
            message=f"网络请求失败: {str(e)}",
            suggestion="请检查网络连接或稍后重试"
        )
    except MCPError:
        raise
    except Exception as e:
        raise MCPError(
            message=f"处理请求时发生异常: {str(e)}",
            suggestion="请检查请求参数，如果问题持续存在，请联系技术支持"
        )

