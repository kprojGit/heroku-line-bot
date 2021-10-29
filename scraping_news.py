import requests
from bs4 import BeautifulSoup
import re

# yahooのサイトから情報取得
URL = "https://www.yahoo.co.jp/"
response = requests.get(URL)
# レスポンスを成形
html = BeautifulSoup(response.content, 'html.parser')
# a要素で抽出
for a in html.select('.topicsList .topicsListItem  a'):
# 出力処理
    print(a['href'], list(a.strings)[0])


# 見出しとURLの情報をhref属性かつnews.yahoo.co.jp/pickupが含まれる箇所」を全て抽出して出力する
data_list = html.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
News_summary = ''
for data in data_list:
    #print(data.span.string)
    #print(data.attrs["href"])
    News_summary = News_summary + data.span.string + '\n' + data.attrs["href"] + '\n'

print(News_summary)