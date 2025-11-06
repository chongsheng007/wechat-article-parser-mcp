"""错误处理工具"""

class MCPError(Exception):
    """MCP 服务器错误基类"""
    
    def __init__(self, message: str, suggestion: str = "", logid: str = ""):
        self.message = message
        self.suggestion = suggestion
        self.logid = logid
        super().__init__(self.message)
    
    def __str__(self):
        result = f"❌ {self.message}"
        if self.suggestion:
            result += f"\n💡 建议: {self.suggestion}"
        if self.logid:
            result += f"\n🔍 Log ID: {self.logid}"
        return result


class APIKeyError(MCPError):
    """API Key 错误"""
    
    def __init__(self):
        super().__init__(
            message="未提供 API 密钥",
            suggestion="请设置环境变量 SEEDREAM_API_KEY 或 ARK_API_KEY，或在调用时提供 api_key 参数"
        )


class APIRequestError(MCPError):
    """API 请求错误"""
    
    def __init__(self, status_code: int, error_detail: dict, logid: str = ""):
        error_code = error_detail.get("error", {}).get("code", "")
        error_message = error_detail.get("error", {}).get("message", "")
        
        suggestion = self._get_suggestion(status_code, error_code)
        
        super().__init__(
            message=f"API 请求失败 (状态码: {status_code})",
            suggestion=suggestion,
            logid=logid
        )
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message
    
    def _get_suggestion(self, status_code: int, error_code: str) -> str:
        """根据错误类型提供建议"""
        if status_code == 404:
            if "InvalidEndpointOrModel" in error_code:
                return "模型名称可能不正确，请检查模型标识符或联系技术支持确认"
            return "请求的资源不存在，请检查 API 端点是否正确"
        elif status_code == 500:
            return "服务器内部错误，可能是 API Key 权限问题或服务配置问题，建议联系技术支持并提供 logid"
        elif status_code == 401 or status_code == 403:
            return "认证失败，请检查 API Key 是否正确且未过期"
        elif status_code == 429:
            return "请求过于频繁，请稍后重试"
        else:
            return "请检查请求参数和网络连接，如果问题持续存在，请联系技术支持"


def handle_api_error(response) -> MCPError:
    """处理 API 响应错误"""
    try:
        error_data = response.json()
        logid = error_data.get("error", {}).get("logid", "") or response.headers.get("X-Request-Id", "")
        
        # 提取详细的错误信息用于调试
        error_code = error_data.get("error", {}).get("code", "")
        error_message = error_data.get("error", {}).get("message", "")
        service = error_data.get("error", {}).get("service", "")
        
        # 构建详细的错误消息
        detailed_message = f"API 请求失败 (状态码: {response.status_code})"
        if error_code:
            detailed_message += f"\n错误代码: {error_code}"
        if error_message:
            detailed_message += f"\n错误消息: {error_message}"
        if service:
            detailed_message += f"\n服务: {service}"
        
        suggestion = "服务器内部错误，可能是：\n"
        suggestion += "1. API Key 权限不足或服务未开通\n"
        suggestion += "2. 模型名称不正确\n"
        suggestion += "3. API 端点或参数格式不正确\n"
        suggestion += "4. 服务配置问题\n"
        suggestion += "建议联系技术支持并提供 logid"
        
        error = MCPError(
            message=detailed_message,
            suggestion=suggestion,
            logid=logid
        )
        error.error_code = error_code
        error.error_message = error_message
        error.service = service
        return error
    except Exception as e:
        # 如果无法解析 JSON，返回原始响应
        error_msg = f"API 请求失败 (状态码: {response.status_code})"
        suggestion = f"无法解析错误响应。"
        
        if response.status_code == 404:
            suggestion += "\n可能的原因：\n"
            suggestion += "1. API 端点不存在（图生图/多图融合功能可能不支持）\n"
            suggestion += "2. 模型名称不正确\n"
        elif response.status_code == 500:
            suggestion += "\n可能的原因：\n"
            suggestion += "1. API Key 权限不足或服务未开通\n"
            suggestion += "2. 服务配置问题\n"
            suggestion += "3. 需要联系技术支持\n"
        
        suggestion += f"\n原始响应: {response.text[:500]}"
        
        return MCPError(
            message=error_msg,
            suggestion=suggestion
        )

