"""尝试列出可用的模型"""
import requests
import json

api_key = "2b9a2920-1636-4549-bfb0-e1af92206aa2"

# 尝试不同的端点来列出模型
endpoints_to_try = [
    "https://ark.cn-beijing.volces.com/api/v1/models",
    "https://ark.cn-beijing.volces.com/api/v3/models",
    "https://ark.cn-beijing.volces.com/v1/models",
]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

for endpoint in endpoints_to_try:
    print(f"\n尝试端点: {endpoint}")
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功！可用模型:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            break
        else:
            print(f"响应: {response.text[:200]}")
    except Exception as e:
        print(f"错误: {str(e)}")
