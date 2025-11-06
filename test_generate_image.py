#!/usr/bin/env python
"""
测试即梦图像生成功能
使用方法：
    export SEEDREAM_API_KEY="your-api-key"
    uv run python test_generate_image.py
"""

import sys
import os
sys.path.insert(0, 'src')

from seedream_image_generator.tools.generate_image import GenerateImageInput, _generate_image_impl

def test_generate_image():
    """测试生成图像"""
    print('🎨 使用即梦生成小猫图片...')
    print('=' * 50)
    
    # 检查环境变量
    api_key = os.getenv("SEEDREAM_API_KEY") or os.getenv("ARK_API_KEY")
    if not api_key:
        print('❌ 错误：未设置 SEEDREAM_API_KEY 环境变量')
        print('请运行：export SEEDREAM_API_KEY="your-api-key"')
        return
    
    print(f'✅ API Key: {api_key[:10]}...{api_key[-10:]}')
    print()
    
    # 创建输入
    input_data = GenerateImageInput(
        prompt='一只可爱的小猫',
        size='1024x1024'
    )
    
    print(f'📝 提示词: {input_data.prompt}')
    print(f'📐 尺寸: {input_data.size}')
    print()
    
    try:
        result = _generate_image_impl(input_data)
        print('✅ 生成成功！')
        print('=' * 50)
        print(result)
        print()
        print('🎉 可以复制上面的 URL 在浏览器中查看生成的图片！')
    except Exception as e:
        print('❌ 生成失败')
        print('=' * 50)
        print(str(e))
        print()
        if 'ModelNotOpen' in str(e):
            print('💡 提示：模型服务尚未激活，请：')
            print('   1. 登录 https://console.volcengine.com/ark/')
            print('   2. 激活模型：doubao-seedream-4-0-250828')
            print('   3. 等待 5-30 分钟后重试')

if __name__ == '__main__':
    test_generate_image()

