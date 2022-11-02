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
    #hv['hv'] = np.where(hv['hv'] < 0.2, 1, 0) # 1 is HV off

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

    ## for standby:
    # badday= [
    #     "2022-07-28", # HV interlock
    #     "2022-08-01", # HV interlock
    #     "2022-08-07", #
    #     "2022-08-14", # HV interlock
    #     "2022-08-17", # thermosiphon trip
    #     "2022-10-21", #
    #     "2022-10-23", # HV interlock
    #     "2022-10-26", # HV interlock
    # ]
    
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
        dft['mod'] = mod[-2:]
        if n == 0:
            dfm = dft
        else:
            dfm = dfm.append(dft)

    if x == 'time':
        dfm['time'] = pd.to_datetime(dfm['time'])
    
    dfm = dfm.sort_values(by=x)

    return dfm


def dist(df, lumi_lut, x='time'):
    dfm = df.groupby(x).agg({'value': ['mean', 'std', 'sem']})
    dfm = dfm.xs('value', axis=1, drop_level=True)
    dfm = dfm.reset_index(x)
    dfm.rename(columns={"mean":"value"}, inplace=True)
    #dfm = dfm[dfm['value'] > 1.6]
    if x != 'time':
        dfm['time'] = dfm['lumi'].map(lumi_lut)
        dfm['lumi'] = dfm['lumi'].divide(1e3)

    frmt = 'none'

    print(dfm.to_string())
    
    fig, ax = plt.subplots()
    p0 = ax.fill_between(x=dfm[x], y1=dfm['value']-dfm['std'], y2=dfm['value']+dfm['std'], color='k', alpha=0.2, step='mid')
    p1 = ax.plot(dfm[x], dfm['value'], marker='o', color='k', markersize=4, linestyle="")
    p2 = ax.errorbar(x=dfm[x], y=dfm['value'], yerr=dfm['sem'], fmt=frmt, marker='x', color='k', capsize=0.1)        
    ax.legend([p0, p1, p2], ['1$\sigma$', 'mean', 'sem'], loc='lower right', fancybox=True)
    
    ampl.set_xlabel("LHC delivered integrated luminosity ($fb^{-1}$)")
    ampl.set_ylabel("PP4LV_I (A)")
    plt.savefig("./plots/I-vs-lumi.pdf")
    plt.savefig("./plots/I-vs-lumi.png")
    plt.show()

    return dfm


def dist_per_mod(df, lumi_lut, x='time'):
    mods = list(set(df['mod']))
    fig, ax = plt.subplots()
    colors = ['k', 'b', 'r', 'c']
    dfs = pd.DataFrame()
    for n,m in enumerate(mods):
        _df = df[df['mod'] == m]
        dfm = _df.groupby(x).agg({'value': ['mean', 'std', 'sem']})
        dfm = dfm.xs('value', axis=1, drop_level=True)
        dfm = dfm.reset_index()
        dfm.rename(columns={"mean":"value"}, inplace=True)
        #dfm = dfm[dfm['value'] > 1.6]
        dfm['time'] = dfm['lumi'].map(lumi_lut)
        dfm['lumi'] = dfm['lumi'].divide(1e3)
        dfm['mod'] = int(m[-1])
        dfs = dfs.append(dfm)
        
        
        frmt = 'none'        
        #p0 = ax.fill_between(x=dfm[x], y1=dfm['value']-dfm['std'], y2=dfm['value']+dfm['std'], color='k', alpha=0.2, step='mid')
        ax.plot(dfm[x], dfm['value'], marker='o', markersize=4, label=m, color=colors[n])
        ax.errorbar(x=dfm[x], y=dfm['value'], yerr=dfm['sem'], fmt=frmt, marker='x', capsize=3, color=colors[n])        

    ax.legend(loc='lower right', fancybox=True)    
    ampl.set_xlabel("Run 3 LHC delivered integrated luminosity ($fb^{-1}$)")
    ampl.set_ylabel("PP4LV_I (A)")
    plt.savefig("./plots/I-vs-lumi_per_mod.pdf")
    plt.show()

    print(dfs)
    # fig, ax = plt.subplots(2,2)
    # for n,m in enumerate(range(1,5)):
    #     ax[n//2, n%2] =
    
    fig, ax = plt.subplots()
    for n,m in enumerate(range(1,5)):
        dfsm = dfs[dfs['mod'] == m] 
        ax.hist(dfsm['value'], label="M"+str(m), color=colors[n], alpha=0.2, bins=50)
    ax.legend(loc='upper right', fancybox=True)    
    ampl.set_xlabel("PP4LV_I (A)")
    ampl.set_ylabel("Frequency")
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
    dist(dfm, time_lut, x=x)
    dist_per_mod(dfm, time_lut, x=x)

    # x = 'time'
    # dfm = plot_box(df, lumi_lut, x=x) 
    # dist(dfm, lumi_lut, x=x)


    #dfr = dist(dfm, time_lut, x=x, plot_change=False, same_canvas=False, same_plot=False)
    
