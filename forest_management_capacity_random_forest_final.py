#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 16:55:39 2025

@author: forootan
"""



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
import gdxpds

########################################


from RenewableEnergyLanguageModel.scenario_generator import GDXScaler
from RenewableEnergyLanguageModel.feature_construction_fm import compute_global_trend, compute_trend

########################################
########################################

"""  
Scenario Generation:
    
    Inserting list of variables
    List of Scaling factors corresponding to variables
    variables = ["FMsgrowth", "costInvLevelFMs"]
    scale_factors = [1.2]  # Example scale factors
    
"""


gdx_base_file = os.path.join(os.path.abspath(os.getcwd()), "scenarios_neg_emi", "base_scenario.gdx")
output_dir = "~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/dataset_scenarios"
variables = []
scale_factors = []  # Example scale factors

scaler = GDXScaler(gdx_base_file, output_dir, variables, scale_factors)
scaler.scale_and_save()


##########################
##########################

gdx_data = gdxpds.to_dataframes(gdx_base_file)


###########################
###########################
###########################

"""
Extracting required variables for doing simulations
"""

from RenewableEnergyLanguageModel.loading_saving_parms_from_gdx_csv import load_and_save_selected_symbols



gdx_dir = os.path.expanduser("~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/dataset_scenarios")
save_dir = os.path.expanduser("~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/csv_outputs")
target_symbols = ["CO2price", "FMsgrowth", "BeechArea0",
                  "ghgTargetLULUCF", "costInvLevelFMs",
                  "costMargFMs","costInvFMs",
                  "ghgFMs", "GrassArea0",
                  ]

load_and_save_selected_symbols(gdx_dir, target_symbols, save_path=save_dir)



#############################################################
#############################################################
#############################################################
#############################################################



from RenewableEnergyLanguageModel.utiles import load_and_rename_csvs, get_dynamic_rename_mapping_fixed



csv_directory = os.path.expanduser("~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/csv_outputs")

datasets = load_and_rename_csvs(csv_directory)


print(datasets)




################################################
################################################



# Apply dynamic renaming and convert "Year" to numeric
for key, df in datasets.items():
    print(key)
    print(df)
    #print("+++++++++++++++++++++++++++")
    rename_dict = get_dynamic_rename_mapping_fixed(key)
    if rename_dict:
        df.rename(columns=rename_dict, inplace=True)
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors='coerce')
        
    





print(datasets)


############################################
############################################
############################################


from collections import defaultdict

variable_dict = defaultdict(dict)

for key in datasets.keys():
    # Split the key into variable name and scenario
    parts = key.split("_")
    variable = parts[0]
    scenario = "_".join(parts[1:]) if len(parts) > 1 else "base"

    variable_dict[variable][scenario] = datasets[key]

# Usage
# variable_dict["costInvFMs"]["CO2price_0.8_FMsgrowth_0.8_BeechArea0_0.8"]


############################################
############################################
############################################

"""
from collections import defaultdict
import re

def build_scenario_hierarchy(datasets):
    """
    #Build hierarchical scenario dictionary from dataset keys.
    
    #Output structure:
    
    #scenarios = {
    #    'CO2price_0.8_FMsgrowth_0.8_BeechArea0_0.8': {
    #        'costInvFMs': dataset,
    #        'FMsgrowth': dataset,
    #        'BeechArea0': dataset,
    #        ...
    #    },
    #    ...
    #}
    
"""
    scenarios = defaultdict(dict)
    
    pattern = re.compile(r"(?P<variable>^[^_]+)(?:_(?P<params>.+))?")
    
    for key in datasets.keys():
        match = pattern.match(key)
        if match:
            variable = match.group("variable")
            params = match.group("params")

            # If there are params, build scenario key
            if params:
                scenario = params
            else:
                scenario = "base"  # for base scenarios

            scenarios[scenario][variable] = datasets[key]

    return scenarios
