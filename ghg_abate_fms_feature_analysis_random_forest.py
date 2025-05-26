#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 14:53:18 2025

@author: forootan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 08:20:32 2025

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

ghg_abate_fms_datasets = datasets.copy() 
"""


##############################################
##############################################
##############################################
##############################################


"""
saving the dataset and loading from the local directory
"""

"""
import os

# Define the new directory to save the agri_datasets as .csv files
save_dir = "./Temporary_backups/data"  # Change this to a path where you have write permissions

# Ensure the directory exists
os.makedirs(save_dir, exist_ok=True)

# Save each dataset in agri_datasets as a .csv file
for name, df in ghg_abate_fms_datasets.items():
    save_path = os.path.join(save_dir, f"{name}.csv")
    df.to_csv(save_path, index=False)

print(f"All datasets saved as .csv in {save_dir}")


import os
import pickle

# Define the new directory to save the agri_datasets
save_dir = "./Temporary_backups/data"  # Change this to a path where you have write permissions

# Ensure the directory exists
os.makedirs(save_dir, exist_ok=True)

# Save the agri_datasets using pickle
save_path = os.path.join(save_dir, "ghg_abate_fms_datasets.pkl")

with open(save_path, "wb") as f:
    pickle.dump(ghg_abate_fms_datasets, f)

print(f"File saved to: {save_path}")
"""


import pickle

# Define the path to the saved .pkl file
pkl_file_path = "./data/ghg_abate_fms_datasets.pkl"  # Adjust the path if needed

# Load the .pkl file
with open(pkl_file_path, "rb") as f:
    ghg_abate_fms_datasets = pickle.load(f)

# Print the loaded datasets (optional)
print(ghg_abate_fms_datasets)


datasets = ghg_abate_fms_datasets.copy()




#############################################
#############################################
#############################################
#############################################

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


####################################
####################################
####################################
####################################




df_ghgAbateFMs = pd.read_csv( "./data/" + "ghgAbateFMs_results.csv")



import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

# Load data
df_ghgAbateFMs = pd.read_csv( "./data/" + "ghgAbateFMs_results.csv")

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

###################################
###################################
###################################



import shap

# Compute SHAP values for ghgAbateFMs
explainer = shap.Explainer(model)
shap_values = explainer(X_test)

# Get global SHAP feature importance
mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
top_indices = np.argsort(mean_abs_shap)[-3:][::-1]

# Extract top 3 feature names and their stats
top_features = [X_test.columns[i] for i in top_indices]
top_shap_vals = [mean_abs_shap[i] for i in top_indices]
top_feature_vals = [X_test.iloc[:, i].mean() for i in top_indices]

# Compute average ghgAbateFMs per Region/Technology

ghg_summary = df_ghgAbateFMs_renamed.groupby(["Region", "Technology"])["ghgAbateFMs"].mean().reset_index()

best_row = ghg_summary.loc[ghg_summary["ghgAbateFMs"].idxmax()]

best_region = best_row["Region"]
best_tech = best_row["Technology"]


# Trends from broadcasted CO2 and GHG target slopes
co2_slope = broadcast_df["CO2_Slope"].mean()
ghg_target_slope = broadcast_df["GHGTarget_Slope"].mean()

# Prompt for SHAP summary (adapt as needed)
prompt = f"""
You are a sustainability analyst preparing a summary report for stakeholders, based on a machine learning model and SHAP analysis focused on GHG abatement from forest management (`ghgAbateFMs`).

🎯 **Objective**: Predict and understand the key drivers of GHG abatement from forest management (`ghgAbateFMs`)

📊 **Model Performance**:  
• R² Score: {r2_orig:.2f}  
• RMSE: {rmse_orig:.2f} MtCO2e

🔍 **Top 3 Influential Features (from SHAP analysis)**:  
1. **{top_features[0]}** – SHAP = {top_shap_vals[0]:.3f}, Avg value = {top_feature_vals[0]:.3f}  
2. **{top_features[1]}** – SHAP = {top_shap_vals[1]:.3f}, Avg value = {top_feature_vals[1]:.3f}  
3. **{top_features[2]}** – SHAP = {top_shap_vals[2]:.3f}, Avg value = {top_feature_vals[2]:.3f}

🌍 **Regional & Policy Highlights**:  
• Region with highest ghgAbateFMs potential: **{best_region}**  
• Leading technology in GHG abatement: **{best_tech}**  
• CO₂ Price Trend (slope): **{co2_slope:.2f}**  
• GHG Target Trend (slope): **{ghg_target_slope:.2f}**

✏️ **Task**:  
Craft a clear and professional report that:
- Summarizes the model performance in non-technical terms  
- Interprets how the top 3 features influence GHG abatement outcomes  
- Highlights regional and technological opportunities  
- Recommends actions that align with long-term decarbonization goals  

The tone should be insight-driven, stakeholder-friendly, and suitable for regional planners, policymakers, and sustainability investors. Avoid equations or technical jargon—focus on actionable insights.
"""



import os
from openai import OpenAI


# Set OpenAI API key and base URL
os.environ["OPENAI_API_KEY"] = "glpat-JHd9xWcVcu2NY76LAK_A" 
os.environ["OPENAI_API_KEY"] = "glpat-xt-xveSd1icPdA_y6h1_"
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























