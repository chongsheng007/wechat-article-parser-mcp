#!/usr/bin/env python3
"""测试不同的模型名称格式"""

import requests
import os
import json

API_KEY = os.getenv("SEEDREAM_API_KEY", "2b9a2920-1636-4549-bfb0-e1af92206aa2")
API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

# 尝试不同的模型名称格式
model_names = [
    "Seedream-4.0",
    "seedream-4.0",
    "seedream4.0",
    "Seedream4.0",
    "seedream_4.0",
    "seedream",
    "Seedream",
    "seedream-4",
    "Seedream-4",
    "seedream4",
    "ep-20241103171656-abc123",  # 可能的端点格式
]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

print("=" * 60)
print("测试不同的模型名称格式")
print("=" * 60)

for model in model_names:
    payload = {
        "model": model,
        "prompt": "一只可爱的小猫",
        "width": 512,
        "height": 512,
        "steps": 20,
        "guidance_scale": 7.5,
        "watermark": False
    }
    
    print(f"\n尝试模型名称: {model}")
    print(f"请求: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ 成功！模型名称: {model}")
            print(f"响应: {response.json()}")
            break
        else:
            try:
                error_data = response.json()
                error_code = error_data.get("error", {}).get("code", "")
                error_message = error_data.get("error", {}).get("message", "")
                logid = error_data.get("error", {}).get("logid", "")
                print(f"❌ 错误代码: {error_code}")
                print(f"   错误消息: {error_message}")
                print(f"   Log ID: {logid}")
            except:
                print(f"❌ 响应: {response.text[:200]}")
                
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
    
    print("-" * 60)

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)


