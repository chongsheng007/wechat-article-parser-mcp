#!/usr/bin/env python3
"""全面调试 API - 尝试所有可能的参数组合和格式"""

import requests
import os
import json

API_KEY = os.getenv("SEEDREAM_API_KEY", "2b9a2920-1636-4549-bfb0-e1af92206aa2")
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("=" * 80)
print("全面调试 Seedream 4.0 API")
print("=" * 80)

# 测试不同的模型名称格式
models = ["Seedream-4.0", "Seedream4.0", "seedream-4.0", "seedream4.0"]

# 测试不同的参数组合
test_cases = []

# 1. 最简参数（只有 model 和 prompt）
for model in models:
    test_cases.append({
        "name": f"最简参数 - {model}",
        "model": model,
        "payload": {
            "model": model,
            "prompt": "一只可爱的小猫"
        }
    })

# 2. 添加 watermark 参数
for model in models:
    test_cases.append({
        "name": f"添加 watermark:false - {model}",
        "model": model,
        "payload": {
            "model": model,
            "prompt": "一只可爱的小猫",
            "watermark": False
        }
    })

# 3. 完整的参数（但简化尺寸）
for model in models:
    test_cases.append({
        "name": f"完整参数(512x512) - {model}",
        "model": model,
        "payload": {
            "model": model,
            "prompt": "一只可爱的小猫",
            "width": 512,
            "height": 512,
            "steps": 20,
            "guidance_scale": 7.5,
            "watermark": False
        }
    })

# 4. 尝试不同的参数名称
test_cases.append({
    "name": "尝试 size 参数",
    "model": "Seedream-4.0",
    "payload": {
        "model": "Seedream-4.0",
        "prompt": "一只可爱的小猫",
        "size": "1K"
    }
})

test_cases.append({
    "name": "尝试 n 参数（批量）",
    "model": "Seedream-4.0",
    "payload": {
        "model": "Seedream-4.0",
        "prompt": "一只可爱的小猫",
        "n": 1
    }
})

# 5. 图生图参数（使用同一端点）
test_cases.append({
    "name": "图生图 - image_url",
    "model": "Seedream-4.0",
    "payload": {
        "model": "Seedream-4.0",
        "prompt": "一只可爱的小猫",
        "image_url": "https://example.com/test.jpg",
        "strength": 0.8
    }
})

test_cases.append({
    "name": "图生图 - image",
    "model": "Seedream-4.0",
    "payload": {
        "model": "Seedream-4.0",
        "prompt": "一只可爱的小猫",
        "image": "https://example.com/test.jpg"
    }
})

# 6. 多图融合参数
test_cases.append({
    "name": "多图融合 - image_urls",
    "model": "Seedream-4.0",
    "payload": {
        "model": "Seedream-4.0",
        "prompt": "融合两张图像",
        "image_urls": ["https://example.com/test1.jpg", "https://example.com/test2.jpg"]
    }
})

# 运行测试
success_cases = []
for i, test_case in enumerate(test_cases, 1):
    print(f"\n[{i}/{len(test_cases)}] {test_case['name']}")
    print(f"请求: {json.dumps(test_case['payload'], indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(BASE_URL, headers=headers, json=test_case['payload'], timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅✅✅ 成功！✅✅✅")
            print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            success_cases.append({
                "name": test_case['name'],
                "payload": test_case['payload'],
                "response": result
            })
            break  # 找到成功的配置就停止
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
    
    if i % 5 == 0:
        print(f"\n已测试 {i}/{len(test_cases)} 个用例...")

print("\n" + "=" * 80)
print("测试总结")
print("=" * 80)

if success_cases:
    print(f"\n✅ 找到 {len(success_cases)} 个成功的配置：")
    for case in success_cases:
        print(f"\n成功配置: {case['name']}")
        print(f"参数: {json.dumps(case['payload'], indent=2, ensure_ascii=False)}")
else:
    print("\n❌ 所有测试用例都失败了")
    print("\n可能的问题：")
    print("1. API Key 权限不足或服务未开通")
    print("2. 模型名称格式不正确")
    print("3. API 端点不正确")
    print("4. 需要联系火山引擎技术支持")

print("=" * 80)


