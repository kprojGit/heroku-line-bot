
import os
from argparse import ArgumentParser
from logging.config import dictConfig
from flask import Flask, request, abort
from flask.logging import default_handler
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent,
    ImageMessage, ImageSendMessage, LocationMessage, AudioMessage,
    FlexSendMessage, StickerSendMessage
)

import wikipedia


from bs4 import BeautifulSoup #BeautifulSoupクラスをインポート
import urllib.request #urllib.requestモジュールをインポート
import time
import requests



import tenki   #同階層の天気スクレイピング用のファイルをインポート
import corona


# じゃんけん用
#import boto3
import logging
import random
import json
import janken



# 標準出力にログ出力することで、Herokuのログに出力する
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'consoleHandler': {
        'class': 'logging.StreamHandler',
        'level': 'INFO',
        'formatter': 'default',
        'stream': 'ext://sys.stdout'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['consoleHandler']
    }
})
app = Flask(__name__)
# 環境変数取得
# LINE Developersで設定されているチャネルアクセストークンとチャネルシークレットを設定
YOUR_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_BOT_CHANNEL_TOKEN")
YOUR_CHANNEL_SECRET = os.getenv("LINE_BOT_CHANNEL_SECRET")
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

wikipedia.set_lang("ja") 





@app.route("/callback", methods=['POST'])
def callback():
    """ Webhookからのリクエストの正当性をチェックし、ハンドラに応答処理を移譲する """
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']
    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    
    try:
        handler.handle(body, signature)
    # 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        app.logger.warn("Invalid Signature.署名検証で失敗してます")
        #abort(400)
        print("署名検証で失敗してます" , YOUR_CHANNEL_ACCESS_TOKEN)
    # handleの処理を終えればOK
    return 'OK'





@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    # text = event.message.address[:event.message.address.find('市' or '区')]
    tenki_id = 'yjw_pinpoint_today'
    text = event.message.address
    result = tenki.get_weather_from_location(text,tenki_id)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=result)
    )



#音声の場合→音声ファイルをそのまま再生
@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    #音声ファイルを保存する
    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)
    img = message_content.content

    P = "static/"+message_id+".m4a"
    #指定したパスが示すファイルが存在するかどうかを分岐
    mode = 'a' if os.path.exists(P) else 'wb'
    with open(P,mode) as f:
        f.write(img)
    
    FQDN = 'https://yama365.herokuapp.com'
    line_bot_api.reply_message(
        event.reply_token,
        AudioSendMessage(
            original_content_url = FQDN + '/static/' +message_id+".m4a"
        )
    )







