"""generate_image 工具实现"""

from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional
import os
from ..utils.api_client import make_api_request
from ..utils.formatters import format_success_response
from ..utils.errors import MCPError, APIKeyError


class GenerateImageInput(BaseModel):
    """图像生成工具输入模型"""
    model_config = {"extra": "ignore"}  # 忽略额外字段，避免 MCP Inspector 添加的 format 等参数导致错误
    
    prompt: str = Field(
        description="图像生成的提示词，描述想要生成的图像内容（支持中文和英文）",
        min_length=1,
        max_length=1000,
        examples=["一只可爱的小猫", "a beautiful sunset over mountains", "室内场景，现代风格"]
    )
    
    negative_prompt: Optional[str] = Field(
        default=None,
        description="负面提示词，描述不希望出现在图像中的内容",
        examples=["模糊", "低质量", "人物"]
    )
    
    width: int = Field(
        default=1024,
        ge=512,
        le=2048,
        description="图像宽度（像素），建议值：512, 768, 1024",
        examples=[512, 768, 1024]
    )
    
    height: int = Field(
        default=1024,
        ge=512,
        le=2048,
        description="图像高度（像素），建议值：512, 768, 1024",
        examples=[512, 768, 1024]
    )
    
    size: Optional[str] = Field(
        default=None,
        description="图像尺寸（可选），格式如 '1024x1024', '1K', '2K'。如果提供此参数，将忽略 width 和 height",
        examples=["1024x1024", "1K", "2K", "2048x2048"]
    )
    
    seed: Optional[int] = Field(
        default=None,
        description="随机种子，用于生成可重复的图像结果",
        ge=0
    )
    
    api_key: Optional[str] = Field(
        default=None,
        description="API 密钥，如果未提供则从环境变量 SEEDREAM_API_KEY 或 ARK_API_KEY 读取"
    )


def _generate_image_impl(input: GenerateImageInput) -> str:
    """图像生成的核心实现"""
    # 获取 API Key（优先使用 SEEDREAM_API_KEY，也支持 ARK_API_KEY 作为备选）
    api_key = input.api_key or os.getenv("SEEDREAM_API_KEY") or os.getenv("ARK_API_KEY")
    if not api_key:
        raise APIKeyError()
    
    # 模型名称 - 根据文档，正确的模型名称是 doubao-seedream-4-0-250828
    model = "doubao-seedream-4-0-250828"
    
    try:
        # 调用 API（优先使用 size 参数）
        result = make_api_request(
            api_key=api_key,
            model=model,
            prompt=input.prompt,
            width=input.width,
            height=input.height,
            size=input.size,  # 如果提供了 size，将优先使用
            negative_prompt=input.negative_prompt,
            seed=input.seed
        )
        
        # 格式化响应
        return format_success_response(result)
        
    except MCPError:
        raise  # 重新抛出 MCPError
    except Exception as e:
        raise MCPError(
            message=f"处理请求时发生异常: {str(e)}",
            suggestion="请检查请求参数，如果问题持续存在，请联系技术支持"
        )


def register_generate_image_tool(mcp: FastMCP):
    """注册 generate_image 工具"""
    
    @mcp.tool(
        annotations={
            "readOnlyHint": False,  # 生成操作
            "destructiveHint": False,  # 不修改现有资源
            "idempotentHint": False,  # 相同参数可能产生不同结果（除非使用 seed）
            "openWorldHint": True  # 可以生成任意内容
        }
    )
    def generate_image(input: GenerateImageInput) -> str:
        """
        使用即梦 Seedream 4.0 模型生成图像
        
        这是一个完整的图像生成工具，支持所有参数控制。使用此工具可以：
        - 根据文本提示词生成高质量图像
        - 自定义图像尺寸（使用 width/height 或 size 参数）
        - 排除不想要的元素（负面提示词）
        - 复现相同的结果（随机种子）
        
        Args:
            prompt: 图像生成提示词，描述想要生成的图像内容
            negative_prompt: 负面提示词，描述不希望出现在图像中的内容
            width: 图像宽度（像素），默认 1024（如果提供了 size，将忽略此参数）
            height: 图像高度（像素），默认 1024（如果提供了 size，将忽略此参数）
            size: 图像尺寸（可选），格式如 '1024x1024', '1K', '2K'。如果提供，将优先使用此参数
            seed: 随机种子，用于生成可重复的图像结果
            api_key: API 密钥，如果未提供则从环境变量读取
        
        Returns:
            图像 URL 或错误信息
        
        Examples:
            generate_image(prompt="一只可爱的小猫")
            generate_image(prompt="风景画", size="1024x1024")
            generate_image(prompt="室内场景", negative_prompt="人物", seed=12345)
        
        Error Handling:
            - API Key 未设置: 提供明确的设置指导
            - 网络错误: 提供超时或连接错误信息
            - API 错误: 提供状态码、错误详情和 logid
            - 参数错误: 提供参数验证错误信息
        
        参考: https://www.volcengine.com/docs/82379/1541523
        """
        return _generate_image_impl(input)

