# GitHub SSH 配置指南

## 步骤 1: 检查是否已有 SSH 密钥

首先检查是否已经存在 SSH 密钥：

```bash
ls -al ~/.ssh
```

如果看到 `id_ed25519.pub` 或 `id_rsa.pub`，说明已有密钥。

## 步骤 2: 生成新的 SSH 密钥（如果没有）

如果还没有 SSH 密钥，执行以下命令生成：

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

**注意**: 
- 将 `your_email@example.com` 替换为你的 GitHub 邮箱
- 按 Enter 使用默认文件位置（推荐）
- 可以设置密码（可选，更安全）或直接按 Enter 跳过

## 步骤 3: 启动 SSH 代理

```bash
eval "$(ssh-agent -s)"
```

## 步骤 4: 添加 SSH 密钥到 SSH 代理

```bash
# 对于 ed25519 密钥
ssh-add ~/.ssh/id_ed25519

# 或对于 RSA 密钥
ssh-add ~/.ssh/id_rsa
```

## 步骤 5: 复制公钥

```bash
# 复制公钥内容（选择对应的密钥类型）
cat ~/.ssh/id_ed25519.pub

# 或
cat ~/.ssh/id_rsa.pub
```

**重要**: 复制输出的完整内容（从 `ssh-ed25519` 或 `ssh-rsa` 开始到邮箱结束）

## 步骤 6: 添加到 GitHub

1. **访问 GitHub SSH 设置**:
   - 打开: https://github.com/settings/ssh/new
   - 或: GitHub → Settings → SSH and GPG keys → New SSH key

2. **填写信息**:
   - **Title**: 给这个密钥起个名字（如：MacBook Pro）
   - **Key**: 粘贴刚才复制的公钥内容
   - **Key type**: 选择 Authentication Key

3. **点击 "Add SSH key"**

## 步骤 7: 测试 SSH 连接

```bash
ssh -T git@github.com
```

如果配置成功，你会看到：
```
Hi chongsheng007! You've successfully authenticated, but GitHub does not provide shell access.
```

## 步骤 8: 配置 Git 使用 SSH

确保远程仓库使用 SSH URL：

```bash
cd /Users/changjp/my-first-mcp-server
git remote set-url origin git@github.com:chongsheng007/wechat-article-parser-mcp.git
git remote -v
```

## 步骤 9: 推送代码

```bash
git push -u origin main
```

如果一切配置正确，推送应该会成功！

## 故障排除

### 问题 1: 提示 "Permission denied (publickey)"

**解决方案**:
- 确认 SSH 密钥已添加到 GitHub
- 确认使用的邮箱与 GitHub 账户一致
- 尝试重新测试: `ssh -T git@github.com`

### 问题 2: 提示 "Host key verification failed"

**解决方案**:
```bash
# 删除旧的 GitHub 主机密钥
ssh-keygen -R github.com

# 重新测试
ssh -T git@github.com
```

### 问题 3: SSH 代理未运行

**解决方案**:
```bash
# 启动 SSH 代理
eval "$(ssh-agent -s)"

# 添加密钥
ssh-add ~/.ssh/id_ed25519
```

## 验证配置

运行以下命令验证所有配置：

```bash
# 1. 检查 SSH 密钥
ls -al ~/.ssh

# 2. 测试 GitHub 连接
ssh -T git@github.com

# 3. 检查远程仓库配置
git remote -v

# 4. 推送测试
git push -u origin main
```

