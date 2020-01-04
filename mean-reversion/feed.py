import asyncio
import pandas as pd
import json
from copra.websocket import Channel, Client
from autobahn.asyncio.websocket import WebSocketClientFactory

class MyClient(Client):

    def on_message(self, message):
        print(message)
        if message['type'] == 'ticker':
            dataFeed = pd.Series(message)
            # print('**************************************')
            # print(dataFeed)
            # print(dataFeed.columns)
            # dataFeed.set_index('time')
            # print(dataFeed)
            # print('**************************************')
            return(dataFeed)

# global dataFeed
class Feed(object):
    def __init__(self,)



        # TODO: implement a way to open up the feed asynchronously, either as a module or using async.get_event_loop()
        # def open_feed():
        #     loop = asyncio.get_event_loop()
        #     ws1 = MyClient(loop, Channel('ticker', 'BTC-USD'))
        #
        #     try:
        #         loop.run_forever()
        #     except KeyboardInterrupt:
        #         # loop.run_until_complete(ws.close())
        #         loop.run_until_complete(ws1.close())
        #         loop.close()



    loop = asyncio.get_event_loop()
    ws1 = MyClient(loop, Channel('ticker', 'BTC-USD'))


    try:
        loop.run_forever()
    except KeyboardInterrupt:
        # loop.run_until_complete(ws.close())
        loop.run_until_complete(ws1.close())
        loop.close()
