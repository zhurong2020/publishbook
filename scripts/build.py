#!/usr/bin/env python3
"""
书籍构建脚本
用于从数据文件生成章节内容、统计信息和导出文件
"""

import json
import os
from pathlib import Path
from datetime import datetime


class BookBuilder:
    def __init__(self, project_root: str = None):
        if project_root is None:
            project_root = Path(__file__).parent.parent
        self.root = Path(project_root)
        self.data_dir = self.root / "data"
        self.content_dir = self.root / "content"
        self.output_dir = self.root / "output"
        self.templates_dir = self.root / "templates"

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

        output_file = self.output_dir / f"word_list.{format}"
        self.output_dir.mkdir(parents=True, exist_ok=True)

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
    import sys

    builder = BookBuilder()

    if len(sys.argv) < 2:
        print("用法: python build.py <command>")
        print("命令:")
        print("  stats     - 显示词汇统计")
        print("  validate  - 验证数据完整性")
        print("  export    - 导出单词列表")
        return

    command = sys.argv[1]

    if command == "stats":
        stats = builder.generate_statistics()
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    elif command == "validate":
        errors = builder.validate_vocabulary()
        if errors:
            print("发现以下问题:")
            for error in errors:
                print(f"  - {error}")
        else:
            print("数据验证通过！")

    elif command == "export":
        format = sys.argv[2] if len(sys.argv) > 2 else "txt"
        output_file = builder.export_word_list(format)
        print(f"已导出到: {output_file}")

    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
