# 疑難排解 (Troubleshooting)

### Q1: `uvx: command not found` 或安裝失敗
* **原因**：Astral `uv` 工具未安裝或尚未加入環境變數 `PATH`。
* **解法**：
  * **macOS / Linux**：
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
    ```
  * **Windows**：
    ```powershell
    powershell -ExecutionPolicy ByPass -Command "irm https://astral.sh/uv/install.ps1 | iex"
    ```

---

### Q2: GSC 呼叫時出現 `User does not have sufficient permissions for this site`
* **原因**：正在查詢的網址未在 GSC 中加入此帳號或 Service Account。
* **解法**：
  1. 先呼叫 `mcp-gsc_list_properties` 確認已授權的網站清單與 URL 格式（例如需精準比對 `https://example.com/` 或 `sc-domain:example.com`）。
  2. 至 Google Search Console 後台新增該 Email 權限。

---

### Q3: GA4 呼叫時出現 `403 Request had insufficient authentication scopes`
* **原因**：ADC 或 Token 權限不足，或是 GCP 專案中尚未啟用 `Google Analytics Data API`。
* **解法**：
  * 前往 GCP Console ➔ API 與服務 ➔ 啟用 `Google Analytics Data API`。
  * 若使用 OAuth，重新執行 `gcloud auth application-default login --scopes=https://www.googleapis.com/auth/analytics.readonly`。
