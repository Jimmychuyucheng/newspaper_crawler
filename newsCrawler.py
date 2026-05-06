'''
1. 取得連結(newspaper)並篩選  (會根據valid topic篩選)
2. 下載連結網址html
3. 清理html
4. 找尋關鍵字並儲存摘要

5. 用ai統整新聞 (optional) -> transformers pipline, model: facebook/bart-large-cnn
'''
from transformers import pipeline
import newspaper 
import requests
import json
import pandas as pd

class myNewsCrawler():
    data = {}

    def __init__(self, companies,base_file_path, valid_topics):
        self.valid_topics = valid_topics
        self.base_file_path = base_file_path
        self.companies = companies
        self.newsPaper = {}
        self.data['newspapers'] = {}
        self.limit = 80   # 設置抓取的最大數量

    def downloadHtml_in_batches(self, articles_num):    
        for company, value in self.companies.items():
            articleList = []
            
            if company == "cnn":
                articleList = self.get_cnn_url(value["link"])
            elif company == "foxnews":
                articleList = self.get_fox_url(value["link"])

            limit_num = min(self.limit, articles_num) 
            
            # 限制抓取的數量
            print(f"catch {len(articleList)} news\n")
            if len(articleList) > limit_num:
                articleList = articleList[:limit_num]

            total_articles = len(articleList)
            batch_size = total_articles // 2

            print(f"Total articles: {total_articles}, Batch size: {batch_size}")
            print("-----------------------------------------------------------")

            # 抓取第一批文章
            self.download_and_save_articles(company, articleList[:batch_size], 1)
            # 抓取第二批文章
            self.download_and_save_articles(company, articleList[batch_size:], 2)

    def download_and_save_articles(self, company, articleList, batch_number):
        count = 1
        newsPaper = {"articles": []}

        for content_url in articleList: 
            if count > self.limit:
                break

            content = newspaper.Article(content_url)
            article = {"link": content.url}
            try:
                content.download()
                content.parse()

                if not content.title or not content.text:
                    print(f"Skipping article with no content: {content.url}")
                    continue

                print(f"{count} download articles from {company} url: {content.url}")
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    print(f"Failed to download article (404 Not Found): {content.url}")
                else:
                    print(f"Failed to download article: {e}")
                continue
            except Exception as e:
                print(f"Failed to download article: {e}")
                continue

            article.update(self.cleanHtml(content.html))
            count += 1 
            newsPaper['articles'].append(article)

        self.data['newspapers'][f"{company}_batch_{batch_number}"] = newsPaper

        with open(f"{self.base_file_path}newsPaperData_batch_{batch_number}.json", "w", encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)  
        
        print(f"Batch {batch_number} saved to newsPaperData_batch_{batch_number}.json")
        print("----------------------------------------------------------------------")

    def cleanHtml(self, html):
        article = newspaper.Article(url='')
        article.set_html(html)
        article.parse()

        articleJ = {}
        articleJ['title'] = article.title
        articleJ['text'] = article.text
        return articleJ

    # findWord 函式加上摘要功能
    def findWord_with_summary(self, word):
        find = 0
        articles_to_save = []  # 用于儲存符合條件的文章

        
        try:
            with open(self.base_file_path + f"newsPaperData_batch_2.json", "r", encoding='utf-8') as f:
                newsArticles = json.load(f)
        except FileNotFoundError:
            print(f"File newsPaperData_batch_2.json not found.")
            

        # 確保 'newspapers' 鍵存在
        if "newspapers" not in newsArticles:
            print(f"'newspapers' key not found in batch 2")
            

        
        #  簡化整個json的dictionary 提取最終的元素
        newsArticles = newsArticles["newspapers"]

        for source, source_data in newsArticles.items():
            for article_data in source_data["articles"]:
                if "title" not in article_data or "link" not in article_data:
                    print(f"Article missing 'title' or 'link': {article_data}")
                    continue
                
                # findInTitle = article_data["title"].find(word)
                
                
                findInText = article_data.get("text", "").find(word)
                
                
                if findInText != -1:
                    find += 1
                    print(f'{find}, found "{word}" in {source}, url: {article_data["link"]}')

                    # 初始化新聞文章物件
                    article = newspaper.Article(article_data['link'])
                    article.download()
                    article.parse()

                    # 只保存内容的前 1000 个字符
                    text_content = article.text[:1000] + " ...(tap the link to see more)"  # 修正索引方式

                    

                    # 使用 NLP 生成摘要
                    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", min_length=30, max_length=60, device=0)
                    summary = summarizer(text_content)[0]['summary_text']
                
                    
                    # 儲存符合條件的文章
                    articles_to_save.append({
                        "Title": article_data["title"],
                        # "Text": text_content,
                        "Summary": summary,  # 儲存摘要
                        "Link": article_data["link"]
                        
                    })

        # 檢查是否有符合條件的文章
        if articles_to_save:
            df = pd.DataFrame(articles_to_save)
            df.to_excel(self.base_file_path + "articles.xlsx", index=False, engine="openpyxl")
            print("符合條件的文章已保存到 articles.xlsx")
        else:
            print("No matching articles found. File failed to save.")
        

    

    def cleanHtml(self, html):
        article = newspaper.Article(url='')
        article.set_html(html)
        article.parse()

        articleJ = {}
        articleJ['title'] = article.title
        articleJ['text'] = article.text
        return articleJ

    

    def get_cnn_url(self, url):
        paper = newspaper.build(url, memoize_articles=False)
        cnn_urls = [article.url for article in paper.articles if any(topic in article.url for topic in self.valid_topics)]
        
        #打亂順序 避免後面輸入到的主題輪不到
        import random
        random.shuffle(cnn_urls)
        
        return cnn_urls

    
    def get_fox_url(self, url):
        paper = newspaper.build(url, memoize_articles=False)
        fox_urls = [article.url for article in paper.articles]
        return fox_urls
