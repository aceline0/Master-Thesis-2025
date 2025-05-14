# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 13:46:08 2025

@author: Celine
"""

# from load_building_data import load_building_data
# data = load_building_data('bikuben')
# bikuben = data['bikuben']
# data = load_building_data('sorhellinga')
# sor = data['sorhellinga']


#%% mark repeated sequences 

def find_repeated_sequences(series, min_repeats=4):
    repeated_indices = []
    current_value = None
    current_count = 0
    start_index = None

    for i, value in enumerate(series):
        if value == current_value:
            current_count += 1
        else:
            if current_count >= min_repeats:
                repeated_indices.append((start_index, i - 1))
            current_value = value
            current_count = 1
            start_index = i

    # Check the last sequence
    if current_count >= min_repeats:
        repeated_indices.append((start_index, len(series) - 1))

    return repeated_indices


