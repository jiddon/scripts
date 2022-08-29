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
    df = pd.read_csv(name+'_HV_IMeas.csv', names=["Day", "Time", "HV_IMeas-mA"], converters={'HV_IMeas-mA':hv_round})
    return df

def plot_correlations(corr_dict, OBSERVABLES, df):
    for k in corr_dict.keys():
        if k in OBSERVABLES:
            for i in corr_dict[k]:
                plt.figure(figsize=(16,9))
                ax = plt.subplot()
                ax.title.set_text(rods[n])
                ax = sns.boxplot(x=i, y=k, data=df, showfliers=False, fliersize=0.2, meanline=True)
                r, p = stats.pearsonr(df[i], df[k])
                plt.tight_layout()
                ax.annotate(f'$\\rho = {r:.3f}$',
                            xy=(0.1, 0.9), xycoords='axes fraction',
                            ha='left', va='center',
                            bbox={'boxstyle': 'round', 'fc': 'powderblue', 'ec': 'navy'})
                plt.savefig("./plots/correlations/"+k+"_vs_"+i+".png")
                print(f"./plots/correlations/"+k+"_vs_"+i+".png")
                plt.close()


if __name__=="__main__":
    PLOT = True # want to see plots? 
    CORR_CUT = 0.8 # correlation coefficient cut. above this, we are interested
    OBSERVABLES = ['HV_IMeas-mA'] # for which observables do we want to see the results
    
    df = get_lumi_daily()
    dfs = []
    rods = ["LI_S05_C_M4"]#, "LI_S01_C_M4", "LI_S11_A_M4", "LI_S13_C_M4"]
    for rod in rods:
        dfr = get_rod_data(rod)
        dfm = pd.merge(df, dfr, on='Day')
        dfs.append(dfm)
    print(df.columns)
    columns = dfm.columns.values.tolist()
    columns.remove('Fills')
    columns.remove('Time')

    # correlation matrix
    corr_dict = {col:None for col in columns}
    for n,df in enumerate(dfs):
        corr = df.corr()
        print(f"\nCorrelation for {rods[n]}:")
        print(corr)
        for col in columns:
            if col in OBSERVABLES:
                print("\n---------------------------------")
                print(col)
                print("---------------------------------")
                df_corr = corr.loc[corr[col] > CORR_CUT]
                print(df_corr[col].sort_values(ascending=False))
                corr_dict[col] = df_corr[col].index.tolist()
                corr_dict[col].remove(col)
        if PLOT:
            plot_correlations(corr_dict, OBSERVABLES, df)


