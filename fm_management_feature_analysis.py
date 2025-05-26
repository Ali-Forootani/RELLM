#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 16:55:39 2025

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
gdx_file = (
    gams_system_dir + "/test_Ali.gdx"
)  # Change this to the actual path of your GDX file
gdx_data = gdxpds.to_dataframes(gdx_file)

# Extract relevant data into Pandas DataFrames
costMargFMs_df = gdx_data["costMargFMs"]
costInvFMs_df = gdx_data["costInvFMs"]
costInvLevelFMs_df = gdx_data["costInvLevelFMs"]
ghgFMs_df = gdx_data["ghgFMs"]
FMsgrowth_df = gdx_data["FMsgrowth"]
BeechArea0_df = gdx_data["BeechArea0"]
GrassArea0_df = gdx_data["GrassArea0"]
ghgTargetLULUCF_df = gdx_data["ghgTargetLULUCF"]
CO2price_df = gdx_data["CO2price"]


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
plt.rcParams.update(
    {
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
    }
)


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
    "CO2price": pd.read_csv("CO2price.csv"),
}

# Rename columns to ensure consistency
rename_columns = {
    "costMargFMs": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "Cost"},
    "costInvFMs": {
        "*": "Year",
        "*.1": "Technology",
        "*.2": "Region",
        "Value": "InvestmentCost",
    },
    "costInvLevelFMs": {
        "*": "Year",
        "*.1": "Technology",
        "*.2": "Region",
        "Value": "InvestmentLevelCost",
    },
    "ghgFMs": {
        "*": "Year",
        "*.1": "Technology",
        "*.2": "Region",
        "Value": "GHG_Removal",
    },
    "FMsgrowth": {
        "*": "Year",
        "*.1": "Technology",
        "*.2": "Region",
        "Value": "ForestManagementGrowth",
    },
    "BeechArea0": {"*": "Year", "*.1": "Region", "Value": "InitialBeechArea"},
    "GrassArea0": {"*": "Year", "*.1": "Region", "Value": "InitialGrassArea"},
    "ghgTargetLULUCF": {"*": "Year", "Value": "GHG_Target_LULUCF"},
    "CO2price": {"*": "Year", "Value": "CO2_Price"},
}

# Apply renaming and ensure Year is numeric
for key, df in datasets.items():
    df.rename(columns=rename_columns[key], inplace=True)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

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
        sns.lineplot(
            data=df,
            x="Year",
            y=df.columns[-1],
            hue="Region",
            style="Technology",
            markers=True,
            dashes=False,
        )
        plt.legend(
            title="Region/Technology", bbox_to_anchor=(1.05, 1), loc="upper left"
        )

    elif "Region" in df.columns:
        sns.lineplot(data=df, x="Year", y=df.columns[-1], hue="Region", markers=True)
        plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")

    else:
        sns.lineplot(data=df, x="Year", y=df.columns[-1], marker="o")

    plt.xlabel("Year")
    plt.ylabel(f"{df.columns[-1]} Values")
    plt.title(f"{key} Evolution Over Time")
    plt.grid(True)
    plt.show()

"""
##############################################
##############################################
##############################################
##############################################


"""

import os
import pickle


fm_datasets = datasets.copy()

# Define the new directory to save the agri_datasets
save_dir = "./Temporary_backups/data"  # Change this to a path where you have write permissions

# Ensure the directory exists
os.makedirs(save_dir, exist_ok=True)

# Save the fm_datasets using pickle
save_path = os.path.join(save_dir, "fm_datasets.pkl")

with open(save_path, "wb") as f:
    pickle.dump(fm_datasets, f)

print(f"File saved to: {save_path}")



import pickle

# Define the path to the saved .pkl file
pkl_file_path = "./Temporary_backups/data/fm_datasets.pkl"  # Adjust the path if needed

# Load the .pkl file
with open(pkl_file_path, "rb") as f:
    fm_datasets = pickle.load(f)

# Print the loaded datasets (optional)
print(fm_datasets)

