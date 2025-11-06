"""测试即梦 API - 根据错误信息调整"""
import requests
import json

api_key = "2b9a2920-1636-4549-bfb0-e1af92206aa2"
prompt = "一只可爱的小猫"

# 根据错误信息，正确的端点应该是这个
api_url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 尝试不同的模型名称格式
model_variants = [
    "seedream-4.0",
    "seedream_v4.0", 
    "seedream4.0",
    "Seedream-4.0"
]

for model_name in model_variants:
    print(f"\n{'='*60}")
    print(f"尝试模型: {model_name}")
    print(f"{'='*60}")
    
    payload = {
        "model": model_name,
        "prompt": prompt,
        "width": 1024,
        "height": 1024,
        "steps": 30,
        "guidance_scale": 7.5,
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功！")
            print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            break
        else:
            error_data = response.json() if response.text else {}
            print(f"❌ 失败: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
