# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 11:26:48 2025

@author: Celine
"""

import pandas as pd

#bikuben= pd.read_csv('bikuben_processed.csv')
#bikuben['Time'] = pd.to_datetime(bikuben['Time'])
#bikuben= bikuben.set_index('Time')


def load_building_data(building_names='all'):
    """
    Load processed CSV files for specified building or all buildings.

    Parameters: building name(s) (str or list) or 'all' to load all buildings.

    Returns DataFrames for the buildings bikuben, sorhellinga, KA, BTB, TF1_2, ur
    """
    
    available_buildings = ['bikuben', 'sorhellinga', 'KA', 'BTB', 'TF', 'ur']
    
    # If 'all' is specified, load all buildings
    if building_names == 'all':
        building_names = available_buildings
    # If a single building name is provided as a string, convert it to a list
    elif isinstance(building_names, str):
        building_names = [building_names]
    
    building_data = {}

    for building in building_names:
        if building in available_buildings:
            file_name = f'processed_{building}.csv'
            df = pd.read_csv(file_name)
            df['Time'] = pd.to_datetime(df['Time'])
            df = df.set_index('Time')
            building_data[building] = df
        else:
            print(f"Building '{building}' not found.")

    return building_data

#data = load_building_data('sorhellinga')

data = load_building_data('all')
ur = data['ur']
bikuben = data['bikuben']
sor = data['sorhellinga']
ka = data['KA']
biotek = data['BTB']
tf = data['TF']

# merge into one dataframe
all_building_data = pd.concat([
    ur.add_suffix('_ur'),
    bikuben.add_suffix('_bikuben'),
    sor.add_suffix('_sor'),
    ka.add_suffix('_ka'),
    biotek.add_suffix('_biotek'),
    tf.add_suffix('_tf')], axis=1)

# ur, bikuben, sor, ka, biotek, tf

#%% keep just one temperature column
columns_to_check = ['Utetemperatur_ur', 'Utetemperatur_bikuben', 'Utetemperatur_sor', 
                    'Utetemperatur_ka', 'Utetemperatur_biotek', 'Utetemperatur_tf']

# Check if all columns are identical
all_building_data[columns_to_check].nunique(axis=1).eq(1).all()

# Find rows where not all selected columns are identical
non_matching_rows = all_building_data[columns_to_check].nunique(axis=1) > 1

# Count how many rows have differences
non_matching_rows.sum()

# Get indices of non-matching rows
non_matching_rows = all_building_data.index[non_matching_rows].tolist()

# which column(s) are not matching:
(all_building_data["Utetemperatur_tf"] == all_building_data["Utetemperatur_ka"]).all()
(all_building_data["Utetemperatur_tf"] == all_building_data["Utetemperatur_bikuben"]).all()
(all_building_data["Utetemperatur_tf"] == all_building_data["Utetemperatur_sor"]).all()
(all_building_data["Utetemperatur_tf"] == all_building_data["Utetemperatur_ur"]).all()
(all_building_data["Utetemperatur_tf"] == all_building_data["Utetemperatur_bikuben"]).all()
# all were true, excet for ur, i doubled checked by plotting


all_building_data.drop(columns=['Utetemperatur_bikuben', 
                                'Utetemperatur_sor', 
                                'Utetemperatur_ka', 
                                'Utetemperatur_biotek', 
                                'Utetemperatur_tf'], inplace=True)

#%% Drop columns that contain 'kjøling'
#all_building_data = all_building_data.drop(columns=[col for col in all_building_data.columns if 'kjøling' in col.lower()])
#all_building_data = all_building_data.drop(columns=[col for col in all_building_data.columns if 'sol' in col.lower()])


#%% Rename columns
all_building_data.rename(columns={
    # Outdoor Temperature
    'Utetemperatur_ur': 'outdoor_temp',
    
    # Visits
    'adjusted_visits_raw_ur': 'visits_ur',
    'adjusted_visits_raw_bikuben': 'visits_bikuben',
    'adjusted_visits_raw_sor': 'visits_sor',
    'adjusted_visits_raw_ka': 'visits_ka',
    'adjusted_visits_raw_biotek': 'visits_biotek',
    'adjusted_visits_raw_tf': 'visits_tf',
    
    # Electricity
    'El_ur': 'el_ur',
    'El_bikuben': 'el_bikuben',
    'El_sor': 'el_sor',
    'El_ka': 'el_ka',
    'El_biotek': 'el_biotek',
    'El_tf': 'el_tf',
    
    # District Heating (Fjernvarme)
    'Fjernvarme_ur': 'district_heat_ur',
    'Fjernvarme_bikuben': 'district_heat_bikuben',
    'Fjernvarme_sor': 'district_heat_sor',
    'Fjernvarme_ka': 'district_heat_ka',
    'Fjernvarme_biotek': 'district_heat_biotek',
    'Fjernvarme_tf': 'district_heat_tf',

    # Number of Bookings
    'Number_of_Bookings_ur': 'bookings_ur',
    'Number_of_Bookings_bikuben': 'bookings_bikuben',
    'Number_of_Bookings_sor': 'bookings_sor',
    'Number_of_Bookings_ka': 'bookings_ka',
    'Number_of_Bookings_biotek': 'bookings_biotek',
    'Number_of_Bookings_tf': 'bookings_tf',
}, inplace=True)

# download as csv
# all_building_data.to_csv('all_building_data.csv')


#%% Make daily and stack for PCA
import matplotlib.pyplot as plt
daily_data = all_building_data.resample('D').mean()

daily_data[['visits_bikuben', 'visits_biotek', 'visits_ka','visits_sor', 'visits_tf', 'visits_ur']].isnull().sum()

# fill ?? until i can use the imputed?
#daily_data = daily_data.fillna(method="ffill")
#daily_data['visits_bikuben'].plot(title='daily visits biku', style='-', label='visits')
#plt.show()



#%%

# Create a new DataFrame with 6 columns, each a copy of 'outdoor_temp'
outdoor_temp_df = pd.DataFrame({
    'outdoor_temp_ur': daily_data['outdoor_temp'],
    'outdoor_temp_bikuben': daily_data['outdoor_temp'],
    'outdoor_temp_sor': daily_data['outdoor_temp'],
    'outdoor_temp_ka': daily_data['outdoor_temp'],
    'outdoor_temp_biotek': daily_data['outdoor_temp'],
    'outdoor_temp_tf': daily_data['outdoor_temp']
})

# Stack the specific columns under each other
stacked_data = pd.DataFrame()

# List of suffixes for the columns
suffixes = ['ur', 'bikuben', 'sor', 'ka', 'biotek', 'tf']

for suffix in suffixes:
    temp_df = pd.DataFrame({
        'outdoor_temp': daily_data['outdoor_temp'],
        'el': daily_data[f'el_{suffix}'],
        'district_heat': daily_data[f'district_heat_{suffix}'],
        'bookings': daily_data[f'bookings_{suffix}'],
        'visits': daily_data[f'visits_{suffix}']
    })
    stacked_data = pd.concat([stacked_data, temp_df], ignore_index=True)

# Rename columns to match the desired output
stacked_data.columns = ['outdoor_temp', 'el', 'district_heat', 'bookings', 'visits']


#%%
import numpy as np
locations = ["ur", "bikuben", "sor", "ka", "biotek", "tf"]
labels = {loc: i for i, loc in enumerate(locations)}

# Create an empty column and assign values
stacked_data["location"] = np.repeat(locations, 365) 
#stacked_data["location"] = np.repeat(locations, 271)  # Repeat each location 271 times
stacked_data["location_label"] = stacked_data["location"].map(labels)  # Map to numeric labels

#stacked_data.to_csv('_mean_daily_data_stacked.csv')






