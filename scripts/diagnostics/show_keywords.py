"""查看数据库中最近一次提取出的舆情关键词。

深度爬取实际使用的关键词来自 MindSpider/data/daily_keywords.txt，
该文件可手动编辑以定向抓取自己关注的话题。
"""

import json
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build_db_url, load_env  # noqa: E402


def main():
    env = load_env()
    engine = create_engine(build_db_url(env))
    with engine.connect() as conn:
        row = conn.execute(
            text(
                "SELECT keywords FROM daily_topics "
                "ORDER BY extract_date DESC LIMIT 1"
            )
        ).fetchone()

    if not row or not row[0]:
        print("daily_topics 表中没有关键词记录，请先运行话题提取。")
        return

    keywords = json.loads(row[0])
    print(f"数据库中的关键词（共 {len(keywords)} 个，显示前 15 个）：")
    for i, kw in enumerate(keywords[:15], 1):
        print(f"  {i}. {kw}")


if __name__ == "__main__":
    main()
