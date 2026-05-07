from dataclasses import dataclass, field
from collections import Counter
import asyncio

async def read_file(path: str) -> tuple[str, str]:
    """返回（文件路径，文件内容）"""
    loop = asyncio.get_event_loop()
    # 文件IO是阻塞操作，用run_in_executor放到线程池里执行
    content = await loop.run_in_executor(None, lambda: open(path, encoding="utf-8").read())
    return path, content

@dataclass
class WordStats:
    total_words: int
    unique_words: int
    top_n: list[tuple[str, int]] = field(default_factory=list)

def count_words(text: str) -> dict[str, int]:
    words = text.lower().split()
    return dict(Counter(words))

def analyze(text: str, top_n: int = 5) -> WordStats:
    counts = count_words(text)
    sorted_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return WordStats(
        total_words=sum(counts.values()),
        unique_words=len(counts),
        top_n=sorted_words[:top_n]
    )


async def analyze_all(paths: list[str]) -> dict[str, WordStats]:
    tasks = [read_file(p) for p in paths]
    results = await asyncio.gather(*tasks)

    return {path: analyze(content) for path, content in results}

async def main() -> None:
    import sys
    if len(sys.argv) < 2:
        print("用法: python word_counter.py <文件1> <文件2> ...")
        sys.exit(1)

    paths = sys.argv[1:]

    all_stats = await analyze_all(paths)
    for path, stats in all_stats.items():
        print(f"\n📄 {path}")
        print(f"  总词数: {stats.total_words}")
        print(f"  不重复词数: {stats.unique_words}")
        print(f"  Top 词汇: {stats.top_n[:3]}")

if __name__ == "__main__":
    asyncio.run(main())