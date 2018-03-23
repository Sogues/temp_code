# encoding: utf-8

import pandas as pd
import numpy as np

def co2():
    data = pd.read_excel('ClimateChange.xlsx',sheet_name='Data')
    country = pd.read_excel('ClimateChange.xlsx', sheet_name='Country')
    series = pd.read_excel('ClimateChange.xlsx', sheet_name='Series')

    data.drop(['SCALE', 'Decimals'], inplace=True, axis=1)

    clean_data = data.merge(country[['Country code', 'Income group']], on='Country code', how='outer')

    clean_data = clean_data.loc[clean_data['Series code'] == 'EN.ATM.CO2E.KT']
    clean_data.drop(['Series code', 'Series name'], axis=1, inplace=True)
    clean_data.replace('..', np.NAN, inplace=True)

    clean_data['all'] = clean_data[list(range(1990, 2012))].fillna(method='ffill', axis=1).fillna(method='bfill', axis=1).sum(axis=1)

    clean_data.drop(list(range(1990, 2012)), axis=1, inplace=True)

    clean_data = clean_data.loc[clean_data['all'] != 0]

    group_data = clean_data.groupby('Income group')

    ret = group_data.sum()
    ret.columns = ['Sum emissions']
    ret[['Highest emission country', 'Highest emissions']] = group_data.max()[['Country name', 'all']]
    ret[['Lowest emission country', 'Lowest emissions']] = group_data.min()[['Country name', 'all']]

    return ret

if __name__ == '__main__':
    ret = co2()
    print(ret.head())

