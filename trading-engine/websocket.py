import asyncio
import logging
import pandas as pd
from datetime import datetime as dt
from pathlib import Path
from copra.websocket import Channel, Client

ticker_csv = Path("../hist-data") / "BTC-USD_ticker.csv"

class CandleMaker(object):
    def __init__(self, data):
        data


class WebsocketHandler(object):
    def __init__(self, message):
        self.message = message
        # TODO: see if this is faster using pythonic 'switch' functionality
        if self.message['type'] == 'ticker':
            loop.create_task(self.handle_ticker())
        # elif self.message['type'] == 'matches':
        #     loop.create_task(self.handle_matches()) etc...

    async def handle_ticker(self):
        await asyncio.sleep(0)
        self.data = pd.DataFrame(self.message, index=[0])
        self.data = self.data.filter(items=['time', 'trade_id', 'product_id', 'best_bid', 'best_ask'])
        self.data.at[0,'time'] = dt.strptime(self.data.at[0, 'time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.data.rename(columns={"time": "datetime"}, inplace=True)
        self.data.set_index('datetime', inplace=True, drop=True)
        print(self.data)
        with open(ticker_csv, mode='a+') as f:
              self.data.to_csv(f, mode='a+', header=f.tell()==0,)

class Websocket(Client):

    def on_message(self, message):
        handler = WebsocketHandler(message)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.set_debug(enabled=True)
    # logging.basicConfig(level=logging.DEBUG)
    # TODO: listen to multiple channels
    ws_ticker = Websocket(loop, Channel('ticker', 'BTC-USD'))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(ws_ticker.close())
        loop.close()
