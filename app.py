from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from wordToVector import findAnswer

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Vm69XP4keizpf1bwUB4VnEGcOhFqByjj0KgIIThu/QKPMc5QKKPL+qy24Y8/mkfMnBP+sn/rqaImNtIdiJtsO4DAu4YaCkzlrMLqPpYtuLR+c0jTR0wC8i7aOlnPlI/Sj9K9BdEcqqJosRbkrXipmQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('f9ffb74813ee757858c2fac1bce86e52')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text=event.message.text
    if (text=="哈囉"):
        reply_text = "你好呀～我叫做蒸汽雞，關於Steam的問題都可以問我喔！"
    elif (text=="謝謝"):
        reply_text = "不客氣，很高興為你服務<3"
    elif (text=="蒸汽雞"):
        reply_text = "來啦來啦～你在呼喚我嗎？"
    else:
        #reply_text = text
        reply_text=findAnswer(text)
    message = TextSendMessage(reply_text)
    line_bot_api.reply_message(event.reply_token, message)

    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
