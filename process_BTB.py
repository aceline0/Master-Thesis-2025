# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 09:24:24 2025

@author: Celine
"""

import pandas as pd

# load energy data
BTB_raw = pd.read_csv('24BTB.csv', skiprows=3, delimiter=',')
BTB_raw.fillna(0, inplace=True)

# make copy
BTB = BTB_raw.copy()

# set timestamp to index
BTB['Tid (Time)'] = pd.to_datetime(BTB['Tid (Time)'].str.extract(r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})')[0], format='%d.%m.%Y %H:%M')

# Rename column
BTB.rename(columns={'Tid (Time)': 'Time'}, inplace=True)

# define start and end dates
start_date = '2024-03-25 15:00:00' 
end_date = '2025-03-24 23:00:00'

# convert dates to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# include only rows within the specified date range
BTB = BTB[(BTB['Time'] >= start_date) & (BTB['Time'] <= end_date)]



#%%
# load timedit data
#timeedit_preprosessed = pd.read_csv('room_bookings_2024.csv', delimiter=',')
timeedit_preprosessed = pd.read_csv('room_bookings.csv', delimiter=',')

timeedit_preprosessed.rename(columns={'Unnamed: 0': 'Time'}, inplace=True)
timeedit_preprosessed['Time'] = pd.to_datetime(timeedit_preprosessed['Time'])


# Add 'Gullvepsen' column from timeedit_preprosessed to bikuben
BTB = BTB.merge(timeedit_preprosessed[['Time',
                                       'BT1A07',
                                       'BT2A05',
                                       'BT2A08',
                                       'BT2A11',
                                       'BT3A10',
                                       'BT3A11',
                                       'BT3A12',
                                       'BT3A13',
                                       'BT3A16',
                                       'BT3A17',
                                       'BTB foaje']], on='Time', how='left')

# List of columns to sum
columns_to_sum = ['BT1A07','BT2A05','BT2A08','BT2A11','BT3A10','BT3A11',
                  'BT3A12','BT3A13','BT3A16','BT3A17','BTB foaje']

# Create a new column with the row-wise sum of the specified columns
BTB['Number_of_Bookings'] = BTB[columns_to_sum].sum(axis=1)
BTB = BTB.drop(['BT1A07','BT2A05','BT2A08','BT2A11','BT3A10','BT3A11',
                  'BT3A12','BT3A13','BT3A16','BT3A17','BTB foaje'], axis=1)


#%%
# load usage data (from cisco)
use = pd.read_csv('Cisco_BTB(ag-grid).csv', delimiter=',')
use = use[['SourceTimeStamp', 'adjusted_visits_raw']]
use.columns

# Convert the 'SourceTimeStamp' to datetime format
use['Time'] = pd.to_datetime(use['SourceTimeStamp'].str.extract(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})')[0], format='%Y-%m-%dT%H:%M')


# specify date range
use = use[(use['Time'] >= start_date) & (use['Time'] <= end_date)]

# Merge bikuben and use on the 'Time' column
BTB = BTB.merge(use[['Time', 'adjusted_visits_raw']], on='Time', how='left')



#%%
# Set the 'Time' column as the index (for the sake of plotting)
BTB.set_index('Time', inplace=True)

# make columns numeric
BTB = BTB.apply(pd.to_numeric, errors='coerce')

BTB.to_csv('processed_BTB.csv')