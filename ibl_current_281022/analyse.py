import csv
import numpy as np
import pandas as pd
import scipy.stats as stats
from functools import reduce
from datetime import datetime
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import os

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
            msg = f"File {f} does not exist!"
            raise FileNotFoundError(msg)
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
        fig.add_trace(go.Scatter(x=df['time'], y=df[value],
                                 mode='lines+markers',
                                 name=mod))
    fig.write_html(value+".html")
    fig.show()

def get_df_hv_on(_df):
    hv = pd.read_csv('hv.csv', names=["time", "hv"],  parse_dates=['time'])
    hv['hv'] = np.where(hv['hv'] > 449, 1, 0) # 1 is HV on
    
    _df.sort_values(by="time", inplace=True, ignore_index=True)
    hv.sort_values(by="time", inplace=True, ignore_index=True)
    
    # change datetime in _df to be equal to the closest datetime in hv
    _df = pd.merge_asof(_df, hv, on="time", direction="nearest")
    # reduce df to only hv on 
    df_hvon = _df[_df['hv'] == 1]
    
    # normalise to base 
    #df_hvon = normalise(_df_hvon, 'value')
    return df_hvon

def lllines(df_hvon, value):
    """
    line plot as a function of x for all modules
    """
    mods = list(set(df_hvon['mod'].to_list()))
    fig = go.Figure()
    print(df_hvon)
    for n,mod in enumerate(mods):
        if n >= 0: # debug 
            df = df_hvon[df_hvon['mod'] == mod]
            dft = df.groupby(df["time"].dt.date)["value"].max()
            dft = dft.reset_index()
            
            fig.add_trace(go.Scatter(x=dft['time'], y=dft[value],
                                     mode='lines+markers',
                                     name=mod))
    fig.write_html(value+".html")
    fig.show()

def plot_mean(df_hvon):
    mods = list(set(df_hvon['mod'].to_list()))
    dfm = pd.DataFrame()
    for n,mod in enumerate(mods):
        df = df_hvon[df_hvon['mod'] == mod]
        dft = df.groupby(df["time"].dt.date)["value"].max()
        dft = dft.reset_index()
        if n == 0:
            dfm = dft
        else:
            dfm = dfm.append(dft)
    dfm = dfm.sort_values(by='time')
    print(dfm)
    dfmm = dfm.groupby(dfm["time"].dt.date)["value"].mean()
    dfmm.plot(x='time', y='value')
    plt.show()
    return dfmm

def kde(df):
    fig, axes = plt.subplots(figsize=(10,10))#, sharey=True)
    mods = list(set(df['mod'].to_list()))
    for n,mod in enumerate(mods):
        dfs = df[df['mod'] == mod]
        dfs['value'].plot.kde(ax=axes, legend=False)
    plt.show()
    
        
if __name__=="__main__":
    dfo = get_dfs_from_paths('dcs_csv')
    df = get_df_hv_on(dfo)
    #lllines(df, 'value')
    plot_mean(df)
    
    #kde(df)
    
