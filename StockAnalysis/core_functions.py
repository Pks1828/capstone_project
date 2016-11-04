import numpy as np

def simple_moving_average(data_points, n):
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


def exponential_moving_average(data_points, n):
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


def relative_strength_index(close_price, n):
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


def stochastic_oscillator(close_price, high_price, low_price, n):
    stoch = [0 for i in range(len(close_price))]
    for i in range(n-1, len(close_price)):
        llow = min(low_price[i-n+1:i+1])
        hhigh = max(high_price[i-n+1:i+1])
        print ("LOW: "+str(llow)+"; HIGH: "+str(hhigh))
        stoch[i] = (close_price[i] - llow)/(hhigh - llow) * 100.0
    return stoch


def aroon_oscillator(high_price, low_price, n):
    aroon = [0 for i in range(len(high_price))]
    for i in range(n-1, len(high_price)):
        llow = low_price[i-n+1:i+1].index(min(low_price[i-n+1:i+1]))
        hhigh = high_price[i-n+1:i+1].index(max(high_price[i-n+1:i+1]))
        print (str(llow)+";"+str(hhigh))
        aroon_low = 100.0*((llow+1)/n)
        aroon_high = 100.0*((hhigh+1)/n)
        aroon[i] = aroon_high - aroon_low
    return aroon


def commodity_channel_index(close_price, high_price, low_price, n):
    typical_price = [(close_price[i]+high_price[i]+low_price[i])/3.0 for i in range(len(close_price))]
    tp_sma = simple_moving_average(typical_price, 20)
    cci = [0 for i in range(len(close_price))]
    for i in range(n-1, len(typical_price)):
        mean = np.mean(typical_price[i-n+1:i+1])
        mean_deviation = 0.0
        for j in typical_price[i-n+1:i+1]:
            mean_deviation += abs(j-mean)
        mean_deviation = mean_deviation*1.0/n
        print (str(typical_price[i])+";"+str(tp_sma[i])+";"+str(mean_deviation))
        cci[i] = (typical_price[i] - tp_sma[i])/(0.015*mean_deviation)
    return cci


def williams_percentage_r(close_price, high_price, low_price, n):
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


def vortex(close_price, high_price, low_price, n):
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

