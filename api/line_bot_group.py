import os
import requests

LINE_TOKEN = os.environ.get('LINE_TOKEN')

def send_message():
    
    headers = {
        'Authorization':f'Bearer {LINE_TOKEN}'
    }
    payload = {
        'message':'問屁問？'
    }
    # files = {'imageFile': open(f, 'rb')}
    res = requests.post('https://notify-api.line.me/api/notify',data=payload,headers=headers)
    # return res.json()



