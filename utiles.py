#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 12:47:27 2025

@author: forootan
"""



import gdxpds
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pyomo.environ import *
#from gams import GamsWorkspace, GamsParameter, GamsSet
#from gams import GamsWorkspace
import os

import sys
import os
import json
from datetime import datetime


import os
import pandas as pd

from Temporary_backups.feature_construction_fm import compute_global_trend, compute_trend





def load_and_rename_csvs(csv_dir, rename_rules=None):
    """
    Automatically loads all .csv files in a directory and applies renaming rules if specified.

    Parameters:
        csv_dir (str): Directory containing the CSV files.
        rename_rules (dict): Optional dictionary of column renaming rules.

    Returns:
        dict: A dictionary of {<base_filename>: DataFrame}
    """
    datasets = {}
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith(".csv")]

    for csv_file in csv_files:
        file_path = os.path.join(csv_dir, csv_file)
        base_name = os.path.splitext(csv_file)[0]  # remove .csv
        try:
            df = pd.read_csv(file_path)

            if rename_rules and base_name in rename_rules:
                df.rename(columns=rename_rules[base_name], inplace=True)

            datasets[base_name] = df
            print(f"✔ Loaded: {csv_file}")
        except Exception as e:
            print(f"✘ Failed to load {csv_file}: {e}")

    return datasets




def get_dynamic_rename_mapping(var_name):
    """
    Returns column renaming rules based on the variable name prefix.
    """
    prefix = var_name.split("_df_sce_")[0] if "_df_sce_" in var_name else var_name

    rename_map = {
        "costMargFMs": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "Cost"},
        "costInvFMs": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "InvestmentCost"},
        "costInvLevelFMs": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "InvestmentLevelCost"},
        "ghgFMs": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "GHG_Removal"},
        "FMsgrowth": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "ForestManagementGrowth"},
        "BeechArea0": {"*": "Year", "*.1": "Region", "Value": "InitialBeechArea"},
        "GrassArea0": {"*": "Year", "*.1": "Region", "Value": "InitialGrassArea"},
        "ghgTargetLULUCF": {"*": "Year", "Value": "GHG_Target_LULUCF"},
        "CO2price": {"*": "Year", "Value": "CO2_Price"},
        "CO2price_2times": {"t": "Year", "Value": "CO2_Price"},
        "CO2price_3times": {"t": "Year", "Value": "CO2_Price"},
        "CO2price_05times": {"t": "Year", "Value": "CO2_Price"},
    }

    return rename_map.get(prefix, None)




def get_dynamic_rename_mapping_2(var_name):
    """
    Returns column renaming rules based on the variable name prefix and dataset structure.
    """
    prefix = var_name.split("_df_sce_")[0] if "_df_sce_" in var_name else var_name
    
    # Check if the dataset name matches any known prefixes for dynamic renaming
    if "costMargFMs" in prefix:
        rename_map = {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "Cost"}
    elif "costInvFMs" in prefix:
        rename_map = {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "InvestmentCost"}
    elif "costInvLevelFMs" in prefix:
        rename_map = {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "InvestmentLevelCost"}
    elif "ghgFMs" in prefix:
        rename_map = {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "GHG_Removal"}
    elif "FMsgrowth" in prefix:
        rename_map = {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "ForestManagementGrowth"}
    elif "BeechArea0" in prefix:
        rename_map = {"*": "Year", "*.1": "Region", "Value": "InitialBeechArea"}
    elif "GrassArea0" in prefix:
        rename_map = {"*": "Year", "*.1": "Region", "Value": "InitialGrassArea"}
    elif "ghgTargetLULUCF" in prefix:
        rename_map = {"*": "Year", "Value": "GHG_Target_LULUCF"}
    elif "CO2price" in prefix:
        rename_map = {"*": "Year", "Value": "CO2_Price"}
    else:
        rename_map = None  # Return None if no match is found
    
    return rename_map



def get_dynamic_rename_mapping_fixed(var_name):
    """
    Improved version that looks ONLY at the first part of the var_name to determine renaming rules.
    """
    main_prefix = var_name.split("_")[0]

    rename_map_dict = {
        "costMargFMs": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "Cost"},
        "costInvFMs": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "InvestmentCost"},
        "costInvLevelFMs": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "InvestmentLevelCost"},
        "ghgFMs": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "GHG_Removal"},
        "FMsgrowth": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "ForestManagementGrowth"},
        "BeechArea0": {"*": "Year", "*.1": "Region", "Value": "InitialBeechArea"},
        "GrassArea0": {"*": "Year", "*.1": "Region", "Value": "InitialGrassArea"},
        "ghgTargetLULUCF": {"*": "Year", "Value": "GHG_Target_LULUCF"},
        "CO2price": {"*": "Year", "Value": "CO2_Price"},
    }

    return rename_map_dict.get(main_prefix, None)










##################################



import os

def get_available_results_scenarios(results_folder):
    """
    Read all Results_*.gdx files and return list of scenario suffixes without Results_ and .gdx.
    """
    result_files = [f for f in os.listdir(results_folder) if f.startswith("Results_") and f.endswith(".gdx")]
    
    # Remove "Results_" prefix and ".gdx" suffix
    scenario_suffixes = [os.path.splitext(f)[0].replace("Results_", "") for f in result_files]
    
    return scenario_suffixes


def process_scenario(scenario_name, datasets_dict):
    """
    Process a single scenario: apply compute_trend, merge all features, fill missing with 0.
    """
    costMarg_features = compute_trend(datasets_dict['costMargFMs'], "Cost", "CostMarg")
    costInv_features = compute_trend(datasets_dict['costInvFMs'], "InvestmentCost", "CostInv")
    costInvLevel_features = compute_trend(datasets_dict['costInvLevelFMs'], "InvestmentLevelCost", "CostInvLevel")
    ghg_features = compute_trend(datasets_dict['ghgFMs'], "GHG_Removal", "GHG")
    growth_features = compute_trend(datasets_dict['FMsgrowth'], "ForestManagementGrowth", "ForestGrowth")

    final_feature_array = costMarg_features.merge(costInv_features, on=["Region", "Technology"], how="outer") \
                                           .merge(costInvLevel_features, on=["Region", "Technology"], how="outer") \
                                           .merge(ghg_features, on=["Region", "Technology"], how="outer") \
                                           .merge(growth_features, on=["Region", "Technology"], how="outer")

    final_feature_array.fillna(0, inplace=True)

    return final_feature_array


def process_all_results_scenarios(scenarios, results_folder):
    """
    Process all scenarios which have corresponding Results_*.gdx file (by suffix match).
    """
    merged_feature_arrays = {}

    # Get result scenario suffixes (without Results_ and .gdx)
    valid_scenario_suffixes = get_available_results_scenarios(results_folder)
    print(f"Found {len(valid_scenario_suffixes)} valid result scenarios.")

    required_keys = ['costMargFMs', 'costInvFMs', 'FMsgrowth', 'ghgFMs', 'costInvLevelFMs']

    for scenario_suffix in valid_scenario_suffixes:

        if scenario_suffix not in scenarios:
            print(f" -> Skipping {scenario_suffix} (not in loaded scenarios)")
            continue

        datasets_dict = scenarios[scenario_suffix]

        if not all(key in datasets_dict for key in required_keys):
            print(f" -> Skipping {scenario_suffix} (missing datasets)")
            continue

        print(f"Processing scenario: {scenario_suffix}")

        # Process and store
        final_feature_array = process_scenario(scenario_suffix, datasets_dict)
        merged_feature_arrays[scenario_suffix] = final_feature_array

    print("\nFinished processing all valid Results scenarios.")
    return merged_feature_arrays


# === Example usage ===
"""
results_folder = "Results_dataset_scenarios$"  # <<<< your Results_*.gdx folder
merged_feature_arrays = process_all_results_scenarios(scenarios, results_folder)

