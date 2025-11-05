# 推送到 GitHub - 快速指南

## ✅ 已完成

- ✅ Git 仓库已初始化
- ✅ 代码已提交到本地仓库
- ✅ 分支已重命名为 `main`

## 📋 下一步：推送到 GitHub

### 步骤 1: 在 GitHub 创建仓库

1. 访问 https://github.com
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   - **Repository name**: `wechat-article-parser-mcp`
   - **Description**: `MCP Server for parsing WeChat public account articles`
   - **Visibility**: Public 或 Private
   - **不要**勾选任何初始化选项（README, .gitignore, license）
4. 点击 "Create repository"

### 步骤 2: 添加远程仓库

复制仓库 URL，然后执行以下命令之一：

#### 使用 HTTPS（推荐新手）

```bash
cd /Users/changjp/my-first-mcp-server
git remote add origin https://github.com/your-username/wechat-article-parser-mcp.git
```

#### 使用 SSH（推荐，更安全）

```bash
cd /Users/changjp/my-first-mcp-server
git remote add origin git@github.com:your-username/wechat-article-parser-mcp.git
```

**注意**: 将 `your-username` 替换为你的 GitHub 用户名

### 步骤 3: 推送到 GitHub

```bash
git push -u origin main
```

如果使用 HTTPS，可能会要求输入 GitHub 用户名和密码（或 Personal Access Token）

### 步骤 4: 验证推送

1. 在浏览器中打开你的 GitHub 仓库
2. 确认所有文件都已上传
3. 检查 `.github/workflows/ci.yml` 是否显示

## 🎉 完成！

推送成功后，你可以：

1. **查看仓库**: https://github.com/your-username/wechat-article-parser-mcp
2. **查看提交**: 在 GitHub 上可以看到你的提交历史
3. **检查 CI**: GitHub Actions 会自动运行测试（如果配置了）

## 📝 后续开发流程

### 开发新功能

```bash
# 1. 创建功能分支
git checkout -b feature/功能名称

# 2. 开发代码
# ... 编写代码 ...

# 3. 提交
git add .
git commit -m "feat: 功能描述"

# 4. 推送
git push origin feature/功能名称

# 5. 在 GitHub 创建 Pull Request
```

### 提交规范

- `feat`: 新功能
- `fix`: 修复问题
- `docs`: 文档更新
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具配置

## 🔧 故障排除

### 问题：推送时提示认证失败

**解决方案**:
1. 使用 Personal Access Token（推荐）
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 生成新 Token（需要 `repo` 权限）
   - 使用 Token 作为密码推送

2. 或使用 SSH 密钥
   - 生成 SSH 密钥: `ssh-keygen -t ed25519 -C "your_email@example.com"`
   - 添加 SSH 密钥到 GitHub: Settings → SSH and GPG keys
   - 使用 SSH URL: `git remote set-url origin git@github.com:user/repo.git`

### 问题：远程仓库已存在

**解决方案**:
```bash
# 移除现有远程仓库
git remote remove origin

# 添加新的远程仓库
git remote add origin https://github.com/your-username/wechat-article-parser-mcp.git
```

## 📚 参考文档

- **GitHub 工作流程**: `.cursor/specs/wechat-article-parser/GITHUB_WORKFLOW.md`
- **GitHub 设置指南**: `src/wechat_article_parser/GITHUB_SETUP.md`
- **项目总结**: `WECHAT_PARSER_COMPLETE.md`

