# Google Search Console & GA4 MCP Setup Skill

跨平台（macOS / Windows / Linux）的 Google Search Console (`mcp-search-console`) 與 Google Analytics 4 (`analytics-mcp`) MCP 伺服器安裝與設定技能。

---

## 🌟 功能特色
* ⚡ **跨平台支援**：完美相容 macOS (Apple Silicon / Intel) 與 Windows 10/11。
* 📦 **自動安裝依賴**：自動檢測並安裝 Astral `uv` / `uvx`。
* 🔐 **雙認證模式**：
  * **Service Account（服務帳戶）**：指定 JSON 金鑰檔案路徑，全自動免彈窗背景認證。
  * **個人帳號 OAuth 2.0**：無金鑰時自動切換至瀏覽器 OAuth 彈窗登入與 Google ADC。
* 🧹 **自動清理衝突**：自動移除舊版重複的 `search-console-mcp`，避免 Context Token 浪費。
* 💾 **安全備份**：修改 `opencode.json` 前自動建立備份 (`.json.bak`)。

---

## 🚀 快速開始

### 1. 互動式安裝 (推薦)
```bash
# macOS / Linux
python3 scripts/setup.py

# Windows
python scripts/setup.py
```

### 2. 指定 Service Account 金鑰
```bash
python3 scripts/setup.py -s "/path/to/service-account.json"
```

### 3. 指定個人帳號 OAuth 模式
```bash
python3 scripts/setup.py --oauth
```

### 4. 移除設定
```bash
python3 scripts/setup.py --uninstall
```

---

## 📂 專案結構
```
google-gsc-ga4-mcp-setup/
├── SKILL.md                  # Skill 定義檔
├── README.md                 # 說明文件
├── .gitignore
├── scripts/
│   ├── setup.py             # 核心跨平台安裝腳本 (Python)
│   ├── install.sh           # macOS / Linux 快速啟動腳本
│   └── install.ps1          # Windows PowerShell 快速啟動腳本
└── references/
    ├── auth-modes.md        # 認證模式比較說明
    ├── gsc-permissions.md   # GSC 權限配置指引
    ├── ga4-permissions.md   # GA4 權限配置指引
    └── troubleshooting.md   # 常見問題與排除
```

---

## 📄 授權
MIT License
