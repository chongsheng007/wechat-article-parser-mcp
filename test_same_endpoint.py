#!/usr/bin/env python3
"""测试图生图是否使用同一个端点"""

import requests
import os
import json

API_KEY = os.getenv("SEEDREAM_API_KEY", "2b9a2920-1636-4549-bfb0-e1af92206aa2")
API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

model = "Seedream-4.0"

print("=" * 60)
print("测试图生图是否使用同一个端点（通过参数区分）")
print("=" * 60)

# 测试不同的参数组合
test_cases = [
    {
        "name": "标准文生图",
        "payload": {
            "model": model,
            "prompt": "一只可爱的小猫"
        }
    },
    {
        "name": "图生图 - 使用 image_url",
        "payload": {
            "model": model,
            "prompt": "一只可爱的小猫",
            "image_url": "https://example.com/test.jpg"
        }
    },
    {
        "name": "图生图 - 使用 image",
        "payload": {
            "model": model,
            "prompt": "一只可爱的小猫",
            "image": "https://example.com/test.jpg"
        }
    },
    {
        "name": "图生图 - 使用 image_url + strength",
        "payload": {
            "model": model,
            "prompt": "一只可爱的小猫",
            "image_url": "https://example.com/test.jpg",
            "strength": 0.8
        }
    },
    {
        "name": "多图融合 - 使用 image_urls",
        "payload": {
            "model": model,
            "prompt": "融合两张图像",
            "image_urls": [
                "https://example.com/test1.jpg",
                "https://example.com/test2.jpg"
            ]
        }
    },
    {
        "name": "多图融合 - 使用 images",
        "payload": {
            "model": model,
            "prompt": "融合两张图像",
            "images": [
                "https://example.com/test1.jpg",
                "https://example.com/test2.jpg"
            ]
        }
    }
]

for test_case in test_cases:
    print(f"\n测试: {test_case['name']}")
    print(f"请求: {json.dumps(test_case['payload'], indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(API_URL, headers=headers, json=test_case['payload'], timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ 成功！")
            print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            try:
                error_data = response.json()
                error_code = error_data.get("error", {}).get("code", "")
                error_message = error_data.get("error", {}).get("message", "")
                print(f"❌ 错误代码: {error_code}")
                print(f"   错误消息: {error_message[:200]}")
            except:
                print(f"❌ 响应: {response.text[:200]}")
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("-" * 60)

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)


