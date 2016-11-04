import core_functions as cf
import numpy as np


class TechnicalIndicators:

    def __init__(self, stock_data):
        '''

        :param stock_data: Object of StockData with minimum 200 data points
        :return:
        '''
        self.stock_data = stock_data
        self.simple_moving_average_20 = self.simple_moving_average(stock_data, 20)


    def simple_moving_average(self, num_days):
        '''
        Finds the num_days simple moving average of a time series using close price
        :param num_days: number of days
        :return: Simple Moving Average of num_days
        '''
        if num_days>len(self.stock_data.len):
            raise ValueError("Number of days cannot be more than length of data")
        if num_days<=0:
            raise ValueError("Number of days cannot be 0 or negative")
        close_price = self.stock_data.close_price
        sma = cf.simple_moving_average(close_price, num_days)
        return sma

    def exponential_moving_average(self, num_days):
        '''
        Finds the num_days exponential moving average of a time series using close price
        :param num_days: number of days
        :return: Simple Moving Average of num_days
        '''
        if num_days>len(self.stock_data.len):
            raise ValueError("Number of days cannot be more than length of data")
        if num_days<=0:
            raise ValueError("Number of days cannot be 0 or negative")
        close_price = self.stock_data.close_price
        running_sum = sum(close_price[0:num_days])*1.0

    def bollinger_bands(self, n, sma=None):
        '''
        Finds the bollinger bands for the given data points. It takes sma as an optional arguments, if not provided it calculates in the function
        :param data_points: data points for which the bollinger bands have to be found
        :param n: period
        :param sma_20: optional simple moving average
        :return: upper and lower bollinger bands
        '''
        close_price = self.stock_data.close_price
        if not sma:
            sma = cf.simple_moving_average(close_price, n)
        upper_band = [0 for i in range(n-1)]
        lower_band = [0 for i in range(n-1)]
        for i in range(n-1, len(close_price)):
            std = np.std(close_price[i-n+1:i])
            print (std)
            upper_band.append(sma[i] + 2 * std)
            lower_band.append(sma[i] - 2 * std)
        return lower_band, upper_band

    def moving_average_convergence_divergence(self):
        '''
            Finds moving average convergence divergence
        :return:
        '''
        close_price = self.stock_data.close_price
        ema12 = cf.exponential_moving_average(close_price, 12)
        ema26 = cf.exponential_moving_average(close_price, 26)
        macd = np.subtract(ema12, ema26).tolist()
        macd_line = cf.exponential_moving_average(macd, 9)
        return macd,macd_line,np.subtract(macd, macd_line).tolist()


    def relative_strength_index(self, n=14):
        '''
            Finds the Indicator Relative Strength index
        :param n: period
        :return: Relative Strength Index
        '''
        close_price = self.stock_data.close_price
        rsi = cf.relative_strength_index(close_price, n)
        return rsi


    def stochastic_oscillator(self, n=14):
        '''
            Finds the stochastic oscillator
        :param n: lookback period
        :return:
        '''
        close_price = self.stock_data.close_price
        high_price = self.stock_data.high_price
        low_price = self.stock_data.low_price
        stoch = cf.stochastic_oscillator(close_price, high_price, low_price, n)
        return stoch


    def aroon_oscillator(self, n=25):
        '''
        :param n:
        :return:
        '''
        high_price = self.stock_data.high_price
        low_price = self.stock_data.low_price
        aroon = cf.aroon_oscillator(high_price, low_price, n)

    def commodity_channel_index(self, n=20):
        '''

        :param n:
        :return:
        '''
        close_price = self.stock_data.close_price
        high_price = self.stock_data.high_price
        low_price = self.stock_data.low_price
        cci = cf.commodity_channel_index(close_price, high_price, low_price, n)
        return cci

    def williams_percentage_r(self, n=14):
        close_price = self.stock_data.close_price
        high_price = self.stock_data.high_price
        low_price = self.stock_data.low_price
        williams = cf.williams_percentage_r(close_price, high_price, low_price, n)
        return williams


    def vortex(self, n=14):
        close_price = self.stock_data.close_price
        high_price = self.stock_data.high_price
        low_price = self.stock_data.low_price
        vortex_p, vortex_m = cf.williams_percentage_r(close_price, high_price, low_price, n)
        return vortex_p, vortex_m
