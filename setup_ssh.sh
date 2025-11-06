#!/bin/bash
# GitHub SSH 配置脚本

set -e

echo "🔐 GitHub SSH 配置向导"
echo "======================"
echo ""

# 检查是否已有 SSH 密钥
if [ -f ~/.ssh/id_ed25519 ] || [ -f ~/.ssh/id_rsa ]; then
    echo "✅ 发现已有 SSH 密钥"
    if [ -f ~/.ssh/id_ed25519 ]; then
        echo "   密钥类型: ed25519"
        KEY_FILE=~/.ssh/id_ed25519
    else
        echo "   密钥类型: RSA"
        KEY_FILE=~/.ssh/id_rsa
    fi
else
    echo "📝 未发现 SSH 密钥，需要生成新密钥"
    echo ""
    read -p "请输入你的 GitHub 邮箱地址: " GITHUB_EMAIL
    
    if [ -z "$GITHUB_EMAIL" ]; then
        echo "❌ 邮箱地址不能为空"
        exit 1
    fi
    
    echo ""
    echo "🔑 生成 SSH 密钥..."
    echo "   提示: 可以直接按 Enter 使用默认位置，也可以设置密码（更安全）"
    echo ""
    
    ssh-keygen -t ed25519 -C "$GITHUB_EMAIL" -f ~/.ssh/id_ed25519
    
    KEY_FILE=~/.ssh/id_ed25519
    echo ""
    echo "✅ SSH 密钥生成成功"
fi

# 启动 SSH 代理
echo ""
echo "🚀 启动 SSH 代理..."
eval "$(ssh-agent -s)" > /dev/null

# 添加密钥到 SSH 代理
echo "📎 添加密钥到 SSH 代理..."
if [ -f ~/.ssh/id_ed25519 ]; then
    ssh-add ~/.ssh/id_ed25519 2>/dev/null || true
else
    ssh-add ~/.ssh/id_rsa 2>/dev/null || true
fi

# 显示公钥
echo ""
echo "📋 你的 SSH 公钥内容："
echo "======================"
if [ -f ~/.ssh/id_ed25519.pub ]; then
    cat ~/.ssh/id_ed25519.pub
    PUBLIC_KEY=$(cat ~/.ssh/id_ed25519.pub)
else
    cat ~/.ssh/id_rsa.pub
    PUBLIC_KEY=$(cat ~/.ssh/id_rsa.pub)
fi
echo "======================"
echo ""

# 复制到剪贴板（macOS）
if command -v pbcopy &> /dev/null; then
    if [ -f ~/.ssh/id_ed25519.pub ]; then
        cat ~/.ssh/id_ed25519.pub | pbcopy
        echo "✅ 公钥已复制到剪贴板"
    else
        cat ~/.ssh/id_rsa.pub | pbcopy
        echo "✅ 公钥已复制到剪贴板"
    fi
else
    echo "⚠️  无法自动复制到剪贴板，请手动复制上面的公钥内容"
fi

echo ""
echo "📝 下一步操作："
echo "1. 访问: https://github.com/settings/ssh/new"
echo "2. Title: 输入一个名称（如：MacBook Pro）"
echo "3. Key: 粘贴上面的公钥内容（已复制到剪贴板）"
echo "4. 点击 'Add SSH key'"
echo ""
read -p "完成后按 Enter 继续测试连接..."

# 测试连接
echo ""
echo "🔍 测试 SSH 连接..."
ssh -T git@github.com 2>&1 || {
    echo ""
    echo "⚠️  SSH 连接测试失败"
    echo "   请确认："
    echo "   1. 已将公钥添加到 GitHub"
    echo "   2. 使用的邮箱与 GitHub 账户一致"
    echo ""
    exit 1
}

# 配置远程仓库
echo ""
echo "🔧 配置 Git 远程仓库使用 SSH..."
cd /Users/changjp/my-first-mcp-server
git remote set-url origin git@github.com:chongsheng007/wechat-article-parser-mcp.git

echo ""
echo "📋 远程仓库配置："
git remote -v

echo ""
echo "✅ SSH 配置完成！"
echo ""
echo "🚀 现在可以推送代码了："
echo "   git push -u origin main"

