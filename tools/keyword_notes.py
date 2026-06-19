from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import textwrap

@dataclass
class KeywordNote:
    keyword: str
    content: str
    source_url: str
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()

    def update_content(self, new_content: str) -> None:
        self.content = new_content
        self.updated_at = datetime.now()

    def summary(self, max_length: int = 60) -> str:
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length].rstrip() + "..."

    def formatted(self) -> str:
        header = f"=== {self.keyword} ==="
        divider = "=" * len(header)
        lines = [
            divider,
            header,
            divider,
            f"来源: {self.source_url}",
            f"创建时间: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        if self.updated_at:
            lines.append(f"更新时间: {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        if self.tags:
            lines.append(f"标签: {', '.join(self.tags)}")
        lines.append("")
        lines.append("内容:")
        lines.append(textwrap.fill(self.content, width=70))
        lines.append("")
        return "\n".join(lines)

@dataclass
class NoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def remove_note(self, keyword: str) -> bool:
        for note in self.notes:
            if note.keyword == keyword:
                self.notes.remove(note)
                return True
        return False

    def find_by_keyword(self, keyword: str) -> Optional[KeywordNote]:
        for note in self.notes:
            if note.keyword == keyword:
                return note
        return None

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [note for note in self.notes if tag in note.tags]

    def all_keywords(self) -> List[str]:
        return [note.keyword for note in self.notes]

    def formatted_all(self) -> str:
        if not self.notes:
            return "暂无笔记"
        result = []
        for note in self.notes:
            result.append(note.formatted())
        return "\n".join(result)

    def export_markdown(self) -> str:
        lines = ["# 关键词笔记", ""]
        for note in self.notes:
            lines.append(f"## {note.keyword}")
            lines.append(f"- 来源: {note.source_url}")
            lines.append(f"- 创建时间: {note.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            if note.tags:
                lines.append(f"- 标签: {', '.join(note.tags)}")
            lines.append("")
            lines.append(note.content)
            lines.append("")
        return "\n".join(lines)


def create_sample_notes() -> NoteCollection:
    collection = NoteCollection()
    note1 = KeywordNote(
        keyword="爱游戏",
        content="爱游戏是一个专注于游戏资讯和社区的平台，提供最新的游戏新闻、评测和玩家交流。",
        source_url="https://mhome-aiyouxi.com.cn",
        tags=["游戏", "资讯", "社区"],
    )
    note2 = KeywordNote(
        keyword="游戏评测",
        content="游戏评测应当从画面、音效、玩法、剧情和可玩性等多个维度进行客观分析。",
        source_url="https://mhome-aiyouxi.com.cn/reviews",
        tags=["游戏", "评测"],
    )
    collection.add_note(note1)
    collection.add_note(note2)
    return collection


def main() -> None:
    collection = create_sample_notes()
    print("=== 格式化输出所有笔记 ===")
    print(collection.formatted_all())
    print("\n=== Markdown 导出 ===")
    print(collection.export_markdown())
    print("\n=== 查找关键词 '爱游戏' ===")
    note = collection.find_by_keyword("爱游戏")
    if note:
        print(note.summary(30))
    print("\n=== 查找标签 '评测' ===")
    for n in collection.find_by_tag("评测"):
        print(f"  - {n.keyword}: {n.summary(40)}")


if __name__ == "__main__":
    main()