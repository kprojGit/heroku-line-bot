


def janken_battle(messe):


    request_message = messe
    bot_answer = random.choice(['ぐー', 'ちょき', 'ぱー'])

    reply_messages = []
    win_reply_message = [TextSendMessage(text='私の勝ちです')]
    win_reply_message.append(StickerSendMessage(package_id='1', sticker_id=random.choice(['106', '407', '125', '100', '110'])))
    win_reply_message.append(FlexSendMessage(alt_text='最初はぐー', contents=saisyohaguu_message))
    lose_reply_message = [TextSendMessage(text='私の負けです')]
    lose_reply_message.append(StickerSendMessage(package_id='2', sticker_id=random.choice(['152', '18', '25', '173', '524'])))
    lose_reply_message.append(FlexSendMessage(alt_text='最初はぐー', contents=saisyohaguu_message))
    draw_reply_message = [FlexSendMessage(alt_text='あいこで', contents=aikode_message)]
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