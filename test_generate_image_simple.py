#!/usr/bin/env python
"""
简单测试 generate_image 工具
直接调用工具函数，不通过 MCP 协议
"""

import sys
import os
sys.path.insert(0, 'src')

from seedream_image_generator.tools.generate_image import GenerateImageInput, _generate_image_impl

# 设置环境变量
os.environ['SEEDREAM_API_KEY'] = '2b9a2920-1636-4549-bfb0-e1af92206aa2'
os.environ['API_BASE_URL'] = 'https://ark.cn-beijing.volces.com'
os.environ['REQUEST_TIMEOUT'] = '60'

print('🎨 测试 generate_image 工具')
print('=' * 60)

# 创建输入（包含 format 字段，测试是否会被忽略）
input_data = GenerateImageInput(
    prompt='一只可爱的小狗',
    size='2048x2048'
)

print(f'📝 提示词: {input_data.prompt}')
print(f'📐 尺寸: {input_data.size}')
print()

try:
    print('⏳ 正在生成图像，请稍候...')
    result = _generate_image_impl(input_data)
    print()
    print('=' * 60)
    print('✅ 生成成功！')
    print('=' * 60)
    print(result)
    print('=' * 60)
except Exception as e:
    print()
    print('=' * 60)
    print('❌ 生成失败')
    print('=' * 60)
    print(f'错误类型: {type(e).__name__}')
    print(f'错误信息: {str(e)}')
    print('=' * 60)


