"""测试即梦 API - 尝试多种格式"""
import requests
import json

api_key = "2b9a2920-1636-4549-bfb0-e1af92206aa2"
prompt = "一只可爱的小猫"
api_url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 测试不同的参数组合
test_configs = [
    {
        "name": "配置1: 使用 bytedance-seedream-4-0-250828",
        "payload": {
            "model": "bytedance-seedream-4-0-250828",
            "prompt": prompt,
            "size": "2K",
            "response_format": "url"
        }
    },
    {
        "name": "配置2: 使用 width/height",
        "payload": {
            "model": "bytedance-seedream-4-0-250828",
            "prompt": prompt,
            "width": 1024,
            "height": 1024,
            "response_format": "url"
        }
    },
    {
        "name": "配置3: 添加 steps 和 guidance_scale",
        "payload": {
            "model": "bytedance-seedream-4-0-250828",
            "prompt": prompt,
            "width": 1024,
            "height": 1024,
            "steps": 30,
            "guidance_scale": 7.5,
            "response_format": "url"
        }
    },
    {
        "name": "配置4: 简化模型名称 seedream-4.0",
        "payload": {
            "model": "seedream-4.0",
            "prompt": prompt,
            "size": "2K",
            "response_format": "url"
        }
    }
]

for i, config in enumerate(test_configs, 1):
    print(f"\n{'='*70}")
    print(f"{i}. {config['name']}")
    print(f"{'='*70}")
    print(f"请求参数: {json.dumps(config['payload'], indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(api_url, headers=headers, json=config['payload'], timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功！")
            print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # 尝试提取图片 URL
            if "data" in result:
                if isinstance(result["data"], list) and len(result["data"]) > 0:
                    first_item = result["data"][0]
                    if "url" in first_item:
                        print(f"\n🖼️  图片 URL: {first_item['url']}")
                    elif "image_url" in first_item:
                        print(f"\n🖼️  图片 URL: {first_item['image_url']}")
            elif "url" in result:
                print(f"\n🖼️  图片 URL: {result['url']}")
            elif "image_url" in result:
                print(f"\n🖼️  图片 URL: {result['image_url']}")
            
            break  # 找到成功的配置就停止
        else:
            error_data = response.json() if response.text else {}
            print(f"❌ 失败")
            print(f"错误: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
