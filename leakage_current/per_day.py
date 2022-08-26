import matplotlib.pyplot as plt
import matplotlib.dates
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import seaborn as sns
import matplotlib.ticker as ticker
from datetime import datetime
import csv

def p2f(x):
    return float(x.strip('%'))/100

def get_lumi_daily():
    df = pd.read_csv('daytable.csv', encoding="utf-8", skipinitialspace=True, converters={'LStableRecPercent':p2f, 'LReadyRecPercent':p2f})
    df = df.rename(columns=lambda x: x.strip())
    print(df.columns)
    return df

def get_rod_data(name):
    df = pd.read_csv(name+'_HV_IMeas.csv', names=["Day", "Time", "HV_IMeas (mA)"])
    return df

if __name__=="__main__":
    df = get_lumi_daily()

    dfs = []
    rods = ["LI_S05_C_M4", "LI_S01_C_M4", "LI_S11_A_M4", "LI_S13_C_M4"]
    for rod in rods:
        dfr = get_rod_data(rod)
        dfm = pd.merge(df, dfr, on='Day')
        dfs.append(dfm)

    # boxplots
    # for column in df.columns:
    #     plt.figure(figsize=(16,9))
    #     for n,df in enumerate(dfs):
    #         ax = plt.subplot(2, 2, n+1)
    #         ax.title.set_text(rods[n])
    #         ax = sns.boxplot(x=column, y="HV_IMeas (mA)", data=df, showfliers=False, fliersize=0.2, meanline=True)
    #         plt.tight_layout()
    #     plt.savefig("./plots/boxplots/HV_I_vs_"+column+".png")
    #     print(f"./plots/boxplots/HV_I_vs_{column}.png saved")
    #     plt.close()

    # max only
    for column in df.columns:
        if column not in ["Fills"]:
            plt.figure(figsize=(16,9))
            for n,df in enumerate(dfs):
                xvalues = list(set(df[column].to_list()))
                #xvalues = [float(x) for x in xvalues_ if float(x) > 0]
                y = []
                for x in xvalues:
                    df_col = df.loc[df[column] == x]
                    y.append(df_col["HV_IMeas (mA)"].max())
                ax = plt.subplot(2, 2, n+1)
                ax.title.set_text(rods[n])
                ax = sns.scatterplot(x=xvalues, y=y)
                ax.set_xlabel(column, fontsize=14)
                ax.set_ylabel("HV_IMeas (mA)", fontsize=14)
                plt.tight_layout()
            plt.savefig("./plots/max_I/HV_I_vs_"+column+".png")
            print(f"./plots/max_I/HV_I_vs_{column}.png saved")
            plt.close()

    # # correlation matrix
    # cmap = sns.diverging_palette(230, 20, as_cmap=True)
    # for n,df in enumerate(dfs):
    #     plt.figure(figsize=(16,9))
    #     ax = plt.subplot()
    #     ax.title.set_text(rods[n])
    #     corr = df.corr()
    #     print(f"\nCorrelation for {rods[n]}:")
    #     print(corr["HV_IMeas (mA)"])
    #     sns.heatmap(corr, cmap=cmap, square=True, annot=True)
    #     bottom, top = ax.get_ylim()
    #     ax.set_ylim(bottom + 0.5, top - 0.5)
    #     plt.tight_layout()
    #     plt.savefig("./plots/corr/HV_I_"+rods[n]+".png")
    #     print(f"./plots/corr/HV_I_{rods[n]}.png saved")
    #     plt.close()
    
        
    
