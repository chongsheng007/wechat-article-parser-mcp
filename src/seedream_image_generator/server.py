"""
Seedream 4.0 图像生成 MCP Server

使用即梦 Seedream 4.0 模型 API 生成高质量图像
参考文档: https://www.volcengine.com/docs/82379/1541523
"""

from fastmcp import FastMCP
import os
from .tools.generate_image import register_generate_image_tool
from .tools.generate_image_group import register_generate_image_group_tool
from .tools.generate_image_from_image import register_generate_image_from_image_tool
from .tools.generate_image_fusion import register_generate_image_fusion_tool

# 创建 FastMCP 实例
mcp = FastMCP(
    name="Seedream 4.0 Image Generator",
    instructions="A MCP server for generating images using Seedream 4.0 model API. Supports text-to-image, batch generation, image-to-image, and image fusion."
)

# 注册所有工具
register_generate_image_tool(mcp)  # 文生图
register_generate_image_group_tool(mcp)  # 生成组图
register_generate_image_from_image_tool(mcp)  # 图生图
register_generate_image_fusion_tool(mcp)  # 多图融合

if __name__ == "__main__":
    # 检查环境变量（优先使用 SEEDREAM_API_KEY，也支持 ARK_API_KEY）
    api_key = os.getenv("SEEDREAM_API_KEY") or os.getenv("ARK_API_KEY")
    if not api_key:
        print("⚠️  警告: 未设置 API 密钥环境变量")
        print("   请设置以下环境变量:")
        print("   export SEEDREAM_API_KEY='your-api-key-here'")
        print("   （也支持 ARK_API_KEY 作为备选）")
        print()
    
    # 运行 MCP 服务器（使用 stdio 传输）
    mcp.run()

