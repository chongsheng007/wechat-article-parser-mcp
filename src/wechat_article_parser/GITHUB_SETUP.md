# GitHub 仓库设置完整指南

## 第一步：在 GitHub 创建仓库

### 1.1 创建新仓库

1. 登录 GitHub: https://github.com
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   ```
   Repository name: wechat-article-parser-mcp
   Description: MCP Server for parsing WeChat public account articles
   Visibility: Public（或 Private，根据需求）
   ```
4. **不要**勾选以下选项：
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license
5. 点击 "Create repository"

### 1.2 获取仓库 URL

创建后会显示仓库 URL，格式如下：
- HTTPS: `https://github.com/your-username/wechat-article-parser-mcp.git`
- SSH: `git@github.com:your-username/wechat-article-parser-mcp.git`

## 第二步：本地初始化 Git

### 2.1 检查 Git 状态

```bash
# 检查是否已有 Git 仓库
cd /Users/changjp/my-first-mcp-server
git status
```

### 2.2 初始化 Git（如果还没有）

```bash
# 初始化 Git 仓库
git init

# 添加远程仓库（替换为你的仓库 URL）
git remote add origin https://github.com/your-username/wechat-article-parser-mcp.git

# 或者使用 SSH（推荐）
git remote add origin git@github.com:your-username/wechat-article-parser-mcp.git
```

### 2.3 配置 Git 用户信息（如果还没有）

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 第三步：首次提交

### 3.1 检查文件状态

```bash
# 查看哪些文件会被提交
git status

# 查看 .gitignore 是否正确配置
cat .gitignore
```

### 3.2 添加文件

```bash
# 添加所有文件（除了 .gitignore 中排除的）
git add .

# 或者只添加特定目录
git add src/wechat_article_parser/
git add .cursor/specs/wechat-article-parser/
git add .github/
git add .gitignore
git add CHANGELOG.md
```

### 3.3 创建首次提交

```bash
git commit -m "feat: 初始项目结构

- 创建项目规范和设计文档
- 实现核心解析器（parser.py, html_extractor.py）
- 实现三个 MCP 工具（parse_article, extract_metadata, extract_images）
- 添加错误处理和格式化工具
- 配置 GitHub Actions CI
- 添加 Issue 模板和文档"
```

### 3.4 推送到 GitHub

```bash
# 设置主分支名称
git branch -M main

# 推送到远程仓库
git push -u origin main
```

## 第四步：验证推送成功

1. 在浏览器中打开你的 GitHub 仓库
2. 确认所有文件都已上传
3. 检查 `.github/workflows/ci.yml` 是否显示（可能需要刷新）

## 第五步：设置分支保护（可选）

### 5.1 在 GitHub 设置分支保护

1. 进入仓库 → Settings → Branches
2. 点击 "Add rule"
3. 配置规则：
   - Branch name pattern: `main`
   - ✅ Require a pull request before merging
   - ✅ Require approvals: 1
   - ✅ Require status checks to pass before merging

## 第六步：日常开发工作流

### 6.1 开发新功能

```bash
# 1. 确保本地代码是最新的
git checkout main
git pull origin main

# 2. 创建功能分支
git checkout -b feature/add-new-feature

# 3. 开发代码
# ... 编写代码 ...

# 4. 提交更改
git add .
git commit -m "feat: 添加新功能描述"

# 5. 推送分支
git push origin feature/add-new-feature

# 6. 在 GitHub 创建 Pull Request
# 访问: https://github.com/your-username/wechat-article-parser-mcp/pulls
# 点击 "New Pull Request"
```

### 6.2 创建 Pull Request

1. 在 GitHub 上点击 "New Pull Request"
2. 选择源分支（feature/xxx）和目标分支（main）
3. 填写 PR 描述：

```markdown
## 功能描述
简要描述本次 PR 的功能

## 变更内容
- [ ] 功能 A
- [ ] 功能 B

## 测试
- [ ] 单元测试通过
- [ ] 手动测试验证

## 相关 Issue
Closes #123
```

4. 等待 Code Review
5. 解决 Review 意见
6. 合并 PR（使用 "Squash and merge"）

## 第七步：版本发布

### 7.1 创建 Release

```bash
# 1. 更新版本号（在 pyproject.toml 中）
# version = "0.1.0"

# 2. 提交版本更新
git add pyproject.toml CHANGELOG.md
git commit -m "chore: 发布版本 v0.1.0"
git push origin main

# 3. 创建 Tag
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

### 7.2 在 GitHub 创建 Release

1. 进入仓库 → Releases → "Draft a new release"
2. 选择 Tag: `v0.1.0`
3. 填写 Release 标题: `v0.1.0`
4. 填写描述（从 CHANGELOG.md 复制）
5. 点击 "Publish release"

## 常见问题

### Q1: 推送时提示认证失败

**解决方案**:
```bash
# 使用 Personal Access Token（推荐）
# 1. GitHub → Settings → Developer settings → Personal access tokens
# 2. 生成新 Token（需要 repo 权限）
# 3. 使用 Token 作为密码推送

# 或使用 SSH 密钥
# 1. 生成 SSH 密钥: ssh-keygen -t ed25519 -C "your_email@example.com"
# 2. 添加 SSH 密钥到 GitHub: Settings → SSH and GPG keys
# 3. 使用 SSH URL: git remote set-url origin git@github.com:user/repo.git
```

### Q2: 想忽略某些文件但没有效果

**解决方案**:
```bash
# 检查 .gitignore 语法
# 确保文件路径正确

# 如果文件已经被 Git 跟踪，需要先移除
git rm --cached <file>
git commit -m "chore: 更新 .gitignore"
```

### Q3: 想撤销最后一次提交

**解决方案**:
```bash
# 只撤销提交，保留修改
git reset --soft HEAD~1

# 撤销提交和修改（谨慎使用）
git reset --hard HEAD~1
```

### Q4: 合并冲突怎么办

**解决方案**:
```bash
# 1. 拉取最新代码
git pull origin main

# 2. 解决冲突（编辑冲突文件）
# 3. 标记冲突已解决
git add <conflicted-file>

# 4. 完成合并
git commit
```

## 快速参考命令

```bash
# 查看状态
git status

# 查看差异
git diff

# 查看提交历史
git log --oneline

# 查看远程仓库
git remote -v

# 拉取最新代码
git pull origin main

# 推送代码
git push origin <branch>

# 创建并切换分支
git checkout -b feature/name

# 切换分支
git checkout main

# 删除分支
git branch -d feature/name

# 查看所有分支
git branch -a

# 查看标签
git tag

# 创建标签
git tag -a v0.1.0 -m "Release v0.1.0"
git push origin v0.1.0
```

## 下一步

- ✅ 代码已推送到 GitHub
- ✅ CI 已配置（自动运行测试）
- 📝 开始日常开发工作流
- 📋 参考 `.cursor/specs/wechat-article-parser/GITHUB_WORKFLOW.md` 了解详细工作流程

