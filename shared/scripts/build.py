#!/usr/bin/env python3
"""
书籍构建脚本
用于从数据文件生成章节内容、统计信息和导出文件
支持多项目管理
"""

import argparse
import json
import os
from pathlib import Path
from datetime import datetime


class BookBuilder:
    def __init__(self, project_name: str = None):
        self.script_dir = Path(__file__).parent
        self.workspace_root = self.script_dir.parent.parent

        if project_name:
            self.project_root = self.workspace_root / "projects" / project_name
        else:
            self.project_root = None

        self.shared_dir = self.workspace_root / "shared"
        self.output_dir = self.workspace_root / "output"

    def _get_project_dir(self, subdir: str) -> Path:
        if not self.project_root:
            raise ValueError("No project specified. Use --project option.")
        return self.project_root / subdir

    @property
    def data_dir(self) -> Path:
        return self._get_project_dir("data")

    @property
    def content_dir(self) -> Path:
        return self._get_project_dir("content")

    @property
    def templates_dir(self) -> Path:
        return self.shared_dir / "templates"

    def list_projects(self) -> list:
        """列出所有项目"""
        projects_dir = self.workspace_root / "projects"
        if not projects_dir.exists():
            return []
        return [p.name for p in projects_dir.iterdir() if p.is_dir()]

    def load_vocabulary(self, filename: str = "vocabulary.json") -> dict:
        """加载词汇数据"""
        vocab_file = self.data_dir / "vocabulary" / filename
        if vocab_file.exists():
            with open(vocab_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"vocabulary": [], "metadata": {}}

    def generate_word_entry(self, word_data: dict) -> str:
        """生成单个单词的 Markdown 条目"""
        lines = []
        lines.append(f"#### {word_data['word']}")
        lines.append("")
        lines.append(f"**音标：** {word_data.get('phonetic_uk', '')} (UK) | {word_data.get('phonetic_us', '')} (US)")
        lines.append("")
        lines.append(f"**词性：** {', '.join(word_data.get('part_of_speech', []))}")
        lines.append("")

        # 释义
        lines.append("**释义：**")
        for i, definition in enumerate(word_data.get("definitions", {}).get("chinese", []), 1):
            lines.append(f"- {definition}")
        lines.append("")

        # 英文解释
        eng_defs = word_data.get("definitions", {}).get("english", [])
        if eng_defs:
            lines.append(f"**英文解释：** {eng_defs[0]}")
            lines.append("")

        # 例句
        lines.append("**例句：**")
        for i, example in enumerate(word_data.get("examples", []), 1):
            lines.append(f"{i}. {example['sentence']}")
            lines.append(f"   *{example['translation']}*")
            lines.append("")

        # 搭配
        collocations = word_data.get("collocations", [])
        if collocations:
            lines.append("**常用搭配：** " + ", ".join(collocations))
            lines.append("")

        # 派生词
        derivatives = word_data.get("derivatives", [])
        if derivatives:
            lines.append("**派生词：**")
            for d in derivatives:
                lines.append(f"- {d['word']} ({d['part_of_speech']}) - {d['meaning']}")
            lines.append("")

        # 记忆技巧
        memory_tip = word_data.get("memory_tip")
        if memory_tip:
            lines.append(f"**记忆技巧：** {memory_tip}")
            lines.append("")

        lines.append("---")
        lines.append("")

        return "\n".join(lines)

    def generate_statistics(self) -> dict:
        """生成词汇统计信息"""
        vocab_data = self.load_vocabulary()
        words = vocab_data.get("vocabulary", [])

        stats = {
            "project": self.project_root.name if self.project_root else "unknown",
            "total_words": len(words),
            "by_level": {},
            "by_chapter": {},
            "by_frequency": {},
            "generated_at": datetime.now().isoformat()
        }

        for word in words:
            # 按等级统计
            level = word.get("level", "unknown")
            stats["by_level"][level] = stats["by_level"].get(level, 0) + 1

            # 按章节统计
            chapter = word.get("chapter", 0)
            stats["by_chapter"][chapter] = stats["by_chapter"].get(chapter, 0) + 1

            # 按词频统计
            freq = word.get("frequency", "unknown")
            stats["by_frequency"][freq] = stats["by_frequency"].get(freq, 0) + 1

        return stats

    def export_word_list(self, format: str = "txt") -> str:
        """导出单词列表"""
        vocab_data = self.load_vocabulary()
        words = vocab_data.get("vocabulary", [])

        project_name = self.project_root.name if self.project_root else "unknown"
        output_file = self.output_dir / project_name / f"word_list.{format}"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if format == "txt":
            content = "\n".join([w["word"] for w in words])
        elif format == "csv":
            lines = ["word,phonetic_uk,phonetic_us,level,chapter"]
            for w in words:
                lines.append(f"{w['word']},{w.get('phonetic_uk','')},{w.get('phonetic_us','')},{w.get('level','')},{w.get('chapter','')}")
            content = "\n".join(lines)
        else:
            content = json.dumps([w["word"] for w in words], ensure_ascii=False, indent=2)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        return str(output_file)

    def validate_vocabulary(self) -> list:
        """验证词汇数据完整性"""
        vocab_data = self.load_vocabulary()
        words = vocab_data.get("vocabulary", [])
        errors = []

        required_fields = ["id", "word", "phonetic_uk", "phonetic_us",
                          "part_of_speech", "definitions", "examples",
                          "level", "chapter"]

        for i, word in enumerate(words):
            for field in required_fields:
                if field not in word:
                    errors.append(f"Word #{i+1} ({word.get('word', 'unknown')}): missing field '{field}'")

            # 检查例句数量
            if len(word.get("examples", [])) < 2:
                errors.append(f"Word #{i+1} ({word.get('word', 'unknown')}): needs at least 2 examples")

        return errors


def main():
    parser = argparse.ArgumentParser(description="书籍构建工具")
    parser.add_argument("command", nargs="?", choices=["stats", "validate", "export", "list"],
                       help="执行的命令")
    parser.add_argument("--project", "-p", help="项目名称")
    parser.add_argument("--format", "-f", default="txt", choices=["txt", "csv", "json"],
                       help="导出格式 (默认: txt)")

    args = parser.parse_args()

    if not args.command:
        print("用法: python build.py <command> [options]")
        print("\n命令:")
        print("  list      - 列出所有项目")
        print("  stats     - 显示词汇统计 (需要 --project)")
        print("  validate  - 验证数据完整性 (需要 --project)")
        print("  export    - 导出单词列表 (需要 --project)")
        print("\n选项:")
        print("  --project, -p  项目名称")
        print("  --format, -f   导出格式 (txt/csv/json)")
        print("\n示例:")
        print("  python build.py list")
        print("  python build.py stats --project vocab-book")
        print("  python build.py export --project vocab-book --format csv")
        return

    if args.command == "list":
        builder = BookBuilder()
        projects = builder.list_projects()
        if projects:
            print("可用项目:")
            for p in projects:
                print(f"  - {p}")
        else:
            print("暂无项目")
        return

    if not args.project:
        print(f"错误: 命令 '{args.command}' 需要指定 --project 参数")
        return

    builder = BookBuilder(args.project)

    if not builder.project_root.exists():
        print(f"错误: 项目 '{args.project}' 不存在")
        return

    if args.command == "stats":
        stats = builder.generate_statistics()
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    elif args.command == "validate":
        errors = builder.validate_vocabulary()
        if errors:
            print("发现以下问题:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("数据验证通过！")

    elif args.command == "export":
        output_file = builder.export_word_list(args.format)
        print(f"已导出到: {output_file}")


if __name__ == "__main__":
    main()
