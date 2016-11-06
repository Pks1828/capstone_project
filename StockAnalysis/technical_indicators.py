import core_functions as cf
import numpy as np


class TechnicalIndicators:

    def __init__(self, stock_data):
        '''

        :param stock_data: Object of StockData with minimum 200 data points
        :return:
        '''
        self.stock_data = stock_data
        self.sma = None
        self.ema = None
        self.bollinger = None
        self.macd = None
        self.rsi = None
        self.stochastic = None
        self.aroon = None
        self.cci = None
        self.willams = None
        self.vortex = None

    def calculate_with_defaults(self):
        self.sma = self.simple_moving_average()
        self.ema = self.exponential_moving_average()
        self.bollinger = self.bollinger_bands()
        self.macd = self.moving_average_convergence_divergence()
        self.rsi = self.relative_strength_index()
        self.stochastic = self.stochastic_oscillator()
        self.aroon = self.aroon_oscillator()
        self.cci = self.commodity_channel_index()
        self.willams = self.williams_percentage_r()
        self.vortex = self.vortex_osc()


    def simple_moving_average(self, num_days=10):
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

    def exponential_moving_average(self, num_days=10):
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

    def bollinger_bands(self, n=20, sma=None):
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
        return aroon

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


    def vortex_osc(self, n=14):
        close_price = self.stock_data.close_price
        high_price = self.stock_data.high_price
        low_price = self.stock_data.low_price
        vortex_p, vortex_m = cf.williams_percentage_r(close_price, high_price, low_price, n)
        return vortex_p, vortex_m


class TechnicalAnalysis:
    def __init__(self,technical_indicators, stock_data):
        self.technical_indicators = technical_indicators
        self.stock_data = stock_data
        self.sma_signal = None
        self.ema_signal = None
        self.bollinger_signal = None
        self.macd_signal = None
        self.rsi_signal = None
        self.stochastic_signal = None
        self.aroon_signal = None
        self.cci_signal = None
        self.williams_signal= None
        self.vortex_signal= None

    def get_sma_signal(self):
        sma = self.technical_indicators.sma
        closep = self.stock_data.close_price
        sma_signal = [0]
        for i in range(1, len(sma)):
            signal = 0
            if closep[i-1]<sma[i-1] and closep[i]>=sma[i]:
                signal = 1
            elif closep[i-1]>sma[i-1] and closep[i]<=sma[i]:
                signal = -1
            sma_signal.append(signal)
        self.sma_signal = self.carryover(sma_signal,4)

    def get_ema_signal(self):
        ema = self.technical_indicators.ema
        closep = self.stock_data.close_price
        ema_signal = [0]
        for i in range(1, len(ema)):
            signal = 0
            if closep[i-1]<ema[i-1] and closep[i]>=ema[i]:
                signal = 1
            elif closep[i-1]>ema[i-1] and closep[i]<=ema[i]:
                signal = -1
            ema_signal.append(signal)
        self.ema_signal = self.carryover(ema_signal,4)

    def get_bollinger_signal(self):
        lower, upper = self.technical_indicators.bollinger
        bollinger_signal = [0]
        closep = self.stock_data.close_price
        for i in range(1, len(upper)):
            signal = 0
            if closep[i-1]<lower[i-1] and closep[i]>=lower[i]:
                signal = 1
            elif closep[i-1]>upper[i-1] and closep[i]<=upper[i]:
                signal = -1
            bollinger_signal.append(signal)
        self.bollinger_signal = self.carryover(bollinger_signal,4)

    def get_macd_signal(self):
        macd, line, hist = self.technical_indicators.macd
        macd_signal = [0]
        for i in range(1, len(hist)):
            signal = 0
            if hist[i-1]<0 and hist[i]>=0:
                signal = 1
            elif hist[i-1]>0 and hist[i]<=0:
                signal = -1
            macd_signal.append(signal)
        self.macd_signal = self.carryover(macd_signal,4)

    def get_rsi_signal(self):
        rsi = self.technical_indicators.rsi
        rsi_signal = [0]
        for i in range(1, rsi):
            signal = 0
            if rsi[i-1]<30 and rsi[i]>=30:
                signal = 1
            elif rsi[i-1]>70 and rsi[i]<=70:
                signal = -1
            rsi_signal.append(signal)
        self.rsi_signal = self.carryover(rsi_signal,4)

    def get_stochastic_signal(self):
        stochastic = self.technical_indicators.stochastic
        stochastic_signal = [0]
        for i in range(1, stochastic):
            signal = 0
            if stochastic[i-1]<30 and stochastic[i]>=30:
                signal = 1
            elif stochastic[i-1]>70 and stochastic[i]<=70:
                signal = -1
            stochastic_signal.append(signal)
        self.stochastic_signal = self.carryover(stochastic_signal,4)

    def get_aroon_signal(self):
        aroon = self.technical_indicators.aroon
        aroon_signal = [0]
        for i in range(1, aroon):
            signal = 0
            if aroon[i-1]<0 and aroon[i]>=0:
                signal = 1
            elif aroon[i-1]>0 and aroon[i]<=0:
                signal = -1
            aroon_signal.append(signal)
        self.aroon_signal = self.carryover(aroon_signal,4)

    def get_cci_signal(self):
        cci = self.technical_indicators.cci
        cci_signal = [0]
        for i in range(1, cci):
            signal = 0
            if cci[i-1]<-100 and cci[i]>=-100:
                signal = 1
            elif cci[i-1]>100 and cci[i]<=100:
                signal = -1
            cci_signal.append(signal)
        self.cci_signal = self.carryover(cci_signal,4)

    def get_williams_signal(self):
        williams = self.technical_indicators.williams
        williams_signal = [0]
        for i in range(1, williams):
            signal = 0
            if williams[i-1]<-80 and williams[i]>=-80:
                signal = 1
            elif williams[i-1]>-20 and williams[i]<=-20:
                signal = -1
            williams_signal.append(signal)
        self.williams_signal = self.carryover(williams_signal,4)

    def get_vortex_signal(self):
        vortex_p, vortex_m = self.technical_indicators.vortex
        vortex_signal = [0]
        for i in range(1, vortex_p):
            signal = 0
            if vortex_p[i-1]<vortex_m[i-1] and vortex_p[i]>=vortex_m[i]:
                signal = 1
            elif vortex_p[i-1]>vortex_m[i-1] and vortex_p[i]<=vortex_m[i]:
                signal = -1
            vortex_signal.append(signal)
        self.vortex_signal = self.carryover(vortex_signal,4)



    def get_signals(self):
        pass

    def calculate_weights(self):
        pass

    def get_returns(self):
        pass

    def give_recommendation(self):
        pass

    def carryover(self, signals_in, n=4):
        i=0
        signals = signals_in[:]
        while i<len(signals):
            if signals[i]!=0:
                count = 0
                i+=1
                while i<len(signals) and signals[i]==0 and count<n:
                    signals[i] = signals[i-1]
                    count+=1
                    i+=1
                continue
            i+=1
        return signals


