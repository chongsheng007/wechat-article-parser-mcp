"""
微信公众号文章解析 MCP Server

提供解析微信公众号文章的工具，提取文章内容、元数据、图片等信息
"""

from fastmcp import FastMCP
import os
from .tools.parse_article import register_parse_article_tool
from .tools.extract_metadata import register_extract_metadata_tool
from .tools.extract_images import register_extract_images_tool

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

