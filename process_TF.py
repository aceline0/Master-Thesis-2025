# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 09:20:40 2025

@author: Celine
"""

import pandas as pd

# load energy data
TF_raw = pd.read_csv('24TF.csv', skiprows=3, delimiter=',')
TF_raw.fillna(0, inplace=True)

# make copy
TF = TF_raw.copy()

# set timestamp to index
TF['Tid (Time)'] = pd.to_datetime(TF['Tid (Time)'].str.extract(r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})')[0], format='%d.%m.%Y %H:%M')

# Rename column
TF.rename(columns={'Tid (Time)': 'Time'}, inplace=True)

# define start and end dates
start_date = '2024-03-25 15:00:00' 
end_date = '2025-03-24 23:00:00'

# convert dates to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# include only rows within the specified date range
TF = TF[(TF['Time'] >= start_date) & (TF['Time'] <= end_date)]



#%%
# load timedit data
#timeedit_preprosessed = pd.read_csv('room_bookings_2024.csv', delimiter=',')
timeedit_preprosessed = pd.read_csv('room_bookings.csv', delimiter=',')

timeedit_preprosessed.rename(columns={'Unnamed: 0': 'Time'}, inplace=True)
timeedit_preprosessed['Time'] = pd.to_datetime(timeedit_preprosessed['Time'])


# Add 'Gullvepsen' column from timeedit_preprosessed to bikuben
TF = TF.merge(timeedit_preprosessed[['Time',
                                     'TF1-102 (TF145)',
                                     'TF1-105 (TF02)',
                                     'TF1-106 (TF01)',
                                     'TF1-107 (164)',
                                     'TF1-108 (163)',
                                     'TF1-112 (159)',
                                     'TF1-113 (158)',
                                     'TF1-115 (156)',
                                     'TF1-201',
                                     'TF1-203',
                                     'TF1-204',
                                     'TF1-205',
                                     'TF1-210',
                                     'TF1-211',
                                     'TF1-212',
                                     'TF1-253',
                                     'TF1-254',
                                     'TF1-U110 Fluidlaboratoriet',
                                     'TF1-U123B',
                                     'TF1-U124A',
                                     'TF1-U124B',
                                     'TF1-U125',
                                     'TF1-U126',
                                     'TF1-U127',
                                     'TF1-U128A',
                                     'TF1-U128B']], on='Time', how='left')

# List of columns to sum
columns_to_sum = ['TF1-102 (TF145)','TF1-105 (TF02)','TF1-106 (TF01)','TF1-107 (164)',
                  'TF1-108 (163)','TF1-112 (159)','TF1-113 (158)','TF1-115 (156)',
                  'TF1-201','TF1-203','TF1-204','TF1-205','TF1-210','TF1-211','TF1-212',
                  'TF1-253','TF1-254','TF1-U110 Fluidlaboratoriet','TF1-U123B',
                  'TF1-U124A','TF1-U124B','TF1-U125','TF1-U126','TF1-U127',
                  'TF1-U128A','TF1-U128B']

# Create a new column with the row-wise sum of the specified columns
TF['Number_of_Bookings'] = TF[columns_to_sum].sum(axis=1)
TF = TF.drop(['TF1-102 (TF145)','TF1-105 (TF02)','TF1-106 (TF01)','TF1-107 (164)',
                  'TF1-108 (163)','TF1-112 (159)','TF1-113 (158)','TF1-115 (156)',
                  'TF1-201','TF1-203','TF1-204','TF1-205','TF1-210','TF1-211','TF1-212',
                  'TF1-253','TF1-254','TF1-U110 Fluidlaboratoriet','TF1-U123B',
                  'TF1-U124A','TF1-U124B','TF1-U125','TF1-U126','TF1-U127',
                  'TF1-U128A','TF1-U128B'], axis=1)


#%%
# load usage data (from cisco)
use = pd.read_csv('Cisco_TF Fløy 1 og 2(ag-grid).csv', delimiter=',')
use = use[['SourceTimeStamp', 'adjusted_visits_raw']]
use.columns

# Convert the 'SourceTimeStamp' to datetime format
use['Time'] = pd.to_datetime(use['SourceTimeStamp'].str.extract(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})')[0], format='%Y-%m-%dT%H:%M')


# specify date range
use = use[(use['Time'] >= start_date) & (use['Time'] <= end_date)]

# Merge bikuben and use on the 'Time' column
TF = TF.merge(use[['Time', 'adjusted_visits_raw']], on='Time', how='left')



#%%
# Set the 'Time' column as the index (for the sake of plotting)
TF.set_index('Time', inplace=True)

# make columns numeric
TF = TF.apply(pd.to_numeric, errors='coerce')

TF.to_csv('processed_TF.csv')