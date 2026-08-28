# Google Analytics 4 權限與配置指引

## 1. 新增使用者/服務帳戶至 GA4
1. 進入 [Google Analytics](https://analytics.google.com/)。
2. 點選左下角 **管理 (Admin)**。
3. 在「資源 (Property)」欄位下點選 **資源存取權管理 (Property Access Management)**。
4. 點選右上角 **+** ➔ **新增使用者 (Add users)**。
5. 輸入 Email（個人帳號或 Service Account Email）。
6. 指派角色：
   * **檢視者 (Viewer)**：僅讀取報告。
   * **分析師 (Analyst)**：建立探索與自訂報表。

## 2. GCP 必要啟用 API
若使用 Service Account，請確認 Google Cloud 專案已啟用：
* `Google Analytics Data API` (v1beta)
* `Google Analytics Admin API` (v1alpha / v1beta)

## 3. 個人 OAuth (ADC) 授權方式
若不使用 Service Account，請於本機終端機執行：
```bash
gcloud auth application-default login
```
這將產生 Application Default Credentials (ADC)，`analytics-mcp` 會自動引用。
