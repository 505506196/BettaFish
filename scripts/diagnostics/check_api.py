"""逐个试调 7 个 Agent 配置的 LLM API，报告哪些可用。"""

import sys
from pathlib import Path

from openai import OpenAI

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_env  # noqa: E402

TARGETS = [
    ("QUERY_ENGINE", "Query Agent"),
    ("INSIGHT_ENGINE", "Insight Agent"),
    ("MEDIA_ENGINE", "Media Agent"),
    ("REPORT_ENGINE", "Report Agent"),
    ("MINDSPIDER", "MindSpider 话题提取"),
    ("FORUM_HOST", "论坛主持人"),
    ("KEYWORD_OPTIMIZER", "SQL 关键词优化"),
]


def main():
    env = load_env()
    for prefix, label in TARGETS:
        key = env.get(f"{prefix}_API_KEY", "")
        base = env.get(f"{prefix}_BASE_URL", "")
        model = env.get(f"{prefix}_MODEL_NAME", "")

        if not key or key.startswith("YOUR_"):
            print(f"[SKIP] {label}: 未配置 {prefix}_API_KEY")
            continue

        try:
            client = OpenAI(api_key=key, base_url=base, timeout=30)
            client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "hi"}],
                max_tokens=5,
            )
            print(f"[OK]   {label}: {model}")
        except Exception as exc:
            msg = str(exc).replace("\n", " ")[:130]
            print(f"[FAIL] {label}: {model} -> {msg}")


if __name__ == "__main__":
    main()
