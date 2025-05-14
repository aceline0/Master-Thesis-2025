# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:36:42 2025

@author: Celine
"""
import pandas as pd

# load energy data
sor_raw = pd.read_csv('24sor.csv', skiprows=3, delimiter=',')
sor_raw.fillna(0, inplace=True)

# make copy
sor = sor_raw.copy()

# set timestamp to index 
sor['Tid (Time)'] = pd.to_datetime(sor['Tid (Time)'].str.extract(r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})')[0], format='%d.%m.%Y %H:%M')

# Rename column
sor.rename(columns={'Tid (Time)': 'Time'}, inplace=True)

# define start and end dates
start_date = '2024-03-25 15:00:00' 
end_date = '2025-03-24 23:00:00'

# convert dates to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# include only rows within the specified date range
sor = sor[(sor['Time'] >= start_date) & (sor['Time'] <= end_date)]



#%%
# load timedit data
#timeedit_preprosessed = pd.read_csv('room_bookings_2024.csv', delimiter=',')
timeedit_preprosessed = pd.read_csv('room_bookings.csv', delimiter=',')

timeedit_preprosessed.rename(columns={'Unnamed: 0': 'Time'}, inplace=True)
timeedit_preprosessed['Time'] = pd.to_datetime(timeedit_preprosessed['Time'])


# Add 'Gullvepsen' column from timeedit_preprosessed to bikuben
sor = sor.merge(timeedit_preprosessed[['Time', 
                                       'S102',
                                       'S104',
                                       'S105',
                                       'S107',
                                       'S108',
                                       'S109',
                                       'S110',
                                       'S111',
                                       'S119',
                                       'S120',
                                       'S121',
                                       'S122',
                                       'S123',
                                       'S124',
                                       'S128',
                                       'S129',
                                       'S130',
                                       'S131',
                                       'S133',
                                       'SU105',
                                       'SU113',
                                       'SU115']], on='Time', how='left')

# List of columns to sum
columns_to_sum = ['S102', 'S104', 'S105', 'S107', 'S108', 'S109', 'S110', 'S111', 
                  'S119', 'S120', 'S121', 'S122', 'S123', 'S124', 'SU105', 'SU113', 'SU115']

# Create a new column with the row-wise sum of the specified columns
sor['Number_of_Bookings'] = sor[columns_to_sum].sum(axis=1)
sor = sor.drop(['S102', 'S104', 'S105', 'S107', 'S108', 'S109', 'S110', 'S111', 'S119', 
                'S120', 'S121', 'S122', 'S123', 'S124','S128','S129','S130','S131',
                'S133', 'SU105', 'SU113', 'SU115'], axis=1)


#%%
# load usage data (from cisco)
use = pd.read_csv('Cisco_Sørhellinga(ag-grid).csv', delimiter=',')
use = use[['SourceTimeStamp', 'adjusted_visits_raw']]
use.columns

# Convert the 'SourceTimeStamp' to datetime format
use['Time'] = pd.to_datetime(use['SourceTimeStamp'].str.extract(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})')[0], format='%Y-%m-%dT%H:%M')


# specify date range
use = use[(use['Time'] >= start_date) & (use['Time'] <= end_date)]

# Merge bikuben and use on the 'Time' column
sor = sor.merge(use[['Time', 'adjusted_visits_raw']], on='Time', how='left')



#%%
# Set the 'Time' column as the index (for the sake of plotting)
sor.set_index('Time', inplace=True)
sor.to_csv('processed_sorhellinga.csv')









