import requests
from bs4 import BeautifulSoup
import re

# yahooのサイトから情報取得
URL = "https://www.yahoo.co.jp/"
response = requests.get(URL)
# レスポンスを成形
html = BeautifulSoup(response.content, 'html.parser')
# 見出しとURLの情報をhref属性かつnews.yahoo.co.jp/pickupが含まれる箇所」を全て抽出して出力する
data_list = html.find_all(href=re.compile("news.yahoo.co.jp/pickup"))


# ヤフーニュース見出のURL情報をループで取得し、リストで格納する。
headline_link_list = [data.attrs["href"] for data in data_list]

# ヤフーニュース見出のURLリストから記事URLを取得し、記事内容を取得する
for headline_link in headline_link_list:

    # ヤフーニュース見出のURLから、　要約ページの内容を取得する
    summary = requests.get(headline_link)

    # 取得した要約ページをBeautifulSoupで解析できるようにする
    summary_soup = BeautifulSoup(summary.text, "html.parser")

    # aタグの中に「続きを読む」が含まれているテキストを抽出する
    # ヤフーのページ構成は[Top] -> [要約] -> [本文] となっており、
    # [要約]から[本文]に遷移するには「続きを読む」をクリックする必要がある。
    summary_soup_a = summary_soup.select("a:-soup-contains('続きを読む')")[0]

    # aタグの中の"href="から先のテキストを抽出する。
    # するとヤフーの記事本文のURLを取得できる
    news_body_link = summary_soup_a.attrs["href"]

    # 記事本文のURLから記事本文のページ内容を取得する
    news_body = requests.get(news_body_link)
    # 取得した記事本文のページをBeautifulSoupで解析できるようにする
    news_soup = BeautifulSoup(news_body.text, "html.parser")

    # 記事本文のタイトルを表示する
    print(news_soup.title.text)

    # 記事本文のURLを表示する
    print(news_body_link)

    # class属性の中に「Direct」が含まれる行を抽出する
    detail_text = news_soup.find(class_=re.compile("Direct"))

    # 記事本文を出力する
    # hasattr:指定のオブジェクトが特定の属性を持っているかを確認する
    # detail_text.textの内容がNoneだった場合は、何も表示しないようにしている。
    print(detail_text.text if hasattr(detail_text, "text") else '', end="\n\n\n") #三項演算子