"""

import pickle

# Define the path to the saved .pkl file
pkl_file_path = "./data/fm_datasets.pkl"  # Adjust the path if needed

# Load the .pkl file
with open(pkl_file_path, "rb") as f:
    fm_datasets = pickle.load(f)

# Print the loaded datasets (optional)
print(fm_datasets)

datasets = fm_datasets.copy()



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
        extracted_features.append(
            [region, technology, initial_value, final_value, slope]
        )

    # Convert to DataFrame
    feature_df = pd.DataFrame(
        extracted_features,
        columns=[
            "Region",
            "Technology",
            f"{feature_prefix}_2020",
            f"{feature_prefix}_2050",
            f"{feature_prefix}_Slope",
        ],
    )

    return feature_df


# Compute features for all datasets regionally
costMarg_features = compute_trend(costMargFMs, "Cost", "CostMarg")
costInv_features = compute_trend(costInvFMs, "InvestmentCost", "CostInv")
costInvLevel_features = compute_trend(
    costInvLevelFMs, "InvestmentLevelCost", "CostInvLevel"
)
ghg_features = compute_trend(ghgFMs, "GHG_Removal", "GHG")
growth_features = compute_trend(FMsgrowth, "ForestManagementGrowth", "ForestGrowth")


# Merge all datasets on both "Region" and "Technology"
final_feature_array = (
    costMarg_features.merge(costInv_features, on=["Region", "Technology"], how="outer")
    .merge(costInvLevel_features, on=["Region", "Technology"], how="outer")
    .merge(ghg_features, on=["Region", "Technology"], how="outer")
    .merge(growth_features, on=["Region", "Technology"], how="outer")
)

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
    return pd.DataFrame(
        {
            f"{feature_prefix}_2020": [initial_value],
            f"{feature_prefix}_2050": [final_value],
            f"{feature_prefix}_Slope": [slope],
        }
    )


# Compute CO2 and GHG trend features
co2_features = compute_global_trend(CO2price, "Year", "CO2_Price", "CO2")
ghg_target_features = compute_global_trend(
    ghgTargetLULUCF, "Year", "GHG_Target_LULUCF", "GHGTarget"
)

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


import pandas as pd

# Load additional datasets
BeechArea0 = datasets["BeechArea0"]
GrassArea0 = datasets["GrassArea0"]


# Drop the "Year" column (not needed) and merge region-wise into final_feature_array
final_feature_array = final_feature_array.merge(
    BeechArea0.drop(columns=["Year"]), on="Region", how="left"
)


final_feature_array = final_feature_array.merge(
    GrassArea0.drop(columns=["Year"]), on="Region", how="left"
)


# ---- Apply Min-Max Scaling ----
scaler = MinMaxScaler()
columns_to_scale = [
    col for col in final_feature_array.columns if col not in ["Region", "Technology"]
]
final_feature_array[columns_to_scale] = scaler.fit_transform(
    final_feature_array[columns_to_scale]
)


############################################
############################################
############################################
############################################
############################################


from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import numpy as np

# Load capFMs results
df_capFMs = pd.read_csv("./data/capFMs_results.csv")

# Step 1: Cross-join features with year
years_df = pd.DataFrame(df_capFMs["year"].unique(), columns=["year"])
temp = final_feature_array.copy()
temp["key"] = 1
years_df["key"] = 1
X_all = temp.merge(years_df, on="key").drop("key", axis=1)

# Step 2: Merge features with target
df_capFMs_renamed = df_capFMs.rename(columns={"techFMs": "Technology", "r": "Region"})
training_df = X_all.merge(
    df_capFMs_renamed, on=["Region", "Technology", "year"], how="left"
)
training_df = training_df.dropna(subset=["capFMs"])

# Step 3: Encode categorical features
categorical_cols = ["Region", "Technology"]
encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(training_df[categorical_cols])
encoded_df = pd.DataFrame(
    encoded, columns=encoder.get_feature_names_out(categorical_cols)
)

# Step 4: Scale numerical features (including year)
numerical_cols = [
    col for col in training_df.columns if col not in categorical_cols + ["capFMs"]
]
scaler = MinMaxScaler()
scaled_numerical = scaler.fit_transform(training_df[numerical_cols])
scaled_numerical_df = pd.DataFrame(scaled_numerical, columns=numerical_cols)

# Step 5: Assemble X and y
X = pd.concat(
    [encoded_df.reset_index(drop=True), scaled_numerical_df.reset_index(drop=True)],
    axis=1,
)
y = training_df["capFMs"]

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
    f"📏 Original scale metrics:\n📈 R² Score: {r2_orig:.4f}\n📉 RMSE: {rmse_orig:.2f} hectares"
)


# print(scaled_numerical_df["year"].describe())


############################################
############################################
############################################


import matplotlib.pyplot as plt

plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Actual capFMs")
plt.ylabel("Predicted capFMs")
plt.title("Predicted vs Actual capFMs")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--")
plt.grid()
plt.show()

residuals = y_test - y_pred
plt.hist(residuals, bins=30)
plt.title("Residual Distribution")
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

# Apply scientific notation
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((-2, 2))

plt.gca().xaxis.set_major_formatter(formatter)
plt.gca().yaxis.set_major_formatter(formatter)

plt.xlabel("Actual capFMs (ha)")
plt.ylabel("Predicted capFMs (ha)")
plt.title("Predicted vs Actual capFMs")
plt.grid(True)
plt.tight_layout()
plt.show()







########################################
########################################
########################################


import shap

# Use TreeExplainer for tree-based models like RandomForest
explainer_shap = shap.TreeExplainer(model)
shap_values = explainer_shap.shap_values(X_test)


#shap.summary_plot(shap_values, X_test, plot_type="bar")


# Generate summary plot and capture figure
shap.summary_plot(shap_values, X_test, plot_type="bar", show=False)

# Add title using suptitle and adjust layout
fig = plt.gcf()
fig.suptitle("Top Features Impacting Forest Management", fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("shap_summary_forst_management.png", dpi=300)
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


#################################################
#################################################
#################################################


# Get global SHAP feature importance
mean_abs_shap = np.abs(shap_values).mean(axis=0)
top_indices = np.argsort(mean_abs_shap)[-3:][::-1]

# Extract top 3 feature names and their stats
top_features = [X_test.columns[i] for i in top_indices]
top_shap_vals = [mean_abs_shap[i] for i in top_indices]
top_feature_vals = [X_test.iloc[:, i].mean() for i in top_indices]

# Compute average capFMs per Region/Technology
cap_summary = df_capFMs.groupby(["r", "techFMs"])["capFMs"].mean().reset_index()
best_row = cap_summary.loc[cap_summary["capFMs"].idxmax()]
best_region = best_row["r"]
best_tech = best_row["techFMs"]

co2_slope = broadcast_df["CO2_Slope"].mean()
ghg_target_slope = broadcast_df["GHGTarget_Slope"].mean()


prompt = f"""
You are an expert sustainability analyst writing a stakeholder-facing summary based on ML and SHAP analysis results.

