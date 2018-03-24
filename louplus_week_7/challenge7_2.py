#!/home/louplus/env/bin python
# encoding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def co2_gdp_plot():
    data = pd.read_excel('ClimateChange.xlsx', sheet_name='Data')
    choice = ['NY.GDP.MKTP.CD', 'EN.ATM.CO2E.KT']
    clean_data = data[['Country code', 'Series code']].copy()
    data.replace('..', np.NAN, inplace=True)
    clean_data['sum'] = (
            data[list(range(1990, 2012))].fillna(
                method='ffill', axis=1
                ).fillna(
                    method='bfill', axis=1
                    ).sum(axis=1)
            )
    clean_data = clean_data.loc[clean_data['Series code'].isin(choice)]
    ret = {}

    def func(x, label, axes, ret):
        countries = ['CHN', 'USA', 'GBR', 'FRA','RUS']
        sum_min = x['sum'].min()
        sum_max = x['sum'].max()
        values = (x['sum'] - sum_min) / (sum_max - sum_min)
        if label == 'NY.GDP.MKTP.CD':
            label = 'GDP-SUM'
        else:
            label= 'CO2-SUM'
        axes.plot(x['Country code'],values, label=label, linewidth=4)
        df = x.copy()
        df['org_idx'] = df.index
        df['idx'] = range(df.shape[0])
        df.set_index('Country code', inplace=True)
        idx = df.loc[countries, 'idx']
        axes.set_xticks(idx)
        axes.set_xticklabels(countries, rotation=90)
        axes.set_xlim([0, df.shape[0]])
        axes.legend(loc='upper left', fontsize=30)
        ret[label] = np.round(values[df.loc['CHN', 'org_idx']], 3)

    fig = plt.figure(figsize=(50, 25))
    axes = fig.add_subplot(1, 1, 1)
    axes.tick_params(labelsize=30)
    axes.set_ylabel('Values', fontsize=40)
    axes.set_xlabel('Countries', fontsize=40)
    axes.set_title('GDP-CO2', fontsize=40)
    for item in clean_data.groupby('Series code'):
        func(item[1], item[0], axes, ret)
    ret = [ret['CO2-SUM'], ret['GDP-SUM']]
    return axes, ret

if __name__ == '__main__':
    _1, ret = co2_gdp_plot()
    print(ret)

