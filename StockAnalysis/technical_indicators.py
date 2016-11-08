import numpy as np
import math


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
        if num_days>self.stock_data.len:
            raise ValueError("Number of days cannot be more than length of data")
        if num_days<=0:
            raise ValueError("Number of days cannot be 0 or negative")
        close_price = self.stock_data.close_price
        sma = simple_moving_average_core(close_price, num_days)
        return sma

    def exponential_moving_average(self, num_days=10):
        '''
        Finds the num_days exponential moving average of a time series using close price
        :param num_days: number of days
        :return: Simple Moving Average of num_days
        '''
        if num_days>self.stock_data.len:
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
            sma = simple_moving_average_core(close_price, n)
        upper_band = [0 for i in range(n-1)]
        lower_band = [0 for i in range(n-1)]
        for i in range(n-1, len(close_price)):
            std = np.std(close_price[i-n+1:i])
            upper_band.append(sma[i] + 2 * std)
            lower_band.append(sma[i] - 2 * std)
        return lower_band, upper_band

    def moving_average_convergence_divergence(self):
        '''
            Finds moving average convergence divergence
        :return:
        '''
        close_price = self.stock_data.close_price
        ema12 = exponential_moving_average_core(close_price, 12)
        ema26 = exponential_moving_average_core(close_price, 26)
        macd = np.subtract(ema12, ema26).tolist()
        macd_line = exponential_moving_average_core(macd, 9)
        return macd,macd_line,np.subtract(macd, macd_line).tolist()


    def relative_strength_index(self, n=14):
        '''
            Finds the Indicator Relative Strength index
        :param n: period
        :return: Relative Strength Index
        '''
        close_price = self.stock_data.close_price
        rsi = relative_strength_index_core(close_price, n)
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
        stoch = stochastic_oscillator_core(close_price, high_price, low_price, n)
        return stoch


    def aroon_oscillator(self, n=25):
        '''
        :param n:
        :return:
        '''
        high_price = self.stock_data.high_price
        low_price = self.stock_data.low_price
        aroon = aroon_oscillator_core(high_price, low_price, n)
        return aroon

    def commodity_channel_index(self, n=20):
        '''

        :param n:
        :return:
        '''
        close_price = self.stock_data.close_price
        high_price = self.stock_data.high_price
        low_price = self.stock_data.low_price
        cci = commodity_channel_index_core(close_price, high_price, low_price, n)
        return cci

    def williams_percentage_r(self, n=14):
        close_price = self.stock_data.close_price
        high_price = self.stock_data.high_price
        low_price = self.stock_data.low_price
        williams = williams_percentage_r_core(close_price, high_price, low_price, n)
        return williams

    def vortex_osc(self, n=14):
        close_price = self.stock_data.close_price
        high_price = self.stock_data.high_price
        low_price = self.stock_data.low_price
        vortex_p, vortex_m = vortex_core(close_price, high_price, low_price, n)
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
        self.weights = None

    def get_all_signals(self):
        self.get_sma_signal()
        self.get_ema_signal()
        self.get_bollinger_signal()
        self.get_macd_signal()
        self.get_rsi_signal()
        self.get_stochastic_signal()
        self.get_aroon_signal()
        self.get_cci_signal()
        self.get_williams_signal()
        self.get_vortex_signal()

    def calculate_weights(self):
        sma_returns = self.get_returns(self.sma_signal)
        ema_returns = self.get_returns(self.ema_signal)
        bollinger_returns = self.get_returns(self.bollinger_signal)
        macd_returns = self.get_returns(self.macd_signal)
        rsi_returns = self.get_returns(self.rsi_signal)
        stochastics_returns = self.get_returns(self.stochastic_signal)
        aroon_returns = self.get_returns(self.aroon_signal)
        cci_returns = self.get_returns(self.cci_signal)
        williams_returns = self.get_returns(self.williams_signal)
        vortex_returns = self.get_returns(self.vortex_signal)
        weights = [sma_returns, ema_returns, bollinger_returns, macd_returns, rsi_returns, stochastics_returns, aroon_returns, cci_returns, williams_returns, vortex_returns]
        mean = np.mean(weights)
        std = np.std(weights)
        self.weights = []
        for w in weights:
            self.weights.append((w-mean)/(2.0*std)+1.0)

    def get_returns(self, signals_in):
        returns = 0
        signals = carryover(signals_in, -1)
        i = 50
        highp = self.stock_data.high_price
        lowp = self.stock_data.low_price
        closep = self.stock_data.close_price
        while i<len(signals):
            if signals[i]>0:
                reco = 1
                target = closep[i]+2*np.std(closep[i-50:i])*math.sqrt(10)
                stoploss = max(closep[i]-2*np.std(closep[i-50:i])*math.sqrt(10),0)
            else:
                reco = -1
                stoploss = closep[i]+2*np.std(closep[i-50:i])*math.sqrt(10)
                target = max(closep[i]-2*np.std(closep[i-50:i])*math.sqrt(10),0)
            reco_price = closep[i]
            i+=1
            count = 0
            reco_made = False
            while i<len(signals) and count<20 and signals[i]==reco:
                if reco>0:
                    if highp[i]>=target:
                        returns += highp[i]-target
                        reco_made = True
                        break
                    elif lowp[i]<=stoploss:
                        returns += lowp[i]-stoploss
                        reco_made = True
                        break
                else:
                    if highp[i]>=stoploss:
                        returns += stoploss-highp[i]
                        reco_made = True
                        break
                    elif lowp[i]<=target:
                        returns += target-lowp[i]
                        reco_made = True
                        break
                count +=1
                i+=1
            if reco_made:
                i+=1
            else:
                returns += closep[i-1] - reco_price
        return returns


    def give_recommendation(self):
        score = 0
        for i in range(len(self.weights)):
            score += self.weights[i]*self.sma_signal[-1]
        return "SELL" if score<0 else ("BUY" if score>0 else "NEUTRAL")

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
        self.sma_signal = carryover(sma_signal,4)

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
        self.ema_signal = carryover(ema_signal,4)

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
        self.bollinger_signal = carryover(bollinger_signal,4)

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
        self.macd_signal = carryover(macd_signal,4)

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
        self.rsi_signal = carryover(rsi_signal,4)

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
        self.stochastic_signal = carryover(stochastic_signal,4)

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
        self.aroon_signal = carryover(aroon_signal,4)

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
        self.cci_signal = carryover(cci_signal,4)

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
        self.williams_signal = carryover(williams_signal,4)

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
        self.vortex_signal = carryover(vortex_signal,4)

