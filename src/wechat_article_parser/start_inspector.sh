#!/bin/bash
# 使用标准 MCP Inspector 启动服务器

set -e

cd /Users/changjp/my-first-mcp-server/src/wechat_article_parser

echo "🚀 启动 MCP Inspector..."
echo ""
echo "📋 服务器配置："
echo "   项目路径: $(pwd)"
echo "   服务器文件: server.py"
echo ""
echo "🌐 MCP Inspector 将在浏览器中自动打开"
echo "   如果未自动打开，请访问显示的 URL"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# 使用标准 MCP Inspector
npx @modelcontextprotocol/inspector --transport stdio -- uv run python wechat_server.py

