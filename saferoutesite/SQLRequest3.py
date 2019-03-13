import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import datetime as dt
import numpy as np
from time import mktime

def round2(num, digits = 6, up = True):
    m = 10**digits 
    num = num * m
    if up:
        num = np.ceil(num)
    else:
        num = np.floor(num)
    return num / m

def edge_to_latlon(edges):
    ret_dic = {}
    for i,edge in enumerate(edges):
        lat = (round2(edge[0][0], 4, False), round2(edge[1][0], 4))
        lon = (round2(edge[0][1], 4, False), round2(edge[1][1], 4))
        ret_dic[(tuple(sorted(lat)),tuple(sorted(lon)),i)] = edge
    return ret_dic


def DataConstructor(c, temp, precip, t_sens, p_sens, time_low = None, time_up = None, lat = None, lon = None):
    '''
    DOC
    '''
    where = ' WHERE DailyWeather.Precip <= ? AND DailyWeather.Precip >= ? '+\
    'AND DailyWeather.AverageTemp <= ? AND DailyWeather.AverageTemp >= ?'
    params = [precip + p_sens, precip - p_sens, temp + t_sens, temp - t_sens]
    if lat:
        select = 'SELECT CrimeData1.Day, CrimeData1.Primary_Type, CrimeData1.Block, '+\
        'CrimeData1.Latitude, CrimeData1.Longitude FROM DailyWeather '+\
        'JOIN CrimeData1 ON DailyWeather.Date = CrimeData1.Day'
        where += ' AND CrimeData1.Latitude >= ? AND CrimeData1.Latitude <= ?'+\
                  ' AND CrimeData1.Longitude >= ? AND CrimeData1.Longitude <= ?'
        where += ' AND CrimeData1.Hour >= ? AND CrimeData1.Hour <= ?'
        params += [*lat, *lon, time_low, time_up]
    else:
        select = 'SELECT Date FROM DailyWeather'
    return pd.read_sql(select + where, c, params = params)

SAFETY_DICT = {'BATTERY': 8, 'ROBBERY': 7, 'THEFT': 2, 'BURGLARY': 6,
       'ASSAULT': 6, 'CRIM SEXUAL ASSAULT': 10, 'KIDNAPPING': 9, 
               'SEX OFFENSE': 5, 'HOMICIDE': 10, 'INTIMIDATION': 3}

def Regression(weather, crimes, date):
    '''
    DOC
    '''
    weather['Score'] = crimes.groupby('Day').sum()['Primary_Type']
    weather['Score'] = weather['Score'].fillna(0)
    X = sm.add_constant(weather.Date)
    model = sm.OLS(weather.Score, X)
    results = model.fit()
    date = mktime(dt.strptime(date, '%Y-%m-%d').timetuple())
    return int(max(10**6 * results.params[0] + results.params[1]*date,1))


def Regression_List(list_of_blocks, temp, precip, t_sens, p_sens, date, time_low, time_up):
    '''
    Inputs:
        list of blocks: list of tuples in the form ((lat1,lon1),(lat2,lon2))
        temp: float
        precip: float
        t_sens: sensitivity of temperature (recommened +- 5)
        p_sens: sensitivity of precipitation 
        date: date to project to
        time_low: hour of minimum time considered 
        time_up: hour of maximum time considered
    Outputs: 
        ret_dic: dictionary connecting list_of_blocks to safety score
    '''
    blocks_dic = edge_to_latlon(list_of_blocks)
    blocks = list(blocks_dic.keys())
    lat = (min([block[0][0] for block in blocks]), max([block[0][1] for block in blocks]))
    lon = (min([block[1][0] for block in blocks]), max([block[1][1] for block in blocks]))
    c = sqlite3.connect("Crime.db")
    weather = DataConstructor(c, temp, precip, t_sens, p_sens).set_index('Date')
    crimes = DataConstructor(c, temp, precip, t_sens, p_sens, time_low, time_up, lat, lon)
    c.close()
    crimes['Primary_Type'] = crimes['Primary_Type'].map(SAFETY_DICT)
    weather = weather.sort_index()
    weather['Date'] = pd.to_datetime(weather.index).astype(np.int64) // 10**9
    ret_dic = {}
    for block in blocks: 
        crime = crimes[((crimes.Latitude >= block[0][0]) & (
            crimes.Latitude <= block[0][1]) & (crimes.Longitude >= block[1][0]) & (crimes.Longitude <= block[1][1]))]
        if len(crime) > 0:
            block_name = crime.groupby('Block').count().sort_values('Longitude', ascending = False).index[0]
            crime = crime[crime.Block == block_name]
        ret_dic[blocks_dic[block]] = Regression(weather, crime, date)
    return ret_dic