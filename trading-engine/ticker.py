import asyncio
import pandas as pd
from pathlib import Path
from copra.websocket import Channel, Client

ticker_csv = Path("../hist-data") / "BTC-USD_ticker.csv"

class TickerClient(Client):

    def on_message(self, message):
        if message['type'] == 'ticker':
            data = pd.Series(message)
            print(data.index)
            # with open(ticker_csv, mode='a+') as f:
            #     print(f.tell())
            #     data.to_csv(f, mode='a+', header=f.tell()==0,)
            # TODO: to_csv needs proper formatting, series index must become csv column header

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    ws_ticker = TickerClient(loop, Channel('ticker', 'BTC-USD'))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(ws_ticker.close())
        loop.close()
