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

def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

def getdata(startdate,enddate,symbols):
    # We need closing prices so the timestamp should be hours=16.
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    ldt_timestamps = du.getNYSEdays(startdate, enddate, dt_timeofday)

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
    
    return na_rets

def simulate(na_rets,portfolio):    
    na_portrets = np.sum(na_rets * portfolio, axis=1)
    na_port_total = np.cumprod(na_portrets + 1)
    na_component_total = np.cumprod(na_rets + 1, axis=0)
    
    days_in_year = len(na_portrets)
    # days_in_year = 250
    
    pf_adr = sum(na_portrets)/days_in_year
    pf_vol = np.std(na_portrets)
    pf_sr = pf_adr/pf_vol * math.sqrt(days_in_year)
    pf_cr = na_port_total[-1]
    
    return pf_adr,pf_vol,pf_sr,pf_cr


def findallocation(na_rets):    
    max_alloc = []
    max_sr = 0
    max_vol = 0
    max_adr = 0
    max_cr = 0
    
    for i1 in range(0,11):
        for i2 in range(0,11-i1):
            for i3 in range(0,11-i1-i2):
                for i4 in range(0,11-i1-i2-i3):
                    if i1+i2+i3+i4==10:
                        pf_adr,pf_vol,pf_sr,pf_cr = simulate(na_rets,[i1/10.0,i2/10.0,i3/10.0,i4/10.0])
                        if pf_sr>max_sr:
                            max_sr = pf_sr
                            max_vol = pf_vol
                            max_adr = pf_adr
                            max_cr = pf_cr
                            max_alloc = [i1/10.0,i2/10.0,i3/10.0,i4/10.0]
    
    return max_sr,max_vol,max_adr,max_cr,max_alloc
    
def main():
    ''' Main Function'''

    # List of symbols
    #ls_symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT'] # HW1 assigment data 1
    ls_symbols = ['BRCM', 'TXN', 'IBM', 'HNZ']  # HW1 assigment data 2
    #ls_symbols = ['AAPL', 'GLD', 'GOOG', 'XOM'] # Example 1
    #ls_symbols = ['AXP', 'HPQ', 'IBM', 'HNZ'] # Example 2

    # Start and End date of the charts
    dt_start = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)
    
    #portfolio = [0.4,0.4,0.0,0.2] # example 1
    #portfolio = [0.0,0.0,0.0,1.0] # example 2

    # simulate(dt_start,dt_end,ls_symbols,portfolio)
    
    na_rets = getdata(dt_start,dt_end,ls_symbols)
    pf_sr,pf_vol,pf_adr,pf_cr,pf_alloc = findallocation(na_rets)
    
    print "Start Date: {0}".format(dt_start)
    print "End Date: {0}".format(dt_end)
    print "Symbols: {0}".format(ls_symbols)
    print "Optimal Allocation: {0}".format(pf_alloc)
    print "Sharpe Ratio: {0}".format( pf_sr )
    print "Volatility: {0}".format( pf_vol )
    print "Average Daily Return: {0}".format( pf_adr )
    print "Cumulative Return: {0}".format( pf_cr )
    

if __name__ == '__main__':
    main()
