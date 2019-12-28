import pandas as pd

class ParseDates(object):
    def __init__(self,product_id, start_date, end_date, granularity):
        self.product_id = product_id
        self.start_date = start_date
        self.end_date = end_date
        self.granularity = granularity

    def get_data(self):
        product = self.product_id
        start = self.start_date
        end = self.end_date
        granularity = self.granularity
        df= pd.read_csv("../hist-data/" + product
                        + "-" + granularity + ".csv",
                        index_col="datetime",
                        parse_dates=['datetime'])
        indexs = df.index.to_pydatetime()
        df_filtered = df[(indexs > start) & (indexs < end)]
        return(df_filtered)
