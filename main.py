from newsCrawler import myNewsCrawler
import sys
import nltk
import base 



# 下載 'punkt' 資料集 for natural language processing
# nltk.download('punkt_tab')
# 用戶輸入 (多個topic會導致後面的無法出現)
selected_topics = input("which topic u like(separated by spaces)\n(0: us, 1: world, 2: politics, 3: business, 4: health, 5: environment, 6: weather): ").split()
valid_topics = [base.topic_dict[int(num)] for num in selected_topics if num.isdigit() and int(num) in base.topic_dict]

word = input("what keyword you would like to search for:  ")  # 設定預設值
articles_num = int(input("how many numbers of news do you want do search:  "))
print("processing...")

companies = {
    # "foxnews": {"link": "http://www.foxnews.com/"}, 
    "cnn": {"link": "https://edition.cnn.com/"}
}

def main():
    global word  # 使用 global 關鍵字來使用外部定義的 word 變數
    
    # 增加靈活性
    if len(sys.argv) == 2: # 2 : 一個參數一個檔名
        word = sys.argv[1]
    
    # 創建 myNewsCrawler 類的實例
    base_file_path = "newspaper_crawler/"
    s = myNewsCrawler(companies, base_file_path, valid_topics)
    
    # 使用 downloadHtml_in_batches 來分批抓取文章
    s.downloadHtml_in_batches(articles_num)
    
    # 使用 findWord 方法來查找關鍵字
    s.findWord_with_summary(word)

if __name__ == "__main__":
    main()





# from newsCrawler import myNewsCrawler
# import sys


# word = "Trump"  # 設定預設值
# newsPapers = {
#     # "foxnews": {"link": "http://www.foxnews.com/"}, 
#     "cnn": {"link": "https://edition.cnn.com"}
# }

# def main():
#     global word  # 使用 global 關鍵字來使用外部定義的 word 變數
#     if len(sys.argv) == 2:
#         word = sys.argv[1]
#     s = myNewsCrawler(newsPapers)
#     s.downloadHtml()
#     s.findWord(word)


# if __name__ == "__main__":
#     main()