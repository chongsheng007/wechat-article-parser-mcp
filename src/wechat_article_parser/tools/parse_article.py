"""parse_article 工具实现"""

from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional
from ..utils.parser import parse_wechat_article
from ..utils.formatters import format_article_response
from ..utils.errors import MCPError


class ParseWeChatArticleInput(BaseModel):
    """解析微信公众号文章工具输入模型"""
    model_config = {"extra": "ignore"}
    
    url: str = Field(
        description="微信公众号文章 URL（必填）",
        examples=[
            "https://mp.weixin.qq.com/s?__biz=MzA5NzM5Mjg2MQ==&mid=2652201234&idx=1&sn=abc123",
            "https://mp.weixin.qq.com/s/abc123def456"
        ]
    )
    
    format: Optional[str] = Field(
        default="markdown",
        description="输出格式，可选值: markdown, text, html",
        examples=["markdown", "text", "html"]
    )
    
    include_images: bool = Field(
        default=True,
        description="是否包含图片信息",
    )
    
    include_links: bool = Field(
        default=True,
        description="是否包含链接信息",
    )


def _parse_article_impl(input: ParseWeChatArticleInput) -> str:
    """解析文章的核心实现"""
    try:
        # 解析文章
        data = parse_wechat_article(input.url)
        
        # 格式化响应
        return format_article_response(
            data,
            format_type=input.format or "markdown",
            include_images=input.include_images,
            include_links=input.include_links
        )
        
    except MCPError:
        raise  # 重新抛出 MCPError
    except Exception as e:
        raise MCPError(
            message=f"解析文章时发生异常: {str(e)}",
            suggestion="请检查 URL 是否有效，或稍后重试"
        )


def register_parse_article_tool(mcp: FastMCP):
    """注册 parse_article 工具"""
    
    @mcp.tool(
        annotations={
            "readOnlyHint": True,  # 只读操作
            "destructiveHint": False,
            "idempotentHint": True,  # 相同 URL 产生相同结果
            "openWorldHint": False  # 只能解析微信公众号文章
        }
    )
    def parse_wechat_article_tool(input: ParseWeChatArticleInput) -> str:
        """
        解析微信公众号文章，提取完整内容
        
        这是一个完整的文章解析工具，可以：
        - 提取文章标题、作者、发布时间等元数据
        - 提取正文内容并转换为 Markdown/Text/HTML 格式
        - 提取文章中的所有图片
        - 提取文章中的所有链接
        
        Args:
            url: 微信公众号文章 URL（必填）
            format: 输出格式，可选值: markdown（默认）, text, html
            include_images: 是否包含图片信息（默认 true）
            include_links: 是否包含链接信息（默认 true）
        
        Returns:
            格式化后的文章内容
        
        Examples:
            parse_wechat_article_tool(url="https://mp.weixin.qq.com/s/...")
            parse_wechat_article_tool(url="https://mp.weixin.qq.com/s/...", format="text")
        
        Error Handling:
            - URL 无效: 提供 URL 格式说明
            - 文章不存在: 提示检查 URL 或文章是否已删除
            - 访问被拒绝: 建议在浏览器中打开链接
            - 解析失败: 提供部分解析的内容（如果有）
        """
        return _parse_article_impl(input)

