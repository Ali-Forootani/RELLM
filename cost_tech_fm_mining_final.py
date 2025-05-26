#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 09:04:18 2025

@author: forootan
"""


import gdxpds

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
import numpy as np

###########################################################
###########################################################


from RenewableEnergyLanguageModel.scenario_generator import GDXScaler
from RenewableEnergyLanguageModel.feature_construction_fm import compute_global_trend, compute_trend


"""  
Scenario Generation:
    
    Inserting list of variables
    List of Scaling factors corresponding to variables
    
GAMS:
    
$loadR costMargFMs, costInvFMs, costInvLevelFMs, ghgFMs,
cap0FMs, ghgTargetLULUCF, FMsgrowth, BeechArea0,GrassArea0

Results_cap0FMs_0.8_ghgTargetLULUCF_0.8_FMsgrowth_0.8_BeechArea0_GrassArea0_0.8
"""


gdx_base_file = os.path.join(os.path.abspath(os.getcwd()), "scenarios_neg_emi", "base_scenario.gdx")
output_dir = "~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/dataset_scenarios"
variables = []
scale_factors = []  # Example scale factors

scaler = GDXScaler(gdx_base_file, output_dir, variables, scale_factors)
scaler.scale_and_save()



###########################################################
###########################################################    
    


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



from RenewableEnergyLanguageModel.utiles import load_and_rename_csvs, get_dynamic_rename_mapping_fixed



csv_directory = os.path.expanduser("~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/csv_outputs")

datasets = load_and_rename_csvs(csv_directory)


print(datasets)




################################################
################################################

import pandas as pd


# Apply dynamic renaming and convert "Year" to numeric
for key, df in datasets.items():
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
gams_system_dir = setting_directory(0)  # Example path for Windows






from RenewableEnergyLanguageModel.utiles import process_all_results_scenarios

# === Example usage ===

gdx_file = gams_system_dir + "/scenarios_neg_emi/"

results_folder = gdx_file + "Results_dataset_scenarios"  # <<<< your folder with Results_*.gdx

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
costTechFMs_dict = {}

scenario_suffixes = get_available_results_scenarios(results_folder)

for suffix in scenario_suffixes:
    gdx_file = os.path.join(results_folder, f"Results_{suffix}.gdx")
    sub_dir = f"Results_{suffix}"
    output_dir = os.path.join(output_root, sub_dir)
    
    # Extract only if not already extracted (optional)
    if not os.path.exists(os.path.join(output_dir, "costTechFMs.csv")):
        extract_gdx_results(gdx_file, output_root, sub_dir=sub_dir)
    
    # Load capFMs CSV if available
    cap_path = os.path.join(output_dir, "costTechFMs.csv")
    
    print(cap_path)
    
    if os.path.exists(cap_path):
        df_cap = pd.read_csv(cap_path)
        costTechFMs_dict[suffix] = df_cap
    else:
        print(f"⚠️ costTechFMs_results.csv not found for: {suffix}")

print(f"✅ Loaded costTechFMs for {len(costTechFMs_dict)} scenarios.")





import pandas as pd

# Initialize lists
costTechFMs_dict_all = []
features_all = []

# Get common keys between both dicts
common_keys = set(costTechFMs_dict) & set(fully_enhanced_arrays)

for key in sorted(common_keys):
    cap_df = costTechFMs_dict[key].copy()
    feat_df = fully_enhanced_arrays[key].copy()

    # Sanity checks
    if not isinstance(cap_df, pd.DataFrame):
        raise TypeError(f"costTechFMs_dict[{key}] is not a DataFrame.")
    if not isinstance(feat_df, pd.DataFrame):
        raise TypeError(f"fully_enhanced_arrays[{key}] is not a DataFrame.")

    costTechFMs_dict_all.append(cap_df)
    features_all.append(feat_df)

# Concatenate vertically
costTechFMs_dict_all = pd.concat(costTechFMs_dict_all, axis=0).reset_index(drop=True)
final_feature_array_all = pd.concat(features_all, axis=0).reset_index(drop=True)



#############################################
#############################################


"""
Finding corrolations between scenarios and their results
Statistical Analysis
PCA
"""


from RenewableEnergyLanguageModel.utiles import parse_scenario_keys, replace_dict_keys
from RenewableEnergyLanguageModel.llm_scenario_query import interpret_stakeholder_query_with_prompt

from RenewableEnergyLanguageModel.correlations_module import (plot_scenario_correlations,
                                                   plot_scenario_dendrogram,
                                                   find_most_and_least_similar_scenarios,
                                                   plot_costTechFMs_correlation,
                                                   pca_projection,
                                                   mds_projection,
                                                   compute_silhouette,
                                                   scenario_cca,
                                                   cca_feature_importance,
                                                   cca_feature_importance_flat,
                                                   pca_features,
                                                   pca_outputs,
                                                   pca_features_per_scenario,
                                                   pca_features_colored,
                                                   pca_features_colored_by_region_tech,
                                                   pca_outputs_colored_by_region_tech,
                                                   get_pca_embedding,
                                                   plot_dendrogram_pca,
                                                   kernel_pca_projection_sampled,
                                                   plot_cost_output_correlation_heatmap,
                                                   generate_pca_summary_text
                                                   )



# Use the keys from either dict (assuming both have matching keys)
scenario_keys = fully_enhanced_arrays.keys()
# Parse and alias
scenario_meta_dict, alias_map, reverse_alias_map = parse_scenario_keys(scenario_keys)
# Replace the keys in both dictionaries
fully_enhanced_arrays_aliased = replace_dict_keys(fully_enhanced_arrays, alias_map)
costTechFMs_dict_aliased = replace_dict_keys(costTechFMs_dict, alias_map)



correlation_matrix = plot_scenario_correlations(fully_enhanced_arrays_aliased)
linkage_matrix = plot_scenario_dendrogram(correlation_matrix)
most_similar, max_corr, least_similar, min_corr = find_most_and_least_similar_scenarios(correlation_matrix)
plot_cost_output_correlation_heatmap(correlation_matrix)



correlation_matrix_costTechFMs = plot_costTechFMs_correlation(costTechFMs_dict_aliased)
linkage_matrix_output = plot_scenario_dendrogram(correlation_matrix_costTechFMs)
most_similar_cost, max_corr_cost, least_similar_cost, min_corr_cost = find_most_and_least_similar_scenarios(correlation_matrix_costTechFMs)
plot_cost_output_correlation_heatmap(correlation_matrix_costTechFMs)





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
os.environ["OPENAI_API_KEY"] = "glpat-JHd9xWcVcu2NY76LAK_A"
os.environ["OPENAI_API_BASE"] = "https://helmholtz-blablador.fz-juelich.de:8000/v1"

client = OpenAI(
    api_key="glpat-JHd9xWcVcu2NY76LAK_A",
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
    correlation_matrix_costTechFMs  # Or input correlation matrix
)

# Optional: Inspect summary (for debug/logging)
print("Scenario Summary:")
print(result["summary"])

# Step 4: Ask your Helmholtz-hosted LLM using the prompt
llm_prompt = result["llm_prompt"]

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant skilled in climate scenario analysis."},
        {"role": "user", "content": llm_prompt}
    ]
)

# Step 5: Print or use the LLM's response
print("\n🔍 OpenAI Response:")
print(response.choices[0].message.content)



"""
END OF THIS Module!!! Furthur ANALYSIS WILL BE FOR OTHER VARIABLES
"""





###################################################################################
###################################################################################
###################################################################################
###################################################################################





###################################################################################
###################################################################################
###################################################################################
###################################################################################


pca_projection(fully_enhanced_arrays_aliased , value_column=None, title="PCA of Input Features (fully_enhanced_arrays)")


pca_projection(costTechFMs_dict_aliased , value_column="costTechFMs", title="PCA of Output costTechFMs")




mds_projection(fully_enhanced_arrays_aliased )







from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import silhouette_score

# After linkage_matrix (Z) is obtained:
n_clusters = 15  # or chosen based on dendrogram
cluster_labels = fcluster(linkage_matrix, n_clusters, criterion='maxclust')

# Use the scenario_matrix from your correlation code
# (if you use correlation, convert it to distances)
sil_score = silhouette_score(1 - correlation_matrix.values, cluster_labels, metric='precomputed')
print(f"Silhouette score for {n_clusters} clusters: {sil_score:.2f}")

cca, X_c, Y_c, scenario_names, corrs = scenario_cca(
    fully_enhanced_arrays,
    costTechFMs_dict,
    input_value_column=None,         # Use all numeric input features
    output_value_column="costTechFMs",
    n_components=2,                 # Number of canonical dimensions
    pca_reduce=(10, 14),             # Optional: reduce input/output to (10,5) PCs before CCA, or None
    plot=True
)


x_weights = cca.x_weights_[:, 0]
top_input_indices = np.argsort(np.abs(x_weights))[::-1][:10]
print("Top 10 input indices for Canonical Var 1:")
for idx in top_input_indices:
    print(f"input_{idx}: {x_weights[idx]:.4f}")


y_weights = cca.y_weights_[:, 0]
top_output_indices = np.argsort(np.abs(y_weights))[::-1][:10]
print("Top 10 output indices for Canonical Var 1:")
for idx in top_output_indices:
    print(f"output_{idx}: {y_weights[idx]:.4f}")


from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=4, random_state=0)
cluster_labels = kmeans.fit_predict(X_c[:, :2])

plt.figure(figsize=(10,14))
plt.scatter(X_c[:, 0], X_c[:, 1], c=cluster_labels, cmap='tab10', s=120)
for i, name in enumerate(scenario_names):
    plt.text(X_c[i, 0], X_c[i, 1], name, fontsize=12)
plt.xlabel("Canonical Var 1")
plt.ylabel("Canonical Var 2")
plt.title("Clustering in Canonical Space")
plt.grid(True)
plt.show()



from scipy.spatial.distance import pdist, squareform

distances = squareform(pdist(X_c[:, :2]))  # pairwise distances in 2D canonical space



pca_features(final_feature_array_all, 10)


pca_outputs(costTechFMs_dict_all)

pca_features_per_scenario(fully_enhanced_arrays_aliased)

pca_features_colored(final_feature_array_all)


pca_features_colored(costTechFMs_dict_all, "r")


pca_input, df_pca_input = pca_features_colored_by_region_tech(final_feature_array_all)


pca_output, df_pca_output = pca_outputs_colored_by_region_tech(costTechFMs_dict_all)


pca_output, df_pca_output = pca_outputs_colored_by_region_tech(costTechFMs_dict_aliased["S01"])

pca_output, df_pca_output = pca_outputs_colored_by_region_tech(costTechFMs_dict_aliased["S12"])

df_summary = df_pca_output.groupby("Region_Tech")[["PC1", "PC2"]].mean().reset_index()

top_extremes = df_pca_output.loc[df_pca_output["PC1"].abs().nlargest(10).index]


pca_summary_text = generate_pca_summary_text(df_pca_output, top_k=5)

# Add this to your existing LLM prompt
result["llm_prompt"] += f"\n\n📊 PCA Insight:\n{pca_summary_text}"





kernel_pca_projection_sampled(costTechFMs_dict_all)



from sklearn.svm import SVC

# Assume df_pca is the output from your PCA
X_pca = df_pca_output[["PC1", "PC2"]].values




X_pca, df = get_pca_embedding(final_feature_array_all)

plot_dendrogram_pca(X_pca, labels=None, method='ward')






from sklearn.kernel_approximation import Nystroem
from sklearn.decomposition import PCA

# Feature map approximation using Nystroem method
feature_map_nystroem = Nystroem(kernel='rbf', gamma=1e-4, n_components=100)
X_features = feature_map_nystroem.fit_transform(X_scaled)

# Linear PCA on kernel features
pca = PCA(n_components=2)
X_kpca_approx = pca.fit_transform(X_features)


#################################################################



# Use the keys from either dict (assuming both have matching keys)
scenario_keys = fully_enhanced_arrays.keys()

# Parse and alias
scenario_meta_dict, alias_map, reverse_alias_map = parse_scenario_keys(scenario_keys)

# Replace the keys in both dictionaries
fully_enhanced_arrays_aliased = replace_dict_keys(fully_enhanced_arrays, alias_map)

costTechFMs_dict_aliased = replace_dict_keys(costTechFMs_dict, alias_map)













##############################################
##############################################


from scipy.cluster.hierarchy import fcluster

# Z: linkage matrix from hierarchical clustering (e.g., from your dendrogram code)
k = 2  # Number of clusters you want to define (change as needed)
labels = fcluster(linkage_matrix, k, criterion='maxclust')

print(labels)  # 1D array, one cluster label per scenario (order matches scenario_matrix_T)





#############################################
#############################################


from RenewableEnergyLanguageModel.random_forest_module import (train_and_predict_capFMs,
                                                    train_and_predict_costTechFMs_ensemble,
                                                    compute_ensemble_shap)


"""
results_ensemble = train_and_predict_costTechFMs_ensemble(
    costTechFMs_dict["CO2price_0.8_FMsgrowth_1.0_BeechArea0_1.0"],
    fully_enhanced_arrays["CO2price_0.8_FMsgrowth_1.0_BeechArea0_1.0"], n_folds = 1)

