

import os
import json
import random
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, FlexSendMessage, StickerSendMessage


# LINE Developersで設定されているチャネルアクセストークンとチャネルシークレットを設定
YOUR_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_BOT_CHANNEL_TOKEN")
YOUR_CHANNEL_SECRET = os.getenv("LINE_BOT_CHANNEL_SECRET")
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)




def janken_battle(messe):

    with open('./janken.json') as f:
            saisyohaguu_message = json.load(f)
    
    request_message = messe
    bot_answer = random.choice(['ぐー', 'ちょき', 'ぱー'])

    reply_messages = []
    win_reply_message = [TextSendMessage(text='私の勝ちです')]
    win_reply_message.append(StickerSendMessage(package_id='1', sticker_id=random.choice(['106', '407', '125', '100', '110'])))
    win_reply_message.append(FlexSendMessage(alt_text='最初はぐー', contents=saisyohaguu_message))
    lose_reply_message = [TextSendMessage(text='私の負けです')]
    lose_reply_message.append(StickerSendMessage(package_id='2', sticker_id=random.choice(['152', '18', '25', '173', '524'])))
    lose_reply_message.append(FlexSendMessage(alt_text='最初はぐー', contents=saisyohaguu_message))
    draw_reply_message = [FlexSendMessage(alt_text='あいこで', contents=saisyohaguu_message)]
    if request_message == 'ぐー':
        reply_messages.append(TextSendMessage(text=bot_answer))
        if bot_answer == 'ぐー':
            reply_messages.extend(draw_reply_message)
        elif bot_answer == 'ちょき':
            reply_messages.extend(lose_reply_message)
        elif bot_answer == 'ぱー':
            reply_messages.extend(win_reply_message)
    elif request_message == 'ちょき':
        reply_messages.append(TextSendMessage(text=bot_answer))
        if bot_answer == 'ぐー':
            reply_messages.extend(win_reply_message)
        elif bot_answer == 'ちょき':
            reply_messages.extend(draw_reply_message)
        elif bot_answer == 'ぱー':
            reply_messages.extend(lose_reply_message)
    elif request_message == 'ぱー':
        reply_messages.append(TextSendMessage(text=bot_answer))
        if bot_answer == 'ぐー':
            reply_messages.extend(lose_reply_message)
        elif bot_answer == 'ちょき':
            reply_messages.extend(win_reply_message)
        elif bot_answer == 'ぱー':
            reply_messages.extend(draw_reply_message)
    else:
        reply_messages.append(FlexSendMessage(alt_text='最初はぐー', contents=saisyohaguu_message))
    
    return reply_messages