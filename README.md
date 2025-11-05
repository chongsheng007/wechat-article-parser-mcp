# MCP Servers 项目集合

本项目包含多个 MCP Server 实现。

## 项目列表

### 1. 微信公众号文章解析 MCP Server

一个用于解析微信公众号文章的 MCP Server，支持提取文章内容、元数据、图片和链接。

**快速开始**:
```bash
cd src/wechat_article_parser
uv sync
```

**配置到 Cursor**:
1. 查看 [src/wechat_article_parser/CURSOR_SETUP.md](src/wechat_article_parser/CURSOR_SETUP.md)
2. 或运行安装脚本：`./src/wechat_article_parser/install_cursor_mcp.sh`

**详细文档**: [src/wechat_article_parser/README.md](src/wechat_article_parser/README.md)

### 2. Seedream 4.0 图像生成 MCP Server

一个用于生成图像的 MCP Server，使用即梦 Seedream 4.0 模型。

**详细文档**: [src/seedream_image_generator/README.md](src/seedream_image_generator/README.md)

## 项目结构

```
.
├── src/
│   ├── wechat_article_parser/      # 微信公众号文章解析
│   └── seedream_image_generator/  # 图像生成
└── ...
```

## 许可证

MIT License
