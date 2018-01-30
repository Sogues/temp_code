#!/home/louplus/env/bin python
# encoding: utf-8

import csv

with open('b.csv', 'w') as f:
    writer = csv.writer(f)
    for i in range(100000):
        writer.writerow([i, i])



