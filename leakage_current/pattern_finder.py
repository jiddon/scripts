import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import seaborn as sns; sns.set()
import matplotlib.ticker as ticker
import csv
import fire
import seaborn_subplots as sfg
import scipy.stats as stats
from functools import reduce
from functools import reduce

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

def get_rod_data(name, meas):
    df = pd.read_csv(name+'_'+meas+'.csv', names=["Day", "Time", meas], converters={meas:hv_round})
    return df

def plot_correlations(corr_dict, OBSERVABLES, df, rodname):
    """
    Plot boxplot for OBSERVABLES whose correlation coefficient exceeds CORR_CUT.
    """
    for k in corr_dict.keys():
        if k in OBSERVABLES:
            for i in corr_dict[k]:
                plt.figure(figsize=(16,9))
                ax = plt.subplot()
                ax.title.set_text(rodname)
                ax = sns.boxplot(x=i, y=k, data=df, showfliers=False, fliersize=0.2, meanline=True)
                r, p = stats.pearsonr(df[i], df[k])
                plt.tight_layout()
                ax.annotate(f'$\\rho = {r:.3f}$',
                            xy=(0.1, 0.9), xycoords='axes fraction',
                            ha='left', va='center',
                            bbox={'boxstyle': 'round', 'fc': 'powderblue', 'ec': 'navy'})
                plt.savefig("./plots/correlations/"+rodname+"_"+k+"_vs_"+i+".png")
                print(f"./plots/correlations/"+rodname+"_"+k+"_vs_"+i+".png")
                plt.close()

def get_corr_dict(df, columns, OBSERVABLES, CORR_CUT):
    """
    Print correlation matrix for OBSERVABLES whose correlation coefficient exceeds CORR_CUT.
    Returns corr_dict, a dict with key OBSERVABLES and value of list containing names of 
    correlations greater than CORR_CUT. 
    """
    corr_dict = {col:None for col in columns}
    corr = df.corr()
    for col in columns:
        if col in OBSERVABLES:
            print("\n---------------------------------")
            print(col)
            print("---------------------------------")
            df_corr = corr.loc[corr[col] > CORR_CUT]
            print(corr[col].sort_values(ascending=False))
            corr_dict[col] = df_corr[col].index.tolist()
            corr_dict[col].remove(col)
    return corr_dict

def find_corr(rod, obs, plot=True, corr_cut=0.7, verbose=False):
    """
    Calculate correlation coefficients for specified observable.
    Rod name and observable of interest are required arguments.
    e.g. --rod LI_S01_C_M4 --obs HV_IMeas
    """
    PLOT = plot # want to see plots? 
    CORR_CUT = corr_cut # correlation coefficient cut. above this, we are interested
    OBSERVABLES = obs # for which observables do we want to see the results?
    
    data_frames = []
    data_frames.append(get_lumi_daily())
    data_frames.append(get_rod_data(rod, 'HV_IMeas'))
    data_frames.append(get_rod_data(rod, 'TModule'))
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Day'],
                                                    how='inner'), data_frames)
    if verbose:
        print(df_merged)
        
    columns = df_merged.columns.values.tolist()
    columns.remove('Fills')
    columns.remove('Time_x')
    columns.remove('Time_y')

    # correlation matrix
    corr_dict = get_corr_dict(df_merged, columns, OBSERVABLES, CORR_CUT)
    if PLOT:
        plot_correlations(corr_dict, OBSERVABLES, df_merged, rod)


if __name__=="__main__":
    fire.Fire(find_corr)
