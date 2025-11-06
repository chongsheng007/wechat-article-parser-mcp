#!/bin/bash
# Git 提交和推送脚本

set -e

cd /Users/changjp/my-first-mcp-server

echo "🚀 准备提交代码到 GitHub"
echo ""

# 检查是否有远程仓库
if git remote -v | grep -q "origin"; then
    echo "✅ 远程仓库已配置"
    REMOTE_URL=$(git remote get-url origin)
    echo "   远程仓库: $REMOTE_URL"
else
    echo "⚠️  远程仓库未配置"
    echo ""
    echo "请先执行以下命令添加远程仓库："
    echo "  git remote add origin https://github.com/your-username/wechat-article-parser-mcp.git"
    echo ""
    echo "或者使用 SSH："
    echo "  git remote add origin git@github.com:your-username/wechat-article-parser-mcp.git"
    echo ""
    exit 1
fi

# 检查是否有未提交的更改
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ 没有需要提交的更改"
    exit 0
fi

echo "📋 当前文件状态："
git status --short

echo ""
read -p "是否继续提交？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消"
    exit 1
fi

# 提交
echo ""
echo "📝 创建提交..."
git commit -m "feat: 初始项目结构

- 创建微信公众号文章解析 MCP Server 项目
- 实现三个核心工具：parse_article, extract_metadata, extract_images
- 实现核心解析器（parser, html_extractor, formatters）
- 配置错误处理和格式化工具
- 添加 GitHub Actions CI 配置
- 添加 Issue 模板和完整文档
- 添加 GitHub 工作流程指南"

echo ""
echo "✅ 提交成功"
echo ""

# 检查当前分支
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "🔄 重命名分支为 main..."
    git branch -M main
fi

echo ""
read -p "是否推送到远程仓库？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⚠️  已跳过推送，你可以稍后手动执行："
    echo "  git push -u origin main"
    exit 0
fi

echo ""
echo "📤 推送到远程仓库..."
git push -u origin main

echo ""
echo "🎉 完成！代码已推送到 GitHub"
echo ""
echo "📝 下一步："
echo "1. 在 GitHub 上查看你的仓库"
echo "2. 检查 GitHub Actions CI 是否运行"
echo "3. 开始开发新功能"

