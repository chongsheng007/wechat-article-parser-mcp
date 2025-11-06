# Cursor 文件打开问题底层修复

## ✅ 已完成的修复

### 1. 修改了 Cursor 底层设置

**文件**: `~/Library/Application Support/Cursor/User/settings.json`

**添加的设置**:

```json
{
    "files.encoding": "utf8",              // 默认文件编码为 UTF-8
    "files.autoGuessEncoding": true,        // 自动检测文件编码
    "files.eol": "\n",                     // 统一使用 LF 换行符
    "files.associations": {                 // 文件关联
        "*.md": "markdown",
        "*.txt": "plaintext"
    },
    "editor.largeFileOptimizations": false, // 禁用大文件优化，确保所有文件都能打开
    "workbench.editor.enablePreview": true, // 启用文件预览
    "workbench.editor.enablePreviewFromQuickOpen": true // 快速打开时启用预览
}
```

---

## 🔧 彻底修复步骤

### 方法 1：使用修复脚本（推荐）

```bash
cd /Users/changjp/my-first-mcp-server
./fix_cursor_settings.sh
```

然后：
1. **完全关闭 Cursor**（按 `Cmd + Q`，不要只是关闭窗口）
2. **重新打开 Cursor**
3. **尝试打开文件**

### 方法 2：手动清理缓存

```bash
# 清理所有缓存
rm -rf ~/Library/Application\ Support/Cursor/Cache
rm -rf ~/Library/Application\ Support/Cursor/CachedData
rm -rf ~/Library/Application\ Support/Cursor/GPUCache

# 重启 Cursor
```

---

## 📋 设置说明

### 关键设置项

1. **`files.encoding: "utf8"`**
   - 强制 Cursor 使用 UTF-8 编码打开文件
   - 解决中文文件名和内容的问题

2. **`files.autoGuessEncoding: true`**
   - 自动检测文件编码
   - 如果 UTF-8 失败，会尝试其他编码

3. **`editor.largeFileOptimizations: false`**
   - 禁用大文件优化
   - 确保所有文件都能正常打开

4. **`workbench.editor.enablePreview: true`**
   - 启用文件预览功能
   - 允许快速预览文件内容

---

## 🔄 如何应用设置

### 步骤 1：确认设置已保存

检查设置文件：
```bash
cat ~/Library/Application\ Support/Cursor/User/settings.json
```

应该看到 `"files.encoding": "utf8"` 等设置。

### 步骤 2：清理缓存

运行修复脚本或手动清理：
```bash
./fix_cursor_settings.sh
```

### 步骤 3：重启 Cursor

**重要**：必须完全关闭 Cursor（`Cmd + Q`），然后重新打开。

### 步骤 4：测试

尝试打开之前打不开的文件：
- `文件命名规范.md`
- `修复完成说明.md`
- `cursor三种模式使用指南.md`

---

## ⚠️ 如果仍然无法打开

### 进一步排查

1. **检查文件权限**
   ```bash
   ls -la 文件名.md
   chmod 644 文件名.md
   ```

2. **清理扩展属性**
   ```bash
   xattr -c 文件名.md
   ```

3. **检查文件编码**
   ```bash
   file -I 文件名.md
   # 应该显示: text/plain; charset=utf-8
   ```

4. **重新安装 Cursor**
   - 如果以上都不行，可能需要重新安装 Cursor

---

## 📌 重要提醒

**设置已修改，但需要重启 Cursor 才能生效！**

1. 完全关闭 Cursor（`Cmd + Q`）
2. 重新打开 Cursor
3. 测试文件打开功能

---

**修复完成时间**: 2025年11月6日

