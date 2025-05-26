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
from gams import GamsWorkspace, GamsParameter, GamsSet
from gams import GamsWorkspace
import os

import sys
import os
import json
from datetime import datetime


def setting_directory(depth):
    current_dir = os.path.abspath(os.getcwd())
    root_dir = current_dir
    for i in range(depth):
        root_dir = os.path.abspath(os.path.join(root_dir, os.pardir))
        sys.path.append(os.path.dirname(root_dir))
    return root_dir

# Specify the GAMS system directory (Update this path according to your GAMS installation)
gams_system_dir = setting_directory(0)  # Example path for Windows

"""
# Load the .gdx file
gdx_file = gams_system_dir + "/test_Ali.gdx"  # Change this to the actual path of your GDX file
gdx_data = gdxpds.to_dataframes(gdx_file)

# Extract relevant data into Pandas DataFrames
costMargFMs_df = gdx_data['costMargFMs']
costInvFMs_df = gdx_data['costInvFMs']
costInvLevelFMs_df = gdx_data['costInvLevelFMs']
ghgFMs_df = gdx_data['ghgFMs']
FMsgrowth_df = gdx_data['FMsgrowth']
BeechArea0_df = gdx_data['BeechArea0']
GrassArea0_df = gdx_data['GrassArea0']
ghgTargetLULUCF_df = gdx_data['ghgTargetLULUCF']
CO2price_df = gdx_data['CO2price']

# Print the first few rows of each dataset
print("Marginal Cost of Forest Management (costMargFMs):\n", costMargFMs_df.head())
print("Investment Cost of Forest Management (costInvFMs):\n", costInvFMs_df.head())

print("costInvLevelFMs_df:\n", costInvLevelFMs_df.head())

print("GHG Removal Potential of FMs (ghgFMs):\n", ghgFMs_df.head())
print("FMsgrowth:\n", FMsgrowth_df.head())
print("BeechArea0_df:\n", BeechArea0_df.head())
print("GrassArea0_df:\n", GrassArea0_df.head())
print("ghgTargetLULUCF_df:\n", ghgTargetLULUCF_df.head())


print("CO2 Price:\n", CO2price_df.head())

# Save to CSV for further analysis (optional)
costMargFMs_df.to_csv("costMargFMs.csv", index=False)
costInvFMs_df.to_csv("costInvFMs.csv", index=False)

costInvLevelFMs_df.to_csv("costInvLevelFMs.csv", index=False)


ghgFMs_df.to_csv("ghgFMs.csv", index=False)

FMsgrowth_df.to_csv("FMsgrowth.csv", index=False)

BeechArea0_df.to_csv("BeechArea0.csv", index=False)

GrassArea0_df.to_csv("GrassArea0.csv", index=False)

ghgTargetLULUCF_df.to_csv("ghgTargetLULUCF.csv", index=False)

CO2price_df.to_csv("CO2price.csv", index=False)

CO2price_df = CO2price_df.rename(columns={"*": "year", "Value": "CO2price"})



#############################################################
#############################################################
#############################################################
#############################################################



# Apply Matplotlib global parameters for consistent formatting
plt.rcParams.update({
    "axes.edgecolor": "gray",
    "axes.linewidth": 1.6,
    "axes.titleweight": "bold",
    "axes.titlesize": 16,
    "axes.labelsize": 14,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "grid.linestyle": "--",
    "grid.alpha": 0.9,
    "legend.frameon": False,
    "figure.titlesize": 18,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "font.family": "DejaVu Sans",  # Change to "Arial", "Calibri", or "Roboto" if preferred
})


#############################################################
#############################################################
#############################################################
#############################################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets from CSV
datasets = {
    "costMargFMs": pd.read_csv("costMargFMs.csv"),
    "costInvFMs": pd.read_csv("costInvFMs.csv"),
    "costInvLevelFMs": pd.read_csv("costInvLevelFMs.csv"),
    "ghgFMs": pd.read_csv("ghgFMs.csv"),
    "FMsgrowth": pd.read_csv("FMsgrowth.csv"),
    "BeechArea0": pd.read_csv("BeechArea0.csv"),
    "GrassArea0": pd.read_csv("GrassArea0.csv"),
    "ghgTargetLULUCF": pd.read_csv("ghgTargetLULUCF.csv"),
    "CO2price": pd.read_csv("CO2price.csv")
}

# Rename columns to ensure consistency
rename_columns = {
    "costMargFMs": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "Cost"},
    "costInvFMs": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "InvestmentCost"},
    "costInvLevelFMs": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "InvestmentLevelCost"},
    "ghgFMs": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "GHG_Removal"},
    "FMsgrowth": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "ForestManagementGrowth"},
    "BeechArea0": {"*": "Year", "*.1": "Region", "Value": "InitialBeechArea"},
    "GrassArea0": {"*": "Year", "*.1": "Region", "Value": "InitialGrassArea"},
    "ghgTargetLULUCF": {"*": "Year", "Value": "GHG_Target_LULUCF"},
    "CO2price": {"*": "Year", "Value": "CO2_Price"}
}

# Apply renaming and ensure Year is numeric
for key, df in datasets.items():
    df.rename(columns=rename_columns[key], inplace=True)
    df["Year"] = pd.to_numeric(df["Year"], errors='coerce')

cost_tech_fm_datasets = datasets.copy()

"""

