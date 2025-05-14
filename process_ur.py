# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 08:27:48 2025

@author: Celine
"""

import pandas as pd

# load energy data
ur_raw = pd.read_csv('24ur.csv', skiprows=3, delimiter=',')
ur_raw.fillna(0, inplace=True)

# make copy
ur = ur_raw.copy()

# set timestamp to index
ur['Tid (Time)'] = pd.to_datetime(ur['Tid (Time)'].str.extract(r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})')[0], format='%d.%m.%Y %H:%M')

# Rename column
ur.rename(columns={'Tid (Time)': 'Time'}, inplace=True)

# define start and end dates
start_date = '2024-03-25 15:00:00' 
end_date = '2025-03-24 23:00:00'

# convert dates to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# include only rows within the specified date range
ur = ur[(ur['Time'] >= start_date) & (ur['Time'] <= end_date)]



#%%
# load timedit data
#timeedit_preprosessed = pd.read_csv('room_bookings_2024.csv', delimiter=',')
timeedit_preprosessed = pd.read_csv('room_bookings.csv', delimiter=',')

timeedit_preprosessed.rename(columns={'Unnamed: 0': 'Time'}, inplace=True)
timeedit_preprosessed['Time'] = pd.to_datetime(timeedit_preprosessed['Time'])


# Add 'Gullvepsen' column from timeedit_preprosessed to bikuben
ur = ur.merge(timeedit_preprosessed[['Time',
                                     'U120',
                                     'U121',
                                     'U122',
                                     'U215',
                                     'U222A',
                                     'U222B',
                                     'U222C',
                                     'U223',
                                     'U224',
                                     'U225',
                                     'U226A',
                                     'U226B',
                                     'U227',
                                     'U302',
                                     'U303',
                                     'U305',
                                     'U306',
                                     'U323A',
                                     'U323B',
                                     'U323C',
                                     'U324',
                                     'U325',
                                     'U327',
                                     'U328']], on='Time', how='left')

# List of columns to sum
columns_to_sum = ['U120','U121','U122','U215','U222A','U222B','U222C','U223',
                  'U224','U225','U226A','U226B','U227','U302','U303','U305',
                  'U306','U323A','U323B','U323C','U324','U325','U327','U328']

# Create a new column with the row-wise sum of the specified columns
ur['Number_of_Bookings'] = ur[columns_to_sum].sum(axis=1)
ur = ur.drop(['U120','U121','U122','U215','U222A','U222B','U222C','U223',
                  'U224','U225','U226A','U226B','U227','U302','U303','U305',
                  'U306','U323A','U323B','U323C','U324','U325','U327','U328'], axis=1)


#%%
# load usage data (from cisco)
use = pd.read_csv('Cisco_Urbygningen(ag-grid).csv', delimiter=',')
use = use[['SourceTimeStamp', 'adjusted_visits_raw']]
use.columns

# Convert the 'SourceTimeStamp' to datetime format
use['Time'] = pd.to_datetime(use['SourceTimeStamp'].str.extract(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})')[0], format='%Y-%m-%dT%H:%M')


# specify date range
use = use[(use['Time'] >= start_date) & (use['Time'] <= end_date)]

# Merge bikuben and use on the 'Time' column
ur = ur.merge(use[['Time', 'adjusted_visits_raw']], on='Time', how='left')



#%%
# Set the 'Time' column as the index (for the sake of plotting)
ur.set_index('Time', inplace=True)
ur.to_csv('processed_ur.csv')








