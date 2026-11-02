"""验证 Media Agent 的流式输出是否正常（部分中转厂商不支持 stream）。"""

import sys
import time
from pathlib import Path

from openai import OpenAI

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_env  # noqa: E402

PROBE_PROMPT = "用 200 字介绍一下舆情分析的常见方法。"


def main():
    env = load_env()
    key = env.get("MEDIA_ENGINE_API_KEY")
    base = env.get("MEDIA_ENGINE_BASE_URL")
    model = env.get("MEDIA_ENGINE_MODEL_NAME")

    if not key:
        print("[SKIP] 未配置 MEDIA_ENGINE_API_KEY")
        return

    print(f"model={model} base={base}")
    client = OpenAI(api_key=key, base_url=base, timeout=60)

    try:
        started = time.time()
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": PROBE_PROMPT}],
            max_tokens=300,
            stream=True,
        )
        chunks = sum(1 for _ in stream)
        print(f"[OK] 流式完成，{chunks} 个 chunk，耗时 {time.time() - started:.1f}s")
    except Exception as exc:
        print(f"[FAIL] {type(exc).__name__}: {str(exc)[:150]}")


if __name__ == "__main__":
    main()
