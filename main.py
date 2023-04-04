import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = "lsYbaVQ96eu3id+lBGEiByhYc9Pei8aRhflvb2sVwd6cVUAKG8OwQw8JDVm0CXF0cg9XQAT9t9gsoQuw9UTolgt6xxY6yIjrDMqELRwpwub5FUXJfxf06cFh3WGHJzCF8TCkdSO3L/FTU+6DRMv31AdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "4dd11fd4040c35df87cf1e0146f5e3e8"
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