# Print evaluation metrics
print(f"📈 R² (scaled): {results_ensemble['r2_scaled']:.4f}")
print(f"📉 RMSE (scaled): {results_ensemble['rmse_scaled']:.4f}")
print(f"📈 R² (original): {results_ensemble['r2_original']:.4f}")
print(f"📉 RMSE (original): {results_ensemble['rmse_original']:.2f} euros")

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
plt.xlabel("Actual costTechFMs (euros)")  # Updated to reflect the new target
plt.ylabel("Predicted costTechFMs (euros)")  # Updated to reflect the new target
plt.title("Predicted vs Actual costTechFMs (Ensemble Voting)")  # Updated to reflect the new target
plt.grid(True)
plt.tight_layout()
plt.show()
"""

##############################################

final_feature_array_all[columns_to_scale] = scaler.fit_transform(final_feature_array_all[columns_to_scale])


# Number of rows per part
rows_per_part = 3472

# Calculate the number of parts
num_parts = len(costTechFMs_dict_all) // rows_per_part

# Split the DataFrame into parts
parts = [costTechFMs_dict_all.iloc[i * rows_per_part:(i + 1) * rows_per_part] for i in range(num_parts)]

# Check the first part
print(parts[0].shape)  # This will print the shape of the first part

# Check the last part
print(parts[-1].shape)  # This will print the shape of the last part





# Number of rows per part
rows_per_part = 112

# Calculate the number of parts
num_parts = len(final_feature_array_all) // rows_per_part

# Split the DataFrame into parts
feature_parts = [final_feature_array_all.iloc[i * rows_per_part:(i + 1) * rows_per_part] for i in range(num_parts)]

# Check the first part
print(feature_parts[0].shape)  # This will print the shape of the first part

# Check the last part
print(feature_parts[-1].shape)  # This will print the shape of the last part




##############################################


results_ensemble = train_and_predict_costTechFMs_ensemble(
    parts[0],
    feature_parts[0], n_folds = 1)




# Print evaluation metrics
print(f"📈 R² (scaled): {results_ensemble['r2_scaled']:.4f}")
print(f"📉 RMSE (scaled): {results_ensemble['rmse_scaled']:.4f}")
print(f"📈 R² (original): {results_ensemble['r2_original']:.4f}")
print(f"📉 RMSE (original): {results_ensemble['rmse_original']:.2f} euros")

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
plt.xlabel("Actual costTechFMs (euros)")  # Updated to reflect the new target
plt.ylabel("Predicted costTechFMs (euros)")  # Updated to reflect the new target
plt.title("Predicted vs Actual costTechFMs (Ensemble Voting)")  # Updated to reflect the new target
plt.grid(True)
plt.tight_layout()
plt.show()



###############################################################################
###############################################################################
###############################################################################

import numpy as np

# Number of rows per part
rows_per_target = 3472
num_target_parts = 14

# Number of rows per part
rows_per_feature = 112
num_feature_parts = 14

# Rename for clarity
df_targets_parts = [costTechFMs_dict_all.iloc[i * rows_per_target:(i + 1) * rows_per_target] 
                    for i in range(num_target_parts)]

df_features_parts = [final_feature_array_all.iloc[i * rows_per_feature:(i + 1) * rows_per_feature] 
                     for i in range(num_feature_parts)]


ensemble_results = []

for i in range(len(df_targets_parts[:num_feature_parts-0])):
    result = train_and_predict_costTechFMs_ensemble(
        df_targets_parts[i],
        df_features_parts[i],
        n_folds=1)
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
print(f"🌍 Global Voting RMSE: {rmse_global:.2f} euros")

###############################################################################
###############################################################################

# Select parts by index (e.g., parts 2, 3, 4, 5 in 0-based index are 1, 2, 3, 4)
selected_indices = [0, 1, 3, 4, 6, 9]


# Select parts by index (e.g., parts 2, 3, 4, 5 in 0-based index are 1, 2, 3, 4)
#selected_indices = [2, 5, 7, 8, 10, 11, 12, 13]


ensemble_results = []

for i in selected_indices:
    result = train_and_predict_costTechFMs_ensemble(
        df_targets_parts[i],
        df_features_parts[i],
        n_folds=1)
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
print(f"🌍 Global Voting RMSE: {rmse_global:.2f} euros")



plt.figure(figsize=(8, 6))
plt.scatter(global_y_true, global_y_pred, alpha=0.6, edgecolor='k')
plt.plot([global_y_true.min(), global_y_true.max()],
         [global_y_pred.min(), global_y_pred.max()], 'r--', lw=2)
plt.xlabel("Actual costTechFMs (euros)")  # Updated to reflect the new target
plt.ylabel("Predicted costTechFMs (euros)")  # Updated to reflect the new target
plt.title("Predicted vs Actual costTechFMs (Ensemble Voting)")  # Updated to reflect the new target
plt.grid(True)
plt.tight_layout()
plt.show()



###############################################################################
###############################################################################

"""
solution to the low efficienct ML method!!!
"""

# Combine all parts into one big dataset
df_costTechFMs_full = pd.concat(df_targets_parts, ignore_index=True)
df_features_full = pd.concat(df_features_parts, ignore_index=True)

# Use the same encoder and scaler setup
results_shared = train_and_predict_costTechFMs_ensemble(
    df_costTechFMs_full, df_features_full, n_folds=num_feature_parts
)

X_test_shared = results_shared["X_test"]
y_test_shared = results_shared["y_test_original"]


# Predict from each trained model on shared X_test
all_preds_shared = []
for res in ensemble_results[:]:
    part_preds = [m.predict(X_test_shared) for m in res["models"]]
    part_mean_pred = np.mean(part_preds, axis=0)
    # Unscale using that model’s scaler
    part_mean_pred_unscaled = res["target_scaler"].inverse_transform(part_mean_pred.reshape(-1, 1)).ravel()
    all_preds_shared.append(part_mean_pred_unscaled)

# Aggregate predictions
global_y_pred_shared = np.mean(np.stack(all_preds_shared), axis=0)

# Compute final metrics
r2_shared = r2_score(y_test_shared, global_y_pred_shared)
rmse_shared = np.sqrt(mean_squared_error(y_test_shared, global_y_pred_shared))

print(f"✅ Fixed Voting R²: {r2_shared:.4f}")
print(f"✅ Fixed Voting RMSE: {rmse_shared:.2f} euros")



###############################################################################
###############################################################################
###############################################################################
###############################################################################
##############################################
##############################################
##############################################
##############################################



######################### 
#########################
#########################




###############################

prompt = f"""
You are a sustainability analyst preparing a summary report for stakeholders, based on a machine learning model and SHAP analysis focused on forest management technology costs (`costTechFMs`).

