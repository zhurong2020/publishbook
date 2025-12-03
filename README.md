# 出版项目工作区 (Publishing Workspace)

## 项目简介

本仓库采用 Monorepo 结构管理多个出版项目，共享模板、脚本和风格指南。

## 仓库结构

```
publishbook/
├── shared/                      # 共享资源
│   ├── templates/              # 通用模板
│   │   └── chapter_template.md
│   ├── scripts/                # 构建脚本
│   │   └── build.py
│   └── styles/                 # 风格指南
│       └── STYLE_GUIDE.md
│
├── projects/                    # 各出版项目
│   ├── vocab-book/             # 项目1: 英文单词书
│   │   ├── OUTLINE.md
│   │   ├── content/
│   │   ├── data/
│   │   └── assets/
│   ├── [project-2]/            # 项目2: 待创建
│   └── [project-3]/            # 项目3: 待创建
│
├── output/                      # 统一输出目录
├── .gitignore
└── README.md
```

## 项目列表

| 项目 | 目录 | 状态 | 描述 |
|------|------|------|------|
| 英文单词学习书 | `projects/vocab-book/` | 规划中 | 面向中国学习者的英语词汇书 |
| 普通人的云生活 | `projects/cloud-life/` | 规划中 | 零成本打造数字王国，自托管入门指南 |

## 快速开始

### 创建新项目

```bash
# 1. 创建项目目录
mkdir -p projects/your-project/{content/chapters,content/appendices,data,assets/images}

# 2. 复制模板
cp shared/templates/chapter_template.md projects/your-project/content/

# 3. 创建项目大纲
touch projects/your-project/OUTLINE.md
```

### 使用共享资源

- **模板**: `shared/templates/` - 章节、词条格式模板
- **脚本**: `shared/scripts/build.py` - 数据验证、统计、导出
- **风格**: `shared/styles/STYLE_GUIDE.md` - 写作规范

### 构建命令

```bash
# 查看词汇统计
python shared/scripts/build.py stats --project vocab-book

# 验证数据完整性
python shared/scripts/build.py validate --project vocab-book

# 导出单词列表
python shared/scripts/build.py export --project vocab-book --format csv
```

## 项目管理原则

1. **独立性**: 每个项目在 `projects/` 下有完整的目录结构
2. **共享性**: 通用模板和工具放在 `shared/`
3. **一致性**: 所有项目遵循 `shared/styles/STYLE_GUIDE.md`
4. **隔离性**: 项目间数据不互相依赖

## 添加新书项目示例

假设要添加一本"商务英语"书籍：

```
projects/
└── business-english/
    ├── OUTLINE.md           # 本书大纲
    ├── README.md            # 项目说明（可选）
    ├── content/
    │   ├── chapters/
    │   └── appendices/
    ├── data/
    │   ├── vocabulary/
    │   └── exercises/
    └── assets/
        └── images/
```

## 许可证

[待定]
