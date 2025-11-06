"""测试最小参数集"""
import requests
import json

api_key = "2b9a2920-1636-4549-bfb0-e1af92206aa2"
api_url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 测试最小参数集
minimal_configs = [
    {
        "name": "最小参数 - 只有 prompt 和 model",
        "payload": {
            "model": "Seedream-4.0",
            "prompt": "一只可爱的小猫"
        }
    },
    {
        "name": "添加 size",
        "payload": {
            "model": "Seedream-4.0",
            "prompt": "一只可爱的小猫",
            "size": "1024x1024"
        }
    },
    {
        "name": "使用 width 和 height",
        "payload": {
            "model": "Seedream-4.0",
            "prompt": "一只可爱的小猫",
            "width": 1024,
            "height": 1024
        }
    },
    {
        "name": "使用 size 字符串 2K",
        "payload": {
            "model": "Seedream-4.0",
            "prompt": "一只可爱的小猫",
            "size": "2K"
        }
    },
    {
        "name": "添加 response_format",
        "payload": {
            "model": "Seedream-4.0",
            "prompt": "一只可爱的小猫",
            "size": "2K",
            "response_format": "url"
        }
    }
]

for config in minimal_configs:
    print(f"\n{'='*70}")
    print(f"测试: {config['name']}")
    print(f"{'='*70}")
    print(f"参数: {json.dumps(config['payload'], indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(api_url, headers=headers, json=config['payload'], timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 成功！")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 提取图片 URL
            if "data" in result:
                if isinstance(result["data"], list) and len(result["data"]) > 0:
                    item = result["data"][0]
                    print(f"\n🖼️  图片 URL: {item.get('url') or item.get('image_url')}")
            elif "url" in result:
                print(f"\n🖼️  图片 URL: {result['url']}")
            elif "image_url" in result:
                print(f"\n🖼️  图片 URL: {result['image_url']}")
            
            print(f"\n🎉 找到正确的参数组合！")
            break
        else:
            error_data = response.json() if response.text else {}
            error_msg = error_data.get("error", {}).get("message", response.text[:200])
            print(f"❌ 失败: {error_msg}")
            
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