###########################################################    
    

"""
import os
import pickle

# Define the new directory to save the agri_datasets
save_dir = "./Temporary_backups/data"  # Change this to a path where you have write permissions

# Ensure the directory exists
os.makedirs(save_dir, exist_ok=True)

# Save the cost_tech_datasets using pickle
save_path = os.path.join(save_dir, "cost_tech_fm_datasets.pkl")

with open(save_path, "wb") as f:
    pickle.dump(cost_tech_fm_datasets, f)

print(f"File saved to: {save_path}")



import pickle

# Define the path to the saved .pkl file
pkl_file_path = "./Temporary_backups/data/cost_tech_fm_datasets.pkl"  # Adjust the path if needed

# Load the .pkl file
with open(pkl_file_path, "rb") as f:
    cost_tech_fm_datasets = pickle.load(f)

# Print the loaded datasets (optional)
print(cost_tech_fm_datasets)

"""

import pickle

# Define the path to the saved .pkl file
pkl_file_path = "./data/cost_tech_fm_datasets.pkl"  # Adjust the path if needed

# Load the .pkl file
with open(pkl_file_path, "rb") as f:
    cost_tech_fm_datasets = pickle.load(f)

# Print the loaded datasets (optional)
print(cost_tech_fm_datasets)

datasets = cost_tech_fm_datasets.copy()



###########################################################

# Special Handling for BeechArea0 and GrassArea0
if "BeechArea0" in datasets and "GrassArea0" in datasets:
    beech_df = datasets["BeechArea0"].sort_values(by="InitialBeechArea", ascending=True)
    grass_df = datasets["GrassArea0"].sort_values(by="InitialGrassArea", ascending=True)

    # Define figure size
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6), sharey=True)

    # Plot Initial Beech Area
    axes[0].barh(beech_df["Region"], beech_df["InitialBeechArea"], color="forestgreen")
    axes[0].set_xlabel("Initial Beech Area")
    axes[0].set_ylabel("Region")
    axes[0].set_title("Initial Beech Area by Region (2020)")

    # Plot Initial Grass Area
    axes[1].barh(grass_df["Region"], grass_df["InitialGrassArea"], color="goldenrod")
    axes[1].set_xlabel("Initial Grass Area")
    axes[1].set_title("Initial Grass Area by Region (2020)")

    # Adjust layout
    plt.tight_layout()
    plt.show()

# Plot other datasets
for key, df in datasets.items():
    if key in ["BeechArea0", "GrassArea0"]:
        continue  # Skip bar plots since they are handled separately

    plt.figure(figsize=(14, 8))

    # Time-series datasets using line plots
    if "Region" in df.columns and "Technology" in df.columns:
        sns.lineplot(data=df, x="Year", y=df.columns[-1], hue="Region", style="Technology", markers=True, dashes=False)
        plt.legend(title="Region/Technology", bbox_to_anchor=(1.05, 1), loc='upper left')

    elif "Region" in df.columns:
        sns.lineplot(data=df, x="Year", y=df.columns[-1], hue="Region", markers=True)
        plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc='upper left')

    else:
        sns.lineplot(data=df, x="Year", y=df.columns[-1], marker="o")

    plt.xlabel("Year")
    plt.ylabel(f"{df.columns[-1]} Values")
    plt.title(f"{key} Evolution Over Time")
    plt.grid(True)
    plt.show()


###############################################
###############################################
###############################################


##############################################
##############################################
##############################################
##############################################



import pandas as pd
from scipy.stats import linregress
from sklearn.preprocessing import MinMaxScaler

# Load datasets
costMargFMs = datasets["costMargFMs"]
costInvFMs = datasets["costInvFMs"]
costInvLevelFMs = datasets["costInvLevelFMs"]
ghgFMs = datasets["ghgFMs"]
FMsgrowth = datasets["FMsgrowth"]




import pandas as pd
from scipy.stats import linregress

# Function to compute initial value, final value, and slope for each region and technology
def compute_trend(df, value_col, feature_prefix):
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

