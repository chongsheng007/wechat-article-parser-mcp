#!/usr/bin/env python
"""
测试所有即梦图像生成工具
使用方法：
    export SEEDREAM_API_KEY="your-api-key"
    uv run python test_all_tools.py
"""

import sys
import os
sys.path.insert(0, 'src')

from seedream_image_generator.tools.generate_image import GenerateImageInput, _generate_image_impl
from seedream_image_generator.tools.generate_image_group import GenerateImageGroupInput, _generate_image_group_impl
from seedream_image_generator.tools.generate_image_from_image import GenerateImageFromImageInput, _generate_image_from_image_impl
from seedream_image_generator.tools.generate_image_fusion import GenerateImageFusionInput, _generate_image_fusion_impl

def test_generate_image():
    """测试文生图"""
    print('\n' + '='*60)
    print('📝 测试 1: generate_image (文生图)')
    print('='*60)
    
    input_data = GenerateImageInput(
        prompt='一只可爱的小狗',
        size='1024x1024'
    )
    
    try:
        result = _generate_image_impl(input_data)
        print('✅ 成功')
        print(result)
        return True
    except Exception as e:
        print(f'❌ 失败: {str(e)}')
        return False

def test_generate_image_group():
    """测试生成组图"""
    print('\n' + '='*60)
    print('📝 测试 2: generate_image_group (生成组图)')
    print('='*60)
    
    input_data = GenerateImageGroupInput(
        prompt='美丽的日落',
        num_images=2,
        size='1024x1024'
    )
    
    try:
        result = _generate_image_group_impl(input_data)
        print('✅ 成功')
        print(result)
        return True
    except Exception as e:
        print(f'❌ 失败: {str(e)}')
        return False

def test_generate_image_from_image():
    """测试图生图（需要提供图片 URL）"""
    print('\n' + '='*60)
    print('📝 测试 3: generate_image_from_image (图生图)')
    print('='*60)
    print('⚠️  需要提供图片 URL，跳过此测试')
    print('如需测试，请提供 image_url 参数')
    return None

def test_generate_image_fusion():
    """测试多图融合（需要提供图片 URL）"""
    print('\n' + '='*60)
    print('📝 测试 4: generate_image_fusion (多图融合)')
    print('='*60)
    print('⚠️  需要提供图片 URL，跳过此测试')
    print('如需测试，请提供 image_urls 参数')
    return None

def main():
    """主测试函数"""
    print('🧪 即梦图像生成工具 - 完整测试')
    print('='*60)
    
    # 检查环境变量
    api_key = os.getenv("SEEDREAM_API_KEY") or os.getenv("ARK_API_KEY")
    if not api_key:
        print('❌ 错误：未设置 SEEDREAM_API_KEY 环境变量')
        print('请运行：export SEEDREAM_API_KEY="your-api-key"')
        return
    
    print(f'✅ API Key: {api_key[:10]}...{api_key[-10:]}')
    
    # 运行测试
    results = []
    
    # 测试 1: 文生图
    results.append(('文生图', test_generate_image()))
    
    # 测试 2: 生成组图
    results.append(('生成组图', test_generate_image_group()))
    
    # 测试 3: 图生图（跳过）
    results.append(('图生图', test_generate_image_from_image()))
    
    # 测试 4: 多图融合（跳过）
    results.append(('多图融合', test_generate_image_fusion()))
    
    # 汇总结果
    print('\n' + '='*60)
    print('📊 测试结果汇总')
    print('='*60)
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    for name, result in results:
        if result is True:
            print(f'✅ {name}: 成功')
            success_count += 1
        elif result is False:
            print(f'❌ {name}: 失败')
            fail_count += 1
        else:
            print(f'⏭️  {name}: 跳过')
            skip_count += 1
    
    print('='*60)
    print(f'总计: 成功 {success_count}, 失败 {fail_count}, 跳过 {skip_count}')
    print('='*60)
    
    if fail_count > 0:
        print('\n💡 提示：如果遇到 ModelNotOpen 错误，请：')
        print('   1. 登录 https://console.volcengine.com/ark/')
        print('   2. 激活模型：doubao-seedream-4-0-250828')
        print('   3. 等待 5-30 分钟后重试')

if __name__ == '__main__':
    main()



