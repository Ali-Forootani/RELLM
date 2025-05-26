

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
from gams import GamsWorkspace, GamsParameter, GamsSet
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

"""
# Load the .gdx file
gdx_file = os.path.join(gams_system_dir, "test_Ali.gdx")  # Update path if needed
gdx_data = gdxpds.to_dataframes(gdx_file)

# Step 1: Extract relevant agriculture datasets
costMargAgri_df       = gdx_data['costMargAgri']
costInvAgri_df        = gdx_data['costInvAgri']
costInvLevelAgri_df   = gdx_data['costInvLevelAgri']
ghgAgri_df            = gdx_data['ghgAgri']
AgriGrowth_df         = gdx_data['Agrigrowth']
AgriArea0_df          = gdx_data['Agriarea0']
PeatExtract_df        = gdx_data['PeatExtract']

# Step 2: Group datasets into a dictionary for convenience
agri_datasets = {
    "costMargAgri": costMargAgri_df,
    "costInvAgri": costInvAgri_df,
    "costInvLevelAgri": costInvLevelAgri_df,
    "ghgAgri": ghgAgri_df,
    "Agrigrowth": AgriGrowth_df,
    "Agriarea0": AgriArea0_df,
    "PeatExtract": PeatExtract_df
}

# Step 3: Define column renaming for each dataset



# Correct mapping from index to desired column names
correct_column_names = {
    "costMargAgri":        ["Year", "Technology", "Region", "Cost"],
    "costInvAgri":         ["Year", "Technology", "Region", "InvestmentCost"],
    "costInvLevelAgri":    ["Year", "Technology", "Region", "InvestmentLevelCost"],
    "ghgAgri":             ["Year", "Technology", "Region", "GHG_Removal"],
    "Agrigrowth":          ["Year", "Technology", "Region", "Agri_Growth"],
    "Agriarea0":           ["Year", "Region", "InitialAgriArea"],
    "PeatExtract":         ["Year", "Peat_Extraction"]
}



# Apply the fixed column names and ensure 'Year' is numeric
for name, df in agri_datasets.items():
    new_columns = correct_column_names.get(name)
    if new_columns and len(df.columns) == len(new_columns):
        df.columns = new_columns

        # Convert 'Year' column to numeric if it exists
        if "Year" in df.columns:
            df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

        agri_datasets[name] = df
    else:
        print(f"⚠️ Skipped {name}: column mismatch.")


# ✅ All agri_datasets now have clean, standardized column names.

# Optional: Print a sample from one of the datasets
print(agri_datasets["costMargAgri"].head())


agri_caps_datasets = agri_datasets.copy()
"""

#######################################
#######################################
#######################################


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
for name, df in agri_datasets.items():
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
save_path = os.path.join(save_dir, "agri_caps_datasets.pkl")

with open(save_path, "wb") as f:
    pickle.dump(agri_datasets, f)

print(f"File saved to: {save_path}")