Inputs:
- Target variable: 'Forest Management Capacity' (capFMs)
- Model performance: R² = {r2_orig:.2f}, RMSE = {rmse_orig:.2f} hectares
- Top 3 influential features from SHAP: 
   1. {top_features[0]} (SHAP = {top_shap_vals[0]:.3f}, Avg value = {top_feature_vals[0]:.3f})
   2. {top_features[1]} (SHAP = {top_shap_vals[1]:.3f}, Avg value = {top_feature_vals[1]:.3f})
   3. {top_features[2]} (SHAP = {top_shap_vals[2]:.3f}, Avg value = {top_feature_vals[2]:.3f})

Regional insight:
- Region with highest capFMs growth: {best_region}
- Technology leading growth: {best_tech}
- CO₂ Price Slope: {co2_slope:.2f}
- GHG Target Slope: {ghg_target_slope:.2f}

Generate a professional report for stakeholders that:
1. Explains overall model accuracy.
2. Interprets the influence of the top features on forest management capacity.
3. Highlights opportunities and regional trends.
4. Advises strategic actions aligned with decarbonization goals.

Use business-friendly language, no equations, and keep the tone clear and insight-driven.
"""


prompt = f"""
You are a sustainability analyst preparing a summary report for stakeholders, based on a machine learning model and SHAP analysis focused on forest management capacity (capFMs).

