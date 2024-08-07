from http.server import BaseHTTPRequestHandler
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import twstock
from typing import Dict


LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
webhook_handler = WebhookHandler(LINE_CHANNEL_SECRET)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        signature = self.headers.get('X-Line-Signature')
        if not signature:
            self.send_response(400)
            self.end_headers()
            return

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')

        try:
            webhook_handler.handle(body, signature)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
        except InvalidSignatureError:
            self.send_response(400)
            self.end_headers()
        except Exception as e:
            print(f"Error: {e}")
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'Welcome Edward\'s Palace.')

    @webhook_handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        user_message = event.message.text
        response = get_close(user_message)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )

def get_close(message:str) -> str:
    
    def process(stock_realtime_info:Dict, price:str) -> str:
        try:
            return stock_realtime_info[price]
        except:
            return "暫無資料"

    stock = twstock.realtime.get(message)
    open  = process(stock['realtime'], "open")
    high  = process(stock['realtime'], "high")
    low   = process(stock['realtime'], "low")
    close = process(stock['realtime'], "close")
    
    return f"開盤價:{open}, 最高價:{high}, 最低價:{low}, 收盤價:{close}"

