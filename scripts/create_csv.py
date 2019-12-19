import sys
sys.path.append('../')

from coinbase import CoinbasePipeline
import datetime as dt



one_year = dt.timedelta(days=365)
days_100 = dt.timedelta(days=100)
days_150 = dt.timedelta(days=150)
days_30  = dt.timedelta(days=30)
month_6  = dt.timedelta(days=180)
start = dt.datetime.now() - one_year
pipeline = CoinbasePipeline('ETH-BTC',start=start, granularity=60)
dataframe = pipeline.get_data()


dataframe.to_csv(
r'/Users/ericbrown/code/shelter/coinbase/hist-data/ETH-BTC-60.csv')