"""

import pickle

# Define the path to the saved .pkl file
pkl_file_path = "./data/agri_caps_datasets.pkl"  # Adjust the path if needed

# Load the .pkl file
with open(pkl_file_path, "rb") as f:
    agri_caps_datasets = pickle.load(f)

# Print the loaded datasets (optional)
print(agri_caps_datasets)


agri_datasets = agri_caps_datasets.copy()

#######################################
#######################################
#######################################


import matplotlib.pyplot as plt
import seaborn as sns

# Special handling for Agriarea0 (barh by Region) if Region column exists
if "Agriarea0" in agri_datasets:
    agri_area_df = agri_datasets["Agriarea0"]
    if "Region" in agri_area_df.columns:
        agri_area_df = agri_area_df.sort_values(by="InitialAgriArea", ascending=True)

        plt.figure(figsize=(10, 6))
        plt.barh(agri_area_df["Region"], agri_area_df["InitialAgriArea"], color="saddlebrown")
        plt.xlabel("Initial Agricultural Area")
        plt.ylabel("Region")
        plt.title("Initial Agricultural Area by Region (2020)")
        plt.tight_layout()
        plt.show()

# Plot other datasets
for key, df in agri_datasets.items():
    if key == "Agriarea0":
        continue  # Already handled above

    plt.figure(figsize=(14, 8))
    y_col = [col for col in df.columns if col not in ["Year", "Technology", "Region"]][0]

    # Time-series datasets using line plots
    if "Region" in df.columns and "Technology" in df.columns:
        sns.lineplot(
            data=df,
            x="Year",
            y=y_col,
            hue="Region",
            style="Technology",
            markers=True,
            dashes=False
        )
        plt.legend(title="Region/Technology", bbox_to_anchor=(1.05, 1), loc="upper left")

    elif "Region" in df.columns:
        sns.lineplot(data=df, x="Year", y=y_col, hue="Region", marker="o")
        plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")

    else:
        sns.lineplot(data=df, x="Year", y=y_col, marker="o")

    plt.xlabel("Year")
    plt.ylabel(f"{y_col} Values")
    plt.title(f"{key} Evolution Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


############################
############################
############################


import pandas as pd
from scipy.stats import linregress
from sklearn.preprocessing import MinMaxScaler


# Function to compute initial value, final value, and slope for each region and technology
def compute_trend(df, value_col, feature_prefix):
    df_agg = df.groupby(["Year", "Region", "Technology"])[value_col].sum().reset_index()
    
    print(df_agg)
    
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




####################################



# === Feature extraction for Region-Technology datasets ===
costMarg_features       = compute_trend(agri_datasets["costMargAgri"], "Cost", "CostMargAgri")
costInv_features        = compute_trend(agri_datasets["costInvAgri"], "InvestmentCost", "CostInvAgri")
costInvLevel_features   = compute_trend(agri_datasets["costInvLevelAgri"], "InvestmentLevelCost", "CostInvLevAgri")
ghg_features            = compute_trend(agri_datasets["ghgAgri"], "GHG_Removal", "GHGAgri")
growth_features         = compute_trend(agri_datasets["Agrigrowth"], "Agri_Growth", "AgriGrowth")

# === Merge all Region-Technology feature sets ===
final_feature_array = (
    costMarg_features
    .merge(costInv_features, on=["Region", "Technology"], how="outer")
    .merge(costInvLevel_features, on=["Region", "Technology"], how="outer")
    .merge(ghg_features, on=["Region", "Technology"], how="outer")
    .merge(growth_features, on=["Region", "Technology"], how="outer")
)

# === Add Agriarea0 (only Region level) ===
#Agriarea0_features = agri_datasets["Agriarea0"].rename(columns={"InitialAgriArea": "Agriarea0_2020"})
#final_feature_array = final_feature_array.merge(Agriarea0_features, on="Region", how="left")


# Drop "Year" and merge like other static area datasets
Agriarea0 = agri_datasets["Agriarea0"].drop(columns=["Year"])
final_feature_array = final_feature_array.merge(Agriarea0, on="Region", how="left")



# === Add PeatExtract trend (global trend broadcasted to all regions) ===
peat_features = compute_global_trend(agri_datasets["PeatExtract"], "Year", "Peat_Extraction", "PeatExtract")
unique_regions = final_feature_array["Region"].unique()
broadcast_df = pd.DataFrame(unique_regions, columns=["Region"])
broadcast_df = broadcast_df.merge(peat_features, how="cross")

final_feature_array_agri = final_feature_array.merge(broadcast_df, on="Region", how="left")

# === Fill missing values ===
final_feature_array_agri.fillna(0, inplace=True)

# === Preview or export ===
print(final_feature_array_agri.head())
# final_feature_array.to_csv("final_agri_feature_array.csv", index=False)








###################################
###################################

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import numpy as np

# Load capAgri results
df_capAgri = pd.read_csv("./data/capAgri_results.csv")

# Step 1: Cross-join features with year
years_df = pd.DataFrame(df_capAgri["year"].unique(), columns=["year"])
temp = final_feature_array.copy()
temp["key"] = 1
years_df["key"] = 1
X_all = temp.merge(years_df, on="key").drop("key", axis=1)

# Step 2: Merge features with target
df_capAgri_renamed = df_capAgri.rename(columns={"techAgri": "Technology", "r": "Region"})
training_df = X_all.merge(
    df_capAgri_renamed, on=["Region", "Technology", "year"], how="left"
)
training_df = training_df.dropna(subset=["capAgri"])

# Step 3: Encode categorical features
categorical_cols = ["Region", "Technology"]
encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(training_df[categorical_cols])
encoded_df = pd.DataFrame(
    encoded, columns=encoder.get_feature_names_out(categorical_cols)
)

# Step 4: Scale numerical features (including year)
numerical_cols = [
    col for col in training_df.columns if col not in categorical_cols + ["capAgri"]
]
scaler = MinMaxScaler()
scaled_numerical = scaler.fit_transform(training_df[numerical_cols])
scaled_numerical_df = pd.DataFrame(scaled_numerical, columns=numerical_cols)

# Step 5: Assemble X and y
X = pd.concat(
    [encoded_df.reset_index(drop=True), scaled_numerical_df.reset_index(drop=True)],
    axis=1,
)
y = training_df["capAgri"]

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




################################

import matplotlib.pyplot as plt

# Scatter plot (scaled)
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.5, edgecolor="k")
plt.xlabel("Actual capAgri (scaled)")
plt.ylabel("Predicted capAgri (scaled)")
plt.title("Predicted vs Actual capAgri (scaled)")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2)
plt.grid(True)
plt.tight_layout()
plt.show()

# Residual distribution (scaled)
residuals = y_test - y_pred
plt.figure(figsize=(8, 5))
plt.hist(residuals, bins=30, edgecolor="black")
plt.title("Residual Distribution (Scaled capAgri)")
plt.xlabel("Error (Residual)")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.show()



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

plt.xlabel("Actual capAgri (ha)")
plt.ylabel("Predicted capAgri (ha)")
plt.title("Predicted vs Actual capAgri (Original Scale)")
plt.grid(True)
plt.tight_layout()
plt.show()


#################################


import shap

# Use TreeExplainer for RandomForest
explainer_shap = shap.TreeExplainer(model)
shap_values = explainer_shap.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values, X_test,  plot_type="bar", show=False)

# Inspect individual prediction (example index: 4)
import numpy as np

i = 4
shap_row = shap_values[i]
input_row = X_test.iloc[i]

top_indices = np.argsort(np.abs(shap_row))[-3:][::-1]

for idx in top_indices:
    feature_name = X_test.columns[idx]
    shap_val = shap_row[idx]
    feature_val = input_row[feature_name]
    print(f"{feature_name}: SHAP = {shap_val:.4f}, Value = {feature_val}")


###################################


# Global SHAP feature importance
mean_abs_shap = np.abs(shap_values).mean(axis=0)
top_indices = np.argsort(mean_abs_shap)[-3:][::-1]

top_features = [X_test.columns[i] for i in top_indices]
top_shap_vals = [mean_abs_shap[i] for i in top_indices]
top_feature_vals = [X_test.iloc[:, i].mean() for i in top_indices]

# Regional summary: highest avg capAgri
cap_summary = df_capAgri.groupby(["r", "techAgri"])["capAgri"].mean().reset_index()
best_row = cap_summary.loc[cap_summary["capAgri"].idxmax()]
best_region = best_row["r"]
best_tech = best_row["techAgri"]




prompt = f"""
You are a sustainability analyst preparing a summary report for stakeholders, based on a machine learning model and SHAP analysis focused on agricultural capacity (`capAgri`).

