import plotly.express as px
import pandas as pd
import numpy as np

df = pd.read_csv('Global YouTube Statistics_Global YouTube Statistics.csv', encoding='utf-16', sep='\t')

columns_to_keep = [
    'Subscribers',
    'Video Views',
    'category',
    'Uploads',
    'Country',
    'Days Since Created',
    # 'Youtuber',
    'Country Rank'
]

countries_to_keep = list(dict(df['Country'].value_counts()[:7]).keys())

condition_1 = df['Country'].isin(countries_to_keep)
condition_2 = df['Country Rank'] <= 10.

df = df[condition_1]
df = df[condition_2]
df = df[columns_to_keep]

from sklearn.preprocessing import LabelEncoder

le_category = LabelEncoder()
df['category'] = le_category.fit_transform(df['category']) + 1

le_country = LabelEncoder()
df['Country'] = le_country.fit_transform(df['Country']) + 1

df[:].to_csv('Data/UpdatedData.csv', index=False)