"""


# === EXAMPLE USAGE ===

from RenewableEnergyLanguageModel.scenario_generator import build_scenario_hierarchy


scenarios = build_scenario_hierarchy(datasets)

# Now you can do:
print("All scenarios:", scenarios.keys())


for i in range(0, 30):
    
    # Example:
    example_scenario = list(scenarios.keys())[i]
    
    print("\nDatasets available for scenario:", example_scenario)
    print(scenarios[example_scenario].keys())
    
    #print(print(scenarios[example_scenario]["ghgFMs"]))
############################################
############################################
############################################


def setting_directory(depth):
    current_dir = os.path.abspath(os.getcwd())
    root_dir = current_dir
    for i in range(depth):
        root_dir = os.path.abspath(os.path.join(root_dir, os.pardir))
        sys.path.append(os.path.dirname(root_dir))
    return root_dir

# Specify the GAMS system directory (Update this path according to your GAMS installation)
gams_system_dir = setting_directory(1)  # Example path for Windows






from RenewableEnergyLanguageModel.utiles import process_all_results_scenarios

# === Example usage ===

gdx_file = gams_system_dir + "/scenarios_neg_emi/"

results_folder = gdx_file + "/Results_dataset_scenarios"  # <<<< your folder with Results_*.gdx

#results_folder = "gdx_file"

merged_feature_arrays = process_all_results_scenarios(scenarios, results_folder)

# Save result (optional)
for scenario, df in merged_feature_arrays.items():
    filename = f"{scenario}_features.csv"
    df.to_csv(filename, index=False)
    print(f"Saved {filename}")


############################################
############################################
###############################################################################
####################################################################################################
##############################################################################################################################

"""
Done enhancing all scenarios with CO2 and GHG trend features.
"""

from RenewableEnergyLanguageModel.utiles import enhance_with_global_trends_from_scenarios, enhance_with_region_level_features


enhanced_merged_feature_arrays = enhance_with_global_trends_from_scenarios(merged_feature_arrays, scenarios)



region_feature_keys = ["BeechArea0", "GrassArea0"]  # extend as needed
fully_enhanced_arrays = enhance_with_region_level_features(
    enhanced_merged_feature_arrays,  # output from previous step
    scenarios,
    region_feature_keys)



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


############################################
############################################
############################################
############################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from RenewableEnergyLanguageModel.gdx_to_csv_function import extract_gdx_results, build_input_output_pairs


#gdx_filename: str, output_dir: str, sub_dir: str


# Parameters
results_folder = gams_system_dir + "/scenarios_neg_emi/Results_dataset_scenarios"
output_dir = gams_system_dir + "/RenewableEnergyLanguageModel/data"



################################################

import os
import pandas as pd

# Define paths
results_folder = os.path.join(gams_system_dir, "scenarios_neg_emi/Results_dataset_scenarios")
output_root = os.path.join(gams_system_dir, "RenewableEnergyLanguageModel/data")

# Get all scenario suffixes from available GDX result files
def get_available_results_scenarios(results_folder):
    result_files = [f for f in os.listdir(results_folder) if f.startswith("Results_") and f.endswith(".gdx")]
    return [os.path.splitext(f)[0].replace("Results_", "") for f in result_files]

# Assume extract_gdx_results(gdx_file, output_dir, sub_dir) is already defined
# Main extraction loop
capFMs_dict = {}

scenario_suffixes = get_available_results_scenarios(results_folder)

for suffix in scenario_suffixes:
    gdx_file = os.path.join(results_folder, f"Results_{suffix}.gdx")
    sub_dir = f"Results_{suffix}"
    output_dir = os.path.join(output_root, sub_dir)
    
    # Extract only if not already extracted (optional)
    if not os.path.exists(os.path.join(output_dir, "capFMs_results.csv")):
        extract_gdx_results(gdx_file, output_root, sub_dir=sub_dir)
    
    # Load capFMs CSV if available
    cap_path = os.path.join(output_dir, "capFMs_results.csv")
    if os.path.exists(cap_path):
        df_cap = pd.read_csv(cap_path)
        capFMs_dict[suffix] = df_cap
    else:
        print(f"⚠️ capFMs_results.csv not found for: {suffix}")

print(f"✅ Loaded capFMs for {len(capFMs_dict)} scenarios.")



###############################################




import pandas as pd

# Initialize lists
capFMs_all = []
features_all = []

# Get common keys between both dicts
common_keys = set(capFMs_dict) & set(fully_enhanced_arrays)

for key in sorted(common_keys):
    cap_df = capFMs_dict[key].copy()
    feat_df = fully_enhanced_arrays[key].copy()

    # Sanity checks
    if not isinstance(cap_df, pd.DataFrame):
        raise TypeError(f"capFMs_dict[{key}] is not a DataFrame.")
    if not isinstance(feat_df, pd.DataFrame):
        raise TypeError(f"fully_enhanced_arrays[{key}] is not a DataFrame.")

    capFMs_all.append(cap_df)
    features_all.append(feat_df)

# Concatenate vertically
df_capFMs_all = pd.concat(capFMs_all, axis=0).reset_index(drop=True)
final_feature_array_all = pd.concat(features_all, axis=0).reset_index(drop=True)





from RenewableEnergyLanguageModel.random_forest_module import (train_and_predict_capFMs,
                                                    train_and_predict_capFMs_ensemble,
                                                    compute_ensemble_shap)


"""
results_ensemble = train_and_predict_capFMs_ensemble(
    capFMs_dict["CO2price_0.8_FMsgrowth_0.8_BeechArea0_0.8"],
    fully_enhanced_arrays["CO2price_0.8_FMsgrowth_0.8_BeechArea0_0.8"], n_folds = 2)

