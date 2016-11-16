
class StockData:
    def __init__ (self, date_series, open_price, high_price, low_price, close_price, reduce_by=200):
        '''
        Takes stock price data points of a particular stock in Ascending order of date
        A minimun of 200 data points is requires for further processing
        :param date_series: List of dates in ascending order
        :param open_price: List of open price in Ascending order of data
        :param high_price: List of high price in Ascending order of data
        :param low_price: List of low price in Ascending order of data
        :param close_price: List of close price in Ascending order of data
        :param volume: List of volume in Ascending order of data
        :return: None
        '''
        if len(open_price) != len(close_price) or len(open_price) != len(high_price) or len(open_price) != len(close_price) or len(open_price) != len(date_series):
            raise ValueError("The dimensions of data do not match")
        if len(date_series)<200:
            raise ValueError("Length of data points is less than 200! for calculation a minimum number of 200 is required!")
        if reduce_by<0:
            self.len = len(date_series)
            self.date_series = date_series
            self.open_price = open_price
            self.high_price = high_price
            self.low_price = low_price
            self.close_price = close_price
            self.len = len(self.date_series)
        else:
            self.len = len(date_series)
            self.date_series = date_series[max(self.len-reduce_by,0):self.len]
            self.open_price = open_price[max(self.len-reduce_by,0):self.len]
            self.high_price = high_price[max(self.len-reduce_by,0):self.len]
            self.low_price = low_price[max(self.len-reduce_by,0):self.len]
            self.close_price = close_price[max(self.len-reduce_by,0):self.len]
            self.len = len(self.date_series)
