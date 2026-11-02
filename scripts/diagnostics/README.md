# 部署自检脚本

部署 BettaFish 后用于快速定位配置问题。所有脚本都只读 `.env` 和数据库，不写入任何数据。

在激活虚拟环境后，从项目根目录运行：

| 脚本 | 作用 |
|---|---|
| `check_db.py` | 验证数据库连通性，列出已建的表 |
| `check_api.py` | 逐个试调 7 个 Agent 的 LLM API，报告哪些可用、哪些报错 |
| `check_topics.py` | 查看核心数据表的记录数，判断数据是否抓到 |
| `show_topics.py` | 查看最近一次话题提取的完整记录 |
| `show_keywords.py` | 查看数据库中当前的舆情关键词 |
| `check_anspire_search.py` | 验证 Anspire 联网搜索接口是否可用 |
| `check_media_stream.py` | 验证 Media Agent 的流式输出（部分中转厂商不支持 stream） |

```powershell
.\venv\Scripts\Activate.ps1
python scripts/diagnostics/check_db.py
python scripts/diagnostics/check_api.py
```

> `check_api.py`、`check_anspire_search.py`、`check_media_stream.py` 会发起真实 API 调用，
> 会消耗少量配额。
