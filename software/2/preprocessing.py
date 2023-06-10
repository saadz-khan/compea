import numpy as np
import pandas as pd
import datetime as dt

gen_1 = pd.read_csv('./generation_data.csv')
gen_1.drop(columns=['PLANT_ID', 'SOURCE_KEY'], axis=1, inplace=True)
sens_1 = pd.read_csv('./weather_data.csv')
sens_1.drop(columns=['PLANT_ID', 'SOURCE_KEY'], axis=1, inplace=True)

# Format datetime
gen_1['DATE_TIME'] = pd.to_datetime(gen_1['DATE_TIME'])
sens_1['DATE_TIME'] = pd.to_datetime(sens_1['DATE_TIME'])

df_gen = gen_1.groupby('DATE_TIME').sum().reset_index()
df_gen['time'] = df_gen['DATE_TIME'].dt.time

final_df = pd.merge(df_gen, sens_1, how='outer', on='DATE_TIME')
final_df.to_csv('./final_data.csv')