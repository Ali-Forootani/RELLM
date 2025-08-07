

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 15:17:18 2025

@author: forootan
"""

import gdxpds
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pyomo.environ import *
#from gams import GamsWorkspace, GamsParameter, GamsSet
import os
import sys
import json
from datetime import datetime


def setting_directory(depth):
    current_dir = os.path.abspath(os.getcwd())
    root_dir = current_dir
    for i in range(depth):
        root_dir = os.path.abspath(os.path.join(root_dir, os.pardir))
        sys.path.append(os.path.dirname(root_dir))
    return root_dir


# Set GAMS system directory (update path if needed)
gams_system_dir = setting_directory(0)


#######################################################
#######################################################

###glpat-dAxzB6taHkQzZ_xyXbzr


from RenewableEnergyLanguageModel.scenario_generator import GDXScaler
from RenewableEnergyLanguageModel.feature_construction_fm import compute_global_trend, compute_trend


"""  
Scenario Generation:
    
    Inserting list of variables
    List of Scaling factors corresponding to variables
    
GAMS:
    
$loadR costMargAgri, costInvAgri, costInvLevelAgri, ghgAgri, Agrigrowth, Agriarea0, PeatExtract

"""


gdx_base_file = os.path.join(os.path.abspath(os.getcwd()), "scenarios_neg_emi", "base_scenario.gdx")
output_dir = "~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/Agri_dataset_scenarios"
variables = []
scale_factors = []  # Example scale factors

scaler = GDXScaler(gdx_base_file, output_dir, variables, scale_factors)
scaler.scale_and_save()


#######################################################
#######################################################
#######################################################

gdx_data = gdxpds.to_dataframes(gdx_base_file)

gdx_test_file = os.path.join(os.path.abspath(os.getcwd()), "scenarios_neg_emi/Agri_dataset_scenarios", "costInvAgri_1.2_costInvLevelAgri_1.2_ghgAgri_1.2.gdx")

gdx_test_data = gdxpds.to_dataframes(gdx_test_file)

###########################
###########################
###########################

"""
Extracting required variables for doing simulations
"""

from RenewableEnergyLanguageModel.loading_saving_parms_from_gdx_csv import load_and_save_selected_symbols


gdx_dir = os.path.expanduser("~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/Agri_dataset_scenarios")
save_dir = os.path.expanduser("~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/Agri_csv_outputs")
target_symbols = ["CO2price", "FMsgrowth", "BeechArea0",
                  "costMargAgri", "costInvAgri",
                  "costInvLevelAgri","ghgAgri",
                  "Agriarea0", "PeatExtract",
                  "Agrigrowth"
                  ]

load_and_save_selected_symbols(gdx_dir, target_symbols, save_path=save_dir)


from RenewableEnergyLanguageModel.utiles import load_and_rename_csvs, get_dynamic_rename_mapping_fixed


csv_directory = os.path.expanduser("~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/Agri_csv_outputs")

datasets = load_and_rename_csvs(csv_directory)




import pandas as pd


# Apply dynamic renaming and convert "Year" to numeric
for key, df in datasets.items():
    rename_dict = get_dynamic_rename_mapping_fixed(key)
    if rename_dict:
        df.rename(columns=rename_dict, inplace=True)
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors='coerce')
        

######################################################




from collections import defaultdict

variable_dict = defaultdict(dict)

for key in datasets.keys():
    # Split the key into variable name and scenario
    parts = key.split("_")
    variable = parts[0]
    scenario = "_".join(parts[1:]) if len(parts) > 1 else "base"

    variable_dict[variable][scenario] = datasets[key]



# === EXAMPLE USAGE ===

from RenewableEnergyLanguageModel.scenario_generator import build_scenario_hierarchy


scenarios = build_scenario_hierarchy(datasets)

# Now you can do:
print("All scenarios:", scenarios.keys())


######################################################
######################################################
######################################################


def setting_directory(depth):
    current_dir = os.path.abspath(os.getcwd())
    root_dir = current_dir
    for i in range(depth):
        root_dir = os.path.abspath(os.path.join(root_dir, os.pardir))
        sys.path.append(os.path.dirname(root_dir))
    return root_dir

# Specify the GAMS system directory (Update this path according to your GAMS installation)
gams_system_dir = setting_directory(0)  # Example path for Windows




from RenewableEnergyLanguageModel.utiles import process_all_results_agri_scenarios

# === Example usage ===

gdx_file = gams_system_dir + "/scenarios_neg_emi/"

results_folder = gdx_file + "Results_agri_dataset_scenarios"  # <<<< your folder with Results_*.gdx

#results_folder = "gdx_file"

merged_feature_arrays = process_all_results_agri_scenarios(scenarios, results_folder)

"""
# Save result (optional)
for scenario, df in merged_feature_arrays.items():
    filename = f"{scenario}_features.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {filename}")
