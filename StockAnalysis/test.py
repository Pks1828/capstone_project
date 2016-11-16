def carryover(signals_in, n=4):
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


signals = [0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, -1, 0, 1, -1, 0]
a = carryover(signals, 2)
print (signals)
print (a)