def carryover(signals_in, n=4):
    i=0
    signals = signals_in[:]
    while i<len(signals):
        if signals[i]!=0:
            count = 0
            i+=1
            while i<len(signals) and signals[i]==0:
                if count>=n and n>=0:
                    break
                signals[i] = signals[i-1]
                count+=1
                i+=1
            continue
        i+=1
    return signals


def simple_moving_average_core(data_points, n):
    '''
    Finds the simple moving average of given points
    :param data_points: data points for whom the average is to be found
    :param n: the period
    :return: the n period simple moving average
    '''
    running_sum = sum(data_points[0:n])*1.0
    sma = [0 for i in range(n-1)]
    sma.append(running_sum/n)
    for i in range(n, len(data_points)):
        running_sum -= data_points[i-n]
        running_sum += data_points[i]
        sma.append(running_sum/n)
    return sma


def exponential_moving_average_core(data_points, n):
    '''
    Finds the exponential moving average of given points
    :param data_points: data points for whom the average is to be found
    :param n: the period
    :return: the n period exponential moving average
    '''
    running_sum = sum(data_points[0:n])*1.0
    ema = [0 for i in range(n-1)]
    ema.append(running_sum/n)
    multiplier = 2.0/(n+1)
    for i in range(n, len(data_points)):
        result = (data_points[i]-ema[-1]) * multiplier + ema[-1]
        ema.append(result)
    return ema


