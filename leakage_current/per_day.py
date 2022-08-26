import matplotlib.pyplot as plt
import matplotlib.dates
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import seaborn as sns
import matplotlib.ticker as ticker
from datetime import datetime
import csv

def get_lumi_daily():
    df = pd.read_csv('daytable.csv')
    df = df.rename(columns=lambda x: x.strip())
    return df

def get_rod_data(name):
    df = pd.read_csv(name+'_HV_IMeas.csv', names=["Day", "Time", "HV_IMeas (mA)"])
    return df

def fmt(s):
    try:
        if float(s) > 0.1:
            n = "{:.2f}".format(float(s))
        else:
            n = "{:.2e}".format(float(s))
    except:
        n = ""
    return n


if __name__=="__main__":
    df = get_lumi_daily()

    dfs = []
    rods = ["LI_S05_C_M4", "LI_S01_C_M4", "LI_S11_A_M4", "LI_S13_C_M4"]
    for rod in rods:
        dfr = get_rod_data(rod)
        dfm = pd.merge(df, dfr, on='Day')
        dfs.append(dfm)

    for column in df.columns:
        plt.figure(figsize=(16,9))
        for n,df in enumerate(dfs):
            ax = plt.subplot(2, 2, n+1)
            ax.title.set_text(rods[n])
            ax = sns.boxplot(x=column, y="HV_IMeas (mA)", data=df, showfliers=False, fliersize=0.2, meanline=True)
            n = 7  # Keeps every 7th label
            [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
            plt.tight_layout()
        plt.savefig("HV_I_vs_"+column+".png")
        print(f"./plots/HV_I_vs_{column}.png saved")
    
        
    
