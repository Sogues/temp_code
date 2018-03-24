#!/home/louplus/env/bin python
# encoding: utf-8

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def climate_plot():
    data = pd.read_excel('ClimateChange.xlsx', sheet_name='Data')
    gt = pd.read_excel('GlobalTemperature.xlsx')

    gas_set = ['EN.ATM.CO2E.KT', 'EN.ATM.METH.KT.CE', 'EN.ATM.NOXE.KT.CE', 'EN.ATM.GHGO.KT.CE', 'EN.CLC.GHGR.MT.CE']

    data.replace('..', np.NAN, inplace=True)
    data = data.loc[data['Series code'].isin(gas_set)].copy()
    clean_data = data[list(range(1990, 2011))].fillna(method='ffill', axis=1).fillna(method='bfill', axis=1).sum()
    #clean_data = data[list(range(1990, 2011))].sum()

    clean_gt = gt.copy()
    clean_gt.index = pd.to_datetime(gt['Date'])
    clean_gt.drop('Date', axis=1, inplace=True)
    #clean_gt = clean_gt.fillna(method='ffill').fillna(method='bfill').copy()
    clean_gt.replace(np.NAN, 0, inplace=True)

    gt_12 = clean_gt.loc['1990':'2010'].resample('Y').sum()
    gt_12.index = clean_data.index
    gt_34 = clean_gt.resample('Q').sum()

    def scale_func(x):
        x_min = x.min(axis=0)
        x_max = x.max(axis=0)
        return (x - x_min) / (x_max - x_min)

    fig = plt.figure(figsize=(40, 20))
    plt.style.use('seaborn-darkgrid')
    axes = fig.subplots(2, 2)
    scale_df_12 = scale_func(gt_12)[['Land Average Temperature', 'Land And Ocean Average Temperature']].copy()
    scale_df_12['Total GHG'] = (clean_data - clean_data.min()) / (clean_data.max() - clean_data.min())#scale_func(clean_data)
    scale_df_12.plot(
                kind='line', ax=axes[0][0],
                    grid=True, fontsize=30, linewidth=4)
    axes[0][0].set_xlabel('Years', fontsize=30)
    axes[0][0].set_ylabel('Values', fontsize=30)
    axes[0][0].set_xticks(range(1990, 2012, 2))
#axes[0][0].set_xticklabels(range(1990, 2012, 2), rotation=90)
    axes[0][0].set_xlim([1990, 2010])
    axes[0][0].legend(loc='lower right', fontsize=20)

    scale_df_12.plot(
                kind='bar', ax=axes[0][1],
                    fontsize=30, linewidth=4)
    axes[0][1].set_xlabel('Years', fontsize=30)
    axes[0][1].set_ylabel('Values', fontsize=30)
    axes[0][1].legend(loc='upper left', fontsize=20)

    scale_df_34 = scale_func(gt_34[['Land Average Temperature', 'Land And Ocean Average Temperature']]).copy()
    scale_df_34.plot(kind='area', ax=axes[1][0],
                                fontsize=30, linewidth=4)
    axes[1][0].set_xlabel('Quarters', fontsize=30)
    axes[1][0].set_ylabel('Temperature', fontsize=30)
    axes[1][0].legend(loc='upper left', fontsize=20)
    axes[1][0].set_xlim([scale_df_34.index[0], scale_df_34.index[-1]])

    scale_df_34.plot(kind='kde', ax=axes[1][1],
                                fontsize=30, linewidth=4)
    axes[1][1].set_xlabel('Values', fontsize=30)
    axes[1][1].set_ylabel('Values', fontsize=30)
    axes[1][1].legend(loc='upper left', fontsize=20)

    return axes

if __name__ == '__main__':
    axes = climate_plot()
