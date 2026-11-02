"""查看核心数据表的记录数，用于判断数据是否已经抓到。"""

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build_db_url, load_env  # noqa: E402

TABLES = ["daily_news", "daily_topics", "topic_news_relation", "crawling_tasks"]


def main():
    env = load_env()
    engine = create_engine(build_db_url(env))
    with engine.connect() as conn:
        for table in TABLES:
            try:
                count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                print(f"{table:24} {count} 条")
            except Exception as exc:
                print(f"{table:24} 查询失败: {str(exc)[:60]}")


if __name__ == "__main__":
    main()