def relative_strength_index_core(close_price, n):
    loss = [0 for i in range(len(close_price))]
    profit = [0 for i in range(len(close_price))]
    rsi = [0 for i in range(len(close_price))]
    prv_avg_profit = None
    prv_avg_loss = None
    for i in range(1, len(close_price)):
        diff = close_price[i]-close_price[i-1]
        if diff<=0:
            loss[i] = abs(diff)
        else:
            profit[i] = diff
        if i>=n-1:
            if i>=n:
                avg_profit = (prv_avg_profit*(n-1)+profit[i])/n
                avg_loss   = (prv_avg_loss*(n-1)+loss[i])/n
                prv_avg_profit = avg_profit
                prv_avg_loss = avg_loss
            else:
                avg_profit = np.average(profit[i-n+1:i+1])
                avg_loss   = np.average(loss[i-n+1:i+1])
                prv_avg_profit = avg_profit
                prv_avg_loss = avg_loss
            if avg_loss!=0:
                rsi[i] = 100.0 - (100.0/(1+(avg_profit/avg_loss)))
            else:
                rsi[i] = 100.0
    return rsi


def stochastic_oscillator_core(close_price, high_price, low_price, n):
    stoch = [0 for i in range(len(close_price))]
    for i in range(n-1, len(close_price)):
        llow = min(low_price[i-n+1:i+1])
        hhigh = max(high_price[i-n+1:i+1])
        stoch[i] = (close_price[i] - llow)/(hhigh - llow) * 100.0
    return stoch


def aroon_oscillator_core(high_price, low_price, n):
    aroon = [0 for i in range(len(high_price))]
    for i in range(n-1, len(high_price)):
        llow = low_price[i-n+1:i+1].index(min(low_price[i-n+1:i+1]))
        hhigh = high_price[i-n+1:i+1].index(max(high_price[i-n+1:i+1]))
        aroon_low = 100.0*((llow+1)/n)
        aroon_high = 100.0*((hhigh+1)/n)
        aroon[i] = aroon_high - aroon_low
    return aroon


def commodity_channel_index_core(close_price, high_price, low_price, n):
    typical_price = [(close_price[i]+high_price[i]+low_price[i])/3.0 for i in range(len(close_price))]
    tp_sma = simple_moving_average_core(typical_price, 20)
    cci = [0 for i in range(len(close_price))]
    for i in range(n-1, len(typical_price)):
        mean = np.mean(typical_price[i-n+1:i+1])
        mean_deviation = 0.0
        for j in typical_price[i-n+1:i+1]:
            mean_deviation += abs(j-mean)
        mean_deviation = mean_deviation*1.0/n
        cci[i] = (typical_price[i] - tp_sma[i])/(0.015*mean_deviation)
    return cci


def williams_percentage_r_core(close_price, high_price, low_price, n):
    '''
    (Highest High - Close)/(Highest High - Lowest Low) * -100

    :param close_price:
    :param high_price:
    :param low_price:
    :param n:
    :return:
    '''
    wr = [0 for i in range(len(close_price))]
    for i in range(n-1, len(close_price)):
         hhigh = min(low_price[i-n+1:i+1])
         llow = max(high_price[i-n+1:i+1])
         wr[i] = (hhigh-close_price[i])/(hhigh-llow)*-100.0
    return wr


def vortex_core(close_price, high_price, low_price, n):
    vm_plus = [0 for i in range(len(close_price))]
    vm_minus = [0 for i in range(len(close_price))]
    vm_plus_n = [0 for i in range(len(close_price))]
    vm_minus_n = [0 for i in range(len(close_price))]
    tr = [0 for i in range(len(close_price))]
    tr_n = [0 for i in range(len(close_price))]
    vortex_plus = [0 for i in range(len(close_price))]
    vortex_minus = [0 for i in range(len(close_price))]
    for i in range(1, len(close_price)):
        vm_plus[i] = abs(high_price[i] - low_price[i-1])
        vm_minus[i] = abs(low_price[i] - high_price[i-1])
        tr[i] = max(high_price[i] - low_price[i], abs(high_price[i]-close_price[i-1]), abs(low_price[i]-close_price[i-1]))
        if i>=n:
            vm_plus_n[i] = sum(vm_plus[i-n+1:i+1])
            vm_minus_n[i] = sum(vm_minus[i-n+1:i+1])
            tr_n[i] = sum(tr[i-n+1:i+1])
            vortex_plus[i] = vm_plus_n[i]*1.0/tr_n[i]
            vortex_minus[i] = vm_minus_n[i]*1.0/tr_n[i]
    return vortex_plus, vortex_minus