🎯 **Objective**: Predict and understand the key drivers of regional agricultural capacity (`capAgri`)

📊 **Model Performance**:  
• R² Score: {r2_orig:.2f}  
• RMSE: {rmse_orig:.2f} hectares

🔍 **Top 3 Influential Features (from SHAP analysis)**:  
1. **{top_features[0]}** – SHAP = {top_shap_vals[0]:.3f}, Avg value = {top_feature_vals[0]:.3f}  
2. **{top_features[1]}** – SHAP = {top_shap_vals[1]:.3f}, Avg value = {top_feature_vals[1]:.3f}  
3. **{top_features[2]}** – SHAP = {top_shap_vals[2]:.3f}, Avg value = {top_feature_vals[2]:.3f}

🌾 **Regional & Technological Highlights**:  
• Region with highest capAgri potential: **{best_region}**  
• Leading growth technology: **{best_tech}**

✏️ **Task**:  
Craft a clear and professional report that:
- Summarizes the model performance in non-technical terms  
- Interprets how the top 3 features influence capAgri outcomes  
- Highlights regional and technological opportunities  
- Recommends actions that support agricultural resilience and long-term sustainability

The tone should be insight-driven, stakeholder-friendly, and suitable for regional planners, policymakers, and sustainability investors. Avoid equations or technical jargon—focus on actionable insights that can support agricultural policy and planning.
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



