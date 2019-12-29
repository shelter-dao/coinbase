import asyncio
import pandas as pd
from pathlib import Path
from copra.websocket import Channel, Client

ticker_csv = Path("../hist-data") / "BTC-USD_ticker.csv"

tick = {}

async def parse_ticker():
    global tick
    while(1):
        if (not tick):
            await asyncio.sleep(0)
        elif(tick):
            data = pd.Series(tick)
            tick = {}
            print(data)

            # data = pd.Series(message, index=['product_id', 'best_bid', 'best_ask', )
            # data.columns = message.keys()
            # with open(ticker_csv, mode='a+') as f:
            #     print(f.tell())
            #     data.to_csv(f, mode='a+', header=f.tell()==0,)
            # TODO: to_csv needs proper formatting, series index must become csv column header


class Ticker(Client):

    def on_message(self, message):
        global tick
        if message['type'] == 'ticker':
            tick = message

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(parse_ticker())
    ws_ticker = Ticker(loop, Channel('ticker', 'BTC-USD'))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(ws_ticker.close())
        loop.close()
