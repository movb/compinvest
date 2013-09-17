'''
@author: Mikhail Plekhanov
@contact: mike.plekhanov@gmail.com
@summary: Homework Assigment 1 for course Computational Investing I.
'''

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

print "Pandas Version", pd.__version__

def simulate(statdate,enddate,symbols,portfolio):
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(statdate, enddate, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Filling the data for NAN
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    # Getting the numpy ndarray of close prices.
    na_price = d_data['close'].values

    # Normalizing the prices to start at 1 and see relative returns
    na_normalized_price = na_price / na_price[0, :]    

    # Copy the normalized prices to a new ndarry to find returns.
    na_rets = na_normalized_price.copy()

    # Calculate the daily returns of the prices. (Inplace calculation)
    # returnize0 works on ndarray and not dataframes.
    tsu.returnize0(na_rets)
    
    average_daily_returns = dict()
    volatility = dict()
    symbol_index = dict()
    
    pf_adr = 0
    pf_vol = 0
    pf_sr  = 0
    pf_cr  = 0
    
    i = 0
    for symbol in symbols:
        average_daily_returns[symbol] = sum(na_rets[:,i])/len(na_rets)
        volatility[symbol] = np.std(na_rets[:,i])
        symbol_index[symbol] = i
        
        pf_adr += average_daily_returns[symbol] * portfolio[i]
        pf_vol += volatility[symbol] * portfolio[i]
        pf_sr += average_daily_returns[symbol]/volatility[symbol]*math.sqrt(len(na_rets)) * portfolio[i]
        
        i+=1
        
    print "Period length: {0}".format(len(na_rets))        
    
    print "Average daily returns:"
    for symbol in symbols:
        print "{0} : {1}".format(symbol, average_daily_returns[symbol])
        
    print "Volatility:"
    for symbol in symbols:
        print "{0} : {1}".format(symbol, volatility[symbol])
        
    print "Sharpe Ratio:"
    for symbol in symbols:
        print "{0} : {1}".format(symbol, average_daily_returns[symbol]/volatility[symbol]*math.sqrt(len(na_rets)))        
        
    print "Summary:"
    print "Sharpe Ratio: {0}".format(pf_sr)
    print "Volatility: {0}".format(pf_vol)
    print "Average Daily Return: {0}".format(pf_adr)
        
    
def main():
    ''' Main Function'''

    # List of symbols
    # ls_symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT'] # HW1 assigment data
    ls_symbols = ['AAPL', 'GLD', 'GOOG', 'XOM'] # Example 1
    # ls_symbols = ['AXP', 'HPQ', 'IBM', 'HNZ'] # Example 2

    # Start and End date of the charts
    dt_start = dt.datetime(2011, 1, 1)
    dt_end = dt.datetime(2011, 12, 31)
    
    portfolio = [0.4,0.4,0.0,0.2] # example 1
    # portfolio = [0.0,0.0,0.0,1.0] # example 2

    simulate(dt_start,dt_end,ls_symbols,portfolio)
    

if __name__ == '__main__':
    main()