🎯 **Objective**: Predict and understand the key drivers of forest management capacity (`capFMs`)

📊 **Model Performance**:  
• R² Score: {r2_orig:.2f}  
• RMSE: {rmse_orig:.2f} hectares

🔍 **Top 3 Influential Features (from SHAP analysis)**:  
1. **{top_features[0]}** – SHAP = {top_shap_vals[0]:.3f}, Avg value = {top_feature_vals[0]:.3f}  
2. **{top_features[1]}** – SHAP = {top_shap_vals[1]:.3f}, Avg value = {top_feature_vals[1]:.3f}  
3. **{top_features[2]}** – SHAP = {top_shap_vals[2]:.3f}, Avg value = {top_feature_vals[2]:.3f}

🌍 **Regional & Policy Highlights**:  
• Region with highest capFMs potential: **{best_region}**  
• Leading growth technology: **{best_tech}**  
• CO₂ Price Trend (slope): **{co2_slope:.2f}**  
• GHG Target Trend (slope): **{ghg_target_slope:.2f}**

✏️ **Task**:  
Craft a clear and professional report that:
- Summarizes the model performance in non-technical terms  
- Interprets how the top 3 features influence capFMs outcomes  
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


##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################


"""

import shap

# Use TreeExplainer for tree-based models like RandomForest
explainer_shap = shap.TreeExplainer(model)
shap_values = explainer_shap.shap_values(X_test)

# Visualize SHAP summary plot
print("🔍 SHAP Summary Plot:")
shap.summary_plot(shap_values, X_test)

# Optional: Visualize for a single prediction
sample_idx = 0  # Change this to any index in X_test
print(f"🔍 SHAP Force Plot for index {sample_idx}:")
shap.initjs()
shap.force_plot(explainer_shap.expected_value, shap_values[sample_idx], X_test.iloc[sample_idx], matplotlib=True)


# SHAP Dependence Plot Example
shap.dependence_plot("ForestGrowth_2020", shap_values, X_test)

# SHAP Force Plot for a specific instance
i = 25
shap.force_plot(explainer_shap.expected_value, shap_values[i], X_test.iloc[i], matplotlib=True)

# List of features you want to explore
features_to_plot = ["CostInv_2050", "GHG_Slope", "Technology_FM02_TSA"]

# Generate dependence plots
for feature in features_to_plot:
    print(f"📊 SHAP dependence plot for: {feature}")
    shap.dependence_plot(feature, shap_values, X_test)


# Force interaction color by 'year'
shap.dependence_plot("CostInv_2050", shap_values, X_test, interaction_index="year")




import shap
import os
import matplotlib.pyplot as plt

# Create output directory
output_dir = "shap_outputs"
os.makedirs(output_dir, exist_ok=True)

# Use TreeExplainer for tree-based models like RandomForest
explainer_shap = shap.TreeExplainer(model)
shap_values = explainer_shap.shap_values(X_test)

# 🔍 SHAP Summary Plot
print("🔍 SHAP Summary Plot:")
plt.figure()
shap.summary_plot(shap_values, X_test, show=False)
plt.savefig(os.path.join(output_dir, "shap_summary.png"), bbox_inches="tight")
plt.close()

# 🔍 SHAP Force Plot for a single prediction
sample_idx = 0
print(f"🔍 SHAP Force Plot for index {sample_idx}:")
shap.initjs()
force_plot = shap.force_plot(
    explainer_shap.expected_value,
    shap_values[sample_idx],
    X_test.iloc[sample_idx],
    matplotlib=True
)
plt.savefig(os.path.join(output_dir, f"shap_force_sample{sample_idx}.png"), bbox_inches="tight")
plt.close()

# 🔍 SHAP Force Plot for another specific instance
i = 25
print(f"🔍 SHAP Force Plot for index {i}:")
force_plot = shap.force_plot(
    explainer_shap.expected_value,
    shap_values[i],
    X_test.iloc[i],
    matplotlib=True
)
plt.savefig(os.path.join(output_dir, f"shap_force_sample{i}.png"), bbox_inches="tight")
plt.close()

# 🔁 SHAP Dependence Plot for ForestGrowth_2020
print("📊 SHAP Dependence Plot for ForestGrowth_2020")
plt.figure()
shap.dependence_plot("ForestGrowth_2020", shap_values, X_test, show=False)
plt.savefig(os.path.join(output_dir, "dep_forestgrowth2020.png"), bbox_inches="tight")
plt.close()

# 🔁 SHAP Dependence Plots for multiple features
features_to_plot = ["CostInv_2050", "GHG_Slope", "Technology_FM02_TSA"]

for feature in features_to_plot:
    print(f"📊 SHAP dependence plot for: {feature}")
    plt.figure()
    shap.dependence_plot(feature, shap_values, X_test, show=False)
    plt.savefig(os.path.join(output_dir, f"dep_{feature}.png"), bbox_inches="tight")
    plt.close()

# 🔁 Dependence Plot with forced interaction coloring
print("📊 SHAP dependence plot for CostInv_2050 (colored by 'year')")
plt.figure()
shap.dependence_plot("CostInv_2050", shap_values, X_test, interaction_index="year", show=False)
plt.savefig(os.path.join(output_dir, "dep_costinv2050_by_year.png"), bbox_inches="tight")
plt.close()



shap_values = explainer_shap.shap_values(X_test)

shap.summary_plot(shap_values, X_test)



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



"""


