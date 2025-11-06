"""generate_image_fusion 工具实现 - 多图融合"""

from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from ..utils.api_client import make_fusion_request
from ..utils.formatters import format_success_response
from ..utils.errors import MCPError, APIKeyError


class GenerateImageFusionInput(BaseModel):
    """多图融合工具输入模型"""
    model_config = {"extra": "ignore"}  # 忽略额外字段，避免 MCP Inspector 添加的 format 等参数导致错误
    
    prompt: str = Field(
        description="图像生成提示词，描述想要生成的图像内容（支持中文和英文）",
        min_length=1,
        max_length=1000,
        examples=["融合两张图像的特征", "create a mixed style image"]
    )
    
    image_urls: List[str] = Field(
        description="参考图像 URL 数组（必填，至少2张）",
        min_length=2,
        examples=[["https://example.com/image1.jpg", "https://example.com/image2.jpg"]]
    )
    
    fusion_weights: Optional[List[float]] = Field(
        default=None,
        description="各图像的融合权重（可选）。如果不提供，将使用平均权重",
        examples=[[0.5, 0.5], [0.3, 0.7]]
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


def register_generate_image_fusion_tool(mcp: FastMCP):
    """注册 generate_image_fusion 工具"""
    
    @mcp.tool(
        annotations={
            "readOnlyHint": False,  # 生成操作
            "destructiveHint": False,  # 不修改现有资源
            "idempotentHint": False,  # 相同参数可能产生不同结果（除非使用 seed）
            "openWorldHint": True  # 可以生成任意内容
        }
    )
    def generate_image_fusion(input: GenerateImageFusionInput) -> str:
        """
        使用即梦 Seedream 4.0 模型融合多张图像生成新图像（多图融合）
        
        融合多张参考图像的特征生成新图像。使用此工具可以：
        - 融合多张图像的特征
        - 创建混合风格的图像
        - 实现复杂的图像合成任务
        
        Args:
            prompt: 图像生成提示词，描述想要生成的图像内容
            image_urls: 参考图像 URL 数组（必填，至少2张）
            fusion_weights: 各图像的融合权重（可选）
            negative_prompt: 负面提示词，描述不希望出现在图像中的内容
            width: 图像宽度（像素），默认 1024
            height: 图像高度（像素），默认 1024
            seed: 随机种子，用于生成可重复的图像结果
            steps: 生成步数，默认 30（范围：10-50）
            guidance_scale: 引导强度，默认 7.5（范围：1.0-20.0）
            api_key: API 密钥，如果未提供则从环境变量读取
        
        Returns:
            融合后的图像 URL 或错误信息
        
        Examples:
            generate_image_fusion(
                prompt="融合两张图像的特征",
                image_urls=["https://example.com/img1.jpg", "https://example.com/img2.jpg"]
            )
            generate_image_fusion(
                prompt="混合风格图像",
                image_urls=["https://example.com/img1.jpg", "https://example.com/img2.jpg"],
                fusion_weights=[0.3, 0.7]
            )
        
        Error Handling:
            - API Key 未设置: 提供明确的设置指导
            - 图像数量不足: 提示需要至少2张图像
            - 网络错误: 提供超时或连接错误信息
            - API 错误: 提供状态码、错误详情和 logid
            - 参数错误: 提供参数验证错误信息
        
        参考: https://www.volcengine.com/docs/82379/1541523
        """
        # 验证图像数量
        if not input.image_urls or len(input.image_urls) < 2:
            raise MCPError(
                message="多图融合需要至少2张参考图像",
                suggestion="请提供至少2张图像的 URL"
            )
        
        # 验证融合权重（如果提供）
        if input.fusion_weights:
            if len(input.fusion_weights) != len(input.image_urls):
                raise MCPError(
                    message="融合权重数量必须与图像数量一致",
                    suggestion=f"请提供 {len(input.image_urls)} 个权重值，或省略此参数使用平均权重"
                )
        
        # 获取 API Key
        # 获取 API Key（优先使用 SEEDREAM_API_KEY，也支持 ARK_API_KEY 作为备选）
        api_key = input.api_key or os.getenv("SEEDREAM_API_KEY") or os.getenv("ARK_API_KEY")
        if not api_key:
            raise APIKeyError()
        
        # 模型名称 - 根据文档，正确的模型名称是 doubao-seedream-4-0-250828
        model = "doubao-seedream-4-0-250828"
        
        try:
            # 调用 API（多图融合）
            result = make_fusion_request(
                api_key=api_key,
                model=model,
                prompt=input.prompt,
                image_urls=input.image_urls,
                fusion_weights=input.fusion_weights,
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

