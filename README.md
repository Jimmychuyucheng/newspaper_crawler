# AI-Powered News Crawler & Summarizer

[cite_start]這是一個基於 Python 開發的自動化新聞爬蟲系統，能夠從主流新聞媒體（如 CNN）抓取指定主題的新聞，並結合 NLP (自然語言處理) 模型自動生成新聞摘要，最後將結果匯出為結構化報表 [cite: 82, 85, 93, 94]。

## 核心功能

* [cite_start]**多主題篩選**：支援美國 (us)、國際 (world)、政治 (politics)、商業 (business)、健康 (health)、環境 (environment) 與天氣 (weather) 等 7 種新聞分類 [cite: 5, 10, 11]。
* [cite_start]**關鍵字檢索**：用戶可自定義搜尋關鍵字，系統會自動在大量新聞內文中進行精準比對 [cite: 13, 31, 35, 41]。
* [cite_start]**AI 自動摘要**：整合 Hugging Face 的 facebook/bart-large-cnn 模型，針對長篇新聞自動產出 30-60 字的精簡摘要 [cite: 5, 60, 61]。
* [cite_start]**分批抓取機制**：實作分批抓取函式，將新聞分為多個批次進行下載與儲存，優化記憶體使用並避免程序中斷 [cite: 17, 26, 28, 29]。
* [cite_start]**自動化報表**：系統會自動將符合關鍵字的新聞標題、AI 摘要及原文連結儲存為 Excel 檔案 [cite: 66, 73, 76]。

## 技術棧

* [cite_start]**新聞抓取**：newspaper3k (解析新聞結構)、requests [cite: 5, 12, 40]。
* [cite_start]**自然語言處理**：transformers (BART 模型)、nltk [cite: 2, 5, 60]。
* [cite_start]**資料處理**：pandas (Excel 匯出)、json [cite: 5, 30, 74]。
* [cite_start]**環境部署**：使用 Replit 作為 IDE，並透過 GitHub 與 Render 進行版本控制與部署 [cite: 87, 94]。

## 運作流程

1.  [cite_start]**使用者輸入**：選擇新聞主題、關鍵字與欲抓取的數量 [cite: 10, 13, 14]。
2.  [cite_start]**連結過濾**：根據 valid_topics 篩選並隨機打亂新聞來源網址，確保抓取多樣性 [cite: 11, 86, 88]。
3.  [cite_start]**分批下載**：下載 HTML 原始碼並進行清理，提取標題與內文 [cite: 26, 30, 31, 56]。
4.  [cite_start]**關鍵字比對與摘要**：在內文中尋找關鍵字，若命中則觸發 AI 摘要生成 [cite: 35, 41, 58, 61]。
5.  [cite_start]**結果儲存**：產出 JSON 備份檔與最終的 Excel 分析報告 [cite: 30, 66, 76]。

## 快速開始

```bash
# 安裝相關模組 (如 newspaper3k, transformers, pandas, openpyxl)
pip install newspaper3k transformers pandas openpyxl

# 執行程式
python main.py
