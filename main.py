import os
import json
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn)

app = Flask(__name__)

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
with open(ABS_PATH+'/conf.json', 'r') as f:
    CONF_DATA = json.load(f)

#LINEへのアクセス情報を入力
LINE_CHANNEL_ACCESS_TOKEN = CONF_DATA["CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = CONF_DATA["CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

#ルーティングの設定、POSTリクエストが来たらcallback関数を返す
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーからアクセス情報の検証のための値を取得
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # アクセス情報を検証し、成功であればhandleの関数を呼び出す
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        #abort(400)
        print("署名検証で失敗してます" , YOUR_CHANNEL_ACCESS_TOKEN)
    return 'OK'

#メッセージを受け取った後にどんな処理を行うかを記述
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):


    if (event.reply_token == '00000000000000000000000000000000' or event.reply_token == 'ffffffffffffffffffffffffffffffff'):
        return

    elif line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)