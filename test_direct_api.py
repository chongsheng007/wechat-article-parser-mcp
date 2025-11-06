"""直接测试 - 不指定模型，让 API 返回可用模型列表"""
import requests
import json

api_key = "2b9a2920-1636-4549-bfb0-e1af92206aa2"
api_url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 尝试不指定模型，或者尝试常见的模型名称
test_models = [
    None,  # 不指定模型
    "seedream",
    "seedream4",
    "seedream_v4",
    "Seedream4.0",
    "seedream-4.0-dev",
    "seedream_lite",
]

for model in test_models:
    payload = {
        "prompt": "一只可爱的小猫",
        "size": "2K"
    }
    
    if model:
        payload["model"] = model
    
    print(f"\n测试模型: {model or '(不指定)'}")
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 成功！")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            break
        elif response.status_code != 404:
            # 非 404 错误可能包含有用信息
            print(f"响应: {response.text[:300]}")
    except Exception as e:
        print(f"错误: {str(e)}")