print(f"📈 R² (scaled): {results_ensemble['r2_scaled']:.4f}")
print(f"📉 RMSE (scaled): {results_ensemble['rmse_scaled']:.4f}")
print(f"📈 R² (original): {results_ensemble['r2_original']:.4f}")
print(f"📉 RMSE (original): {results_ensemble['rmse_original']:.2f} hectares")

# Get true and predicted values
y_pred_original = results_ensemble["y_pred_original"]
y_test_original = results_ensemble["y_test_original"]

# No single model anymore, it's a list of models
models = results_ensemble["models"]  
X_train = results_ensemble["X_train"]
X_test = results_ensemble["X_test"]
encoder = results_ensemble["encoder"]

# Visualization: Predicted vs Actual
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(y_test_original, y_pred_original, alpha=0.6, edgecolor='k')
plt.plot([y_test_original.min(), y_test_original.max()],
         [y_test_original.min(), y_test_original.max()], 'r--', lw=2)
plt.xlabel("Actual capFMs (ha)")
plt.ylabel("Predicted capFMs (ha)")
plt.title("Predicted vs Actual capFMs (Ensemble Voting)")
plt.grid(True)
plt.tight_layout()
plt.show()
"""


#######################################################
#######################################################
#######################################################

final_feature_array_all[columns_to_scale] = scaler.fit_transform(final_feature_array_all[columns_to_scale])



results_ensemble = train_and_predict_capFMs_ensemble(
    df_capFMs_all,
    final_feature_array_all, n_folds = 10)

print(f"📈 R² (scaled): {results_ensemble['r2_scaled']:.4f}")
print(f"📉 RMSE (scaled): {results_ensemble['rmse_scaled']:.4f}")
print(f"📈 R² (original): {results_ensemble['r2_original']:.4f}")
print(f"📉 RMSE (original): {results_ensemble['rmse_original']:.2f} hectares")

# Get true and predicted values
y_pred_original = results_ensemble["y_pred_original"]
y_test_original = results_ensemble["y_test_original"]

# No single model anymore, it's a list of models
models = results_ensemble["models"]  
X_train = results_ensemble["X_train"]
X_test = results_ensemble["X_test"]
encoder = results_ensemble["encoder"]

# Visualization: Predicted vs Actual
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(y_test_original, y_pred_original, alpha=0.6, edgecolor='k')
plt.plot([y_test_original.min(), y_test_original.max()],
         [y_test_original.min(), y_test_original.max()], 'r--', lw=2)
plt.xlabel("Actual capFMs (ha)")
plt.ylabel("Predicted capFMs (ha)")
plt.title("Predicted vs Actual capFMs (Ensemble Voting)")
plt.grid(True)
plt.tight_layout()
plt.show()


#######################################################
#######################################################
#######################################################

import shap
import numpy as np

sample_size = 2
n_samples = 10

# Example usage:
aggregated_shap_values = compute_ensemble_shap(models, X_test, sample_size= sample_size, n_samples= n_samples)

# Visualize the aggregated SHAP values (summary plot)
#shap.summary_plot(aggregated_shap_values, X_test)

# Randomly sample the same subset of X_test that was used for SHAP calculations
sampled_indices = np.random.choice(X_test.index, size=sample_size, replace=False)
X_test_sampled = X_test.loc[sampled_indices]

# Now plot the SHAP values for the sampled subset
shap.summary_plot(aggregated_shap_values, X_test_sampled)

#######################################
#######################################
#######################################

import shap
import pandas as pd
import numpy as np

# Assuming `aggregated_shap_values` is a numpy.ndarray containing the SHAP values for the model (or ensemble)
# `X_test` is the feature set used to generate the SHAP values

# Get the absolute SHAP values to sort features by importance
shap_values_abs = np.abs(aggregated_shap_values)

# Sum the absolute SHAP values for each feature (this gives the overall importance)
feature_importance = shap_values_abs.mean(axis=0)

# Get feature names (assuming `X_test` has column names)
feature_names = X_test.columns

# Create a DataFrame to store feature importance and feature names
shap_df = pd.DataFrame({
    'Feature': feature_names,
    'SHAP Value (mean abs)': feature_importance
})

# Sort by the highest absolute SHAP values (importance)
shap_df_sorted = shap_df.sort_values(by='SHAP Value (mean abs)', ascending=False)

# Extract the top N features
top_n = 3  # Change to the number of top features you want
top_features = shap_df_sorted.head(top_n)

print(top_features)



#######################################
#######################################
#######################################
# Assuming top_features is a DataFrame containing the top features
top_features = shap_df_sorted.head(top_n)

# Extract the top feature names and SHAP values for the prompt
top_feature_names = top_features['Feature'].tolist()
top_shap_vals = top_features['SHAP Value (mean abs)'].tolist()
top_feature_vals = [X_test[feature].mean() for feature in top_feature_names]





# Group by 'r' (region) and 'techFMs' (technology), and calculate the mean of 'capFMs' for each combination
region_capFMs = df_capFMs_all.groupby('r')['capFMs'].mean().reset_index()
tech_capFMs = df_capFMs_all.groupby('techFMs')['capFMs'].mean().reset_index()

# Find the region with the highest average capFMs
best_region_row = region_capFMs.loc[region_capFMs['capFMs'].idxmax()]
best_region = best_region_row['r']

# Find the technology with the highest average capFMs
best_tech_row = tech_capFMs.loc[tech_capFMs['capFMs'].idxmax()]
best_tech = best_tech_row['techFMs']




# Now use these variables in your prompt
prompt = f"""
You are a sustainability analyst preparing a summary report for stakeholders, based on a machine learning ensemble model and SHAP analysis focused on forest management capacity (`capFMs`).

