#!/bin/bash
# 准备 Git 提交的脚本

set -e

cd /Users/changjp/my-first-mcp-server

echo "🚀 准备 Git 提交..."
echo ""

# 检查是否已有 .git 目录
if [ -d .git ]; then
    echo "✅ Git 已初始化"
else
    echo "📦 初始化 Git 仓库..."
    git init
    echo "✅ Git 初始化完成"
fi

echo ""
echo "📋 检查文件状态..."
git status --short | head -20

echo ""
echo "📝 添加项目文件..."
# 添加项目相关文件
git add .gitignore
git add .github/
git add .cursor/specs/wechat-article-parser/
git add src/wechat_article_parser/
git add CHANGELOG.md
git add WECHAT_PARSER_COMPLETE.md

# 检查是否有其他项目文件需要添加
if [ -f README.md ]; then
    git add README.md
fi

echo ""
echo "✅ 文件已添加到暂存区"
echo ""
echo "📋 准备提交的文件："
git status --short

echo ""
echo "⚠️  注意："
echo "1. 请先在 GitHub 创建仓库"
echo "2. 然后运行以下命令添加远程仓库："
echo "   git remote add origin https://github.com/your-username/wechat-article-parser-mcp.git"
echo ""
echo "3. 提交代码："
echo "   git commit -m \"feat: 初始项目结构\""
echo ""
echo "4. 推送代码："
echo "   git branch -M main"
echo "   git push -u origin main"

