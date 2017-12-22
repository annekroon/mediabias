#!/usr/bin/env python3

import json
import pandas as pd

data = [item for sublist in json.load(open('../wordfreqs/output.json')) for item in sublist]

print(len(data))
df = pd.DataFrame.from_dict(data)
keys = list(df.head(1)['distance'][0].keys())

df.rename(columns = {'distance':'oldshit'},inplace=True)

for key in keys:
    df[key] = df['oldshit'].map(lambda x: x[key])

df['w1'] = df['pair'].map(lambda x: x[0])
df['w2'] = df['pair'].map(lambda x: x[1])

print(len(df))
df.drop('oldshit',axis=1).to_csv('../wordfreqs/output.csv')

