import csv
import fire
import matplotlib.dates
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import seaborn as sns; sns.set()
import matplotlib.ticker as ticker
import seaborn_subplots as sfg
import scipy.stats as stats
from functools import reduce
from os.path import exists
from split_files import split_files

def p2f(x):
    return float(x.strip('%'))/100

def mu_round(x):
    base = 1
    return base * round(float(x)/base)
    #return round(float(x))

def hv_round(x):
    return round(float(x),2)

def get_lumi_daily():
    df = pd.read_csv('./lumi_files/daytable.csv', encoding="utf-8", skipinitialspace=True, converters={'LStableRecPercent':p2f, 'LReadyRecPercent':p2f, 'AvgMu':mu_round, 'PeakMu':mu_round})
    df = df.rename(columns=lambda x: x.strip())
    return df

def get_rod_data(name, meas):
    df = pd.read_csv('./dcs_csv/'+name+'_'+meas+'.csv', names=["Day", "Time", meas], converters={meas:hv_round})
    return df

def plot_correlations(corr_dict, obs, df, rodname):
    """
    Plot boxplot for OBSERVABLES whose correlation coefficient exceeds CORR_CUT.
    """
    for k in corr_dict.keys():
        if k in obs:
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

def get_corr_dict(df, columns, obs, corr_cut):
    """
    Print correlation matrix for OBSERVABLES whose correlation coefficient exceeds CORR_CUT.
    Returns corr_dict, a dict with key OBSERVABLES and value of list containing names of 
    correlations greater than CORR_CUT. 
    """
    corr_dict = {col:None for col in columns}
    corr = df.corr()
    for col in columns:
        if col in obs:
            print("\n---------------------------------")
            print(col)
            print("---------------------------------")
            df_corr = corr.loc[corr[col] > corr_cut]
            print(corr[col].sort_values(ascending=False))
            corr_dict[col] = df_corr[col].index.tolist()
            corr_dict[col].remove(col)
    return corr_dict


def get_dfs(rod, obs):
    data_frames = []
    data_frames.append(get_lumi_daily())
    for ob in obs:
        f = './dcs_csv/'+str(rod)+'_'+str(ob)+'.csv'
        if exists(f):
            data_frames.append(get_rod_data(rod, ob))
        else:
            msg = f"File {f} does not exist!"
            raise FileNotFoundError(msg)
        
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Day'],
                                                    how='inner'), data_frames)
    return df_merged


def clean_columns(columns):
    if 'Fills' in columns:
        columns.remove('Fills')
    if 'Time' in columns:
        columns.remove('Time')
    if 'Time_x' in columns:
        columns.remove('Time_x')
    if 'Time_y' in columns:
        columns.remove('Time_y')


class ci_functions():

    def find_corr(self, rod, *obs, plot=True, corr_cut=0.7, verbose=False):
        """
        Calculate correlation coefficients for specified observable.
        Rod name and observable of interest are required arguments.
        e.g. find_corr --rod LI_S01_C_M4 --obs HV_IMeas
        e.g. find_corr LI_S01_C_M4 HV_IMeas TModule
        """
        df = get_dfs(rod, obs)
        columns = df.columns.values.tolist()
        clean_columns(columns)
        if verbose:
            print(df)
        
        # correlation matrix
        corr_dict = get_corr_dict(df, columns, obs, corr_cut)
        if verbose:
            print(corr_dict)

        if plot:
            plot_correlations(corr_dict, obs, df, rod)

            
    def correlation_matrix(self, rod, *obs):
        """
        Plot correlation matrix.
        """
        df = get_dfs(rod, obs)
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        plt.figure(figsize=(16,9))
        ax = plt.subplot()
        ax.title.set_text(rod)
        corr = df.corr()
        print(f"\nCorrelation for {rod}:")
        sns.heatmap(corr, cmap=cmap, square=True, annot=True)
        bottom, top = ax.get_ylim()
        ax.set_ylim(bottom + 0.5, top - 0.5)
        plt.tight_layout()
        plt.savefig("./plots/corr/"+rod+".png")
        print(f"./plots/corr/{rod}.png saved")
        plt.close()

    def find_dcs_corr(self, filename, plot=True, corr_cut=0.7, verbose=False):
        """
        Plot correlation plots for single DCS raw file.
        """
        file_path = "./dcs_raw/"+filename
        if exists(file_path):
            paths = split_files(file_path)
            rods_obs = {}
            for p in paths:
                rod_start = p.find("dcs_csv/") + 8
                rod_end = rod_start + 11
                rod = p[rod_start:rod_end]
                obs_start = rod_end + 1
                obs_end = p.find(".csv")
                obs = p[obs_start:obs_end]
                if rod not in rods_obs.keys():
                    rods_obs[rod] = [obs]
                else:
                    rods_obs[rod].append(obs)
            for rod in rods_obs.keys():
                print(f"\nRod {rod}:")
                self.find_corr(rod, *rods_obs[rod], plot=plot, corr_cut=corr_cut, verbose=verbose)
        else:
            msg = f"File {file_path} does not exist!"
            raise FileNotFoundError(msg)
                
        
if __name__=="__main__":
    fire.Fire(ci_functions)
