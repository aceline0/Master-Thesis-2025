# -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 10:39:06 2025

@author: annec
"""
import pandas as pd

# load timedit data
timeedit_2024 = pd.read_csv('room_bookings_2024.csv', delimiter=',')
timeedit_2025 = pd.read_csv('room_bookings_2025.csv', delimiter=',')

#%% merge csv
import pandas as pd
import numpy as np

# load timedit data
timeedit_24 = pd.read_csv('timeedit.csv', skiprows=4, delimiter=';')
timeedit_25 = pd.read_csv('timeedit25.csv', skiprows=4, delimiter=',', encoding='latin-1')

timeedit_24 = timeedit_24[['Rom', 'Startdato','Starttidspunkt', 'Sluttdato', 'Sluttidspunkt']]
timeedit_25 = timeedit_25[['Rom', 'Startdato','Starttidspunkt', 'Sluttdato', 'Sluttidspunkt']]

timeedit = pd.concat([timeedit_24, timeedit_25])

# spleis start and slutt
timeedit.loc[:, 'Start time'] = timeedit['Startdato'] + ' ' + timeedit['Starttidspunkt']
timeedit.loc[:, 'End time'] = timeedit['Sluttdato'] + ' ' + timeedit['Sluttidspunkt']

# convert 'Start time' and 'End time' to datetime format
timeedit.loc[:, 'Start time'] = pd.to_datetime(timeedit['Start time'], format='%d.%m.%Y %H:%M')
timeedit.loc[:, 'End time'] = pd.to_datetime(timeedit['End time'], format='%d.%m.%Y %H:%M')

# floor dates to nearest hour
timeedit.loc[:, 'Start time'] = timeedit['Start time'].dt.floor('H')
timeedit.loc[:, 'End time'] = timeedit['End time'].dt.floor('H')

# define start and end dates
start_date = '2024-03-25 00:00:00'
end_date = '2025-03-24 23:00:00'

# convert dates to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# include only rows within the specified date range
timeedit = timeedit[(timeedit['Start time'] >= start_date) & (timeedit['Start time'] <= end_date)]

# drop Na's
timeedit['Rom'].isna().sum()
timeedit = timeedit.dropna(subset=['Rom'])

# reset index
timeedit.reset_index(drop=True, inplace=True)

# drop excess columns
timeedit = timeedit.drop(['Startdato', 'Starttidspunkt', 'Sluttdato', 'Sluttidspunkt'], axis=1)

# create column with number of hours the booking last for
timeedit['hours'] = (timeedit['End time'] - timeedit['Start time']) / pd.Timedelta(hours=1)


#%% get room names

# split the strings in the 'Rom' column by comma
split_rooms = timeedit['Rom'].str.split(', ')

# check for Na's and drop
sum(split_rooms.isna())
split_rooms = split_rooms.dropna()

# flatten the list of lists to a single list of room numbers
all_rooms = [room for sublist in split_rooms for room in sublist]

# convert the list to a set to get unique room numbers
unique_rooms = set(all_rooms)

# function for finding rooms in spesific buildings
def is_in_building(room):
    if room.startswith('U'):
        return 'Urbygningen'
    elif room.startswith('S') and room[1:].isdigit() or room.startswith('SU'):
        return 'Sørhellinga'
    elif room.startswith('KA'):
        return 'KA'
    elif room.startswith('BT'):
        return 'Biotek'
    elif room.startswith('B') or room == 'Gullvepsen':
        return 'Bikuben'
    elif room.startswith('TF1') or room.startswith('TF2'):
        return 'TF1 and 2'
    else:
        return None

# Filter the unique rooms based on the criteria
rooms = {room for room in unique_rooms if is_in_building(room) is not None}
rooms = sorted(rooms)


#%% make data frame for selected rooms and their respective bookings
date_range = pd.date_range(start=start_date, end=end_date, freq='H')
room_bookings = pd.DataFrame(index=date_range, columns=rooms)


#deep
def fill_room_bookings(room_bookings, timeedit):
    for _, row in timeedit.iterrows():
        rooms = row['Rom'].split(', ')
        start_time = row['Start time']
        duration = row['hours']
        
        # Calculate end time
        end_time = start_time + pd.Timedelta(hours=duration)
        
        # Iterate through each room
        for room in rooms:
            if room in room_bookings.columns:  # Check if room exists in room_bookings
                # Find the time slots in room_bookings that overlap with the booking
                time_slots = room_bookings.index.to_series().between(start_time, end_time, inclusive='left')
                
                # Update the room_bookings DataFrame
                room_bookings.loc[time_slots, room] = 1
    
    # Fill remaining cells with NaN
    room_bookings.fillna(np.nan, inplace=True)
    return room_bookings

# Call the function
room_bookings = fill_room_bookings(room_bookings, timeedit)

# Fill any remaining NaN values with 0
room_bookings = room_bookings.fillna(0)


# export room_bookings to a csv
room_bookings.to_csv('room_bookings.csv', index=True)





