# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 07:53:47 2025

@author: Celine
"""

import pandas as pd

# load energy data
ka_raw = pd.read_csv('24KA.csv', skiprows=3, delimiter=',')
ka_raw.fillna(0, inplace=True)

# make copy
ka = ka_raw.copy()

# set timestamp to index
ka['Tid (Time)'] = pd.to_datetime(ka['Tid (Time)'].str.extract(r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})')[0], format='%d.%m.%Y %H:%M')

# Rename column
ka.rename(columns={'Tid (Time)': 'Time'}, inplace=True)

# define start and end dates
start_date = '2024-03-25 15:00:00' 
end_date = '2025-03-24 23:00:00'

# convert dates to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# include only rows within the specified date range
ka = ka[(ka['Time'] >= start_date) & (ka['Time'] <= end_date)]



#%%
# load timedit data
#timeedit_preprosessed = pd.read_csv('room_bookings_2024.csv', delimiter=',')
timeedit_preprosessed = pd.read_csv('room_bookings.csv', delimiter=',')

timeedit_preprosessed.rename(columns={'Unnamed: 0': 'Time'}, inplace=True)
timeedit_preprosessed['Time'] = pd.to_datetime(timeedit_preprosessed['Time'])


# Add 'Gullvepsen' column from timeedit_preprosessed to bikuben
ka = ka.merge(timeedit_preprosessed[['Time', 
                                       'KA232',
                                       'KA233',
                                       'KA332a',
                                       'KA332b',
                                       'KA333',
                                       'KA334']], on='Time', how='left')

# List of columns to sum
columns_to_sum = ['KA232','KA233','KA332a','KA332b','KA333','KA334']

# Create a new column with the row-wise sum of the specified columns
ka['Number_of_Bookings'] = ka[columns_to_sum].sum(axis=1)
ka = ka.drop(['KA232','KA233','KA332a','KA332b','KA333','KA334'], axis=1)


#%%
# load usage data (from cisco)
use = pd.read_csv('Cisco_KA-bygningen(ag-grid).csv', delimiter=',')
use = use[['SourceTimeStamp', 'adjusted_visits_raw']]
use.columns

# Convert the 'SourceTimeStamp' to datetime format
use['Time'] = pd.to_datetime(use['SourceTimeStamp'].str.extract(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})')[0], format='%Y-%m-%dT%H:%M')


# specify date range
use = use[(use['Time'] >= start_date) & (use['Time'] <= end_date)]

# Merge bikuben and use on the 'Time' column
ka = ka.merge(use[['Time', 'adjusted_visits_raw']], on='Time', how='left')



#%%
# Set the 'Time' column as the index (for the sake of plotting)
ka.set_index('Time', inplace=True)

ka.to_csv('processed_ka.csv')







