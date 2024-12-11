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
    message = event.message.text.strip()  # 去掉多餘空格

    # 推薦餐廳功能
    if message == "推薦餐廳":
        imagemap_message = ImagemapSendMessage(
            base_url='https://i.imgur.com/AjSt5jd.jpeg',
            alt_text='組圖訊息',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                URIImagemapAction(
                    link_uri='https://www.facebook.com/2017Ninja.Sushi/',  # 日料左上
                    area=ImagemapArea(x=0, y=0, width=700, height=700)
                ),
                URIImagemapAction(
                    link_uri='http://www.facebook.com/PUROtaverna',  # 西式右上
                    area=ImagemapArea(x=700, y=0, width=700, height=700)
                ),
                URIImagemapAction(
                    link_uri='https://www.facebook.com/yangsbeefnoodle/',  # 中式左下
                    area=ImagemapArea(x=0, y=700, width=700, height=700)
                ),
                URIImagemapAction(
                    link_uri='https://www.windsortaiwan.com/tw/food/2C25b1caC2E19A4c',  # 法式右下
                    area=ImagemapArea(x=700, y=700, width=700, height=700)
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)

    # 推薦景點功能
    elif message == "推薦景點":
        try:
            carousel_template_message = TemplateSendMessage(
                alt_text='熱門旅行景點',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url='https://i.imgur.com/kNBl363.jpg',  # 確保 URL 可用
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
                            thumbnail_image_url='https://i.imgur.com/GBPcUEP.png',  # 確保 URL 可用
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
                            thumbnail_image_url='https://i.imgur.com/kRW5zTO.png',  # 確保 URL 可用
                            title='首爾塔',
                            text='首爾的標誌性建築物。',
                            actions=[
                                URIAction(
                                    label='查看詳細資訊',
                                    uri='https://zh.wikipedia.org/wiki/%E9%87%91%E9%96%A3%E5%AF%BA'
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
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"推薦景點功能發生錯誤：{str(e)}"))

    # 我要訂餐功能
    elif message == "我要訂餐":
        try:
            confirm_template = TemplateSendMessage(
                alt_text='訂餐確認',
                template=ConfirmTemplate(
                    text='無敵好吃牛肉麵 * 1 ，總價NT200',
                    actions=[
                        MessageAction(
                            label='確定',
                            text='訂單已確認，謝謝您的購買！'
                        ),
                        MessageAction(
                            label='取消',
                            text='已取消訂單，謝謝您的光臨！'
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, confirm_template)
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"訂餐功能發生錯誤：{str(e)}"))

    # 我想吃飯功能
    elif message == "我想吃飯":
        try:
            quick_reply_buttons = TextSendMessage(
                text='請選擇您想加入購物車的品項：',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="主菜", text="您已成功將【主菜】加入購物車")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="湯品", text="您已成功將【湯品】加入購物車")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="飲料", text="您已成功將【飲料】加入購物車")
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, quick_reply_buttons)
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"功能發生錯誤：{str(e)}"))

    # 電影推薦功能
    elif message == "電影推薦":
        try:
            image_carousel_template = TemplateSendMessage(
                alt_text='電影推薦',
                template=ImageCarouselTemplate(
                    columns=[
                        ImageCarouselColumn(
                            image_url='https://upload.wikimedia.org/wikipedia/zh/a/af/Shawshank_Redemption_ver2.jpg',  # 確保 URL 可用
                            action=URIAction(
                                label='查看詳細資訊',
                                uri='https://www.imdb.com/title/tt0111161/'  # 例如《肖申克的救贖》
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://pic.pimg.tw/tony871204/1587345864-1851924135_wn.jpg',  # 確保 URL 可用
                            action=URIAction(
                                label='查看詳細資訊',
                                uri='https://www.imdb.com/title/tt0068646/'  # 例如《教父》
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://upload.wikimedia.org/wikipedia/zh/7/7f/Inception_ver3.jpg',  # 確保 URL 可用
                            action=URIAction(
                                label='查看詳細資訊',
                                uri='https://www.imdb.com/title/tt1375666/'  # 例如《全面啟動》
                            )
                        ),
                        ImageCarouselColumn(
                            image_url='https://upload.wikimedia.org/wikipedia/zh/a/ad/Forrestgumppost.jpg',  # 確保 URL 可用
                            action=URIAction(
                                label='查看詳細資訊',
                                uri='https://www.imdb.com/title/tt0109830/'  # 例如《阿甘正傳》
                            )
                        )
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, image_carousel_template)
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"電影推薦功能發生錯誤：{str(e)}"))
    # 餐廳菜單推薦系統
    elif message == "查看菜單":
        try:
            flex_message = FlexSendMessage(
                alt_text="餐廳菜單",
                contents={
                    "type": "carousel",
                    "contents": [
                        {
                            "type": "bubble",
                            "hero": {
                                "type": "image",
                                "url": "https://i.imgur.com/abc123.jpg",
                                "size": "full",
                                "aspectRatio": "20:13",
                                "aspectMode": "cover"
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "招牌牛排",
                                        "weight": "bold",
                                        "size": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": "嫩滑多汁的高品質牛排，搭配特製醬汁",
                                        "size": "sm",
                                        "wrap": True
                                    },
                                    {
                                        "type": "text",
                                        "text": "價格: NT$500",
                                        "size": "sm",
                                        "color": "#555555"
                                    }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "button",
                                        "style": "primary",
                                        "action": {
                                            "type": "message",
                                            "label": "訂購",
                                            "text": "已加入購物車: 招牌牛排"
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "type": "bubble",
                            "hero": {
                                "type": "image",
                                "url": "https://i.imgur.com/xyz456.jpg",
                                "size": "full",
                                "aspectRatio": "20:13",
                                "aspectMode": "cover"
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "海鮮燉飯",
                                        "weight": "bold",
                                        "size": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": "新鮮海鮮與濃郁米飯的絕妙搭配",
                                        "size": "sm",
                                        "wrap": True
                                    },
                                    {
                                        "type": "text",
                                        "text": "價格: NT$350",
                                        "size": "sm",
                                        "color": "#555555"
                                    }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "button",
                                        "style": "primary",
                                        "action": {
                                            "type": "message",
                                            "label": "訂購",
                                            "text": "已加入購物車: 海鮮燉飯"
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "type": "bubble",
                            "hero": {
                                "type": "image",
                                "url": "https://i.imgur.com/lmn789.jpg",
                                "size": "full",
                                "aspectRatio": "20:13",
                                "aspectMode": "cover"
                            },
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "巧克力熔岩蛋糕",
                                        "weight": "bold",
                                        "size": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": "濃郁巧克力與香甜內餡的完美融合",
                                        "size": "sm",
                                        "wrap": True
                                    },
                                    {
                                        "type": "text",
                                        "text": "價格: NT$150",
                                        "size": "sm",
                                        "color": "#555555"
                                    }
                                ]
                            },
                            "footer": {
                                "type": "box",
                                "layout": "vertical",
                                "spacing": "sm",
                                "contents": [
                                    {
                                        "type": "button",
                                        "style": "primary",
                                        "action": {
                                            "type": "message",
                                            "label": "訂購",
                                            "text": "已加入購物車: 巧克力熔岩蛋糕"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            )
            line_bot_api.reply_message(event.reply_token, flex_message)
        except Exception as e:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"菜單推薦功能發生錯誤：{str(e)}"))
    
    # 未知指令處理
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="無法識別的指令"))
        
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
