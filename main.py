
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
    ImageMessage, ImageSendMessage
)

import wikipedia



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


    elif messe == "画像" or messe == "写真":
        line_bot_api.reply_message(
　　        event.reply_token,
　　        ImageSendMessage(
　　        original_content_url=’https://1.bp.blogspot.com/-eaDZ7sDP9uY/Xhwqlve5SUI/AAAAAAABXBo/EcI2C2vim7w2WV6EYy3ap0QLirX7RPohgCNcBGAsYHQ/s400/pose_syanikamaeru_man.png’,
　　        preview_image_url=’https://1.bp.blogspot.com/-eaDZ7sDP9uY/Xhwqlve5SUI/AAAAAAABXBo/EcI2C2vim7w2WV6EYy3ap0QLirX7RPohgCNcBGAsYHQ/s400/pose_syanikamaeru_man.png’))

   
    else: #"確認" または "チェック"以外のメッセージを入力した場合はオウム返し
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="不明な言葉です→" + event.message.text))







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