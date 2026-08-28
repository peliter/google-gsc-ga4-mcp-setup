# Google API 認證模式比較 (Service Account vs OAuth 2.0)

| 特性 | Service Account (服務帳戶) | 個人帳號 OAuth 2.0 |
| :--- | :--- | :--- |
| **互動需求** | 完全無互動，背景自動驗證 | 首次或過期需點擊瀏覽器彈窗授權 |
| **金鑰檔案** | 需要 GCP 下載的 `.json` 私鑰 | 不需要任何本機私鑰檔案 |
| **權限控管** | 需手動將 `xxx@iam.gserviceaccount.com` 加至資源 | 自動使用登入帳號原本在 GSC/GA4 的既有權限 |
| **Token 有效期**| 永遠有效（除非撤銷金鑰） | 自動透過 Refresh Token 刷新（預設持久） |
| **推薦環境** | 伺服器、背景 Agent、自動化腳本 | 本地個人筆電開發、臨時除錯 |

---

## Service Account 設定摘要
1. 在 GCP Console 建立服務帳戶並下載 JSON Key。
2. 啟用相關 API：
   * `Google Search Console API`
   * `Google Analytics Data API`
   * `Google Analytics Admin API`
3. 將服務帳戶 Email 賦予 GSC / GA4 資源存取權。
