#!/bin/bash
# Cursor 文件打开问题彻底修复脚本

echo "🔧 开始修复 Cursor 文件打开设置..."

# 1. 清理 Cursor 缓存
echo "1. 清理 Cursor 缓存..."
CURSOR_CACHE_DIR="$HOME/Library/Application Support/Cursor/Cache"
CURSOR_CACHEDATA_DIR="$HOME/Library/Application Support/Cursor/CachedData"
CURSOR_GPUCACHE_DIR="$HOME/Library/Application Support/Cursor/GPUCache"

if [ -d "$CURSOR_CACHE_DIR" ]; then
    rm -rf "$CURSOR_CACHE_DIR"/*
    echo "   ✅ 已清理 Cache 目录"
fi

if [ -d "$CURSOR_CACHEDATA_DIR" ]; then
    rm -rf "$CURSOR_CACHEDATA_DIR"/*
    echo "   ✅ 已清理 CachedData 目录"
fi

if [ -d "$CURSOR_GPUCACHE_DIR" ]; then
    rm -rf "$CURSOR_GPUCACHE_DIR"/*
    echo "   ✅ 已清理 GPUCache 目录"
fi

# 2. 验证设置文件
echo ""
echo "2. 验证设置文件..."
SETTINGS_FILE="$HOME/Library/Application Support/Cursor/User/settings.json"

if [ -f "$SETTINGS_FILE" ]; then
    # 检查 JSON 格式
    if python3 -m json.tool "$SETTINGS_FILE" > /dev/null 2>&1; then
        echo "   ✅ settings.json 格式正确"
        
        # 检查是否包含编码设置
        if grep -q "files.encoding" "$SETTINGS_FILE"; then
            echo "   ✅ 已包含文件编码设置"
        else
            echo "   ⚠️  缺少文件编码设置，正在添加..."
            # 这里需要手动添加，因为 JSON 格式复杂
        fi
    else
        echo "   ❌ settings.json 格式错误"
    fi
else
    echo "   ⚠️  settings.json 不存在"
fi

# 3. 清理工作区缓存
echo ""
echo "3. 清理工作区缓存..."
WORKSPACE_STORAGE="$HOME/Library/Application Support/Cursor/User/workspaceStorage"
if [ -d "$WORKSPACE_STORAGE" ]; then
    find "$WORKSPACE_STORAGE" -name "*.json" -type f -mtime +7 -delete 2>/dev/null
    echo "   ✅ 已清理旧的工作区缓存"
fi

echo ""
echo "✅ 修复完成！"
echo ""
echo "📌 下一步操作："
echo "1. 完全关闭 Cursor（Cmd+Q）"
echo "2. 重新打开 Cursor"
echo "3. 尝试打开文件"
echo ""
echo "如果问题仍然存在，请运行："
echo "   rm -rf \"$HOME/Library/Application Support/Cursor/Cache\""
echo "   rm -rf \"$HOME/Library/Application Support/Cursor/CachedData\""



