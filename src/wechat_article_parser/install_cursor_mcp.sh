#!/bin/bash
# Cursor MCP 自动安装脚本

set -e

echo "🚀 微信公众号文章解析 MCP Server - Cursor 配置安装"
echo ""

# 获取项目路径（脚本所在目录的父目录的父目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "📁 项目路径: $PROJECT_ROOT"
echo ""

# 确定配置文件位置
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    CONFIG_DIR="$HOME/.cursor"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    CONFIG_DIR="$HOME/.cursor"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash)
    CONFIG_DIR="$APPDATA/Cursor/User"
else
    CONFIG_DIR="$HOME/.cursor"
fi

CONFIG_FILE="$CONFIG_DIR/mcp.json"

echo "📝 配置文件位置: $CONFIG_FILE"
echo ""

# 创建配置目录
mkdir -p "$CONFIG_DIR"

# 检查配置文件是否已存在
if [ -f "$CONFIG_FILE" ]; then
    echo "⚠️  配置文件已存在"
    echo ""
    read -p "是否要添加 wechat-article-parser 配置到现有文件？(y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 已取消"
        exit 0
    fi
    
    # 检查是否已存在配置
    if grep -q "wechat-article-parser" "$CONFIG_FILE"; then
        echo "⚠️  wechat-article-parser 配置已存在"
        read -p "是否要更新配置？(y/n) " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "❌ 已取消"
            exit 0
        fi
    fi
    
    # TODO: 这里可以添加 JSON 合并逻辑
    echo "💡 请手动编辑配置文件添加以下内容："
    echo ""
    echo "  \"wechat-article-parser\": {"
    echo "    \"command\": \"uv\","
    echo "    \"args\": ["
    echo "      \"run\","
    echo "      \"--directory\","
    echo "      \"$PROJECT_ROOT/src/wechat_article_parser\","
    echo "      \"python\","
    echo "      \"$PROJECT_ROOT/src/wechat_article_parser/wechat_server.py\""
    echo "    ]"
    echo "  }"
    echo ""
    echo "添加到 \"mcpServers\" 对象中"
else
    # 创建新配置文件
    echo "📝 创建新配置文件..."
    cat > "$CONFIG_FILE" << EOF
{
  "mcpServers": {
    "wechat-article-parser": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "$PROJECT_ROOT/src/wechat_article_parser",
        "python",
        "$PROJECT_ROOT/src/wechat_article_parser/wechat_server.py"
      ]
    }
  }
}
EOF
    
    echo "✅ 配置文件已创建"
fi

echo ""
echo "📋 配置内容："
echo "  项目路径: $PROJECT_ROOT"
echo "  服务器路径: $PROJECT_ROOT/src/wechat_article_parser/wechat_server.py"
echo ""

echo "✅ 配置完成！"
echo ""
echo "📝 下一步："
echo "1. 重启 Cursor（完全退出并重新启动）"
echo "2. 在聊天中验证配置："
echo "   \"你能看到 wechat-article-parser 的工具吗？\""
echo "3. 开始使用："
echo "   \"解析这篇文章: https://mp.weixin.qq.com/s/...\""
echo ""

