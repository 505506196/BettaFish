"""验证数据库连通性，并列出已建的表。"""

import sys
from pathlib import Path

from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import build_db_url, load_env  # noqa: E402


def main():
    env = load_env()
    name = env.get("DB_NAME")
    try:
        engine = create_engine(build_db_url(env))
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            dialect = (env.get("DB_DIALECT") or "mysql").lower()
            if dialect in ("postgresql", "postgres"):
                rows = conn.execute(
                    text(
                        "SELECT tablename FROM pg_tables "
                        "WHERE schemaname = 'public' ORDER BY tablename"
                    )
                )
            else:
                rows = conn.execute(text("SHOW TABLES"))
            tables = [r[0] for r in rows]
    except Exception as exc:
        print(f"[FAIL] {str(exc)[:200]}")
        return 1

    print(f"[OK] 数据库已连接: db={name}, 共 {len(tables)} 张表")
    if tables:
        print("     " + ", ".join(tables[:10]))
    else:
        print("     警告: 没有任何表，请先执行 python MindSpider/schema/init_database.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
