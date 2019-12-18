import sys
sys.path.append('../')
sys.path.append('../scripts')

from parse_dates import ParseDates
from coinbase import CoinbasePipeline
from sma_golden_cross import SMAGoldenCross

import datetime as dt
import backtrader as bt
import backtrader.feeds as feeds
import backtrader.indicators as btind
import backtrader.analyzers as btanalyzers

if __name__ == '__main__':
    strategy = SMAGoldenCross
    startcash = 10 #BTC

    cerebro = bt.Cerebro(runonce=False, optreturn=False)

    cerebro.optstrategy(strategy, pfast=range(10,15), pslow=range(20,30))

    hist_data = ParseDates("ETH-BTC", dt.datetime(2019, 10, 1),dt.datetime.now(),"3600" )
    dataframe = hist_data.get_data()

    data = feeds.PandasData(dataname=dataframe)
    cerebro.adddata(data)
    cerebro.broker.setcash(startcash)
    SharpeRatioDay = bt.analyzers.SharpeRatio
    cerebro.addanalyzer(SharpeRatioDay, _name='mysharpe',timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='areturn')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='ddown')

    thestrats = cerebro.run()
