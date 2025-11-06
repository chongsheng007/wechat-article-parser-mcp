"""generate_image_from_image 工具实现 - 图生图"""

from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional
import os
from ..utils.api_client import make_img2img_request
from ..utils.formatters import format_success_response
from ..utils.errors import MCPError, APIKeyError


class GenerateImageFromImageInput(BaseModel):
    """图生图工具输入模型"""
    model_config = {"extra": "ignore"}  # 忽略额外字段，避免 MCP Inspector 添加的 format 等参数导致错误
    
    prompt: str = Field(
        description="图像生成提示词，描述想要生成的图像内容（支持中文和英文）",
        min_length=1,
        max_length=1000,
        examples=["一只可爱的小猫", "a beautiful sunset over mountains", "室内场景，现代风格"]
    )
    
    image_url: str = Field(
        description="参考图像 URL（必填）",
        min_length=1,
        examples=["https://example.com/image.jpg"]
    )
    
    strength: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="参考图像影响强度，默认 0.8（范围：0.0-1.0）。值越大，参考图像的影响越大",
        examples=[0.5, 0.8, 1.0]
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
    
    seed: Optional[int] = Field(
        default=None,
        description="随机种子，用于生成可重复的图像结果",
        ge=0
    )
    
    steps: int = Field(
        default=30,
        ge=10,
        le=50,
        description="生成步数，更多步数通常质量更好但耗时更长（范围：10-50）",
        examples=[20, 30, 40]
    )
    
    guidance_scale: float = Field(
        default=7.5,
        ge=1.0,
        le=20.0,
        description="引导强度，控制提示词的影响程度（范围：1.0-20.0）",
        examples=[5.0, 7.5, 10.0]
    )
    
    api_key: Optional[str] = Field(
        default=None,
        description="API 密钥，如果未提供则从环境变量 SEEDREAM_API_KEY 或 ARK_API_KEY 读取"
    )


def register_generate_image_from_image_tool(mcp: FastMCP):
    """注册 generate_image_from_image 工具"""
    
    @mcp.tool(
        annotations={
            "readOnlyHint": False,  # 生成操作
            "destructiveHint": False,  # 不修改现有资源
            "idempotentHint": False,  # 相同参数可能产生不同结果（除非使用 seed）
            "openWorldHint": True  # 可以生成任意内容
        }
    )
    def generate_image_from_image(input: GenerateImageFromImageInput) -> str:
        """
        使用即梦 Seedream 4.0 模型基于参考图像生成新图像（图生图）
        
        基于参考图像和文本提示词生成新图像，保持参考图像的部分特征。使用此工具可以：
        - 基于现有图像生成变体
        - 图像风格转换
        - 图像编辑和增强
        - 保持风格一致性
        
        Args:
            prompt: 图像生成提示词，描述想要生成的图像内容
            image_url: 参考图像 URL（必填）
            strength: 参考图像影响强度，默认 0.8（范围：0.0-1.0）
            negative_prompt: 负面提示词，描述不希望出现在图像中的内容
            width: 图像宽度（像素），默认 1024
            height: 图像高度（像素），默认 1024
            seed: 随机种子，用于生成可重复的图像结果
            steps: 生成步数，默认 30（范围：10-50）
            guidance_scale: 引导强度，默认 7.5（范围：1.0-20.0）
            api_key: API 密钥，如果未提供则从环境变量读取
        
        Returns:
            生成的图像 URL 或错误信息
        
        Examples:
            generate_image_from_image(prompt="一只可爱的小猫", image_url="https://example.com/cat.jpg")
            generate_image_from_image(prompt="风景画", image_url="https://example.com/scene.jpg", strength=0.6)
            generate_image_from_image(prompt="室内场景", image_url="https://example.com/room.jpg", negative_prompt="人物")
        
        Error Handling:
            - API Key 未设置: 提供明确的设置指导
            - 网络错误: 提供超时或连接错误信息
            - API 错误: 提供状态码、错误详情和 logid
            - 参数错误: 提供参数验证错误信息
        
        参考: https://www.volcengine.com/docs/82379/1541523
        """
        # 获取 API Key
        # 获取 API Key（优先使用 SEEDREAM_API_KEY，也支持 ARK_API_KEY 作为备选）
        api_key = input.api_key or os.getenv("SEEDREAM_API_KEY") or os.getenv("ARK_API_KEY")
        if not api_key:
            raise APIKeyError()
        
        # 模型名称 - 根据文档，正确的模型名称是 doubao-seedream-4-0-250828
        model = "doubao-seedream-4-0-250828"
        
        try:
            # 调用 API（图生图）
            result = make_img2img_request(
                api_key=api_key,
                model=model,
                prompt=input.prompt,
                image_url=input.image_url,
                strength=input.strength,
                width=input.width,
                height=input.height,
                steps=input.steps,
                guidance_scale=input.guidance_scale,
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

