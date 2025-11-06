# Cursor Create PR 和 Review 功能说明

## 📋 功能概述

在 Cursor 对话框右上角，您会看到两个按钮：
- **Create PR**（创建拉取请求）
- **Review**（审查代码）

这些功能与 GitHub 集成，用于简化代码管理和协作流程。

---

## 🔵 Create PR（创建拉取请求）

### 什么是 PR？

**Pull Request（拉取请求）**，简称 PR，是 Git/GitHub 工作流程中的核心功能：
- 用于向主分支（如 `main`）提交代码更改
- 允许团队成员审查代码后再合并
- 保持代码库的质量和一致性

### Create PR 的作用

1. **自动生成 PR**：基于当前分支的更改自动创建 PR
2. **填充 PR 信息**：自动生成标题、描述和更改的文件列表
3. **提高效率**：无需手动在 GitHub 上创建 PR
4. **规范化提交**：确保提交信息的规范性

### 使用场景

当您完成以下操作后，可以使用 Create PR：

```bash
# 1. 创建功能分支
git checkout -b feature/新功能

# 2. 开发并提交代码
git add .
git commit -m "feat: 添加新功能"

# 3. 推送到远程
git push origin feature/新功能
```

然后点击 **Create PR** 按钮，Cursor 会：
- 自动检测当前分支
- 生成 PR 标题和描述
- 在 GitHub 上创建 Pull Request

### 实际使用步骤

#### 步骤 1：准备工作

1. **确保代码已提交并推送**
   ```bash
   git add .
   git commit -m "feat: 功能描述"
   git push origin feature/分支名
   ```

2. **确保 GitHub 仓库已配置**
   - 项目已连接到 GitHub 仓库
   - 有远程仓库地址：`git remote -v`

#### 步骤 2：使用 Create PR

1. **在 Cursor 中完成代码开发**
   - 编写或修改代码
   - 确保代码已保存

2. **点击对话框右上角的 "Create PR" 按钮**

3. **填写 PR 信息**（如果有弹出窗口）
   - **标题**：简要描述本次更改
   - **描述**：详细说明更改内容
   - **目标分支**：通常是 `main` 或 `master`

4. **确认创建**
   - Cursor 会在 GitHub 上创建 PR
   - 自动打开浏览器或显示 PR 链接

#### 步骤 3：后续操作

1. **查看 PR**
   - 在 GitHub 上查看创建的 PR
   - 检查更改的文件和代码差异

2. **等待审查**
   - 团队成员会审查您的代码
   - 根据反馈进行修改

3. **合并 PR**
   - 审查通过后，在 GitHub 上合并 PR
   - 使用 "Squash and merge"（推荐）

---

## 🔍 Review（审查代码）

### 什么是 Code Review？

**Code Review（代码审查）**是代码质量控制的重要环节：
- 团队成员检查代码质量
- 发现潜在问题和 bug
- 确保代码符合项目规范
- 分享知识和最佳实践

### Review 的作用

1. **审查现有 PR**：查看已创建的 Pull Request
2. **添加评论**：对代码提出建议或问题
3. **提出修改建议**：指出需要改进的地方
4. **批准或拒绝**：决定是否合并 PR

### 使用场景

当您需要审查其他人的代码时：

1. **查看 PR 列表**
   - 在 Cursor 中点击 "Review" 按钮
   - 查看待审查的 Pull Request

2. **审查代码更改**
   - 查看文件变更
   - 检查代码逻辑
   - 验证测试是否通过

3. **添加审查意见**
   - 对特定行添加评论
   - 提出改进建议
   - 询问问题

4. **批准或请求修改**
   - **Approve**：批准 PR，可以合并
   - **Request Changes**：需要修改后再审查
   - **Comment**：仅添加评论，不阻止合并

### 实际使用步骤

#### 步骤 1：打开 Review

1. **点击对话框右上角的 "Review" 按钮**

2. **选择要审查的 PR**
   - 从列表中选择一个 Pull Request
   - 或输入 PR 编号

#### 步骤 2：审查代码

1. **查看更改的文件**
   - 查看新增、修改、删除的文件
   - 检查文件大小和复杂度

2. **检查代码差异**
   - 逐行查看代码更改
   - 理解代码逻辑
   - 检查是否有潜在问题

3. **运行测试**（如果适用）
   - 确保 CI/CD 测试通过
   - 验证功能是否正常

#### 步骤 3：添加审查意见

1. **对特定行添加评论**
   - 点击代码行的左侧（`+` 号）
   - 输入评论内容
   - 提交评论

2. **添加一般评论**
   - 在 PR 底部添加总体评论
   - 说明审查结果

#### 步骤 4：完成审查

1. **选择审查结果**
   - **Approve**：代码可以合并
   - **Request Changes**：需要修改
   - **Comment**：仅评论

2. **提交审查**
   - 提交审查意见
   - PR 作者会收到通知

---

## 💡 实际工作流程示例

### 场景 1：开发新功能并创建 PR

