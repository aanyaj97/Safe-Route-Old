import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import datetime as dt
import numpy as np
from time import mktime

#c = sqlite3.connect("Crime.db")

def DataConstructor(c, temp, precip, t_sens, p_sens, time_low = None, time_up = None, block = None):
    '''
    DOC
    '''
    where = ' WHERE DailyWeather.Precip <= ? AND DailyWeather.Precip >= ? '+\
    'AND DailyWeather.AverageTemp <= ? AND DailyWeather.AverageTemp >= ?'
    params = [precip + p_sens, precip - p_sens, temp + t_sens, temp - t_sens]
    if block:
        select = 'SELECT CrimeData1.Day, CrimeData1.Primary_Type FROM DailyWeather '+\
        'JOIN CrimeData1 ON DailyWeather.Date = CrimeData1.Day'
        where += ' AND CrimeData1.Block = ? AND CrimeData1.Hour >= ? '+\
        'AND CrimeData1.Hour <= ?'
        params += [block, time_low, time_up]
    else:
        select = 'SELECT Date FROM DailyWeather'
    return pd.read_sql(select + where, c, params = params)

SAFETY_DICT = {'BATTERY': 8, 'ROBBERY': 7, 'THEFT': 2, 'BURGLARY': 6,
       'ASSAULT': 6, 'CRIM SEXUAL ASSAULT': 10, 'KIDNAPPING': 9, 
               'SEX OFFENSE': 5, 'HOMICIDE': 10, 'INTIMIDATION': 3}

def Regression(c, temp, precip, t_sens, p_sens, block, date, time_low, time_up):
    crimes = DataConstructor(c, temp, precip, t_sens, p_sens, time_low, time_up, block)
    weather = DataConstructor(c, temp, precip, t_sens, p_sens).set_index('Date')
    crimes['Primary_Type'] = crimes['Primary_Type'].map(SAFETY_DICT)
    weather['Score'] = crimes.groupby('Day').sum()['Primary_Type']
    weather['Score'] = weather['Score'].fillna(0)
    weather = weather.sort_index()
    weather['Date'] = pd.to_datetime(weather.index).astype(np.int64) // 10**9
    X = sm.add_constant(weather.Date)
    model = sm.OLS(weather.Score, X)
    results = model.fit()
    date = mktime(dt.strptime(date, '%Y-%m-%d').timetuple())
    return results.params[0] + results.params[1]*date

#c.close()

