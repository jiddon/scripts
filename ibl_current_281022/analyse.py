import csv
import math
import numpy as np
import pandas as pd
import scipy.stats as stats
from functools import reduce
from datetime import datetime
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import os

import atlas_mpl_style as ampl
ampl.use_atlas_style()

def get_lumi_daily():
    """
    get lumi per day
    LStableDel is delivered stable lumi (pb^-1)
    """
    dateparse = lambda x: datetime.strptime(x, '%y%m%d')
    df = pd.read_csv('./daytable.csv', parse_dates=['Day'], date_parser=dateparse)
    _lumi_del = reversed(df[' LStableDel'].to_list())
    lumi_del = []
    sum_so_far = 0
    for l in _lumi_del:
        sum_so_far = l + sum_so_far
        lumi_del.append(sum_so_far)
    lumi_del.reverse()
    df['LSum'] = lumi_del
    return df

def get_lumi_lut():
    dfl = get_lumi_daily()
    df_lumi_lut = dfl.filter(['Day', 'LSum'], axis=1)
    
    days = df_lumi_lut['Day'].to_list()
    sums = df_lumi_lut['LSum'].to_list()    
    lumi_lut = {}
    for n,i in enumerate(days):
        lumi_lut[i] = sums[n]

    df_time_lut = dfl.filter(['LSum', 'Day'], axis=1)
    days = df_time_lut['Day'].to_list()
    sums = df_time_lut['LSum'].to_list()    
    time_lut = {}
    for n,i in enumerate(sums):
        time_lut[i] = days[n]
    return dfl, lumi_lut, time_lut
    

    
def normalise(dfo, col):
    result = pd.DataFrame()
    mods = list(set(dfo['mod'].to_list()))
    for n,mod in enumerate(mods):
        #df = df.groupby(df['mod'])
        df = dfo[dfo['mod'] == mod]
        max_value = df[col].max()
        _df_baseline = df[df['time'] < datetime(2022, 7, 6)]
        df_baseline = _df_baseline[_df_baseline['time'] > datetime(2022, 6, 27)]
        min_value = df_baseline[col].min()
        df[col] = (df[col] - min_value) / (max_value - min_value)
        if n == 0:
            result = df
        else:
            result = result.append(df)

    return result

def p2f(x):
    return float(x.strip('%'))/100

def mu_round(x):
    base = 1
    return base * round(float(x)/base)

def hv_round(x):
    return round(float(x),2)

def get_rod_data(name, meas):
    df = pd.read_csv('./dcs_csv/'+name+'_'+meas+'.csv', names=["Day", meas], converters={meas:hv_round})
    return df

def read_csv_to_df(path):
    df = pd.read_csv(path, names=["time", "value"],  parse_dates=['time'])
    return df

def get_dfs_from_paths(directory):
    df = pd.DataFrame()
    for n,filename in enumerate(os.listdir(directory)):
        p = os.path.join(directory, filename)
        if os.path.isfile(p):
            dfi = read_csv_to_df(p)
            dfi['mod'] = filename.replace("_PP4LV.csv", "")
            df = df.append(dfi, ignore_index=True)
        else:
            raise FileNotFoundError()
    return df

def llines(df, x, value):
    """
    line plot as a function of x for all modules
    """
    _df = df.sort_values(by=x)
    mods = list(set(_df['mod'].to_list()))
    
    fig = go.Figure()
    for mod in mods:
        df = _df[_df['mod'] == mod]
        fig.add_trace(go.Scatter(x=df[x], y=df[value],
                                 mode='lines+markers',
                                 name=mod))
    fig.write_html(value+".html")
    fig.show()

def get_df_hv_on(_df):
    hv = pd.read_csv('hv.csv', names=["time", "hv"],  parse_dates=['time'])
    hv['hv'] = np.where(hv['hv'] > 449, 1, 0) # 1 is HV on

    #_df.drop(_df[_df['value'] < 1.5].index, inplace=True) # require current to be greater than cut
    
    _df.sort_values(by="time", inplace=True, ignore_index=True)
    hv.sort_values(by="time", inplace=True, ignore_index=True)
    
    # change datetime in _df to be equal to the closest datetime in hv
    _df = pd.merge_asof(_df, hv, on="time", direction="nearest")
    # reduce df to only hv on 
    df_hvon = _df[_df['hv'] == 1]
    
    # normalise to base 
    #df_hvon = normalise(_df_hvon, 'value')
    return df_hvon

