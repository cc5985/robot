import json, time
from websocket import create_connection

for i in range(3):
    try:
        # wscat -c wss://ws.kraken.com/
        ws = create_connection("wss://ws.kraken.com/")
    except Exception as error:
        print('Caught this errr: ' + repr(error))
        time.sleep(3)
    else:
        break

ws.send(json.dumps({
    "event": "subscribe",
    #"event": "ping",
    "pair": ["XBT/USD"],
    #"subscription": {"name": "ticker"}
    #"subscription": {"name": "spread"}
    # "subscription": {"name": "trade"}
    "subscription": {"name": "book", "depth": 10}
    #"subscription": {"name": "ohlc", "interval": 5}
}))

while True:
    try:
        result = ws.recv()
        result = json.loads(result)
        print ("Received '%s'" % result, time.time())
    except Exception as error:
        print('Caught this error: ' + repr(error))
        time.sleep(3)

ws.close()
