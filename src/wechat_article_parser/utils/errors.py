"""错误处理模块"""

from typing import Optional


class MCPError(Exception):
    """MCP 错误基类"""
    def __init__(self, message: str, suggestion: Optional[str] = None):
        self.message = message
        self.suggestion = suggestion
        super().__init__(self.message)
    
    def __str__(self):
        error_msg = f"❌ {self.message}"
        if self.suggestion:
            error_msg += f"\n💡 建议: {self.suggestion}"
        return error_msg


class URLInvalidError(MCPError):
    """URL 无效错误"""
    def __init__(self, url: str):
        super().__init__(
            message=f"无效的微信公众号文章 URL: {url}",
            suggestion="请检查 URL 格式是否正确。微信公众号文章 URL 格式应为: https://mp.weixin.qq.com/s/..."
        )


class ArticleNotFoundError(MCPError):
    """文章不存在错误"""
    def __init__(self, url: str):
        super().__init__(
            message=f"文章不存在或已被删除: {url}",
            suggestion="请确认 URL 是否正确，或文章是否仍然存在"
        )


class AccessDeniedError(MCPError):
    """访问被拒绝错误"""
    def __init__(self, url: str):
        super().__init__(
            message=f"访问被拒绝: {url}",
            suggestion="文章可能需要登录或授权访问。请尝试在浏览器中打开该链接"
        )


class ParseError(MCPError):
    """解析错误"""
    def __init__(self, message: str, url: str):
        super().__init__(
            message=f"解析失败: {message}",
            suggestion=f"无法解析文章内容。请检查 URL 是否有效: {url}"
        )


def handle_request_error(error: Exception, url: str) -> MCPError:
    """处理 HTTP 请求错误"""
    error_msg = str(error)
    
    if "404" in error_msg or "Not Found" in error_msg:
        return ArticleNotFoundError(url)
    elif "403" in error_msg or "Forbidden" in error_msg:
        return AccessDeniedError(url)
    else:
        return MCPError(
            message=f"请求失败: {error_msg}",
            suggestion="请检查网络连接或稍后重试"
        )