def lllines(df_hvon, x, value):
    """
    line plot as a function of x for all modules
    """
    mods = list(set(df_hvon['mod'].to_list()))
    fig = go.Figure()
    print(df_hvon)
    for n,mod in enumerate(mods):
        if n >= 0: # debug 
            df = df_hvon[df_hvon['mod'] == mod]
            if x != 'time':
                dft = df.groupby(df[x])["value"].max()
            else:
                dft = df.groupby(df[x].dt.date)["value"].max()
                
            dft = dft.reset_index()
            
            fig.add_trace(go.Scatter(x=dft[x], y=dft[value],
                                     mode='lines+markers',
                                     name=mod))
    fig.write_html(value+".html")
    fig.show()

def plot_box(df_hvon, time_lut, x='time'):
    """ mean of each day """
    badtime =  [ # monitoring scans 
        "2022-07-07 12", "2022-07-07 13",
        "2022-07-12 11", "2022-07-12 12", "2022-07-12 13", "2022-07-12 14", "2022-07-12 15", "2022-07-12 16", "2022-07-12 17", "2022-07-12 18", "2022-07-12 19",
        "2022-07-13 10", "2022-07-13 11", "2022-07-13 12",
        "2022-07-31 11", "2022-07-31 12", "2022-07-31 13",
        "2022-08-05 12", "2022-08-05 13",
        "2022-08-05 16", "2022-08-05 17",
        "2022-08-22 14", "2022-08-22 15",
        "2022-08-23 15", "2022-08-23 16",
        "2022-08-25 16", "2022-08-25 17",
        "2022-08-26 09", "2022-08-26 10",
        "2022-09-28 11", "2022-09-28 12", "2022-09-28 13", "2022-09-28 14",
        "2022-10-10 20",
        "2022-10-12 11", "2022-10-12 12", "2022-10-12 13", "2022-10-12 14",
        "2022-10-18 10",
        "2022-10-23 15", "2022-10-23 16",
        "2022-10-26 14"
    ]
    badday = [
        "2022-10-06", #
        "2022-10-19", # broken optoboard day
    ]
    
    mods = list(set(df_hvon['mod'].to_list()))
    dfm = pd.DataFrame()
    dfdm = pd.DataFrame()
    for n,mod in enumerate(mods):
        df = df_hvon[df_hvon['mod'] == mod]
        if x != 'time':
            df['time'] = df['lumi'].map(time_lut)
        df = df[~df['time'].dt.strftime("%Y-%m-%d %H").isin(badtime)]
        df = df[~df['time'].dt.strftime("%Y-%m-%d").isin(badday)]

        if x != 'time':
            dft = df.groupby(df[x])["value"].max()
        else:
            dft = df.groupby(df[x].dt.strftime("%Y-%m-%d %H"))["value"].max() # every hour
        dft = dft.reset_index()

        if x != 'time':
            dfd = df.groupby(df[x])["value"].max() # every day
        else:
            dfd = df.groupby(df[x].dt.strftime("%Y-%m-%d"))["value"].max() # every day
        dfd = dfd.reset_index()
        if n == 0:
            dfm = dft
            dfdm = dfd
        else:
            dfm = dfm.append(dft)
            dfdm = dfdm.append(dfd)

    if x == 'time':
        dfm['time'] = pd.to_datetime(dfm['time'])
        dfdm['time'] = pd.to_datetime(dfdm['time'])
    
    dfm = dfm.sort_values(by=x)
    dfdm = dfdm.sort_values(by=x)
    
    dfmm = dfm.groupby(x).mean()
    dfmm = dfmm.reset_index()
  
    dfdmm = dfdm.groupby(x).mean()
    dfdmm = dfdmm.reset_index()

    # if x != 'time':
    #     sns.boxplot(data=dfm, x=x, y="value", meanline=True)
    # else:
    #     sns.boxplot(data=dfdm, x=x, y="value", meanline=True)
        
    #sns.scatterplot(data=dfm, x=x, y="value", s=2, alpha=0.4)
    
    #sns.scatterplot(data=dfdmm, x="time", y="value", s=3, color='k')

    #badtime = ["2022-08-18", "2022-10-06", "2022-10-17", "2022-10-18", "2022-10-19"]
    #dfdmm = dfdmm[~dfdmm[x].isin(badtime)]
    
    #plt.plot(dfdmm[x], dfdmm['value'], color='k')
    #sns.boxplot(data=dfdm, x="time", y="value", meanline=True)
    
    #plt.ylim(1.0, 2.4)
    #plt.show()

    return dfm