##################################################
##################################################
##################################################
##################################################


"""
# Drop non-numeric columns (like 'Region') before grouping
numeric_cols = shap_df.select_dtypes(include=[np.number]).columns
shap_year = shap_df[numeric_cols].groupby(shap_df["year"]).mean()

# Pick features to visualize
top_features = ["ForestGrowth_2020", "Technology_FM02_TSA", "year"]
shap_year[top_features].plot(figsize=(12, 5), marker="o")
plt.title("📊 Mean SHAP Value Over Time")
plt.ylabel("Average SHAP Value")
plt.xlabel("Year")
plt.grid(True)
plt.tight_layout()
plt.show()
"""

##################################################
##################################################
##################################################

"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score, mean_squared_error
from catboost import CatBoostRegressor, Pool
import shap
import matplotlib.pyplot as plt

# ----------------------------
# Load your capFMs data
# ----------------------------
df_capFMs = pd.read_csv("capFMs_results.csv")

# Step 1: Cross-join with final_feature_array and year
years_df = pd.DataFrame(df_capFMs["year"].unique(), columns=["year"])
temp = final_feature_array.copy()
temp["key"] = 1
years_df["key"] = 1
X_all = temp.merge(years_df, on="key").drop("key", axis=1)

# Step 2: Merge with capFMs target
df_capFMs_renamed = df_capFMs.rename(columns={"techFMs": "Technology", "r": "Region"})
training_df = X_all.merge(df_capFMs_renamed, on=["Region", "Technology", "year"], how="left")
training_df = training_df.dropna(subset=["capFMs"])

# ----------------------------
# Feature preparation
# ----------------------------
categorical_features = ["Region", "Technology"]
all_features = categorical_features + [col for col in training_df.columns 
                                       if col not in categorical_features + ["capFMs"]]

# Scale numerical columns (excluding categorical and year)
scaler = MinMaxScaler()
numerical_cols = [col for col in all_features if col not in categorical_features]
training_df[numerical_cols] = scaler.fit_transform(training_df[numerical_cols])

# Prepare X and y
X_cat = training_df[all_features]
y_cat = training_df["capFMs"]

# ----------------------------
# Train/test split
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(X_cat, y_cat, test_size=0.2, random_state=42)

# ----------------------------
# Train CatBoost model
# ----------------------------
model = CatBoostRegressor(
    iterations=300,
    learning_rate=0.05,
    depth=6,
    cat_features=categorical_features,
    verbose=50,
    random_state=42
)

model.fit(X_train, y_train)

