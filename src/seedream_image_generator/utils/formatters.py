"""响应格式化工具"""

import json
from typing import Any, Dict, List


def format_success_response(result: Dict[str, Any], is_batch: bool = False) -> str:
    """
    格式化成功响应
    
    根据实际 API 响应格式：
    {
        "model": "doubao-seedream-4-0-250828",
        "created": 1757321139,
        "data": [
            {
                "url": "https://...",
                "size": "3104x1312"
            }
        ],
        "usage": {
            "generated_images": 1,
            "output_tokens": xxx,
            "total_tokens": xxx
        }
    }

    Args:
        result: API 响应数据
        is_batch: 是否为批量生成（多个图像）

    Returns:
        格式化后的字符串（图像 URL 或多个 URL）
    """
    # 根据实际 API 响应格式处理
    if "data" in result:
        data = result["data"]
        if isinstance(data, list) and len(data) > 0:
            urls = []
            sizes = []
            for item in data:
                if "url" in item:
                    urls.append(item["url"])
                    if "size" in item:
                        sizes.append(item["size"])
                elif "image_url" in item:
                    urls.append(item["image_url"])
                    if "size" in item:
                        sizes.append(item["size"])
            
            if urls:
                if len(urls) == 1:
                    size_info = f" (尺寸: {sizes[0]})" if sizes else ""
                    return f"✅ 图像生成成功！\n🖼️  图像 URL: {urls[0]}{size_info}"
                else:
                    result_text = f"✅ 成功生成 {len(urls)} 张图像！\n\n"
                    for i, url in enumerate(urls, 1):
                        size_info = f" (尺寸: {sizes[i-1]})" if i-1 < len(sizes) else ""
                        result_text += f"🖼️  图像 {i}: {url}{size_info}\n"
                    return result_text
        
        elif isinstance(data, dict):
            if "url" in data:
                size_info = f" (尺寸: {data.get('size', 'unknown')})" if "size" in data else ""
                return f"✅ 图像生成成功！\n🖼️  图像 URL: {data['url']}{size_info}"
            elif "image_url" in data:
                return f"✅ 图像生成成功！\n🖼️  图像 URL: {data['image_url']}"
    
    # 如果都不匹配，返回完整响应用于调试
    return f"⚠️  图像生成成功，但响应格式未识别：\n{json.dumps(result, indent=2, ensure_ascii=False)}\n\n请检查 API 响应格式，可能需要调整代码。"


def format_batch_response(result: Dict[str, Any]) -> str:
    """
    格式化批量生成响应

    Args:
        result: API 响应数据

    Returns:
        格式化后的字符串（多个图像 URL）
    """
    return format_success_response(result, is_batch=True)

