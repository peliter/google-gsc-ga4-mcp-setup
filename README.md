# Google Search Console (GSC) & Google Analytics 4 (GA4) MCP Setup

跨平台（macOS / Windows / Linux）的 GSC (`mcp-search-console`) 與 GA4 (`analytics-mcp`) MCP 伺服器一鍵安裝與配置技能。

---

## 🤖 給 AI Agent 的自動執行指引 (AI Agent Instructions)

當使用者在對話中輸入：
> **「幫我安裝 https://github.com/peliter/google-gsc-ga4-mcp-setup」** 或 **「設定 GSC 與 GA4 MCP」**

請 AI Agent 依循以下 3 步驟自動完成安裝：

### 步驟 1：詢問認證方式（或直接檢測）
詢問使用者是否有 Google Cloud Service Account JSON 金鑰路徑：
* **若有提供路徑**：使用該金鑰進行非互動設定。
* **若未提供或選擇個人登入**：自動採用個人 OAuth 2.0 模式。

### 步驟 2：執行安裝指令 (由 Agent 呼叫 Bash/Terminal 執行)

**macOS / Linux：**
```bash
# 1. 下載 / Clone 至暫存目錄或 Skills 目錄
git clone https://github.com/peliter/google-gsc-ga4-mcp-setup.git /tmp/gsc-ga4-setup || (cd /tmp/gsc-ga4-setup && git pull)

# 2. 執行安裝 (有 Service Account)
python3 /tmp/gsc-ga4-setup/install.py --service-account "/path/to/key.json" --non-interactive

# 或 執行安裝 (個人 OAuth 模式)
python3 /tmp/gsc-ga4-setup/install.py --oauth --non-interactive
```

**Windows (PowerShell)：**
```powershell
# 1. 下載 / Clone
git clone https://github.com/peliter/google-gsc-ga4-mcp-setup.git "$env:TEMP\gsc-ga4-setup"

# 2. 執行安裝 (有 Service Account)
python "$env:TEMP\gsc-ga4-setup\install.py" --service-account "C:\path\to\key.json" --non-interactive

# 或 執行安裝 (個人 OAuth 模式)
python "$env:TEMP\gsc-ga4-setup\install.py" --oauth --non-interactive
```

### 步驟 3：回報結果與後續指引
向使用者回報安裝成功，並提示：
* **Service Account 模式**：請將該 Service Account Email 加至 GSC 與 GA4 權限。
* **個人 OAuth 模式**：首次使用 GSC 工具時依瀏覽器彈窗授權；GA4 可於終端執行 `gcloud auth application-default login`。

---

## 🌟 核心功能特色
* ⚡ **跨平台支援**：macOS (Apple Silicon / Intel)、Windows 10/11、Linux。
* 📦 **自動安裝依賴**：自動檢測並安裝 Astral `uv` / `uvx`。
* 🔐 **雙認證模式**：
  * **Service Account**：全自動免彈窗背景認證（支援 GSC & GA4）。
  * **個人 OAuth 2.0**：支援瀏覽器彈窗登入與 Google ADC。
* 🧹 **清理舊版衝突**：自動移除重複的 `search-console-mcp`。
* 💾 **配置安全備份**：修改 `opencode.json` 前自動建立備份。

---

## 🚀 人工手動執行方式

```bash
# 互動式安裝（依提示選擇模式）
python3 install.py

# 指定 Service Account 金鑰
python3 install.py -s "/path/to/service-account.json"

# 指定個人 OAuth 模式
python3 install.py --oauth

# 移除設定
python3 install.py --uninstall
```

---

## 📂 專案結構
```
google-gsc-ga4-mcp-setup/
├── install.py               # 根目錄通用安裝入口 (Python)
├── install.sh               # macOS / Linux 快速入口
├── install.ps1              # Windows PowerShell 快速入口
├── SKILL.md                 # Agent Skill 定義檔
├── README.md                # 說明文件與 Agent 指引
├── .gitignore
├── scripts/
│   ├── setup.py             # 核心跨平台安裝腳本
│   ├── install.sh
│   └── install.ps1
└── references/
    ├── auth-modes.md        # 認證模式比較
    ├── gsc-permissions.md   # GSC 權限配置
    ├── ga4-permissions.md   # GA4 權限配置
    └── troubleshooting.md   # 常見問題與排除
```

---

## 📄 授權
MIT License