🎯 **Objective**: Predict and understand the key drivers of forest management capacity (`capFMs`)

📊 **Model Performance**:  
• R² Score: {results_ensemble['r2_original']:.4f}  
• RMSE: {results_ensemble['rmse_original']:.2f} hectares

🔍 **Top 3 Influential Features (from SHAP analysis across ensemble models)**:  
1. **{top_feature_names[0]}** – SHAP = {top_shap_vals[0]:.3f}, Avg value = {top_feature_vals[0]:.3f}  
2. **{top_feature_names[1]}** – SHAP = {top_shap_vals[1]:.3f}, Avg value = {top_feature_vals[1]:.3f}  
3. **{top_feature_names[2]}** – SHAP = {top_shap_vals[2]:.3f}, Avg value = {top_feature_vals[2]:.3f}

🌍 **Regional & Policy Highlights**:  
• Region with highest capFMs potential: **{best_region}**  
• Leading growth technology: **{best_tech}**  


✏️ **Task**:  
Craft a clear and professional report that:
- Summarizes the ensemble model's performance in non-technical terms  
- Interprets how the top 3 features influence capFMs outcomes across the ensemble models  
- Highlights regional and technological opportunities  
- Recommends actions that align with long-term decarbonization goals  

The tone should be insight-driven, stakeholder-friendly, and suitable for regional planners, policymakers, and sustainability investors. Avoid equations or technical jargon—focus on actionable insights.
"""


import os
from openai import OpenAI


# Set OpenAI API key and base URL
os.environ["OPENAI_API_KEY"] = "glpat-JHd9xWcVcu2NY76LAK_A"
os.environ["OPENAI_API_BASE"] = "https://helmholtz-blablador.fz-juelich.de:8000/v1"

api_key = "glpat-JHd9xWcVcu2NY76LAK_A"
api_base = "https://helmholtz-blablador.fz-juelich.de:8000/v1"

# Initialize the OpenAI client
client = OpenAI(api_key=api_key, base_url=api_base)


response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant skilled in climate dataset analysis.",
        },
        {"role": "user", "content": prompt},
    ],
)

# -----------------------------
# 6) Print the response
# -----------------------------
print("OpenAI Response:")
print(response.choices[0].message.content)



#####################################################
#####################################################
#####################################################

