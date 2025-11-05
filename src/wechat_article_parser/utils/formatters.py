"""格式化工具模块"""

import html2text
from typing import Dict, List, Optional


def html_to_markdown(html_content: str) -> str:
    """将 HTML 转换为 Markdown"""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # 不换行
    h.unicode_snob = True  # 保留 Unicode 字符
    return h.handle(html_content)


def html_to_text(html_content: str) -> str:
    """将 HTML 转换为纯文本"""
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.body_width = 0
    return h.handle(html_content)


def format_article_response(
    data: Dict,
    format_type: str = "markdown",
    include_images: bool = True,
    include_links: bool = True
) -> str:
    """
    格式化文章响应
    
    Args:
        data: 提取的文章数据
        format_type: 输出格式 (markdown, text, html)
        include_images: 是否包含图片信息
        include_links: 是否包含链接信息
    
    Returns:
        格式化后的字符串
    """
    lines = []
    
    # 标题
    if data.get('title'):
        lines.append(f"# {data['title']}")
        lines.append("")
    
    # 元数据
    meta_lines = []
    if data.get('author'):
        meta_lines.append(f"作者: {data['author']}")
    if data.get('publish_time'):
        meta_lines.append(f"发布时间: {data['publish_time']}")
    
    if meta_lines:
        lines.append(" | ".join(meta_lines))
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # 正文内容
    if data.get('content'):
        content = data['content']
        if format_type == "markdown":
            content = html_to_markdown(content)
        elif format_type == "text":
            content = html_to_text(content)
        # html 格式保持原样
        
        lines.append(content)
        lines.append("")
    
    # 图片信息
    if include_images and data.get('images'):
        images = data['images']
        lines.append(f"\n## 图片 ({len(images)} 张)")
        lines.append("")
        for img in images:
            if img.get('alt'):
                lines.append(f"- [{img['alt']}]({img['url']})")
            else:
                lines.append(f"- {img['url']}")
        lines.append("")
    
    # 链接信息
    if include_links and data.get('links'):
        links = data['links']
        lines.append(f"\n## 链接 ({len(links)} 个)")
        lines.append("")
        for link in links:
            if link.get('text'):
                lines.append(f"- [{link['text']}]({link['url']})")
            else:
                lines.append(f"- {link['url']}")
        lines.append("")
    
    # 统计信息
    word_count = len(data.get('content', '')) if data.get('content') else 0
    if format_type == "text":
        word_count = len(html_to_text(data.get('content', '')))
    elif format_type == "markdown":
        word_count = len(html_to_markdown(data.get('content', '')))
    
    lines.append("---")
    lines.append(f"**统计**: 字数 {word_count} | 图片 {len(data.get('images', []))} | 链接 {len(data.get('links', []))}")
    
    return "\n".join(lines)


def format_metadata_response(data: Dict) -> str:
    """格式化元数据响应"""
    lines = []
    
    if data.get('title'):
        lines.append(f"**标题**: {data['title']}")
    
    if data.get('author'):
        lines.append(f"**作者**: {data['author']}")
    
    if data.get('publish_time'):
        lines.append(f"**发布时间**: {data['publish_time']}")
    
    if data.get('cover_image'):
        lines.append(f"**封面图**: {data['cover_image']}")
    
    if data.get('summary'):
        lines.append(f"**摘要**: {data['summary']}")
    
    return "\n".join(lines) if lines else "未找到元数据"


def format_images_response(images: List[Dict], include_cover: bool = True) -> str:
    """格式化图片列表响应"""
    lines = []
    
    if not images:
        return "未找到图片"
    
    lines.append(f"共找到 {len(images)} 张图片:\n")
    
    for img in images:
        img_info = f"**图片 {img.get('index', 0) + 1}**"
        if img.get('is_cover'):
            img_info += " (封面图)"
        lines.append(img_info)
        lines.append(f"URL: {img['url']}")
        if img.get('alt'):
            lines.append(f"描述: {img['alt']}")
        lines.append("")
    
    return "\n".join(lines)

