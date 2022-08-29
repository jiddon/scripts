import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import seaborn as sns; sns.set()
import matplotlib.ticker as ticker
from datetime import datetime
import csv
import seaborn_subplots as sfg
import scipy.stats as stats

def p2f(x):
    return float(x.strip('%'))/100

def mu_round(x):
    base = 1
    return base * round(float(x)/base)
    #return round(float(x))

def hv_round(x):
    return round(float(x),2)

def get_lumi_daily():
    df = pd.read_csv('daytable.csv', encoding="utf-8", skipinitialspace=True, converters={'LStableRecPercent':p2f, 'LReadyRecPercent':p2f, 'AvgMu':mu_round, 'PeakMu':mu_round})
    df = df.rename(columns=lambda x: x.strip())
    return df

def get_rod_data(name):
    df = pd.read_csv(name+'_HV_IMeas.csv', names=["Day", "Time", "HV_IMeas (mA)"], converters={'HV_IMeas (mA)':hv_round})
    return df

if __name__=="__main__":
    CORR_CUT = 0.5
    
    df = get_lumi_daily()
    dfs = []
    rods = ["LI_S05_C_M4"]#, "LI_S01_C_M4", "LI_S11_A_M4", "LI_S13_C_M4"]
    for rod in rods:
        dfr = get_rod_data(rod)
        dfm = pd.merge(df, dfr, on='Day')
        dfs.append(dfm)
    print(df.columns)
    columns = df.columns.values.tolist()
    columns.remove('Fills')

    # correlation matrix
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    for n,df in enumerate(dfs):
        corr = df.corr()
        print(f"\nCorrelation for {rods[n]}:")
        print(corr)
        for col in columns:
            print("\n---------------------------------")
            print(col)
            print("---------------------------------")
            df_corr = corr.loc[corr[col] > CORR_CUT]
            print(df_corr[col].sort_values(ascending=False))