# ----------------------------
# Evaluate model
# ----------------------------
y_pred = model.predict(X_test)
r2_cb = r2_score(y_test, y_pred)
rmse_cb = mean_squared_error(y_test, y_pred, squared=False)

print(f"✅ CatBoost R² Score: {r2_cb:.4f}")
print(f"📉 CatBoost RMSE: {rmse_cb:.2f} hectares")

# ----------------------------
# SHAP Analysis
# ----------------------------
explainer = shap.Explainer(model)
shap_values = explainer(X_test)

# SHAP summary plot
shap.summary_plot(shap_values, X_test, feature_names=X_test.columns.tolist())

"""


##################################################
##################################################
##################################################


"""
First try of DNN
"""


"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# Convert your data to PyTorch tensors
X_tensor = torch.tensor(X.values, dtype=torch.float32)
y_tensor = torch.tensor(y_scaled.reshape(-1, 1), dtype=torch.float32)

dataset = TensorDataset(X_tensor, y_tensor)
loader = DataLoader(dataset, batch_size=64, shuffle=True)

# Define a simple feedforward network
class DNNModel(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
    
    def forward(self, x):
        return self.model(x)

model = DNNModel(X.shape[1])
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training loop
for epoch in range(100):
    for xb, yb in loader:
        pred = model(xb)
        loss = criterion(pred, yb)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")



model.eval()
with torch.no_grad():
    preds = model(X_tensor).numpy().ravel()
    preds_orig = target_scaler.inverse_transform(preds.reshape(-1, 1)).ravel()
    y_orig = target_scaler.inverse_transform(y_scaled.reshape(-1, 1)).ravel()

r2_dnn = r2_score(y_orig, preds_orig)
rmse_dnn = np.sqrt(mean_squared_error(y_orig, preds_orig))
print(f"DNN R²: {r2_dnn:.4f}, RMSE: {rmse_dnn:.2f} ha")

"""


##########################################
##########################################
##########################################

"""

from pytorch_forecasting import TimeSeriesDataSet
from pytorch_forecasting.data import NaNLabelEncoder

max_encoder_length = 5  # how many past timesteps to use
max_prediction_length = 1  # predict 1 timestep ahead (or more if needed)

tft_dataset = TimeSeriesDataSet(
    training_df,
    time_idx="time_idx",
    target="capFMs",
    group_ids=["group_id"],
    max_encoder_length=max_encoder_length,
    max_prediction_length=max_prediction_length,

    # Time-varying features (change each year)
    time_varying_known_reals=["time_idx", "year", "CO2_2020", "CO2_2050", "CO2_Slope",
                               "GHGTarget_2020", "GHGTarget_2050", "GHGTarget_Slope"],
    time_varying_unknown_reals=["capFMs"],

    # Static features (same for the whole series)
    static_categoricals=["Region", "Technology"],
    static_reals=["CostMarg_2020", "CostMarg_2050", "CostMarg_Slope",
                  "CostInv_2020", "CostInv_2050", "CostInv_Slope",
                  "CostInvLevel_2020", "CostInvLevel_2050", "CostInvLevel_Slope",
                  "GHG_2020", "GHG_2050", "GHG_Slope",
                  "ForestGrowth_2020", "ForestGrowth_2050", "ForestGrowth_Slope",
                  "InitialBeechArea", "InitialGrassArea"],

    target_normalizer=NaNLabelEncoder(),  # For classification tasks
    allow_missing_timesteps=True)




train_dataloader = tft_dataset.to_dataloader(train=True, batch_size=64, num_workers=0)




from pytorch_forecasting.models import TemporalFusionTransformer
from pytorch_forecasting.metrics import RMSE
from pytorch_lightning import Trainer

# Instantiate the model
tft = TemporalFusionTransformer.from_dataset(
    tft_dataset,
    learning_rate=1e-3,
    hidden_size=16,
    attention_head_size=1,
    dropout=0.1,
    loss=RMSE(),  # ⚠️ use RMSE or QuantileLoss, not nn.MSELoss
    log_interval=10,
    reduce_on_plateau_patience=4
)

# Trainer
trainer = Trainer(
    max_epochs=30,
    gradient_clip_val=0.1,
    accelerator="auto"
)

# Train the model
trainer.fit(tft, train_dataloaders=train_dataloader)


"""


