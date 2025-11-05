"""文章解析核心逻辑"""

import re
import requests
from typing import Dict, Optional
from .html_extractor import WeChatArticleExtractor
from .errors import (
    URLInvalidError,
    ArticleNotFoundError,
    AccessDeniedError,
    handle_request_error,
    ParseError,
)


# 请求头配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}


def validate_wechat_url(url: str) -> bool:
    """
    验证是否为有效的微信公众号文章 URL
    
    Args:
        url: 待验证的 URL
    
    Returns:
        是否为有效的微信公众号文章 URL
    """
    patterns = [
        r'https://mp\.weixin\.qq\.com/s\?.*',
        r'https://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+',
        r'http://mp\.weixin\.qq\.com/s\?.*',
        r'http://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+',
    ]
    return any(re.match(pattern, url) for pattern in patterns)


def normalize_url(url: str) -> str:
    """
    规范化 URL（移除多余参数，转换为标准格式）
    
    Args:
        url: 原始 URL
    
    Returns:
        规范化后的 URL
    """
    # 移除尾部的斜杠和空格
    url = url.strip().rstrip('/')
    
    # 如果是短链接，直接返回
    if re.match(r'https?://mp\.weixin\.qq\.com/s/[a-zA-Z0-9_-]+', url):
        return url
    
    # 如果是长链接，保留关键参数
    if '?' in url:
        base_url = url.split('?')[0]
        params = url.split('?')[1]
        # 可以在这里添加参数过滤逻辑
        return f"{base_url}?{params}"
    
    return url


def fetch_article_html(url: str, timeout: int = 10) -> str:
    """
    获取文章 HTML 内容
    
    Args:
        url: 文章 URL
        timeout: 请求超时时间（秒）
    
    Returns:
        HTML 内容
    
    Raises:
        URLInvalidError: URL 无效
        ArticleNotFoundError: 文章不存在
        AccessDeniedError: 访问被拒绝
        ParseError: 解析失败
    """
    # 验证 URL
    if not validate_wechat_url(url):
        raise URLInvalidError(url)
    
    # 规范化 URL
    url = normalize_url(url)
    
    try:
        # 发送请求
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        
        # 检查状态码
        if response.status_code == 404:
            raise ArticleNotFoundError(url)
        elif response.status_code == 403:
            raise AccessDeniedError(url)
        elif response.status_code != 200:
            raise ParseError(
                f"HTTP {response.status_code}: {response.reason}",
                url
            )
        
        # 检查内容是否有效
        if not response.text or len(response.text) < 100:
            raise ParseError("返回内容为空或过短", url)
        
        # 检查是否被重定向到登录页
        if 'mp.weixin.qq.com/mp/verify' in response.url:
            raise AccessDeniedError(url)
        
        return response.text
        
    except requests.exceptions.Timeout:
        raise ParseError("请求超时", url)
    except requests.exceptions.ConnectionError:
        raise ParseError("连接失败", url)
    except (URLInvalidError, ArticleNotFoundError, AccessDeniedError, ParseError):
        raise  # 重新抛出已定义的错误
    except Exception as e:
        raise handle_request_error(e, url)


def parse_wechat_article(url: str) -> Dict:
    """
    解析微信公众号文章
    
    Args:
        url: 文章 URL
    
    Returns:
        包含文章信息的字典
    
    Raises:
        各种解析错误
    """
    # 获取 HTML
    html_content = fetch_article_html(url)
    
    # 提取内容
    extractor = WeChatArticleExtractor(html_content, url)
    data = extractor.extract_all()
    
    # 添加 URL
    data['url'] = url
    
    # 计算统计信息
    content_html = data.get('content', '')
    if content_html:
        from .formatters import html_to_text
        text_content = html_to_text(content_html)
        data['metadata'] = {
            'word_count': len(text_content),
            'image_count': len(data.get('images', [])),
            'link_count': len(data.get('links', [])),
        }
    else:
        data['metadata'] = {
            'word_count': 0,
            'image_count': 0,
            'link_count': 0,
        }
    
    return data

