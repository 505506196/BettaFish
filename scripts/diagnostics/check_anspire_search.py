"""验证 Anspire 联网搜索接口是否可用。"""

import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import load_env  # noqa: E402

PROBE_QUERY = "人工智能"


def main():
    env = load_env()
    key = env.get("ANSPIRE_API_KEY")
    url = env.get("ANSPIRE_BASE_URL")

    if not key or not url:
        print("[SKIP] 未配置 ANSPIRE_API_KEY / ANSPIRE_BASE_URL")
        return

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Accept": "*/*",
    }
    params = {"query": PROBE_QUERY, "top_k": 3, "Insite": "", "FromTime": "", "ToTime": ""}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=30)
    except Exception as exc:
        print(f"[ERROR] {str(exc)[:150]}")
        return

    print(f"HTTP {resp.status_code}")
    if resp.status_code != 200:
        print("[FAIL]", resp.text[:200])
        return

    results = resp.json().get("results", [])
    print(f"[OK] Anspire 可用，返回 {len(results)} 条结果")
    if results:
        print("首条标题:", str(results[0].get("title"))[:60])


if __name__ == "__main__":
    main()
