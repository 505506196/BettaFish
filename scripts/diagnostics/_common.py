"""诊断脚本共用工具：定位项目根、加载 .env、拼装数据库连接串。"""

from pathlib import Path
from urllib.parse import quote_plus

from dotenv import dotenv_values

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"


def load_env():
    """读取项目根目录的 .env，不存在时给出明确提示。"""
    if not ENV_PATH.exists():
        raise SystemExit(
            f"未找到 {ENV_PATH}\n请先复制 .env.example 为 .env 并填写配置。"
        )
    return dotenv_values(ENV_PATH)


def build_db_url(env):
    """按 DB_DIALECT 拼装 SQLAlchemy 连接串，密码做 URL 编码。"""
    user = env.get("DB_USER") or ""
    pwd = quote_plus(env.get("DB_PASSWORD") or "")
    host = env.get("DB_HOST") or "127.0.0.1"
    port = env.get("DB_PORT") or ""
    name = env.get("DB_NAME") or ""
    dialect = (env.get("DB_DIALECT") or "mysql").lower()

    if dialect in ("postgresql", "postgres"):
        return f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{name}"

    charset = env.get("DB_CHARSET", "utf8mb4")
    return f"mysql+pymysql://{user}:{pwd}@{host}:{port}/{name}?charset={charset}"
