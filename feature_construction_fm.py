#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 15:17:10 2025

@author: forootan
"""



import pandas as pd
from scipy.stats import linregress
from sklearn.preprocessing import MinMaxScaler

import pandas as pd
from scipy.stats import linregress

# Function to compute initial value, final value, and slope for each region and technology
def compute_trend(df, value_col, feature_prefix):
    
    # Normalize common column names
    df.columns = [col.strip().capitalize() if col.lower() in ['year', 'region', 'technology'] else col for col in df.columns]
    
    df_agg = df.groupby(["Year", "Region", "Technology"])[value_col].sum().reset_index()
    extracted_features = []
    
    for (region, technology), group in df_agg.groupby(["Region", "Technology"]):
        year = group["Year"]
        values = group[value_col]

        # Compute slope using linear regression
        slope, _, _, _, _ = linregress(year, values)

        # Extract initial (2020) and final (2050) values
        initial_value = values.iloc[0]
        final_value = values.iloc[-1]

        # Store extracted features
        extracted_features.append([region, technology, initial_value, final_value, slope])

    # Convert to DataFrame
    feature_df = pd.DataFrame(extracted_features, columns=["Region", "Technology", f"{feature_prefix}_2020", f"{feature_prefix}_2050", f"{feature_prefix}_Slope"])
    
    return feature_df

######################################

def compute_trend_debug(df, value_col, feature_prefix):
    # Step 1: Standardize column names to lowercase
    df.columns = [col.strip().lower() for col in df.columns]
    print("Normalized columns:", df.columns.tolist())  # Debug line

    # Step 2: Group and compute trends
    try:
        df_agg = df.groupby(["year", "region", "technology"])[value_col].sum().reset_index()
    except KeyError as e:
        raise KeyError(f"Missing expected column in input DataFrame: {e}")

    extracted_features = []
    for (region, technology), group in df_agg.groupby(["region", "technology"]):
        year = group["year"]
        values = group[value_col]

        slope, _, _, _, _ = linregress(year, values)
        initial_value = values.iloc[0]
        final_value = values.iloc[-1]

        extracted_features.append([region, technology, initial_value, final_value, slope])

    return pd.DataFrame(
        extracted_features, 
        columns=["Region", "Technology", f"{feature_prefix}_2020", f"{feature_prefix}_2050", f"{feature_prefix}_Slope"]
    )




#####################################

# Function to compute trend (initial, final, slope) for non-region, non-tech datasets
def compute_global_trend(df, year_col, value_col, feature_prefix):
    # Normalize column names
    df.columns = [col.strip().capitalize() if col.lower() == year_col.lower() else col for col in df.columns]
    
    years = df[year_col]
    values = df[value_col]
    
    slope, _, _, _, _ = linregress(years, values)
    initial_value = values.iloc[0]
    final_value = values.iloc[-1]

    # Create a one-row DataFrame with consistent format
    return pd.DataFrame({
        f"{feature_prefix}_2020": [initial_value],
        f"{feature_prefix}_2050": [final_value],
        f"{feature_prefix}_Slope": [slope]
    })