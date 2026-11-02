"""查看最近一次话题提取的完整记录，含表结构。"""

import sys
from pathlib import Path

from sqlalchemy import create_engine, inspect, text

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build_db_url, load_env  # noqa: E402

FIELD_PREVIEW_CHARS = 400


def main():
    env = load_env()
    engine = create_engine(build_db_url(env))

    columns = [c["name"] for c in inspect(engine).get_columns("daily_topics")]
    print("daily_topics 列:", columns)

    with engine.connect() as conn:
        row = (
            conn.execute(
                text("SELECT * FROM daily_topics ORDER BY extract_date DESC LIMIT 1")
            )
            .mappings()
            .first()
        )

    if not row:
        print("\ndaily_topics 表为空。")
        return

    for key, value in dict(row).items():
        print(f"\n[{key}]: {str(value)[:FIELD_PREVIEW_CHARS]}")


if __name__ == "__main__":
    main()