def kde(df):
    fig, axes = plt.subplots(figsize=(10,10))#, sharey=True)
    mods = list(set(df['mod'].to_list()))
    for n,mod in enumerate(mods):
        dfs = df[df['mod'] == mod]
        dfs['value'].plot.kde(ax=axes, legend=False)
    plt.show()


def dist(df, lumi_lut, x='time'):
    dfm = df.groupby(x).agg({'value': ['mean', 'std', 'sem']})
    dfm = dfm.xs('value', axis=1, drop_level=True)
    dfm = dfm.reset_index(x)
    dfm.rename(columns={"mean":"value"}, inplace=True)
    #dfm = dfm[dfm['value'] > 1.6]
    dfm['time'] = dfm['lumi'].map(lumi_lut)
    dfm['lumi'] = dfm['lumi'].divide(1e3)

    dfma = dfm[dfm['time'] < datetime(2022,8,22)]
    dfmb = dfm[dfm['time'] > datetime(2022,9,28)]
    print(dfmb.to_string())

    min_lumi = 0
    if plot_change:
        min_lumi = dfmb['lumi'].min()

    frmt = 'none'

    fig, ax = plt.subplots()
    p0 = ax.fill_between(x=dfm[x], y1=dfm['value']-dfm['std'], y2=dfm['value']+dfm['std'], color='k', alpha=0.2, step='mid')
    p1 = ax.plot(dfm[x], dfm['value'], marker='o', color='k', markersize=4, linestyle="")
    p2 = ax.errorbar(x=dfm[x], y=dfm['value'], yerr=dfm['sem'], fmt=frmt, marker='x', color='k', capsize=0.1)        
    ax.legend([p0, p1, p2], ['1$\sigma$', 'mean', 'sem'], loc='lower right', fancybox=True)
    
    if plot_change:
        ampl.set_xlabel("Cumulative integrated luminosity since base($fb^{-1}$)")
    else:
        ampl.set_xlabel("LHC delivered integrated luminosity ($fb^{-1}$)")
    ampl.set_ylabel("PP4LV_I (A)")
    plt.savefig("./plots/I-vs-lumi.pdf")
    plt.savefig("./plots/I-vs-lumi.png")
    plt.show()

    return dfm



def plot_lumi(df):
    """
    plot total lumi to cross check with official plots.
    """
    df.plot('time', 'lumi')
    plt.show()
    


        
if __name__=="__main__":
    dfo = get_dfs_from_paths('dcs_csv')
    dfl, lumi_lut, time_lut = get_lumi_lut()
    df = get_df_hv_on(dfo)
    df['lumi'] = df['time'].dt.date.map(lumi_lut)
    print("Removing the following rows since lumi is undefined:")
    print(df[df['lumi'].isnull()])
    print("leaving:")
    df = df[df['lumi'].notnull()] 
    print(df)

    
    #plot_lumi(df)
    #lllines(df, 'lumi', 'value')
    x = 'lumi'
    dfm = plot_box(df, time_lut, x=x) 
    dfr = dist(dfm, time_lut, x=x)
    #dfr = dist(dfm, time_lut, x=x, plot_change=False, same_canvas=False, same_plot=False)
    