# Compute features for all datasets regionally
costMarg_features = compute_trend(costMargFMs, "Cost", "CostMarg")
costInv_features = compute_trend(costInvFMs, "InvestmentCost", "CostInv")
costInvLevel_features = compute_trend(costInvLevelFMs, "InvestmentLevelCost", "CostInvLevel")
ghg_features = compute_trend(ghgFMs, "GHG_Removal", "GHG")
growth_features = compute_trend(FMsgrowth, "ForestManagementGrowth", "ForestGrowth")



# Merge all datasets on both "Region" and "Technology"
final_feature_array = costMarg_features.merge(costInv_features, on=["Region", "Technology"], how="outer") \
                                       .merge(costInvLevel_features, on=["Region", "Technology"], how="outer") \
                                       .merge(ghg_features, on=["Region", "Technology"], how="outer") \
                                       .merge(growth_features, on=["Region", "Technology"], how="outer")

# Fill missing values with 0
final_feature_array.fillna(0, inplace=True)






######################### 
#########################
#########################

"""
CO_2 price 
GHG Target LULUCF
"""

ghgTargetLULUCF = datasets["ghgTargetLULUCF"]
CO2price = datasets["CO2price"]



from scipy.stats import linregress

# Function to compute trend (initial, final, slope) for non-region, non-tech datasets
def compute_global_trend(df, year_col, value_col, feature_prefix):
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

# Compute CO2 and GHG trend features
co2_features = compute_global_trend(CO2price, "Year", "CO2_Price", "CO2")
ghg_target_features = compute_global_trend(ghgTargetLULUCF, "Year", "GHG_Target_LULUCF", "GHGTarget")

# Broadcast these to all regions in the final_feature_array
unique_regions = final_feature_array["Region"].unique()
broadcast_df = pd.DataFrame(unique_regions, columns=["Region"])

# Cross join with co2 and ghg features (same values for all regions)
broadcast_df = broadcast_df.merge(co2_features, how="cross")
broadcast_df = broadcast_df.merge(ghg_target_features, how="cross")

# Merge with final_feature_array
final_feature_array = final_feature_array.merge(broadcast_df, on="Region", how="left")


#####################################
#####################################
#####################################

import pandas as pd

# Load additional datasets
BeechArea0 = datasets["BeechArea0"]
GrassArea0 = datasets["GrassArea0"]


# Drop the "Year" column (not needed) and merge region-wise into final_feature_array
final_feature_array = final_feature_array.merge(
    BeechArea0.drop(columns=["Year"]), on="Region", how="left")


final_feature_array = final_feature_array.merge(
    GrassArea0.drop(columns=["Year"]), on="Region", how="left")



# ---- Apply Min-Max Scaling ----
scaler = MinMaxScaler()
columns_to_scale = [col for col in final_feature_array.columns if col not in ["Region", "Technology"]]
final_feature_array[columns_to_scale] = scaler.fit_transform(final_feature_array[columns_to_scale])

#####################################
#####################################
#####################################



from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import numpy as np

# Load costTechFMs results
df_costTechFMs = pd.read_csv("./data/" + "costTechFMs.csv")




# Step 1: Cross-join features with year
years_df = pd.DataFrame(df_costTechFMs["year"].unique(), columns=["year"])
temp = final_feature_array.copy()  # Assuming this contains ['Region', 'Technology', other features...]
temp["key"] = 1
years_df["key"] = 1
X_all = temp.merge(years_df, on="key").drop("key", axis=1)

# Step 2: Merge features with target
df_costTechFMs_renamed = df_costTechFMs.rename(columns={"techFMs": "Technology", "r": "Region"})
training_df = X_all.merge(
    df_costTechFMs_renamed, on=["Region", "Technology", "year"], how="left"
)
training_df = training_df.dropna(subset=["costTechFMs"])

# Step 3: Encode categorical features
categorical_cols = ["Region", "Technology"]
encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(training_df[categorical_cols])
encoded_df = pd.DataFrame(
    encoded, columns=encoder.get_feature_names_out(categorical_cols)
)

# Step 4: Scale numerical features (including year and others)
numerical_cols = [
    col for col in training_df.columns if col not in categorical_cols + ["costTechFMs"]
]
scaler = MinMaxScaler()
scaled_numerical = scaler.fit_transform(training_df[numerical_cols])
scaled_numerical_df = pd.DataFrame(scaled_numerical, columns=numerical_cols)

# Step 5: Assemble X and y
X = pd.concat(
    [encoded_df.reset_index(drop=True), scaled_numerical_df.reset_index(drop=True)],
    axis=1,
)
y = training_df["costTechFMs"]

# Scale target
target_scaler = MinMaxScaler()
y_scaled = target_scaler.fit_transform(y.values.reshape(-1, 1)).ravel()

