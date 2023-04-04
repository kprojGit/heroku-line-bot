import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_BOT_CHANNEL_TOKEN")
YOUR_CHANNEL_SECRET = os.getenv("LINE_BOT_CHANNEL_SECRET")
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    except LineBotApiError as e:
        print("LineBotApiError:", e.status_code, e.error.message)
        abort(500)


if __name__ == "__main__":
    app.run()