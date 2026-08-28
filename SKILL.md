---
name: google-gsc-ga4-mcp-setup
description: "Cross-platform setup & configuration skill for Google Search Console (mcp-search-console) and Google Analytics 4 (analytics-mcp) MCP servers on macOS and Windows. Supports Service Account keys and personal Google OAuth 2.0 authentication."
---

# Google Search Console (GSC) & GA4 MCP Setup Skill

本技能用於在 macOS 與 Windows 環境下一鍵安裝、配置與維護 Google Search Console (`mcp-search-console`) 與 Google Analytics 4 (`analytics-mcp`) MCP 伺服器，支援 **Service Account (服務帳戶)** 與 **個人帳號 OAuth 2.0** 兩種認證模式。

---

## 支援環境與前置依賴
* **作業系統**：macOS (Apple Silicon / Intel)、Windows 10/11、Linux
* **自動安裝依賴**：
  * Astral `uv` / `uvx`（安裝腳本會自動檢測並於缺失時自動安裝）
  * Python 3.8+

---

## 觸發情境 (Triggers)
當使用者提到以下情境時觸發此 Skill：
* 「安裝 GSC / GA4 MCP」
* 「設定 Google Search Console / Google Analytics」
* 「切換 GSC / GA4 為 Service Account 登入」
* 「切換 GSC / GA4 為個人 OAuth 登入」
* 「設定 Windows / Mac 上的 Search Console MCP」

---

## 認證模式 (Authentication Modes)

### 模式 A：Service Account 服務帳戶（推薦）
* **適用場景**：背景自動化、無需人機互動彈窗、團隊共用。
* **流程**：
  1. 使用者提供 GCP Service Account JSON 金鑰檔案路徑（如 `~/.config/gcloud/pi-sa-xxx.json`）。
  2. 腳本解析金鑰，自動提取 `client_email`。
  3. 設定環境變數：
     * GSC: `GSC_CREDENTIALS_PATH` + `GSC_SKIP_OAUTH=true`
     * GA4: `GOOGLE_APPLICATION_CREDENTIALS`
  4. 提示使用者將該 Service Account Email 加至 GSC 資源（擁有者/完整權限）與 GA4 資源（檢視者/分析師）。

### 模式 B：個人帳號 OAuth 2.0（免金鑰檔案）
* **適用場景**：個人開發者、無 GCP 專案管理權限。
* **流程**：
  1. 使用者選擇 OAuth 模式（不提供 Service Account 路徑）。
  2. 移除 `GSC_SKIP_OAUTH` 與金鑰環境變數。
  3. **GSC 登入**：呼叫 GSC 相關工具或執行 `mcp-gsc_reauthenticate` 時自動彈出瀏覽器授權。
  4. **GA4 登入**：透過 `gcloud auth application-default login` 完成本機 ADC 授權。

---

## 執行與操作指令

### 1. 互動式安裝 (推薦)
```bash
# macOS / Linux
python3 scripts/setup.py

# Windows PowerShell
python scripts/setup.py
```

### 2. 指定 Service Account 非互動式安裝
```bash
python3 scripts/setup.py --service-account "/path/to/service-account.json"
```

### 3. 指定個人帳號 OAuth 2.0 模式
```bash
python3 scripts/setup.py --oauth
```

### 4. 移除 / 清除 GSC & GA4 MCP
```bash
python3 scripts/setup.py --uninstall
```

---

## 配置對照表 (Generated `opencode.json`)

```json
{
  "mcp": {
    "mcp-gsc": {
      "command": ["uvx", "mcp-search-console"],
      "enabled": true,
      "type": "local",
      "environment": {
        "GSC_CREDENTIALS_PATH": "/path/to/sa.json",
        "GSC_SKIP_OAUTH": "true",
        "PATH": "..."
      }
    },
    "analytics-mcp": {
      "command": ["uvx", "analytics-mcp"],
      "enabled": true,
      "type": "local",
      "environment": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/path/to/sa.json",
        "PATH": "..."
      }
    }
  }
}
```

---

## 疑難排解 (Troubleshooting)
1. **GSC 出現 403 Forbidden**：確認 GSC 網站資源內是否已將 Service Account Email / 個人帳號新增為使用者。
2. **GA4 出現 Permission Denied**：確認 Google Cloud 專案內已啟用 `Google Analytics Data API` 與 `Google Analytics Admin API`。
3. **找不到 uvx 指令**：確認環境 PATH 包含 `~/.local/bin` (Mac/Linux) 或 `%USERPROFILE%\.local\bin` (Windows)。
