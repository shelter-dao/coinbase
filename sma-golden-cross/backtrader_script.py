import sys
sys.path.append('../')
sys.path.append('../scripts')

from parse_dates import ParseDates
from coinbase import CoinbasePipeline
from sma_golden_cross import SMAGoldenCross

import datetime as dt
import pandas as pd
import backtrader as bt
import backtrader.feeds as feeds
import backtrader.indicators as btind
import backtrader.analyzers as btanalyzers

import matplotlib

if __name__ == '__main__':
    startTime = dt.datetime.now()
    strategy = SMAGoldenCross
    startcash = 10 #BTC
    cerebro = bt.Cerebro(runonce=False, optreturn=False)
    cerebro.addstrategy(strategy)

    hist_data = ParseDates("ETH-BTC", dt.datetime(2019, 10, 1),dt.datetime.now(),"3600" )
    dataframe = hist_data.get_data()

    data = feeds.PandasData(dataname=dataframe)
    cerebro.adddata(data)
    cerebro.broker.setcash(startcash)
    cerebro.broker.setcommission(commission=0.005)
    SharpeRatioDay = bt.analyzers.SharpeRatio
    cerebro.addanalyzer(SharpeRatioDay, _name='mysharpe',timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='areturn')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='ddown')
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    thestrats = cerebro.run()
    print(thestrats)

    print('\nFinal Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('\nSharpe Ratio:', thestrats[0].analyzers.mysharpe.get_analysis()['sharperatio'])
    print('\n2019 Annual Return:',(thestrats[0].analyzers.areturn.get_analysis()[2019] * 100), "%" )
    print('\nDraw Down:\n',
          '    Duration: %.2f' % thestrats[0].analyzers.ddown.get_analysis().get("len"),
          '    Percent: %.2f' % thestrats[0].analyzers.ddown.get_analysis().get("drawdown"), "%",
          '    Dollars: %.2f' % thestrats[0].analyzers.ddown.get_analysis().get("moneydown"))

    totalTime = dt.datetime.now() - startTime
    print('Processing Time:{}'.format(totalTime))

    cerebro.plot()

    # pipeline.change_graph()
    # pipeline.candlestick_graph()
