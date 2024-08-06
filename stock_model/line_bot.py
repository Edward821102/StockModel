from http.server import BaseHTTPRequestHandler
import json
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 从环境变量获取 Line 的凭证
LINE_CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
LINE_CHANNEL_SECRET = os.environ['LINE_CHANNEL_SECRET']

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 获取 X-Line-Signature 头
        signature = self.headers['X-Line-Signature']

        # 获取请求体
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')

        # 验证 Webhook 签名
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            self.send_response(400)
            self.end_headers()
            return

        # 回复 HTTP 200
        self.send_response(200)
        self.end_headers()

    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        user_message = event.message.text
        
        # 处理逻辑并返回结果
        response = execute_python_logic(user_message)
        
        # 回复用户
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )

def execute_python_logic(param):
    # 实现您的 Python 逻辑，这里只是简单回传消息
    return f"您传递的参数是：{param}"