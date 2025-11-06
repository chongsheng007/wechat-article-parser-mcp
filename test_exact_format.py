#!/usr/bin/env python3
"""测试精确的参数格式 - 移除可能导致问题的参数"""

import requests
import os
import json

API_KEY = os.getenv("SEEDREAM_API_KEY", "2b9a2920-1636-4549-bfb0-e1af92206aa2")
API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("=" * 80)
print("测试精确参数格式（移除可能导致问题的参数）")
print("=" * 80)

# 测试 1: 最简参数（不包含 watermark）
test_cases = [
    {
        "name": "最简参数 - 只有 model 和 prompt",
        "payload": {
            "model": "Seedream-4.0",
            "prompt": "一只可爱的小猫"
        }
    },
    {
        "name": "添加 width 和 height",
        "payload": {
            "model": "Seedream-4.0",
            "prompt": "一只可爱的小猫",
            "width": 1024,
            "height": 1024
        }
    },
    {
        "name": "添加 steps",
        "payload": {
            "model": "Seedream-4.0",
            "prompt": "一只可爱的小猫",
            "width": 1024,
            "height": 1024,
            "steps": 30
        }
    },
    {
        "name": "添加 guidance_scale",
        "payload": {
            "model": "Seedream-4.0",
            "prompt": "一只可爱的小猫",
            "width": 1024,
            "height": 1024,
            "steps": 30,
            "guidance_scale": 7.5
        }
    },
    {
        "name": "使用 n 参数而不是 num_images",
        "payload": {
            "model": "Seedream-4.0",
            "prompt": "一只可爱的小猫",
            "width": 1024,
            "height": 1024,
            "n": 1
        }
    },
    {
        "name": "移除 watermark 参数",
        "payload": {
            "model": "Seedream-4.0",
            "prompt": "一只可爱的小猫",
            "width": 1024,
            "height": 1024,
            "steps": 30,
            "guidance_scale": 7.5
            # 注意：不包含 watermark
        }
    }
]

for i, test_case in enumerate(test_cases, 1):
    print(f"\n[{i}/{len(test_cases)}] {test_case['name']}")
    print(f"请求: {json.dumps(test_case['payload'], indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(API_URL, headers=headers, json=test_case['payload'], timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅✅✅ 成功！✅✅✅")
            print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            print(f"\n🎉 找到正确的参数格式！")
            print(f"使用以下参数格式:")
            print(json.dumps(test_case['payload'], indent=2, ensure_ascii=False))
            break
        else:
            try:
                error_data = response.json()
                error_code = error_data.get("error", {}).get("code", "")
                error_message = error_data.get("error", {}).get("message", "")[:100]
                print(f"❌ 错误代码: {error_code}")
                print(f"   错误消息: {error_message}")
            except:
                print(f"❌ 响应: {response.text[:200]}")
                
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("-" * 80)

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)