##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################


"""

from lime.lime_tabular import LimeTabularExplainer

# Create LIME explainer
lime_explainer = LimeTabularExplainer(
    training_data=X_train.values,
    feature_names=X.columns.tolist(),
    mode='regression',
    verbose=True,
    random_state=42
)

# Choose an instance to explain
instance_idx = 2
exp = lime_explainer.explain_instance(
    data_row=X_test.iloc[instance_idx].values,
    predict_fn=model.predict
)

# Visualize explanation
print(f"🔍 LIME Explanation for instance {instance_idx}:")
exp.show_in_notebook(show_table=True)

# Or save explanation as HTML
exp.save_to_file("lime_explanation_instance_0.html")

"""


############################################
############################################
############################################
############################################
############################################
############################################

"""
df_ghgAbateFMs = pd.read_csv("ghgAbateFMs_results.csv")



import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

# Load data
df_ghgAbateFMs = pd.read_csv("ghgAbateFMs_results.csv")

# Cross-join with year
years_df = pd.DataFrame(df_ghgAbateFMs["year"].unique(), columns=["year"])
temp = final_feature_array.copy()
temp["key"] = 1
years_df["key"] = 1
X_all = temp.merge(years_df, on="key").drop("key", axis=1)



# Rename columns to match expected format
df_ghgAbateFMs_renamed = df_ghgAbateFMs.rename(columns={
    "techFMs": "Technology",
    "r": "Region",
    "ghgAbateTechFMs": "ghgAbateFMs"  # <- this is the important rename
})

# Merge with feature set
training_df = X_all.merge(df_ghgAbateFMs_renamed, on=["Region", "Technology", "year"], how="left")

# Drop rows without target
training_df = training_df.dropna(subset=["ghgAbateFMs"])



# Encode categorical features
categorical_cols = ["Region", "Technology"]
encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(training_df[categorical_cols])
encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical_cols))

# Assemble input and target
X = pd.concat([encoded_df, training_df.drop(columns=categorical_cols + ["ghgAbateFMs"])], axis=1)
y = training_df["ghgAbateFMs"]

# Scale target
target_scaler = MinMaxScaler()
y_scaled = target_scaler.fit_transform(y.values.reshape(-1, 1)).ravel()

# Train/test split and model training
X_train, X_test, y_train, y_test = train_test_split(X, y_scaled, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"✅ Model trained for ghgAbateFMs!")
print(f"📈 R² Score: {r2:.4f}")
print(f"📉 RMSE: {rmse:.4f}")

# Inverse transform
y_pred_original = target_scaler.inverse_transform(y_pred.reshape(-1, 1)).ravel()
y_test_original = target_scaler.inverse_transform(y_test.reshape(-1, 1)).ravel()

r2_orig = r2_score(y_test_original, y_pred_original)
rmse_orig = np.sqrt(mean_squared_error(y_test_original, y_pred_original))

print(f"📏 Original scale metrics:")
print(f"📈 R² Score: {r2_orig:.4f}")
print(f"📉 RMSE: {rmse_orig:.4f} MtCO2e")

# Visualization
plt.figure(figsize=(8, 6))
plt.scatter(y_test_original, y_pred_original, alpha=0.6, edgecolor='k')
plt.plot([y_test_original.min(), y_test_original.max()],
         [y_test_original.min(), y_test_original.max()], 'r--', lw=2)
plt.xlabel("Actual ghgAbateFMs (MtCO2e)")
plt.ylabel("Predicted ghgAbateFMs (MtCO2e)")
plt.title("Predicted vs Actual ghgAbateFMs")
plt.grid(True)
plt.tight_layout()
plt.show()

residuals = y_test_original - y_pred_original
plt.hist(residuals, bins=30)
plt.title("Residual Distribution")
plt.xlabel("Prediction Error (MtCO2e)")
plt.ylabel("Frequency")
plt.grid()
plt.tight_layout()
plt.show()

"""