```bash
# 1. 从 main 分支创建新分支
git checkout main
git pull origin main
git checkout -b feature/add-user-authentication

# 2. 开发代码
# ... 编写代码 ...

# 3. 提交代码
git add .
git commit -m "feat: 添加用户认证功能"
git push origin feature/add-user-authentication

# 4. 在 Cursor 中点击 "Create PR"
# 5. 填写 PR 信息
# 6. 确认创建
```

### 场景 2：审查队友的 PR

1. **收到审查请求**（GitHub 通知）
2. **在 Cursor 中点击 "Review"**
3. **查看 PR 详情和代码更改**
4. **添加审查意见**
   - 指出问题
   - 提出改进建议
5. **批准或请求修改**

### 场景 3：根据审查意见修改代码

```bash
# 1. 切换到 PR 分支
git checkout feature/分支名

# 2. 根据审查意见修改代码
# ... 修改代码 ...

# 3. 提交修改
git add .
git commit -m "fix: 根据审查意见修复问题"
git push origin feature/分支名

# 4. PR 会自动更新
# 5. 审查者会收到通知
```

---

## ⚙️ 配置要求

### 1. GitHub 账户连接

确保 Cursor 已连接到您的 GitHub 账户：

1. **打开 Cursor 设置**
   - `Cmd + ,`（Mac）或 `Ctrl + ,`（Windows/Linux）

2. **查找 GitHub 设置**
   - 搜索 "GitHub"
   - 查看账户连接状态

3. **如果需要连接**
   - 点击 "Sign in with GitHub"
   - 授权 Cursor 访问 GitHub

### 2. Git 仓库配置

确保项目已连接到 GitHub 仓库：

```bash
# 检查远程仓库
git remote -v

# 如果没有，添加远程仓库
git remote add origin https://github.com/用户名/仓库名.git
```

### 3. 分支设置

确保使用正确的分支命名和分支策略：

```bash
# 主分支通常是 main 或 master
git branch -M main

# 功能分支使用 feature/ 前缀
git checkout -b feature/功能名称
```

---

## 🎯 最佳实践

### Create PR 最佳实践

1. **清晰的 PR 标题**
   - 使用格式：`feat: 功能描述` 或 `fix: 问题描述`
   - 遵循 [Conventional Commits](https://www.conventionalcommits.org/)

2. **详细的 PR 描述**
   ```markdown
   ## 功能描述
   简要说明本次更改的目的
   
   ## 变更内容
   - 功能 A
   - 功能 B
   
   ## 测试
   - [ ] 单元测试通过
   - [ ] 手动测试验证
   
   ## 相关 Issue
   Closes #123
   ```

3. **保持 PR 小而专注**
   - 一个 PR 只做一件事
   - 避免过大的 PR（超过 500 行）

4. **确保测试通过**
   - 运行所有测试
   - 确保 CI/CD 通过

### Review 最佳实践

1. **及时审查**
   - 尽快审查 PR，不要拖延
   - 设置审查提醒

2. **建设性反馈**
   - 指出问题时，提供解决方案
   - 保持友好和专业的态度

3. **全面审查**
   - 检查代码逻辑
   - 验证测试覆盖
   - 检查代码风格

4. **明确批准条件**
   - 明确说明批准的条件
   - 不要模糊审批

---

## ❓ 常见问题

### Q1: Create PR 按钮是灰色的，无法点击？

**可能原因**：
1. 当前不在功能分支上（在 main 分支）
2. 没有未推送的提交
3. GitHub 账户未连接

**解决方法**：
```bash
# 检查当前分支
git branch

# 创建功能分支
git checkout -b feature/分支名

# 检查是否有未推送的提交
git status
git push origin feature/分支名
```

### Q2: Review 按钮看不到其他 PR？

**可能原因**：
1. 仓库中没有其他 PR
2. GitHub 权限不足
3. 网络连接问题

**解决方法**：
- 在 GitHub 上手动查看 PR
- 检查 GitHub 账户权限
- 刷新 Cursor 连接

### Q3: PR 创建后如何修改？

**方法 1：在 GitHub 上修改**
- 直接在 GitHub PR 页面编辑标题和描述

**方法 2：通过代码更新**
```bash
# 修改代码后
git add .
git commit -m "fix: 修改内容"
git push origin feature/分支名

# PR 会自动更新
```

---

## 📚 相关资源

- **GitHub Pull Request 文档**：https://docs.github.com/en/pull-requests
- **Conventional Commits**：https://www.conventionalcommits.org/
- **代码审查最佳实践**：https://github.com/google/eng-practices

---

## 🎓 总结

**Create PR** 和 **Review** 是 Cursor 与 GitHub 集成的重要功能：

- **Create PR**：快速创建 Pull Request，提高开发效率
- **Review**：方便地审查代码，保证代码质量

这两个功能让您可以在 Cursor 中完成完整的 Git 工作流程，无需频繁切换到 GitHub 网站。

---

**最后更新**：2025年11月6日  
**适用版本**：Cursor 最新版

