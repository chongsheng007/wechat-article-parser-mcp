"""HTML 内容提取器"""

from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from .errors import ParseError


class WeChatArticleExtractor:
    """微信公众号文章内容提取器"""
    
    def __init__(self, html_content: str, url: str):
        """
        初始化提取器
        
        Args:
            html_content: HTML 内容
            url: 文章 URL（用于错误提示）
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.url = url
    
    def extract_title(self) -> Optional[str]:
        """提取文章标题"""
        try:
            # 尝试多种选择器
            title_selectors = [
                'h1.rich_media_title',
                'h1#activity-name',
                'h1.article-title',
                'h1',
            ]
            
            for selector in title_selectors:
                title_elem = self.soup.select_one(selector)
                if title_elem:
                    return title_elem.get_text(strip=True)
            
            return None
        except Exception as e:
            raise ParseError(f"提取标题失败: {str(e)}", self.url)
    
    def extract_author(self) -> Optional[str]:
        """提取作者信息"""
        try:
            author_selectors = [
                'a.rich_media_meta_text',
                '.rich_media_meta_text',
                '#meta_content .rich_media_meta_text',
            ]
            
            for selector in author_selectors:
                author_elem = self.soup.select_one(selector)
                if author_elem:
                    text = author_elem.get_text(strip=True)
                    # 排除时间信息
                    if '年' not in text and '月' not in text and '日' not in text:
                        return text
            
            return None
        except Exception as e:
            raise ParseError(f"提取作者失败: {str(e)}", self.url)
    
    def extract_publish_time(self) -> Optional[str]:
        """提取发布时间"""
        try:
            time_selectors = [
                '#publish_time',
                '.publish_time',
                '.rich_media_meta_text:contains("年")',
            ]
            
            for selector in time_selectors:
                time_elem = self.soup.select_one(selector)
                if time_elem:
                    return time_elem.get_text(strip=True)
            
            # 尝试从 meta 标签提取
            time_meta = self.soup.find('meta', {'property': 'article:published_time'})
            if time_meta and time_meta.get('content'):
                return time_meta['content']
            
            return None
        except Exception as e:
            raise ParseError(f"提取发布时间失败: {str(e)}", self.url)
    
    def extract_content(self) -> Optional[str]:
        """提取正文内容"""
        try:
            content_selectors = [
                'div.rich_media_content',
                '#js_content',
                '.article-content',
                'div[class*="content"]',
            ]
            
            for selector in content_selectors:
                content_elem = self.soup.select_one(selector)
                if content_elem:
                    # 处理图片懒加载，将 data-src 转换为 src
                    self._fix_lazy_images(content_elem)
                    # 同时处理其他懒加载属性
                    self._fix_all_lazy_images(content_elem)
                    return str(content_elem)
            
            return None
        except Exception as e:
            raise ParseError(f"提取正文失败: {str(e)}", self.url)
    
    def extract_images(self) -> List[Dict[str, str]]:
        """提取所有图片"""
        images = []
        try:
            content_elem = self.soup.select_one('div.rich_media_content') or self.soup.select_one('#js_content')
            if not content_elem:
                return images
            
            img_tags = content_elem.find_all('img')
            for idx, img in enumerate(img_tags):
                # 尝试多种方式获取图片 URL
                img_url = (
                    img.get('src') or 
                    img.get('data-src') or 
                    img.get('data-original') or
                    img.get('data-src-s') or  # 微信有时使用这个属性
                    img.get('data-lazy-src')  # 懒加载图片
                )
                
                # 处理相对路径
                if img_url and not img_url.startswith('http'):
                    # 如果是相对路径，尝试转换为完整 URL
                    if img_url.startswith('//'):
                        img_url = 'https:' + img_url
                    elif img_url.startswith('/'):
                        img_url = 'https://mp.weixin.qq.com' + img_url
                
                # 处理微信图片的特殊格式（data:image 或 base64）
                if img_url and img_url.startswith('data:image'):
                    # base64 图片，保留原样
                    pass
                elif img_url:
                    # 处理微信图片 URL（可能需要添加 Referer）
                    # 微信图片通常使用 mmbiz.qpic.cn 或 mmbizurl.cn
                    if 'mmbiz.qpic.cn' in img_url or 'mmbizurl.cn' in img_url:
                        # 微信图片 URL，可能需要特殊处理
                        # 但先返回原始 URL
                        pass
                    
                    images.append({
                        'url': img_url,
                        'alt': img.get('alt', '') or img.get('title', ''),
                        'index': idx
                    })
            
            return images
        except Exception as e:
            raise ParseError(f"提取图片失败: {str(e)}", self.url)
    
    def extract_links(self) -> List[Dict[str, str]]:
        """提取所有链接"""
        links = []
        try:
            content_elem = self.soup.select_one('div.rich_media_content') or self.soup.select_one('#js_content')
            if not content_elem:
                return links
            
            link_tags = content_elem.find_all('a', href=True)
            for idx, link in enumerate(link_tags):
                href = link.get('href', '')
                text = link.get_text(strip=True)
                if href and href.startswith('http'):
                    links.append({
                        'url': href,
                        'text': text,
                        'index': idx
                    })
            
            return links
        except Exception as e:
            raise ParseError(f"提取链接失败: {str(e)}", self.url)
    
    def extract_cover_image(self) -> Optional[str]:
        """提取封面图"""
        try:
            cover_selectors = [
                'meta[property="og:image"]',
                'meta[name="twitter:image"]',
                'img.rich_media_cover',
            ]
            
            for selector in cover_selectors:
                cover_elem = self.soup.select_one(selector)
                if cover_elem:
                    if cover_elem.name == 'meta':
                        return cover_elem.get('content')
                    else:
                        return cover_elem.get('src') or cover_elem.get('data-src')
            
            return None
        except Exception as e:
            raise ParseError(f"提取封面图失败: {str(e)}", self.url)
    
    def _fix_lazy_images(self, element):
        """修复懒加载图片，将 data-src 转换为 src"""
        for img in element.find_all('img', {'data-src': True}):
            if not img.get('src'):
                img['src'] = img.get('data-src', '')
    
    def _fix_all_lazy_images(self, element):
        """修复所有类型的懒加载图片"""
        for img in element.find_all('img'):
            # 尝试从各种懒加载属性中获取图片 URL
            lazy_url = (
                img.get('data-src') or 
                img.get('data-original') or
                img.get('data-src-s') or
                img.get('data-lazy-src')
            )
            
            # 如果当前没有 src 或 src 是占位符，使用懒加载的 URL
            current_src = img.get('src', '')
            if lazy_url and (not current_src or 'data:image' in current_src or 'placeholder' in current_src.lower()):
                img['src'] = lazy_url
                
                # 处理相对路径
                if not lazy_url.startswith('http'):
                    if lazy_url.startswith('//'):
                        img['src'] = 'https:' + lazy_url
                    elif lazy_url.startswith('/'):
                        img['src'] = 'https://mp.weixin.qq.com' + lazy_url
    
    def extract_all(self) -> Dict:
        """提取所有信息"""
        return {
            'title': self.extract_title(),
            'author': self.extract_author(),
            'publish_time': self.extract_publish_time(),
            'content': self.extract_content(),
            'images': self.extract_images(),
            'links': self.extract_links(),
            'cover_image': self.extract_cover_image(),
        }

