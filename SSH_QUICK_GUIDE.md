# SSH 配置快速指南

## 🚀 快速开始（推荐）

运行配置脚本（交互式）：

```bash
cd /Users/changjp/my-first-mcp-server
./setup_ssh.sh
```

脚本会自动：
- ✅ 检查是否已有 SSH 密钥
- ✅ 如果没有，引导你生成新密钥
- ✅ 复制公钥到剪贴板
- ✅ 引导你添加到 GitHub
- ✅ 测试连接
- ✅ 配置 Git 远程仓库

## 📝 手动配置步骤

### 1. 生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

**说明**:
- 将 `your_email@example.com` 替换为你的 GitHub 邮箱
- 按 Enter 使用默认位置（推荐）
- 可以设置密码（可选）或直接按 Enter

### 2. 启动 SSH 代理

```bash
eval "$(ssh-agent -s)"
```

### 3. 添加密钥到 SSH 代理

```bash
ssh-add ~/.ssh/id_ed25519
```

### 4. 复制公钥

```bash
cat ~/.ssh/id_ed25519.pub
```

**复制输出的完整内容**（从 `ssh-ed25519` 开始到邮箱结束）

### 5. 添加到 GitHub

1. 访问: https://github.com/settings/ssh/new
2. **Title**: 输入名称（如：MacBook Pro）
3. **Key**: 粘贴刚才复制的公钥
4. 点击 **"Add SSH key"**

### 6. 测试连接

```bash
ssh -T git@github.com
```

成功会看到：
```
Hi chongsheng007! You've successfully authenticated, but GitHub does not provide shell access.
```

### 7. 配置 Git 使用 SSH

```bash
cd /Users/changjp/my-first-mcp-server
git remote set-url origin git@github.com:chongsheng007/wechat-article-parser-mcp.git
```

### 8. 推送代码

```bash
git push -u origin main
```

## ✅ 验证配置

运行以下命令验证：

```bash
# 1. 检查密钥是否存在
ls -al ~/.ssh

# 2. 测试 GitHub 连接
ssh -T git@github.com

# 3. 检查远程仓库
cd /Users/changjp/my-first-mcp-server
git remote -v

# 应该显示：
# origin  git@github.com:chongsheng007/wechat-article-parser-mcp.git (fetch)
# origin  git@github.com:chongsheng007/wechat-article-parser-mcp.git (push)
```

## 🔧 故障排除

### 问题 1: "Permission denied (publickey)"

**原因**: SSH 密钥未添加到 GitHub 或密钥不匹配

**解决**:
1. 确认已将公钥添加到 GitHub
2. 确认使用的邮箱与 GitHub 账户一致
3. 重新测试: `ssh -T git@github.com`

### 问题 2: "Host key verification failed"

**解决**:
```bash
ssh-keygen -R github.com
ssh -T git@github.com
```

### 问题 3: SSH 代理未运行

**解决**:
```bash
eval "$(ssh-agent -s)
ssh-add ~/.ssh/id_ed25519
```

## 📚 详细文档

完整配置指南请查看: `SETUP_SSH.md`

## 🎯 下一步

SSH 配置完成后，执行：

```bash
cd /Users/changjp/my-first-mcp-server
git push -u origin main
```

代码就会推送到 GitHub 了！

