"""extract_metadata 工具实现"""

from fastmcp import FastMCP
from pydantic import BaseModel, Field
from ..utils.parser import parse_wechat_article
from ..utils.formatters import format_metadata_response
from ..utils.errors import MCPError


class ExtractArticleMetadataInput(BaseModel):
    """提取文章元数据工具输入模型"""
    model_config = {"extra": "ignore"}
    
    url: str = Field(
        description="微信公众号文章 URL（必填）",
        examples=[
            "https://mp.weixin.qq.com/s?__biz=MzA5NzM5Mjg2MQ==&mid=2652201234&idx=1&sn=abc123",
            "https://mp.weixin.qq.com/s/abc123def456"
        ]
    )


def _extract_metadata_impl(input: ExtractArticleMetadataInput) -> str:
    """提取元数据的核心实现"""
    try:
        # 解析文章（只获取元数据部分）
        data = parse_wechat_article(input.url)
        
        # 格式化元数据响应
        metadata = {
            'title': data.get('title'),
            'author': data.get('author'),
            'publish_time': data.get('publish_time'),
            'cover_image': data.get('cover_image'),
            'url': data.get('url'),
        }
        
        return format_metadata_response(metadata)
        
    except MCPError:
        raise  # 重新抛出 MCPError
    except Exception as e:
        raise MCPError(
            message=f"提取元数据时发生异常: {str(e)}",
            suggestion="请检查 URL 是否有效，或稍后重试"
        )


def register_extract_metadata_tool(mcp: FastMCP):
    """注册 extract_metadata 工具"""
    
    @mcp.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    def extract_article_metadata(url: str) -> str:
        """
        快速提取微信公众号文章的元数据（不解析全文）
        
        用于快速预览文章信息，包括：
        - 标题
        - 作者
        - 发布时间
        - 封面图
        
        Args:
            url: 微信公众号文章 URL（必填）
        
        Returns:
            格式化后的元数据信息
        
        Examples:
            extract_article_metadata(url="https://mp.weixin.qq.com/s/...")
        
        Error Handling:
            - URL 无效: 提供 URL 格式说明
            - 文章不存在: 提示检查 URL
            - 访问被拒绝: 建议在浏览器中打开链接
        """
        # 创建输入模型
        input_data = ExtractArticleMetadataInput(url=url)
        return _extract_metadata_impl(input_data)

