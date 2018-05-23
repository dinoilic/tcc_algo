#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 18:48:34 2018

@author: dilic
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import csv

scaler = MinMaxScaler()

bldtyp = ['0-', '0+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+']

bldtypdict = {
    '0-': 0,
    '0+': 1,
    'A-': 2,
    'A+': 3,
    'B-': 4,
    'B+': 5,
    'AB-': 6,
    'AB+': 7        
}

minsup = np.array([38, 115, 46, 100, 38, 23, 8, 16])
optsup = np.array([58, 177, 71, 155, 60, 36, 13, 26])
maxsup = np.array([78, 240, 96, 210, 82, 50, 18, 36])
wekcon = np.array([35, 105, 42, 91, 35, 21, 7, 14])

cursup = np.array([50, 130, 60, 150, 50, 30, 8, 20])

def loss(x, i):
    r = maxsup[i] - minsup[i]

    if x <= minsup[i]:
        return (200 / r) * (minsup[i] - x) + 35
    elif x > minsup[i] and x <= (r / 3 + minsup[i]):
        return (100 / r) * (minsup[i] + r / 3 - x)
    elif x > (r / 3 + minsup[i]) and x <= (2 * r / 3 + minsup[i]):
        return 0
    elif x > (2 * r / 3 + minsup[i]) and x <= maxsup[i]:
        return (100 / r) * (x - 2 * r / 3 - minsup[i])
    else:
        return (200 / r) * (x - maxsup[i]) + 35

def get_new_data(data, days_passed):
    new_data = []
    
    data['freq_norm'] = data['frequency']
    data['dist_norm'] = np.exp(data['distance'])
    
    data[['freq_norm', 'dist_norm']] = scaler.fit_transform(data[['frequency', 'distance']])
    data['freq_norm'] = abs(1 - data['freq_norm'])
    
    for index, row in data.iterrows():
        okay = 0
        if row['sex'] == 'M' and (row['last_donation'] + days_passed) >= 90:
            okay = 1
        elif row['sex'] == 'Z' and (row['last_donation'] + days_passed) >= 120:
            okay = 1
            
        if okay:
            row['goodness'] = np.sqrt(row['dist_norm'] ** 2 +  row['freq_norm'] ** 2)
            new_data.append(row)


    return pd.DataFrame(new_data)

def correct():
    pass

data = pd.read_csv('donors.csv')
print(data.head())

blddata = pd.DataFrame([
    minsup,
    optsup,
    maxsup,
    wekcon,
    cursup
], columns=bldtyp)


available_people = get_new_data(data, 0)
available_people_sorted = available_people.sort_values(['goodness'], ascending=[True])

plt.scatter(available_people_sorted[1:1000]['frequency'], available_people_sorted[1:1000]['distance'])

cursup -= wekcon

people_called = []

for index, row in data.iterrows():
    bldid = bldtypdict[row['blood_group']]
    if cursup[bldid] < optsup[bldid]:
        u = np.random.rand()
        
        if(u >= 0.8):    
            cursup[bldid] += 1

        people_called.append(row['id'])
        
with open('test.csv', 'w') as csvfile:
    testwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    testwriter.writerow(people_called)
    
