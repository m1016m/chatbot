import requests
import re
import random
import configparser
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('Iv0pLZ9KfdUAP9sbqHFTW1DIje5deJPHOpD1WIzFNXLpiPYD/c+pIAOFmj/RMQ7w55EKviMuQ4Nn5xCdzOQSKRtZl8i4PhWCBx2wdict1OETx3HZkV29/+jzBm5lbiOEnNg6fMMkQFasTuRv30veVQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('5bf6d4b3d34b5b7a331ada40e4b25435')

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
def apple_news():
    target_url = 'https://tw.appledaily.com/new/realtime'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for index, data in enumerate(soup.select('.rtddt a'), 0):
        if index == 5:
            return content
        link = data['href']
        content += '{}\n\n'.format(link)
    return content
def technews():
    target_url = 'https://technews.tw/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('article div h1.entry-title a')):
        if index == 12:
            return content
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content
def oil_price():
    target_url = 'https://gas.goodlife.tw/'
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.select('#main')[0].text.replace('\n', '').split('(')[0]
    gas_price = soup.select('#gas-price')[0].text.replace('\n\n\n', '').replace(' ', '')
    cpc = soup.select('#cpc')[0].text.replace(' ', '')
    content = '{}\n{}{}'.format(title, gas_price, cpc)
    return content
def ptt_hot():
    target_url = 'http://disp.cc/b/PttHot'
    print('Start parsing pttHot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('#list div.row2 div span.listTitle'):
        title = data.text
        link = "http://disp.cc/b/" + data.find('a')['href']
        if data.find('a')['href'] == "796-59l9":
            break
        content += '{}\n{}\n\n'.format(title, link)
    return content

def technews():
    target_url = 'https://technews.tw/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('article div h1.entry-title a')):
        if index == 12:
            return content
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content


def panx():
    target_url = 'https://panx.asia/'
    print('Start parsing ptt hot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('div.container div.row div.desc_wrap h2 a'):
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # message = TextSendMessage(text=event.message.text)
    # line_bot_api.reply_message(event.reply_token, message)
    # message = StickerSendMessage(
    # package_id='1',
    # sticker_id='1')
    # line_bot_api.reply_message(event.reply_token, message)
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    if event.message.text == "油價查詢":
        content = oil_price()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if event.message.text == "蘋果即時新聞":
        content = apple_news()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if event.message.text == "近期熱門廢文":
        content = ptt_hot()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    
    if event.message.text == "觸電網-youtube":
        target_url = 'https://www.youtube.com/user/truemovie1/videos'
        rs = requests.session()
        res = rs.get(target_url, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        seqs = ['https://www.youtube.com{}'.format(data.find('a')['href']) for data in soup.select('.yt-lockup-title')]
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=seqs[random.randint(0, len(seqs) - 1)]),
                TextSendMessage(text=seqs[random.randint(0, len(seqs) - 1)])
            ])
        return 0
    if event.message.text == "科技新報":
        content = technews()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "PanX泛科技":
        content = panx()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "開始玩":
        buttons_template = TemplateSendMessage(
            alt_text='開始玩 template',
            template=ButtonsTemplate(
                title='選擇服務',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/xQF5dZT.jpg',
                actions=[
                    MessageTemplateAction(
                        label='新聞',
                        text='新聞'
                    ),
                    MessageTemplateAction(
                        label='電影',
                        text='電影'
                    ),
                    MessageTemplateAction(
                        label='看廢文',
                        text='看廢文'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "電影":
        buttons_template = TemplateSendMessage(
            alt_text='電影 template',
            template=ButtonsTemplate(
                title='服務類型',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/sbOTJt4.png',
                actions=[
                    MessageTemplateAction(
                        label='觸電網-youtube',
                        text='觸電網-youtube'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "看廢文":
        buttons_template = TemplateSendMessage(
            alt_text='看廢文 template',
            template=ButtonsTemplate(
                title='你媽知道你在看廢文嗎',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/ocmxAdS.jpg',
                actions=[
                    MessageTemplateAction(
                        label='近期熱門廢文',
                        text='近期熱門廢文'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "新聞":
        buttons_template = TemplateSendMessage(
            alt_text='新聞 template',
            template=ButtonsTemplate(
                title='新聞類型',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/vkqbLnz.png',
                actions=[
                    MessageTemplateAction(
                        label='蘋果即時新聞',
                        text='蘋果即時新聞'
                    ),
                    MessageTemplateAction(
                        label='科技新報',
                        text='科技新報'
                    ),
                    MessageTemplateAction(
                        label='PanX泛科技',
                        text='PanX泛科技'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    message = TemplateSendMessage(
    alt_text='目錄 template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/PN23ONG.png',
                    title='選擇服務',
                    text='請選擇',
                    actions=[
                        MessageAction(
                            label='開始玩',
                            text='開始玩'
                        ),
                        URIAction(
                            label='韓團 SISTAR',
                            uri='https://www.youtube.com/watch?v=E0ZHXVp_wUE'
                        ),
                        URIAction(
                            label='粉絲團',
                            uri='https://www.facebook.com/mengno.1/'
                        )
                    ]
                ),
            CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/DrsmtKS.jpg',
                    title='選擇服務',
                    text='請選擇',
                    actions=[
                        MessageAction(
                            label='other bot',
                            text='imgur bot'
                        ),
                        MessageAction(
                            label='油價查詢',
                            text='油價查詢'
                        ),
                        URIAction(
                            label='聯絡作者',
                            uri='https://www.facebook.com/TWTRubiks?ref=bookmarks'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/h4UzRit.jpg',
                    title='選擇服務',
                    text='請選擇',
                    actions=[
                        URIAction(
                            label='分享 bot',
                            uri='https://line.me/R/nv/recommendOA/@vbi2716y'
                        ),
                        URIAction(
                            label='PTT正妹網',
                            uri='https://ptt-beauty-infinite-scroll.herokuapp.com/'
                        ),
                        URIAction(
                            label='youtube 程式教學分享頻道',
                            uri='https://www.youtube.com/channel/UCPhn2rCqhu0HdktsFjixahA'
                        )
                    ]
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



# 訊息物件中的Imagemap, template messages，可以供使用者點擊互動的介面，會產生一個Action，這些Actions可以分為
# 以下四種：
# (1) Postback：點擊後，Line server會送一個HTTPS POST至Webhook URL開發者後台，並將剛才點擊項目的參數一同帶入
# ，e.g “action=buy&itemid=111”，後台就知道使用者剛剛點擊了哪一個項目。
# (2) Message：點擊後，Line App會自動幫使用者送出一個文字訊息。
# (3) URL：訪問一個網站連結。
# (4) Datetime picker：如下圖，當選擇完畢按下Send(發送)，Line server會送一個HTTPS POST到開發者後台，告知剛剛
# 使用者選擇的時間細節。
