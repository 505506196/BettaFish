"""通过国内镜像下载多语言情感分析模型。

HF_ENDPOINT 必须在导入 huggingface_hub 之前设置，否则不生效。
"""

import os

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

from huggingface_hub import snapshot_download  # noqa: E402

REPO_ID = "tabularisai/multilingual-sentiment-analysis"
LOCAL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")

print(f"使用镜像 {os.environ['HF_ENDPOINT']} 下载模型...")
snapshot_download(repo_id=REPO_ID, local_dir=LOCAL_DIR)
print(f"下载完成: {LOCAL_DIR}")
