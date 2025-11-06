#!/usr/bin/env python3
"""
Seedream 4.0 图像生成 MCP Server - 入口文件

用于在项目根目录直接运行服务器
"""

import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from seedream_image_generator.server import mcp

if __name__ == "__main__":
    # 检查环境变量（优先使用 SEEDREAM_API_KEY，也支持 ARK_API_KEY）
    api_key = os.getenv("SEEDREAM_API_KEY") or os.getenv("ARK_API_KEY")
    if not api_key:
        print("=" * 60)
        print("⚠️  警告: 未设置 API 密钥环境变量")
        print("   请设置以下环境变量:")
        print("   export SEEDREAM_API_KEY='your-api-key-here'")
        print("   （也支持 ARK_API_KEY 作为备选）")
        print("=" * 60)
        print()
    
    # 运行 MCP 服务器
    mcp.run()


