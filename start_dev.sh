#!/bin/bash
# 启动开发服务器脚本

set -e

echo "🚀 启动即梦 Seedream 4.0 MCP Server 开发模式..."
echo ""

# 检查环境变量
if [ -z "$SEEDREAM_API_KEY" ] && [ -z "$ARK_API_KEY" ]; then
    echo "⚠️  警告: 未设置 API 密钥环境变量"
    echo ""
    echo "请先设置环境变量:"
    echo "  export SEEDREAM_API_KEY='your-api-key-here'"
    echo "  或"
    echo "  export ARK_API_KEY='your-api-key-here'"
    echo ""
    echo "可选配置:"
    echo "  export API_BASE_URL='https://ark.cn-beijing.volces.com'"
    echo "  export REQUEST_TIMEOUT='60'"
    echo ""
    exit 1
fi

echo "✅ 环境变量检查通过"
echo ""

# 启动开发服务器
echo "📡 启动 MCP Inspector..."
echo "   访问: http://localhost:6274"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

uv run fastmcp dev src/seedream_image_generator/server.py

