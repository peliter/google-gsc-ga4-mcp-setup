# Google Search Console 權限與配置指引

## 1. 新增使用者/服務帳戶至 GSC
1. 進入 [Google Search Console](https://search.google.com/search-console)。
2. 選擇左上角的網站資源（如 `https://example.com` 或 `sc-domain:example.com`）。
3. 點選左下角 **設定 (Settings)** ➔ **使用者和權限 (Users and permissions)**。
4. 點選 **新增使用者 (Add user)**。
5. 輸入使用者 Email 或 Service Account Email（例如 `xxx@project-id.iam.gserviceaccount.com`）。
6. 權限設定為 **完整 (Full)** 或 **擁有者 (Owner)**。

## 2. 常用 GSC MCP 工具說明
* `mcp-gsc_list_properties`: 列出當前帳號/服務帳戶有權存取的所有 GSC 網站資源清單。
* `mcp-gsc_get_search_analytics`: 查詢指定網站的點擊次數、曝光次數、點閱率 (CTR)、排名。
* `mcp-gsc_get_advanced_search_analytics`: 支援多維度篩選與分頁進階查詢。
* `mcp-gsc_inspect_url_enhanced`: 檢測特定網址在 Google 索引中的狀態與結構化資料。
* `mcp-gsc_manage_sitemaps`: 管理與檢查 Sitemap 提交狀態。
