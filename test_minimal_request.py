#!/usr/bin/env python3
"""测试最小参数的请求"""

import requests
import os
import json

API_KEY = os.getenv("SEEDREAM_API_KEY", "2b9a2920-1636-4549-bfb0-e1af92206aa2")
API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 测试 1: 最小参数（只有 model 和 prompt）
print("=" * 60)
print("测试 1: 最小参数（只有 model 和 prompt）")
print("=" * 60)

payload = {
    "model": "Seedream-4.0",
    "prompt": "一只可爱的小猫"
}

print(f"请求: {json.dumps(payload, indent=2, ensure_ascii=False)}")

try:
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"异常: {str(e)}")

print("\n" + "=" * 60)
print("测试 2: 添加 watermark: false")
print("=" * 60)

payload = {
    "model": "Seedream-4.0",
    "prompt": "一只可爱的小猫",
    "watermark": False
}

print(f"请求: {json.dumps(payload, indent=2, ensure_ascii=False)}")

try:
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"异常: {str(e)}")

print("\n" + "=" * 60)
print("测试 3: 使用不同的模型名称（Seedream4.0）")
print("=" * 60)

payload = {
    "model": "Seedream4.0",
    "prompt": "一只可爱的小猫"
}

print(f"请求: {json.dumps(payload, indent=2, ensure_ascii=False)}")

try:
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    print(f"状态码: {response.status_code}")
    print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
except Exception as e:
    print(f"异常: {str(e)}")


