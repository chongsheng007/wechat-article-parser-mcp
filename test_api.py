#!/usr/bin/env python3
"""直接测试 Seedream API"""

import requests
import os
import json
import sys

# 从环境变量读取配置
api_key = os.getenv('SEEDREAM_API_KEY', '2b9a2920-1636-4549-bfb0-e1af92206aa2')
api_url = 'https://ark.cn-beijing.volces.com/api/v3/images/generations'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# 测试参数
payload = {
    'model': 'doubao-seedream-4-0-250828',
    'prompt': '一只可爱的小猫',
    'size': '1024x1024',
    'response_format': 'url',
    'watermark': False,
    'sequential_image_generation': 'disabled',
    'stream': False
}

print('🧪 测试 Seedream API...')
print('=' * 60)
print(f'API URL: {api_url}')
print(f'模型: doubao-seedream-4-0-250828')
print(f'提示词: {payload["prompt"]}')
print('=' * 60)
print()

try:
    response = requests.post(api_url, headers=headers, json=payload, timeout=60)
    print(f'状态码: {response.status_code}')
    print()
    
    if response.status_code == 200:
        result = response.json()
        print('✅ ✅ ✅ 成功！模型已激活！')
        print()
        print('📊 响应数据:')
        if 'data' in result and len(result['data']) > 0:
            image_url = result['data'][0].get('url', 'N/A')
            image_size = result['data'][0].get('size', 'N/A')
            print(f'✅ 图像 URL: {image_url}')
            print(f'✅ 图像大小: {image_size}')
        print()
        print('完整响应:')
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print()
        print('🎉 可以在 MCP Inspector 中测试了！')
    else:
        error_data = response.json()
        error_code = error_data.get('error', {}).get('code', 'Unknown')
        error_message = error_data.get('error', {}).get('message', 'Unknown error')
        request_id = error_data.get('error', {}).get('request_id', 'N/A')
        
        print(f'❌ 错误代码: {error_code}')
        print(f'❌ 错误消息: {error_message}')
        print(f'🔍 Request ID: {request_id}')
        print()
        
        if 'ModelNotOpen' in error_code or 'not activated' in error_message:
            print('💡 模型尚未激活，请：')
            print('   1. 登录 Ark Console: https://console.volcengine.com/ark/')
            print('   2. 激活模型服务: doubao-seedream-4-0-250828')
            print('   3. 等待几分钟后再次测试')
        elif '401' in str(response.status_code) or 'Unauthorized' in error_message:
            print('💡 API Key 可能无效或权限不足')
            print('   请检查 SEEDREAM_API_KEY 是否正确')
            
except requests.exceptions.Timeout:
    print('❌ 请求超时（60秒）')
    print('💡 可以增加 REQUEST_TIMEOUT 环境变量')
except Exception as e:
    print(f'❌ 请求异常: {str(e)}')
    import traceback
    traceback.print_exc()

print('=' * 60)