"""



"""
Done enhancing all scenarios with Peatextarction
"""

from RenewableEnergyLanguageModel.utiles import enhance_agri_with_global_trends_from_scenarios, enhance_agri_with_region_level_features


enhanced_merged_feature_arrays = enhance_agri_with_global_trends_from_scenarios(merged_feature_arrays, scenarios)



region_feature_keys = ["Agriarea0"]  # extend as needed

fully_enhanced_arrays = enhance_agri_with_region_level_features(
    enhanced_merged_feature_arrays,  # output from previous step
    scenarios,
    region_feature_keys)



# |-------------------------------------------|
# |-------------------------------------------|



from sklearn.preprocessing import MinMaxScaler
import pandas as pd

# === Step 1: Concatenate the enhanced feature arrays ===
# (Choose any subset or all scenarios you want to combine)
combined_df = pd.concat(
    [df for df in fully_enhanced_arrays.values()],
    ignore_index=True
)

# === Step 2: Identify columns to scale (excluding Region and Technology) ===
columns_to_scale = [col for col in combined_df.columns if col not in ["Region", "Technology"]]

# === Step 3: Apply Min-Max Scaling ===
scaler = MinMaxScaler()
combined_df[columns_to_scale] = scaler.fit_transform(combined_df[columns_to_scale])



# === Step 3: Apply Min-Max Scaling ===
scaler = MinMaxScaler()
#fully_enhanced_arrays["CO2price_0.8_FMsgrowth_0.8_BeechArea0_0.8"][columns_to_scale] = scaler.fit_transform(fully_enhanced_arrays["CO2price_0.8_FMsgrowth_0.8_BeechArea0_0.8"][columns_to_scale])


# |-------------------------------------------|
# |-------------------------------------------|



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from RenewableEnergyLanguageModel.gdx_to_csv_function import extract_gdx_results, build_input_output_pairs


#gdx_filename: str, output_dir: str, sub_dir: str


# Parameters
results_folder = gams_system_dir + "/scenarios_neg_emi/Results_agri_dataset_scenarios"
output_dir = gams_system_dir + "/RenewableEnergyLanguageModel/data_agri"




import os
import pandas as pd

# Define paths
results_folder = os.path.join(gams_system_dir, "scenarios_neg_emi/Results_agri_dataset_scenarios")
output_root = os.path.join(gams_system_dir, "RenewableEnergyLanguageModel/data_agri")

# Get all scenario suffixes from available GDX result files
def get_available_results_scenarios(results_folder):
    result_files = [f for f in os.listdir(results_folder) if f.startswith("Results_") and f.endswith(".gdx")]
    return [os.path.splitext(f)[0].replace("Results_", "") for f in result_files]

# Assume extract_gdx_results(gdx_file, output_dir, sub_dir) is already defined
# Main extraction loop
capAgri_dict = {}

scenario_suffixes = get_available_results_scenarios(results_folder)

for suffix in scenario_suffixes:
    gdx_file = os.path.join(results_folder, f"Results_{suffix}.gdx")
    sub_dir = f"Results_{suffix}"
    output_dir = os.path.join(output_root, sub_dir)
    
    # Extract only if not already extracted (optional)
    if not os.path.exists(os.path.join(output_dir, "capAgri_results.csv")):
        extract_gdx_results(gdx_file, output_root, sub_dir=sub_dir)
    
    # Load capAgri CSV if available
    cap_path = os.path.join(output_dir, "capAgri_results.csv")
    
    print(cap_path)
    
    if os.path.exists(cap_path):
        df_cap = pd.read_csv(cap_path)
        capAgri_dict[suffix] = df_cap
    else:
        print(f"⚠️ capAgri_results.csv not found for: {suffix}")

print(f"✅ Loaded capAgri for {len(capAgri_dict)} scenarios.")




"""
27th May -------------------------\---------\
"""



import pandas as pd

# Initialize lists
capAgri_dict_all = []
features_all = []

# Get common keys between both dicts
common_keys = set(capAgri_dict) & set(fully_enhanced_arrays)

for key in sorted(common_keys):
    cap_df = capAgri_dict[key].copy()
    feat_df = fully_enhanced_arrays[key].copy()

    # Sanity checks
    if not isinstance(cap_df, pd.DataFrame):
        raise TypeError(f"costTechFMs_dict[{key}] is not a DataFrame.")
    if not isinstance(feat_df, pd.DataFrame):
        raise TypeError(f"fully_enhanced_arrays[{key}] is not a DataFrame.")

    capAgri_dict_all.append(cap_df)
    features_all.append(feat_df)

# Concatenate vertically
capAgri_dict_all = pd.concat(capAgri_dict_all, axis=0).reset_index(drop=True)
final_feature_array_all = pd.concat(features_all, axis=0).reset_index(drop=True)




# === Step 2: Identify columns to scale (excluding Region and Technology) ===
columns_to_scale = [col for col in combined_df.columns if col not in ["Region", "Technology"]]

# === Step 3: Apply Min-Max Scaling ===
scaler = MinMaxScaler()


final_feature_array_all[columns_to_scale] = scaler.fit_transform(final_feature_array_all[columns_to_scale])


from RenewableEnergyLanguageModel.random_forest_module import (train_and_predict_capAgri_ensemble)



import numpy as np

# Number of rows per part
rows_per_target = 2976 * 17
num_target_parts = 1

# Number of rows per part
rows_per_feature = 96 * 17
num_feature_parts = 1

# Rename for clarity
df_targets_parts = [capAgri_dict_all.iloc[i * rows_per_target:(i + 1) * rows_per_target] 
                    for i in range(num_target_parts)]

df_features_parts = [final_feature_array_all.iloc[i * rows_per_feature:(i + 1) * rows_per_feature] 
                     for i in range(num_feature_parts)]


ensemble_results = []



for i in range(len(df_targets_parts[:num_feature_parts-0])):
    result = train_and_predict_capAgri_ensemble(
        df_targets_parts[i],
        df_features_parts[i],
        n_folds=17)
    ensemble_results.append(result)

# Stack predictions from each part
all_preds = np.stack([res["y_pred_original"] for res in ensemble_results])

# Mean voting across models
global_y_pred = np.mean(all_preds[:,:], axis=0)

# Assume ground truth from the first part (ensure alignment)
global_y_true = ensemble_results[0]["y_test_original"]


from sklearn.metrics import r2_score, mean_squared_error

r2_global = r2_score(global_y_true, global_y_pred)
rmse_global = np.sqrt(mean_squared_error(global_y_true, global_y_pred))

print(f"🌍 Global Voting R²: {r2_global:.4f}")
print(f"🌍 Global Voting RMSE: {rmse_global:.2f} hectars")


###########################################

# Select parts by index (e.g., parts 2, 3, 4, 5 in 0-based index are 1, 2, 3, 4)
#selected_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

selected_indices = [0]


# Select parts by index (e.g., parts 2, 3, 4, 5 in 0-based index are 1, 2, 3, 4)
#selected_indices = [2, 5, 7, 8, 10, 11, 12, 13]


ensemble_results = []

for i in selected_indices:
    result = train_and_predict_capAgri_ensemble(
        df_targets_parts[i],
        df_features_parts[i],
        n_folds=17)
    ensemble_results.append(result)

# Stack predictions from each part
all_preds = np.stack([res["y_pred_original"] for res in ensemble_results])

# Mean voting across models
global_y_pred = np.mean(all_preds, axis=0)

# Assume ground truth from the first selected part
global_y_true = ensemble_results[0]["y_test_original"]

from sklearn.metrics import r2_score, mean_squared_error

r2_global = r2_score(global_y_true, global_y_pred)
rmse_global = np.sqrt(mean_squared_error(global_y_true, global_y_pred))

print(f"🌍 Global Voting R²: {r2_global:.4f}")
print(f"🌍 Global Voting RMSE: {rmse_global:.2f} hectars")



plt.figure(figsize=(8, 6))
plt.scatter(global_y_true, global_y_pred, alpha=0.6, edgecolor='k')
plt.plot([global_y_true.min(), global_y_true.max()],
         [global_y_pred.min(), global_y_pred.max()], 'r--', lw=2)
plt.xlabel("Actual capAgri (scaled)")
plt.ylabel("Predicted capAgri (scaled)")
plt.title("Predicted vs Actual capAgri (scaled)")
plt.grid(True)
plt.tight_layout()
plt.show()






#################################################



from RenewableEnergyLanguageModel.utiles import parse_scenario_keys, replace_dict_keys
from RenewableEnergyLanguageModel.llm_scenario_query import interpret_stakeholder_query_with_prompt

from RenewableEnergyLanguageModel.correlations_module import (plot_scenario_correlations,
                                                   plot_scenario_dendrogram,
                                                   find_most_and_least_similar_scenarios,
                                                   plot_capAgri_correlation,
                                                   plot_scenario_correlations_better
                                                   )



# Use the keys from either dict (assuming both have matching keys)
scenario_keys = fully_enhanced_arrays.keys()
# Parse and alias
scenario_meta_dict, alias_map, reverse_alias_map = parse_scenario_keys(scenario_keys)
# Replace the keys in both dictionaries
fully_enhanced_arrays_aliased = replace_dict_keys(fully_enhanced_arrays, alias_map)
capAgri_dict_aliased = replace_dict_keys(capAgri_dict, alias_map)



correlation_matrix = plot_scenario_correlations(fully_enhanced_arrays_aliased)

linkage_matrix = plot_scenario_dendrogram(correlation_matrix)
most_similar, max_corr, least_similar, min_corr = find_most_and_least_similar_scenarios(correlation_matrix)



correlation_matrix_capAgri = plot_capAgri_correlation(capAgri_dict_aliased)
linkage_matrix_output = plot_scenario_dendrogram(correlation_matrix_capAgri)
most_similar_capAgri, max_corr_cost, least_similar_cost, min_corr_cost = find_most_and_least_similar_scenarios(correlation_matrix_capAgri)
#plot_cost_output_correlation_heatmap(correlation_matrix_capAgri)







"""
28th May -------------------------\---------\
"""





"""
# Use the keys from either dict (assuming both have matching keys)
scenario_keys = fully_enhanced_arrays.keys()
# Parse and alias
scenario_meta_dict, alias_map, reverse_alias_map = parse_scenario_keys(scenario_keys)
# Replace the keys in both dictionaries
fully_enhanced_arrays_aliased = replace_dict_keys(fully_enhanced_arrays, alias_map)
costTechFMs_dict_aliased = replace_dict_keys(costTechFMs_dict, alias_map)
"""


import os
from openai import OpenAI

# Step 1: Set API credentials and initialize client
os.environ["OPENAI_API_KEY"] = "glpat-9yb_koabaZYLzUMZm-hg"
os.environ["OPENAI_API_BASE"] = "https://helmholtz-blablador.fz-juelich.de:8000/v1"

client = OpenAI(
    api_key="glpat-9yb_koabaZYLzUMZm-hg",
    base_url="https://helmholtz-blablador.fz-juelich.de:8000/v1"
)

# Step 2: Ask a stakeholder query
query = "What happens if CO2 price increases by 20%?"


parsed_dict, alias_map, reverse_alias_map = parse_scenario_keys(scenario_keys)

# Step 3: Use helper function to get prompt for LLM
result = interpret_stakeholder_query_with_prompt(
    query,
    parsed_dict,
    alias_map,
    reverse_alias_map,
    linkage_matrix_output,          # Or linkage_matrix if you're using input features
    correlation_matrix_capAgri  # Or input correlation matrix
)

# Optional: Inspect summary (for debug/logging)
print("Scenario Summary:")
print(result["summary"])

# Step 4: Ask your Helmholtz-hosted LLM using the prompt
llm_prompt = result["llm_prompt"]

response = client.chat.completions.create(
    model="alias-code",
    messages=[
        {"role": "system", "content": "You are a helpful assistant skilled in climate scenario analysis."},
        {"role": "user", "content": llm_prompt}
    ]
)

# Step 5: Print or use the LLM's response
print("\n🔍 OpenAI Response:")
print(response.choices[0].message.content)



"""
30th May -----------------------------\-----------\
"""


######################################################
######################################################
######################################################
