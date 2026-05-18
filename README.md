# AI-Powered News Crawler & Summarizer

這是一個基於 Python 開發的自動化新聞爬蟲系統，能夠從主流新聞媒體（如 CNN）抓取指定主題的新聞，並結合 NLP (自然語言處理) 模型自動生成新聞摘要，最後將結果匯出為結構化報表 。
網站 → 爬取連結 → 下載HTML → 清理內容 → 保存JSON → 搜索關鍵字 → AI生成摘要 → 轉Excel
## 核心功能

* **多主題篩選**：支援美國 (us)、國際 (world)、政治 (politics)、商業 (business)、健康 (health)、環境 (environment) 與天氣 (weather) 等 7 種新聞分類 
* **關鍵字檢索**：用戶可自定義搜尋關鍵字，系統會自動在大量新聞內文中進行精準比對 
* **AI 自動摘要**：整合 Hugging Face 的 facebook/bart-large-cnn 模型，針對長篇新聞自動產出 30-60 字的精簡摘要 
* **分批抓取機制**：實作分批抓取函式，將新聞分為多個批次進行下載與儲存，優化記憶體使用並避免程序中斷 
* **自動化報表**：系統會自動將符合關鍵字的新聞標題、AI 摘要及原文連結儲存為 Excel 檔案 

## 技術棧

* **新聞抓取**：newspaper3k (解析新聞結構)、requests 
* **自然語言處理**：transformers (BART 模型)、nltk 
* **資料處理**：pandas (Excel 匯出)、json 
* **環境部署**：使用 Replit 作為 IDE，並透過 GitHub 與 Render 進行版本控制與部署

## 運作流程

1.  **使用者輸入**：選擇新聞主題、關鍵字與欲抓取的數量 
2.  **連結過濾**：根據 valid_topics 篩選並隨機打亂新聞來源網址，確保抓取多樣性 
3.  **分批下載**：下載 HTML 原始碼並進行清理，提取標題與內文 
4.  **關鍵字比對與摘要**：在內文中尋找關鍵字，若命中則觸發 AI 摘要生成
5.  **結果儲存**：產出 JSON 備份檔與最終的 Excel 分析報告 

## 快速開始

```bash
# 安裝相關模組 (如 newspaper3k, transformers, pandas, openpyxl)
pip install newspaper3k transformers pandas openpyxl

# 執行程式
python main.py
```
📋 所有使用的第三方套件
套件	            用途
newspaper3k	   	爬取文章連結、下載HTML、清理內容
requests	    	HTTP請求（newspaper內部使用）
transformers	 	AI模型管道
pandas	        數據處理、轉DataFrame
openpyxl	    	Excel寫入引擎


📥 詳細的數據流向圖
CNN網站
    ↓
newspaper.build() [爬取所有連結]
    ↓
article.download() & parse() [下載每篇HTML]
    ↓
cleanHtml() [去除標籤，提取標題+文本]
    ↓
json.dump() [保存成 newsPaperData_batch_X.json]
    ↓
json.load() [讀取JSON]
    ↓
.find(keyword) [搜尋關鍵字]
    ↓
summarizer(text) [用BART AI生成摘要]
    ↓
pd.DataFrame() [組織成表格格式]
    ↓
df.to_excel() [寫入 articles.xlsx]


🎯 關鍵要點
爬蟲：newspaper 套件負責幾乎所有爬蟲工作（連結、下載、清理）
數據儲存：JSON作為中間格式，便於保存和後續處理
AI摘要：首次運行會下載 ~1.6GB 的BART模型到本機快取
Excel輸出：pandas + openpyxl 無縫轉換，生成可讀的Excel報告
