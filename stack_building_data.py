# -*- coding: utf-8 -*-
"""
Created on Tue Apr  8 11:04:39 2025

@author: annec
"""

import pandas as pd
import numpy as np

def stack_building_data(data):
    """
    Stack building data row-wise (vertically) and add metadata.
    
    Parameters:
    data : pd.DataFrame
        Input DataFrame containing columns with suffixes for different locations.
        Expected columns: outdoor_temp, el_*, district_heat_*, bookings_*, visits_*
        where * is one of ['ur', 'bikuben', 'sor', 'ka', 'biotek', 'tf']
    
    Returns:
    Stacked DataFrame with columns:['Time', 'outdoor_temp', 'el', 'district_heat', 
                                    'bookings', 'visits', 'location', 'location_label']
    """
       
    # Stack the data for each location
    stacked_data = pd.DataFrame()
    suffixes = ['ur', 'bikuben', 'sor', 'ka', 'biotek', 'tf']
    
    for suffix in suffixes:
        temp_df = pd.DataFrame({
            'outdoor_temp': data['outdoor_temp'],
            'el': data[f'el_{suffix}'],
            'district_heat': data[f'district_heat_{suffix}'],
            'bookings': data[f'bookings_{suffix}'],
            'visits': data[f'visits_{suffix}']
        })
        stacked_data = pd.concat([stacked_data, temp_df], ignore_index=True)
    
    # Add location information
    locations = ["ur", "bikuben", "sor", "ka", "biotek", "tf"]
    labels = {loc: i for i, loc in enumerate(locations)}
    
    # Calculate number of time points per location
    n_timepoints = len(data)
    stacked_data["location"] = np.repeat(locations, n_timepoints)
    stacked_data["location_label"] = stacked_data["location"].map(labels)
    
    return stacked_data

data = pd.read_csv('all_building_data.csv')
data['Time'] = pd.to_datetime(data['Time'])
data = data.set_index('Time')

hourly_data_stacked = stack_building_data(data)

# Add time index
time_index = pd.date_range(
    start='2024-03-25 15:00:00', 
    end='2025-03-24 23:00:00', 
    freq='H')
repeated_time = pd.Series(time_index.tolist() * 6)
time_df = pd.DataFrame({'Time': repeated_time})


hourly_stacked = pd.concat([time_df, hourly_data_stacked], axis=1)

#%% make daily 
daily_data = data.resample('D').mean()
daily_data_stacked = stack_building_data(daily_data)


# Add time index
time_index = pd.date_range(
    start='2024-03-25 15:00:00', 
    end='2025-03-24 23:00:00', 
    freq='D')
repeated_time = pd.Series(time_index.tolist() * 6)
time_df = pd.DataFrame({'Time': repeated_time})


daily_stacked = pd.concat([time_df, daily_data_stacked], axis=1)
#daily_stacked.to_csv('daily_data_stacked.csv')









