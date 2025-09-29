import pandas as pd
from price_loaders.tradingview import load_asset_price

from datetime import date

def contractCloseData(contract):
    df = load_asset_price(contract, 10000, 'D')[['time', 'close']]
    df.time = df.time.apply(lambda x: date(x.year, x.month, x.day))
    return df

def marketSpreadYearFlag(longMonth, shortMonth, longExpYear, shortExpYear):
    expMonthToNum = {
        'U':  9,    # September
        'X':  11,   # November
        'F':  1,    # January
        'H':  3,    # March
        'K':  5,    # May
        'N':  7,    # Jul
        'Q':  8     # August
    }

    minYear = min(longExpYear, shortExpYear)
    maxYear = max(longExpYear, shortExpYear)

    maxMonth = max(expMonthToNum[longMonth], expMonthToNum[shortMonth])

    if (minYear == maxYear) and (maxMonth <= expMonthToNum['Q']): return f"{minYear-1}/{str(maxYear)[-2:]}"
    else:
        #print('erro') 
        if (minYear == longExpYear) and (expMonthToNum[longMonth] >= expMonthToNum['U']) and (expMonthToNum[shortMonth] <= expMonthToNum['Q']):
            return f"{maxYear-1}/{str(maxYear)[-2:]}"
        elif (minYear == shortExpYear) and (expMonthToNum[shortMonth] >= expMonthToNum['U']) and (expMonthToNum[longMonth] <= expMonthToNum['Q']):
            return f"{maxYear-1}/{str(maxYear)[-2:]}"
        else:
            return False

def calendarSpreadData(asset, longMonth, longExpYear, shortMonth, shortExpYear):
    if not (marketSpreadYearFlag(longMonth, shortMonth, longExpYear, shortExpYear)): "Please, input two contracts in the same market year"
    else: marketYear = marketSpreadYearFlag(longMonth, shortMonth, longExpYear, shortExpYear)

    long = contractCloseData(f"{asset}{longMonth}{longExpYear}")
    short = contractCloseData(f"{asset}{shortMonth}{shortExpYear}")

    DF = long.merge(short, on = 'time', suffixes = ('_long', '_short'))
    DF['spread'] = DF['close_long'] - DF['close_short']

    DF['marketYear'] = marketYear

    return DF