@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    LINEへのテキストメッセージに対して応答を返す
    Parameters
    ----------
    event: MessageEvent
      LINEに送信されたメッセージイベント
    """


    messe = event.message.text

    if (event.reply_token == '00000000000000000000000000000000' or event.reply_token == 'ffffffffffffffffffffffffffffffff'):
        return

    elif messe == "test" or messe == "テスト":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="バッチリだよ！！"))
            

    # 天気用のスクリプト
    elif "今日" in messe and "天気" in messe:   #tenki.pyのgetw関数を呼び出す
        tenki_id = 'yjw_pinpoint_today'
        line_bot_api.reply_message(
        event.reply_token,
        [
        TextSendMessage(text='天気予報を知りたい場所を指定してください'),
        TextSendMessage(text='line://nv/location')
        ]
        )

    elif "明日" in messe and "天気" in messe:   #tenki.pyのtom_getw関数を呼び出す
        tenki_id = 'yjw_pinpoint_tomorrow'
        line_bot_api.reply_message(
        event.reply_token,
        [
        TextSendMessage(text='天気予報を知りたい場所を指定してください'),
        TextSendMessage(text='line://nv/location')
        ]
        )


    # コロナ用のスクリプト
    elif "コロナ" in messe:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=corona.get_num_infect()))


    # じゃんけん用のスクリプト
    elif "じゃんけん" in messe:
        with open('./janken.json') as f:
            saisyohaguu_message = json.load(f)
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text='最初はぐー', contents=saisyohaguu_message)
        )

    elif "ぐー" in messe or "ちょき" in messe or "ぱー" in messe:
        reply_messages = janken.janken_battle(messe)        
        line_bot_api.reply_message(event.reply_token,reply_messages)

    # 番組表の映画を抽出
    elif "映画" in messe or "番組表" in messe: 
        url = 'https://movie.jorudan.co.jp/cinema/broadcast/'
        response = urllib.request.urlopen(url) #flaskのrequestとは違うので注意
        soup = BeautifulSoup(response,'html.parser')
        response.close()
        #print(soup)
        # 得られたsoupオブジェクトを操作していく
        list_movie = list()
        for tag in soup.find_all('div', class_='title'):
            tag = str(tag) #引数に指定したオブジェクトを文字列にして取得
            if "/cinema/" in tag:
                movie_name = tag.split('"')
                #print(movie_name[5])
                list_movie.append(movie_name[5])

        list_day = list()
        for tag in soup.find_all('th'):
            tag = str(tag)
            day = tag.split('>')
            day = day[1].split('<')
            #print(day[0])
            list_day.append(day[0])

        list_time = list()
        for tag in soup.find_all('td', class_='tvdate'):
            tag = str(tag)
            time = tag.split()
            #print(time[2]+" "+time[3])
            list_time.append(time[2]+" "+time[3])

        i=0
        movieLIST = ""
        for tag in list_day:
            #print(tag+" "+list_movie[i]+"\n("+list_time[i]+")\n\n")
            movieLIST = movieLIST + tag+" "+list_movie[i]+"\n("+list_time[i]+")\n\n"
            i+=1
        #print(movieLIST)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(movieLIST))


    elif messe == "画像" or messe == "photo":
        FQDN = 'https://yama365.herokuapp.com'
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url = FQDN + '/static/' + 'test.jpg',
                preview_image_url = FQDN + '/static/' + 'test.jpg'
            )
        )
            


    elif " 検索" in  messe:
        return_message = messe[:messe.find(' 検索')]
        
        try:
                wikipedia_page = wikipedia.page(return_message)
                # wikipedia.page()の処理で、ページ情報が取得できれば、以下のようにタイトル、リンク、サマリーが取得できる。
                wikipedia_title = wikipedia_page.title
                wikipedia_url = wikipedia_page.url
                wikipedia_summary = wikipedia.summary(return_message)
                reply_message = '【' + wikipedia_title + '】\n' + wikipedia_summary + '\n\n' + '【詳しくはこちら】\n' + wikipedia_url
        # ページが見つからなかった場合
        except wikipedia.exceptions.PageError:
            reply_message = '【' + return_message + '】\nについての情報は見つかりませんでした。'
        # 曖昧さ回避にひっかかった場合
        except wikipedia.exceptions.DisambiguationError as e:
            disambiguation_list = e.options
            reply_message = '複数の候補が返ってきました。以下の候補から、お探しの用語に近いものを再入力してください。\n\n'
            for word in disambiguation_list:
                reply_message += '・' + word + '\n'
        #print(reply_message)
            
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(reply_message)
        )


   
    else: #"確認" または "チェック"以外のメッセージを入力した場合はオウム返し
        
        text1='検索したい場合→「検索したい語句＋検索」\n'
        text2='じゃんけん→「*じゃんけん*」\n'
        text3='コロナ感染者数→「*コロナ*」\n'
        text4='映画検索→「*映画* or *番組表*」\n'
        text5='監視カメラ写真→「*画像* or *photo*」\n'
        text6='天気予報→「今日+天気」\n'
        text7='を入力してください！'

        text = text1 + text2+ text3+ text4+ text5+ text6 + text7
        line_bot_api.reply_message(
            event.reply_token,
            [
            TextSendMessage(text)
            ]
            )






if __name__ == "__main__":
    # app.run()
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    # Herokuは環境変数PORTのポートで起動したWeb Appの起動を待ち受けるため、そのポート番号でApp起動する
    arg_parser.add_argument('-p', '--port', type=int,
                            default=int(os.getenv('PORT', 5000)), help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    arg_parser.add_argument('--host', default='0.0.0.0', help='host')
    options = arg_parser.parse_args()
    app.run(debug=options.debug, host=options.host, port=options.port)