# Save result (optional)
for scenario, df in merged_feature_arrays.items():
    filename = f"{scenario}_features.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {filename}")
"""




from scipy.stats import linregress
import pandas as pd

def enhance_with_global_trends_from_scenarios(merged_feature_arrays, scenarios):
    """
    For each merged feature array, add CO2 and GHG_Target_LULUCF trend features
    by computing trends from corresponding entries in `scenarios`.
    """
    enhanced_arrays = {}

    for scenario_name, feature_array in merged_feature_arrays.items():
        print(f"Enhancing: {scenario_name}")

        datasets_dict = scenarios.get(scenario_name, {})
        enhanced_df = feature_array.copy()

        # CO2 Trend
        if "CO2price" in datasets_dict:
            df_co2 = datasets_dict["CO2price"].copy()
            df_co2["Year"] = pd.to_numeric(df_co2["Year"], errors="coerce")
            df_co2["CO2_Price"] = pd.to_numeric(df_co2["CO2_Price"], errors="coerce")
            co2_features = compute_global_trend(df_co2, "Year", "CO2_Price", "CO2")
        else:
            co2_features = pd.DataFrame({col: [0.0] for col in ["CO2_2020", "CO2_2050", "CO2_Slope"]})

        # GHG Target Trend
        if "ghgTargetLULUCF" in datasets_dict:
            df_ghg = datasets_dict["ghgTargetLULUCF"].copy()
            df_ghg["Year"] = pd.to_numeric(df_ghg["Year"], errors="coerce")
            df_ghg["GHG_Target_LULUCF"] = pd.to_numeric(df_ghg["GHG_Target_LULUCF"], errors="coerce")
            ghg_features = compute_global_trend(df_ghg, "Year", "GHG_Target_LULUCF", "GHGTarget")
        else:
            ghg_features = pd.DataFrame({col: [0.0] for col in ["GHGTarget_2020", "GHGTarget_2050", "GHGTarget_Slope"]})

        # Broadcast to each region
        unique_regions = enhanced_df["Region"].unique()
        broadcast_df = pd.DataFrame(unique_regions, columns=["Region"])
        broadcast_df = broadcast_df.merge(co2_features, how="cross")
        broadcast_df = broadcast_df.merge(ghg_features, how="cross")

        # Merge with main feature array
        enhanced_df = enhanced_df.merge(broadcast_df, on="Region", how="left")
        enhanced_arrays[scenario_name] = enhanced_df

    print("Done enhancing all scenarios with CO2 and GHG trend features.")
    return enhanced_arrays


def enhance_with_region_level_features(merged_feature_arrays, scenarios, region_feature_keys):
    """
    Merge region-level features (e.g., BeechArea0, GrassArea0) into each merged feature array.
    
    Parameters:
    - merged_feature_arrays: dict of scenario_name -> DataFrame
    - scenarios: full scenarios dictionary
    - region_feature_keys: list of dataset keys to look for (e.g., ["BeechArea0", "GrassArea0"])
    """
    enhanced_arrays = {}

    for scenario_name, df in merged_feature_arrays.items():
        print(f"Merging region-level features into: {scenario_name}")
        datasets_dict = scenarios.get(scenario_name, {})
        updated_df = df.copy()

        for key in region_feature_keys:
            if key in datasets_dict:
                region_df = datasets_dict[key].copy()
                if "Year" in region_df.columns:
                    region_df = region_df.drop(columns=["Year"])
                updated_df = updated_df.merge(region_df, on="Region", how="left")
            else:
                print(f" -> Warning: {key} not found in scenario {scenario_name}")

        enhanced_arrays[scenario_name] = updated_df

    print("All region-level features merged.")
    return enhanced_arrays


######################################




import re

def parse_scenario_keys(scenario_keys):
    parsed_dict = {}
    alias_map = {}
    reverse_alias_map = {}
    
    for idx, key in enumerate(sorted(scenario_keys), 1):
        # Extract all (parameter, value) pairs
        components = re.findall(r'([A-Za-z0-9]+)_(\d+(?:\.\d+)?)', key)
        scenario_dict = {param: float(val) for param, val in components}
        
        # Create an alias like S01, S02, ...
        alias = f"S{idx:02}"
        parsed_dict[alias] = scenario_dict
        alias_map[key] = alias
        reverse_alias_map[alias] = key
    
    return parsed_dict, alias_map, reverse_alias_map

def replace_dict_keys(original_dict, alias_map):
    return {alias_map[k]: v for k, v in original_dict.items() if k in alias_map}



