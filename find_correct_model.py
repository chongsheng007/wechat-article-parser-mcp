"""尝试找到正确的模型名称格式"""
import requests
import json

api_key = "2b9a2920-1636-4549-bfb0-e1af92206aa2"
api_url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 基于 Seedream4.0 返回 500 而不是 404，尝试变体
model_variants = [
    "Seedream4.0",  # 已知返回 500
    "seedream4.0",
    "Seedream-4.0",
    "Seedream_4.0",
    "SEEDREAM-4.0",
    "seedream-4.0",
    "Seedream-4.0-dev",
]

payload_base = {
    "prompt": "一只可爱的小猫",
    "size": "2K",
    "response_format": "url"
}

for model in model_variants:
    payload = payload_base.copy()
    payload["model"] = model
    
    print(f"\n测试: {model}")
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 成功！")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print(f"\n🎉 找到正确的模型名称: {model}")
            break
        elif response.status_code == 500:
            print("⚠️  500 内部错误（可能格式接近但需要调整）")
            print(f"响应: {response.text[:200]}")
        elif response.status_code != 404:
            print(f"响应: {response.text[:200]}")
    except Exception as e:
        print(f"错误: {str(e)}")
