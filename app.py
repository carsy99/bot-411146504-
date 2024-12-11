# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('AqdPI25N8m7KW2ZuA7pECAmvcjCmmVZ6ezWGEm1Ev8k0fYB5RWZ5AuNPyaH+KxxMv7l9OQ78l+7KOzuLg3ff72t7go6w7N4UOJAIDF3zA0c6he23xXOrFlmq8yw/gg+DlQ5F6JqcYejCSFRz/v7FVwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('369ea26c223ee20d7176222640fbbbbb')

line_bot_api.push_message('U2ab8673f9943f92c39b32e016a81e934', TextSendMessage(text='你可以開始了'))

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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('推薦餐廳',message):
        imagemap_message = ImagemapSendMessage(
            base_url='https://i.imgur.com/AjSt5jd.jpeg',
            alt_text='組圖訊息',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='https://www.facebook.com/2017Ninja.Sushi/',#日料左上
                    area=ImagemapArea(
                        x=0, y=0, width=700, height=700
                    )
                ),
                URIImagemapAction(
                    link_uri='http://www.facebook.com/PUROtaverna',#西式右上
                    area=ImagemapArea(
                        x=700, y=0, width=700, height=700
                    )
                ),
                URIImagemapAction(
                    link_uri='https://www.facebook.com/yangsbeefnoodle/',#中式左下
                    area=ImagemapArea(
                        x=0, y=700, width=700, height=700
                    )
                ),
                URIImagemapAction(
                    link_uri='https://www.windsortaiwan.com/tw/food/2C25b1caC2E19A4c',#法式右下
                    area=ImagemapArea(
                        x=700, y=700, width=700, height=700
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)
    
    # 推薦景點功能
    elif re.match('推薦景點', message):
        carousel_template_message = TemplateSendMessage( 
            alt_text='熱門旅行景點',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/kNBl363.jpg',
                        title='台北101',
                        text='台灣最高的摩天大樓。',
                        actions=[
                            URIAction(
                                label='查看詳細資訊',
                                uri='https://zh.wikipedia.org/wiki/%E5%8F%B0%E5%8C%97%E5%8D%81%E4%B8%80'
                            ),
                            URIAction(
                                label='導航至此',
                                uri='https://www.google.com/maps?q=台北101'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/GBPcUEP.png',
                        title='金閣寺',
                        text='京都著名的世界遺產。',
                        actions=[
                            URIAction(
                                label='查看詳細資訊',
                                uri='https://zh.wikipedia.org/wiki/%E9%87%91%E9%96%A3%E5%AF%BA'
                            ),
                            URIAction(
                                label='導航至此',
                                uri='https://www.google.com/maps?q=金閣寺'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/kRW5zTO.png',
                        title='首爾塔',
                        text='首爾的標誌性建築物。',
                        actions=[
                            URIAction(
                                label='查看詳細資訊',
                                uri='https://zh.wikipedia.org/wiki/%E5%8C%97%E9%87%91%E5%B1%B1%E5%AF%BA'
                            ),
                            URIAction(
                                label='導航至此',
                                uri='https://www.google.com/maps?q=首爾塔'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
        
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
