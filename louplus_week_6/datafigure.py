# encoding: utf-8

import pandas as pd
from matplotlib import pyplot as plt

def data_plot():
    data = pd.read_json('user_study.json')
    user_data_group = data[['user_id', 'minutes']].groupby('user_id').sum()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(user_data_group)
    ax.set_title('StudyData')
    ax.set_xlabel('User ID')
    ax.set_ylabel('Study Time')
    plt.show()
    return ax

if __name__ == '__main__':
    data_plot()
