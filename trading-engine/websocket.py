import asyncio
import pandas as pd
from datetime import datetime as dt
from pathlib import Path
from copra.websocket import Channel, Client

ticker_csv = Path("../hist-data") / "BTC-USD_ticker.csv"


class WebsocketHandler(object):
    def __init__(self, message):
        # TODO: see if this is faster using pythonic switch statement
        if message['type'] == 'ticker':
            loop.create_task(self.handle_ticker(message))
        elif message['type'] == 'matches':
            loop.create_task(self.handle_matches(message))

    async def handle_ticker(self, message):
        await asyncio.sleep(0)
        data = pd.DataFrame(message, index=[0])
        data = data.filter(items=['time', 'product_id', 'best_bid', 'best_ask'])
        data.time[0] = dt.strptime(data.time[0], '%Y-%m-%dT%H:%M:%S.%fZ')
        data.rename(columns={"time": "datetime"}, inplace=True)
        data.set_index('datetime', inplace=True, drop=True)
        print(data)
        # data['time'] = dt.fromtimestamp(data['time']) = int(data['time'])

        # data.columns = ['time', 'product_id', 'best_bid', 'best_ask']
        # data['time'] = dt.fromtimestamp(data['time'])
        # data.set_index('time', inplace=True, drop=True)
        # print(data)

        # data.columns = message.keys()
        # with open(ticker_csv, mode='a+') as f:
        #     print(f.tell())
        #     data.to_csv(f, mode='a+', header=f.tell()==0,)
        # TODO: to_csv needs proper formatting, series index must become csv column header

    # TODO: implement handle_matches()
    async def handle_matches(self, matches):
        await asyncio.sleep(0)


class Websocket(Client):

    def on_message(self, message):
        handler = WebsocketHandler(message)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # TODO: listen to multiple channels
    ws_ticker = Websocket(loop, Channel('ticker', 'BTC-USD'))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(ws_ticker.close())
        loop.close()
