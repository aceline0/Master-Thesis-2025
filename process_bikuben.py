# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:17:46 2025

@author: Celine
"""

import pandas as pd

# load energy data
bikuben_raw = pd.read_csv('24bikuben.csv', skiprows=3, delimiter=',')
#bikuben_raw.fillna(0, inplace=True)

# make copy
bikuben = bikuben_raw.copy()

# set timestamp to index 
bikuben['Tid (Time)'] = pd.to_datetime(bikuben['Tid (Time)'].str.extract(r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})')[0], format='%d.%m.%Y %H:%M')

# Rename column
bikuben.rename(columns={'Tid (Time)': 'Time'}, inplace=True)

# define start and end dates
start_date = '2024-03-25 15:00:00' # since adjusted_visits_raw from cisco starts here
end_date = '2025-03-24 23:00:00'

# convert dates to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# include only rows within the specified date range
bikuben = bikuben[(bikuben['Time'] >= start_date) & (bikuben['Time'] <= end_date)]


#%%
# load timedit data
#timeedit_preprosessed = pd.read_csv('room_bookings_2024.csv', delimiter=',')
timeedit_preprosessed = pd.read_csv('room_bookings.csv', delimiter=',')

timeedit_preprosessed.rename(columns={'Unnamed: 0': 'Time'}, inplace=True)
timeedit_preprosessed['Time'] = pd.to_datetime(timeedit_preprosessed['Time'])


# Add 'Gullvepsen' column from timeedit_preprosessed to bikuben
bikuben = bikuben.merge(timeedit_preprosessed[['Time', 'Gullvepsen']], on='Time', how='left')

bikuben.rename(columns={'Gullvepsen': 'Number_of_Bookings'}, inplace=True)

#%%
# load usage data (from cisco)
use = pd.read_csv('Cisco_Bikuben(ag-grid).csv', delimiter=',')
use = use[['SourceTimeStamp', 'adjusted_visits_raw']]
use.columns

# Convert the 'SourceTimeStamp' to datetime format
use['Time'] = pd.to_datetime(use['SourceTimeStamp'].str.extract(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})')[0], format='%Y-%m-%dT%H:%M')


# specify date range
use = use[(use['Time'] >= start_date) & (use['Time'] <= end_date)]

# Merge bikuben and use on the 'Time' column
bikuben = bikuben.merge(use[['Time', 'adjusted_visits_raw']], on='Time', how='left')

bikuben['adjusted_visits_raw'].isna().sum()


#%%
# Set the 'Time' column as the index (for the sake of plotting)
bikuben.set_index('Time', inplace=True)
bikuben.to_csv('processed_bikuben.csv')


# =============================================================================


#%% EDA
import matplotlib.pyplot as plt

bikuben['adjusted_visits_raw'].plot(title='Number of visits bikuben - Time Plot', figsize=(10,6))
#bikuben['El'].plot(title='El Energi - Time Plot', figsize=(10,6))
#plt.ylabel('El Energi [kWh]')
plt.ylabel('Number of visits')
plt.xlabel('Date (hourly timestamp)')

def time_plots(df, x_label='Date (hourly timestamp)'):
    for column in df.columns:
        plt.figure(figsize=(10, 6))
        df[column].plot(title=f"{column} - Time Plot")
        plt.xlabel(x_label)
        plt.ylabel(column)
        plt.show()

time_plots(bikuben)


#%% From the time plots it looks like there is a need for some imputation
# impute temperature (capture night and day pluss a nice plot)
# 



#%% impute visits (capture week and weekend pluss a nice plot)



#%%
describe = bikuben.describe()


#%%
# Defining required fields
df = bikuben.loc[:'2024-07-03 23:00:00']

df = bikuben

# quick plot
df['adjusted_visits_raw'].plot(title='Number of visits bikuben - Time Plot', figsize=(10,6))

#df['Utetemperatur'].plot(title='Temp - Time Plot', figsize=(8,5))
#plt.ylabel('celcius')
#plt.xlabel('Date (hourly timestamp)')


#df['year'] = [x for x in df.index.year]
df['month'] = [x for x in df.index.month]
df['hour'] = [x for x in df.index.hour]
df['day'] = [x for x in df.index.day_of_week]

df = df.reset_index()
df['week'] = df['Time'].apply(lambda x:x.week)

df = df.set_index('Time')

df['day_str'] = [x.strftime('%a') for x in df.index]
#df['year_month'] = [str(x.year) + '_' + str(x.month) for x in df.index]


# Defining the dataframe
df_plot = df[['hour', 'day_str', 'adjusted_visits_raw']].dropna().groupby(['hour', 'day_str']).mean()[['adjusted_visits_raw']].reset_index()




#%% Plot using Matplotlib
plt.figure(figsize=(10, 8))

# Loop through each unique day_str and plot a line
for day in df_plot['day_str'].unique():
    day_data = df_plot[df_plot['day_str'] == day]
    plt.plot(day_data['hour'], day_data['adjusted_visits_raw'], label=day)

# Customize the plot
plt.title("Seasonal Plot - Daily Visits", fontsize=20)
plt.ylabel('Number of visits')
plt.xlabel('Hour')
plt.legend(title='Day of Week')  # Add a legend with a title
plt.locator_params(axis='x', nbins=24)  # Set 24 ticks on the x-axis
plt.grid(True)  # Add a grid for better readability
plt.show()

#%%














