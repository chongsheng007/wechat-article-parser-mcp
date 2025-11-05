"""extract_images 工具实现"""

from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional
from ..utils.parser import parse_wechat_article
from ..utils.formatters import format_images_response
from ..utils.errors import MCPError


class ExtractArticleImagesInput(BaseModel):
    """提取文章图片工具输入模型"""
    model_config = {"extra": "ignore"}
    
    url: str = Field(
        description="微信公众号文章 URL（必填）",
        examples=[
            "https://mp.weixin.qq.com/s?__biz=MzA5NzM5Mjg2MQ==&mid=2652201234&idx=1&sn=abc123",
            "https://mp.weixin.qq.com/s/abc123def456"
        ]
    )
    
    include_cover: bool = Field(
        default=True,
        description="是否包含封面图",
    )
    
    image_format: Optional[str] = Field(
        default=None,
        description="图片格式过滤（可选: jpg, png, gif）",
    )


def _extract_images_impl(input: ExtractArticleImagesInput) -> str:
    """提取图片的核心实现"""
    try:
        # 解析文章
        data = parse_wechat_article(input.url)
        
        # 获取图片列表
        images = data.get('images', [])
        cover_image = data.get('cover_image')
        
        # 处理封面图
        if input.include_cover and cover_image:
            # 检查封面图是否已在图片列表中
            cover_exists = any(img['url'] == cover_image for img in images)
            if not cover_exists:
                images.insert(0, {
                    'url': cover_image,
                    'alt': '封面图',
                    'index': -1,
                    'is_cover': True
                })
        
        # 格式过滤
        if input.image_format:
            filtered_images = []
            for img in images:
                img_url = img.get('url', '').lower()
                if f'.{input.image_format.lower()}' in img_url:
                    filtered_images.append(img)
            images = filtered_images
        
        # 格式化响应
        return format_images_response(images, include_cover=input.include_cover)
        
    except MCPError:
        raise  # 重新抛出 MCPError
    except Exception as e:
        raise MCPError(
            message=f"提取图片时发生异常: {str(e)}",
            suggestion="请检查 URL 是否有效，或稍后重试"
        )


def register_extract_images_tool(mcp: FastMCP):
    """注册 extract_images 工具"""
    
    @mcp.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False
        }
    )
    def extract_article_images(
        url: str,
        include_cover: bool = True,
        image_format: str = None
    ) -> str:
        """
        提取微信公众号文章中的所有图片
        
        提取文章中的所有图片，包括：
        - 封面图（可选）
        - 正文中的图片
        
        Args:
            url: 微信公众号文章 URL（必填）
            include_cover: 是否包含封面图（默认 true）
            image_format: 图片格式过滤（可选: jpg, png, gif）
        
        Returns:
            格式化后的图片列表
        
        Examples:
            extract_article_images(url="https://mp.weixin.qq.com/s/...")
            extract_article_images(url="https://mp.weixin.qq.com/s/...", include_cover=False)
            extract_article_images(url="https://mp.weixin.qq.com/s/...", image_format="jpg")
        
        Error Handling:
            - URL 无效: 提供 URL 格式说明
            - 文章不存在: 提示检查 URL
            - 访问被拒绝: 建议在浏览器中打开链接
        """
        # 创建输入模型
        input_data = ExtractArticleImagesInput(
            url=url,
            include_cover=include_cover,
            image_format=image_format
        )
        return _extract_images_impl(input_data)

