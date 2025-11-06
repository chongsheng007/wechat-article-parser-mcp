#!/usr/bin/env python3
"""测试图生图的不同 API 端点"""

import requests
import os
import json

API_KEY = os.getenv("SEEDREAM_API_KEY", "2b9a2920-1636-4549-bfb0-e1af92206aa2")

# 尝试不同的图生图端点
endpoints = [
    "https://ark.cn-beijing.volces.com/api/v3/images/img2img",
    "https://ark.cn-beijing.volces.com/api/v3/images/image-to-image",
    "https://ark.cn-beijing.volces.com/api/v3/images/img_to_img",
    "https://ark.cn-beijing.volces.com/api/v3/images/generations",  # 可能使用同一个端点
]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

model = "Seedream-4.0"

print("=" * 60)
print("测试图生图的不同 API 端点")
print("=" * 60)

# 测试每个端点
for endpoint in endpoints:
    print(f"\n尝试端点: {endpoint}")
    
    # 尝试不同的参数格式
    test_payloads = [
        {
            "model": model,
            "prompt": "一只可爱的小猫",
            "image_url": "https://example.com/test.jpg"
        },
        {
            "model": model,
            "prompt": "一只可爱的小猫",
            "image": "https://example.com/test.jpg"
        },
        {
            "model": model,
            "prompt": "一只可爱的小猫",
            "input_image": "https://example.com/test.jpg"
        },
        {
            "model": model,
            "prompt": "一只可爱的小猫",
            "image_url": "https://example.com/test.jpg",
            "strength": 0.8
        }
    ]
    
    for i, payload in enumerate(test_payloads, 1):
        print(f"\n  测试 {i}: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ 成功！端点: {endpoint}")
                print(f"  响应: {response.json()}")
                break
            elif response.status_code == 404:
                try:
                    error_data = response.json()
                    error_code = error_data.get("error", {}).get("code", "")
                    print(f"  ❌ 404 - 错误代码: {error_code}")
                except:
                    print(f"  ❌ 404 - 响应: {response.text[:200]}")
            else:
                try:
                    error_data = response.json()
                    error_code = error_data.get("error", {}).get("code", "")
                    print(f"  ❌ {response.status_code} - 错误代码: {error_code}")
                except:
                    print(f"  ❌ {response.status_code} - 响应: {response.text[:200]}")
                    
        except Exception as e:
            print(f"  ❌ 异常: {str(e)}")
    
    print("-" * 60)

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)