# Step 6: Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_scaled, test_size=0.2, random_state=42
)

# Step 7: Train Random Forest
model = RandomForestRegressor(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# Step 8: Predict and evaluate
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"✅ Model trained!\n📈 R² Score: {r2:.4f}\n📉 RMSE: {rmse:.2f}")

# Inverse scale prediction and ground truth
y_pred_original = target_scaler.inverse_transform(y_pred.reshape(-1, 1)).ravel()
y_test_original = target_scaler.inverse_transform(y_test.reshape(-1, 1)).ravel()

r2_orig = r2_score(y_test_original, y_pred_original)
rmse_orig = np.sqrt(mean_squared_error(y_test_original, y_pred_original))
print(
    f"📏 Original scale metrics:\n📈 R² Score: {r2_orig:.4f}\n📉 RMSE: {rmse_orig:.2f} EUR"
)

##########################
##########################
##########################


import matplotlib.pyplot as plt

plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Actual costTechFMs (scaled)")
plt.ylabel("Predicted costTechFMs (scaled)")
plt.title("Predicted vs Actual costTechFMs (scaled)")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
plt.grid()
plt.show()

residuals = y_test - y_pred
plt.hist(residuals, bins=30)
plt.title("Residual Distribution (scaled)")
plt.xlabel("Error")
plt.ylabel("Frequency")
plt.grid()
plt.show()


import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

plt.figure(figsize=(8, 6))
plt.scatter(y_test_original, y_pred_original, alpha=0.6, edgecolor="k")
plt.plot(
    [y_test_original.min(), y_test_original.max()],
    [y_test_original.min(), y_test_original.max()],
    "r--",
    lw=2,
)

# Apply scientific notation for cost values
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((-2, 2))

plt.gca().xaxis.set_major_formatter(formatter)
plt.gca().yaxis.set_major_formatter(formatter)

plt.xlabel("Actual costTechFMs (EUR)")
plt.ylabel("Predicted costTechFMs (EUR)")
plt.title("Predicted vs Actual costTechFMs (original scale)")
plt.grid(True)
plt.tight_layout()
plt.show()

###############################
###############################
###############################


import shap

# Use TreeExplainer for tree-based models like RandomForest
explainer_shap = shap.TreeExplainer(model)
shap_values = explainer_shap.shap_values(X_test)


#shap.summary_plot(shap_values, X_test)

# Generate summary plot and capture figure
shap.summary_plot(shap_values, X_test, plot_type="bar", show=False)

# Add title using suptitle and adjust layout
fig = plt.gcf()
fig.suptitle("Top Features Impacting costTechFM Prediction", fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("shap_summary_costtechFM.png", dpi=300)
plt.show()





import numpy as np

i = 4  # Sample index
shap_row = shap_values[i]
input_row = X_test.iloc[i]

# Get top 3 features by absolute SHAP value
top_indices = np.argsort(np.abs(shap_row))[-3:][::-1]

# Extract feature names, SHAP values, and actual feature values
for idx in top_indices:
    feature_name = X_test.columns[idx]
    shap_val = shap_row[idx]
    feature_val = input_row[feature_name]
    print(f"{feature_name}: SHAP = {shap_val:.4f}, Value = {feature_val}")



# Global SHAP feature importance
mean_abs_shap = np.abs(shap_values).mean(axis=0)

# Get top 3 features by average absolute SHAP value
top_indices = np.argsort(mean_abs_shap)[-3:][::-1]

# Extract feature names and stats
top_features = [X_test.columns[i] for i in top_indices]
top_shap_vals = [mean_abs_shap[i] for i in top_indices]
top_feature_vals = [X_test.iloc[:, i].mean() for i in top_indices]

# Get region and tech with highest costTechFMs
cost_summary = df_costTechFMs.groupby(["r", "techFMs"])["costTechFMs"].mean().reset_index()
best_row = cost_summary.loc[cost_summary["costTechFMs"].idxmax()]
best_region = best_row["r"]
best_tech = best_row["techFMs"]

# Assume these are defined or computed earlier in your code
# co2_slope = broadcast_df["CO2_Slope"].mean()
# ghg_target_slope = broadcast_df["GHGTarget_Slope"].mean()



###############################

prompt = f"""
You are a sustainability analyst preparing a summary report for stakeholders, based on a machine learning model and SHAP analysis focused on forest management technology costs (`costTechFMs`).

🎯 **Objective**: Predict and understand the key drivers influencing technology investment costs (`costTechFMs`) in forest management.

📊 **Model Performance**:  
• R² Score: {r2_orig:.2f}  
• RMSE: {rmse_orig:.2f} EUR

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









