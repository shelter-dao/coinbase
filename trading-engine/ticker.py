import asyncio
import pandas as pd
from pathlib import Path
from copra.websocket import Channel, Client

ticker_csv = Path("../hist-data") / "BTC-USD_ticker.csv"


class WebsocketHandler(object):
    def __init__(self, message):
        if message['type'] == 'ticker':
            loop.create_task(self.handle_ticker(message))

    async def handle_ticker(self, message):
        await asyncio.sleep(0)
        data = pd.Series(message)
        print(data)
        # data.columns = message.keys()
        # with open(ticker_csv, mode='a+') as f:
        #     print(f.tell())
        #     data.to_csv(f, mode='a+', header=f.tell()==0,)
        # TODO: to_csv needs proper formatting, series index must become csv column header


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
