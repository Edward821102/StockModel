from http.server import BaseHTTPRequestHandler
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from stock_model.fetch_twstock import WebCrawlerStockVolumes
from stock_model.neuron import Neuron
from twstock import Stock
import os

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
    
def get_close(stock_id:str) -> str:
    wcsv = WebCrawlerStockVolumes(stock_id)
    vol = int(wcsv.get_volumes())
    stock = Stock(stock_id)
    data = stock.fetch_from(2018, 1)
    ohlcv_list = [(i.open / 1000, i.high / 1000, i.low / 1000, i.close / 1000, i.capacity / (vol * 1000)) for i in data]
    target_list = [i[3] for i in ohlcv_list]
    train_samples = ohlcv_list[:-30]
    train_targets = target_list[1:-29]
    neuron = Neuron()
    loss = neuron.train(train_samples, train_targets)
    prediction = neuron.predict(ohlcv_list[-1])
    return f"Loss:{loss}, 隔日收盤價:{prediction * 1000}"