🎯 **Objective**: Predict and understand the key drivers influencing technology investment costs (`costTechFMs`) in forest management.

📊 **Model Performance**:  
• R² Score: {r2_original:.2f}  
• RMSE: {rmse_original:.2f} EUR

💡 **Top 3 Influential Features (from SHAP analysis)**:  
1. **{top_features[0]}** – SHAP = {top_shap_vals[0]:.3f}, Avg value = {top_feature_vals[0]:.3f}  
2. **{top_features[1]}** – SHAP = {top_shap_vals[1]:.3f}, Avg value = {top_feature_vals[1]:.3f}  
3. **{top_features[2]}** – SHAP = {top_shap_vals[2]:.3f}, Avg value = {top_feature_vals[2]:.3f}

🌍 **Regional & Policy Highlights**:  
• Region with highest tech investment cost potential: **{best_region}**  
• Most capital-intensive technology: **{best_tech}**  


✏️ **Task**:  
Craft a clear and professional report that:
- Summarizes model accuracy in business terms  
- Explains how the top 3 features influence technology costs in forest management  
- Identifies regional and technological investment trends  
- Recommends strategic actions to optimize decarbonization budgets and funding pathways

The tone should be stakeholder-friendly, policy-relevant, and tailored for climate-focused planners, regional authorities, and sustainability investors. Emphasize clarity and actionable takeaways without technical jargon.
"""



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


"""






