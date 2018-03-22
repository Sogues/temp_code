#!/home/louplus/env/bin python
# encoding: utf-8

import pandas as pd
def quarter_volume():
    data = pd.read_csv('apple.csv', header=0)
    data.set_index('Date', inplace=True)
    data.index = pd.to_datetime(data.index)
    sum_data = data['Volume'].resample('Q').sum()
    return sum_data.sort_values(ascending=False).iloc[1]

if __name__ == '__main__':
    print(quarter_volume())
