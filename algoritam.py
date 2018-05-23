#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 23 18:48:34 2018

@author: dilic
"""

import numpy as np
import pandas as pd


bldtyp = ['0-', '0+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+']
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

# Week 0

