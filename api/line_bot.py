from http.server import BaseHTTPRequestHandler
import json
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
web_hook_handler = WebhookHandler(LINE_CHANNEL_SECRET)

# from http.server import BaseHTTPRequestHandler

# class handler(BaseHTTPRequestHandler):

#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-type','text/plain')
#         self.end_headers()
#         self.wfile.write('Hello, world!'.encode('utf-8'))
#         return

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):

        signature = self.headers['X-Line-Signature']
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            self.send_response(400)
            self.end_headers()
            return

        self.send_response(200)
        self.end_headers()

    @web_hook_handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        user_message = event.message.text
        response = execute_python_logic(user_message)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )

def execute_python_logic(param):
    return f"傳遞：{param}"