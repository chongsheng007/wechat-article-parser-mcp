"""
微信公众号文章解析 MCP Server - 入口文件

用于 fastmcp dev 启动，避免相对导入问题
"""

import sys
from pathlib import Path

# 添加项目路径到 sys.path
# 确保可以导入 wechat_article_parser 包
project_root = Path(__file__).parent
src_root = project_root.parent  # src 目录
sys.path.insert(0, str(src_root))  # 添加 src 目录，这样可以从 wechat_article_parser 导入

# 现在使用绝对导入
from fastmcp import FastMCP
from wechat_article_parser.tools.parse_article import register_parse_article_tool
from wechat_article_parser.tools.extract_metadata import register_extract_metadata_tool
from wechat_article_parser.tools.extract_images import register_extract_images_tool

# 创建 FastMCP 实例
mcp = FastMCP(
    name="WeChat Article Parser",
    instructions="A MCP server for parsing WeChat public account articles. Supports extracting article content, metadata, images, and links."
)

# 注册所有工具
register_parse_article_tool(mcp)  # 解析文章
register_extract_metadata_tool(mcp)  # 提取元数据
register_extract_images_tool(mcp)  # 提取图片

if __name__ == "__main__":
    # 运行 MCP 服务器（使用 stdio 传输）
    mcp.run()

