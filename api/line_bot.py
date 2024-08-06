# from http.server import BaseHTTPRequestHandler
# import json
# import os
# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage

# LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
# LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')

# line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# webhook_handler = WebhookHandler(LINE_CHANNEL_SECRET)

# class handler(BaseHTTPRequestHandler):
#     def do_POST(self):
#         signature = self.headers.get('X-Line-Signature')
#         content_length = int(self.headers['Content-Length'])
#         body = self.rfile.read(content_length).decode('utf-8')

#         try:
#             handler.handle(body, signature)
#             self.send_response(200)
#         except InvalidSignatureError:
#             self.send_response(400)

#         self.send_header('Content-Type', 'text/plain; charset=utf-8')
#         self.end_headers()

#     def do_GET(self):
#         self.send_response(200)
#         self.send_header('Content-Type', 'text/plain; charset=utf-8')
#         self.end_headers()
#         self.wfile.write(b'Welcome Edward\'s Palace.')

#     @webhook_handler.add(MessageEvent, message=TextMessage)
#     def handle_message(event):
#         user_message = event.message.text
#         response = execute_python_logic(user_message)

#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=response)
#         )

# def execute_python_logic(user_message):
#     if user_message.lower() == "hi":
#         return "Hello! How can I help you today?"
#     elif user_message.lower() == "bye":
#         return "Goodbye! Have a nice day!"
#     else:
#         return f"你說的都對：{user_message}"
    
from http.server import BaseHTTPRequestHandler
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 从环境变量获取 Line 的凭证
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
        response = f"你傳了這是什麼鬼?{user_message}"

        # 发送回复消息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )