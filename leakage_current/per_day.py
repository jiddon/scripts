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
    print(df.columns)
    return df

def get_rod_data(name):
    df = pd.read_csv(name+'_HV_IMeas.csv', names=["Day", "Time", "HV_IMeas (mA)"], converters={'HV_IMeas (mA)':hv_round})
    return df

if __name__=="__main__":
    df = get_lumi_daily()

    dfs = []
    rods = ["LI_S05_C_M4", "LI_S01_C_M4", "LI_S11_A_M4", "LI_S13_C_M4"]
    for rod in rods:
        dfr = get_rod_data(rod)
        dfm = pd.merge(df, dfr, on='Day')
        dfs.append(dfm)

    ##boxplots
    for column in df.columns:
        plt.figure(figsize=(16,9))
        for n,df in enumerate(dfs):
            ax = plt.subplot(2, 2, n+1)
            ax.title.set_text(rods[n])
            ax = sns.boxplot(x=column, y="HV_IMeas (mA)", data=df, showfliers=False, fliersize=0.2, meanline=True)
            plt.tight_layout()
        plt.savefig("./plots/boxplots/HV_I_vs_"+column+".png")
        print(f"./plots/boxplots/HV_I_vs_{column}.png saved")
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


    # # max only regression
    # #for column in ['AvgMu', 'PeakMu']:#df.columns:
    # for column in df.columns:
    #     if column not in ["Fills"]:
    #         jps = []
    #         for n,df in enumerate(dfs):
    #             x_ = list(set(df[column].to_list()))
    #             y_ = []
    #             for x in x_:
    #                 df_col = df.loc[df[column] == x]
    #                 y_.append(df_col["HV_IMeas (mA)"].max())
    #             ### cut on low mu
    #             if column in ['AvgMu', 'PeakMu']:
    #                 x, y = zip(*((i, j) for i, j in zip(x_, y_) if i > 20))
    #                 g = sns.jointplot(x=x, y=y)
    #             else:
    #                 x = x_
    #                 y = y_
    #                 g = sns.jointplot(x=x, y=y)
    #             g.set_axis_labels(column, "HV_IMeas (mA)", fontsize=14)
    #             #r, p = stats.pearsonr(x, y)
    #             #g.ax_joint.annotate(f'$\\rho = {r:.3f}$',
    #             #                    xy=(0.1, 0.9), xycoords='axes fraction',
    #             #                    ha='left', va='center',
    #             #                    bbox={'boxstyle': 'round', 'fc': 'powderblue', 'ec': 'navy'})
    #             jps.append(g)
                
    #         fig = plt.figure(figsize=(16,9))
    #         gs = gridspec.GridSpec(2, 2)
    #         mg0 = sfg.SeabornFig2Grid(jps[0], fig, gs[0])
    #         mg1 = sfg.SeabornFig2Grid(jps[1], fig, gs[1])
    #         mg2 = sfg.SeabornFig2Grid(jps[2], fig, gs[3])
    #         mg3 = sfg.SeabornFig2Grid(jps[3], fig, gs[2])            
    #         gs.tight_layout(fig)
    #         plt.savefig("./plots/max_reg/HV_I_vs_"+column+".png")
    #         print(f"./plots/max_reg/HV_I_vs_{column}.png saved")
    #         plt.close()

    
