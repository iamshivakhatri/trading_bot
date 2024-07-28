import websocket, json
from dotenv import load_dotenv
import os

load_dotenv()

socket = 'wss://paper-api.alpaca.markets/stream'
# socket = 'wss://data.alpaca.markets/stream'
print(os.environ.get("API_KEY"))
print(os.environ.get("API_SECRET"))


def on_open(ws):
    print('opened')
    auth_data = {
        "action" : "authenticate",
        "key": os.environ.get("API_KEY"),
        "secret": os.environ.get("API_SECRET")
        
    }
    ws.send(json.dumps(auth_data))

    listen_message = {"action": "listen", "data": {"streams": ["T.SPY"]}}
    ws.send(json.dumps(listen_message))

def on_message(ws, message):
    print('received a message')
    print(message)
  
     

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()