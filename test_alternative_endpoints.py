#!/usr/bin/env python3
"""测试其他可能的 API 端点或区域"""

import requests
import os
import json

API_KEY = os.getenv("SEEDREAM_API_KEY", "2b9a2920-1636-4549-bfb0-e1af92206aa2")

# 尝试不同的端点和区域
endpoints = [
    "https://ark.cn-beijing.volces.com/api/v3/images/generations",
    "https://ark.volces.com/api/v3/images/generations",
    "https://api.volcengine.com/ark/v1/images/generations",
    "https://open.volcengine.com/api/v3/images/generations",
    "https://ark.cn-beijing.volces.com/api/v1/images/generations",
]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "Seedream-4.0",
    "prompt": "一只可爱的小猫"
}

print("=" * 80)
print("测试不同的 API 端点")
print("=" * 80)

for endpoint in endpoints:
    print(f"\n尝试端点: {endpoint}")
    print(f"请求: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅✅✅ 成功！端点: {endpoint} ✅✅✅")
            print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            break
        else:
            try:
                error_data = response.json()
                error_code = error_data.get("error", {}).get("code", "")
                print(f"❌ 错误代码: {error_code}")
            except:
                print(f"❌ 响应: {response.text[:200]}")
    except Exception as e:
        print(f"❌ 异常: {str(e)}")

print("\n" + "=" * 80)


