from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import configparser

# import config file
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
line_bot_api = LineBotApi(config['LineBot']['linebotapi'])
handler = WebhookHandler(config['LineBot']['webhookhandler'])

line_bot_api.push_message(config['LineBot']['username'], TextSendMessage(text='It is begining.'))

@app.route("/", methods=['GET'])
def hello():
    return 'Hello!!!'
    
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    pretty_text = ''
    for i in event.message.text:
        pretty_text+=i
    line_bot_api.reply_message(event.reply_token,
                              TextSendMessage(text=pretty_text))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

