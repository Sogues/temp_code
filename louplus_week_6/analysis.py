# encoding: utf-8

import json
import pandas as pd

def analysis(file, user_id):
    times = 0
    minutes = 0
    data = pd.read_json(file)
    user_data = data.loc[data['user_id'].apply(lambda x: x==user_id)]
    times = user_data.shape[0]
    minutes = user_data['minutes'].sum()
    return times, minutes

if __name__ == '__main__':
    print(analysis('user_study.json', 199071))
