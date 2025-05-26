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




##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################


"""
Deep Neural Netwroks Implementation with categorical features
"""



import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics import r2_score, mean_squared_error

# --- Load and prepare capFMs results ---
df_capFMs = pd.read_csv("capFMs_results.csv")

# Step 1: Cross-join with year
years_df = pd.DataFrame(df_capFMs["year"].unique(), columns=["year"])
temp = final_feature_array.copy()
temp["key"] = 1
years_df["key"] = 1
X_all = temp.merge(years_df, on="key").drop("key", axis=1)

# Step 2: Merge features with target
df_capFMs_renamed = df_capFMs.rename(columns={"techFMs": "Technology", "r": "Region"})
training_df = X_all.merge(df_capFMs_renamed, on=["Region", "Technology", "year"], how="left")
training_df = training_df.dropna(subset=["capFMs"])

# Step 3: Encode categorical variables (Region, Technology)
region_encoder = LabelEncoder()
tech_encoder = LabelEncoder()
training_df["Region_idx"] = region_encoder.fit_transform(training_df["Region"])
training_df["Technology_idx"] = tech_encoder.fit_transform(training_df["Technology"])

# Step 4: Scale numerical features (including year)
numerical_cols = [col for col in training_df.columns if col not in ["Region", "Technology", "capFMs", "Region_idx", "Technology_idx"]]
scaler = MinMaxScaler()
training_df[numerical_cols] = scaler.fit_transform(training_df[numerical_cols])

# Step 5: Prepare X and y
X_cat = training_df[["Region_idx", "Technology_idx"]].values
X_num = training_df[numerical_cols].values
y = training_df["capFMs"].values.reshape(-1, 1)

# Scale target
target_scaler = MinMaxScaler()
y_scaled = target_scaler.fit_transform(y)

# Step 6: Split dataset
X_cat_train, X_cat_test, X_num_train, X_num_test, y_train, y_test = train_test_split(
    X_cat, X_num, y_scaled, test_size=0.2, random_state=42
)

# Convert to tensors
X_cat_train = torch.tensor(X_cat_train, dtype=torch.long)
X_cat_test = torch.tensor(X_cat_test, dtype=torch.long)
X_num_train = torch.tensor(X_num_train, dtype=torch.float32)
X_num_test = torch.tensor(X_num_test, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

train_dataset = TensorDataset(X_cat_train, X_num_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# Step 7: Define DNN model with embeddings
class DNNWithEmbedding(nn.Module):
    def __init__(self, num_numerical, num_regions, num_techs):
        super().__init__()
        self.region_emb = nn.Embedding(num_regions, 4)  # You can tune dimensions
        self.tech_emb = nn.Embedding(num_techs, 4)
        input_dim = num_numerical + 4 + 4  # numerical + region_emb + tech_emb
        
        self.mlp = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, cat_input, num_input):
        region_vec = self.region_emb(cat_input[:, 0])
        tech_vec = self.tech_emb(cat_input[:, 1])
        x = torch.cat([region_vec, tech_vec, num_input], dim=1)
        return self.mlp(x)

model = DNNWithEmbedding(
    num_numerical=X_num_train.shape[1],
    num_regions=len(region_encoder.classes_),
    num_techs=len(tech_encoder.classes_)
)

# Step 8: Train the model
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    model.train()
    for cat_batch, num_batch, y_batch in train_loader:
        preds = model(cat_batch, num_batch)
        loss = criterion(preds, y_batch)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    if epoch % 10 == 0:
        print(f"Epoch {epoch} - Loss: {loss.item():.4f}")

# Step 9: Evaluation
model.eval()
with torch.no_grad():
    y_pred = model(X_cat_test, X_num_test).numpy()
    y_pred_original = target_scaler.inverse_transform(y_pred)
    y_test_original = target_scaler.inverse_transform(y_test)

r2_dnn = r2_score(y_test_original, y_pred_original)
rmse_dnn = np.sqrt(mean_squared_error(y_test_original, y_pred_original))
print(f"📈 DNN R² Score: {r2_dnn:.4f}")
print(f"📉 DNN RMSE: {rmse_dnn:.2f} hectares")




import shap

# Step 1: Define a wrapper that merges categorical + numeric features
class DNNWrapper(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, input_tensor):
        # Split the input tensor into categorical and numerical parts
        cat_input = input_tensor[:, :2].long()  # First 2 columns = categorical (Region_idx, Tech_idx)
        num_input = input_tensor[:, 2:].float() # Remaining columns = numerical
        return self.model(cat_input, num_input)

# Step 2: Create input tensors for SHAP (merged cat + num)
X_shap_train = torch.cat([X_cat_train.float(), X_num_train], dim=1)
X_shap_test = torch.cat([X_cat_test.float(), X_num_test], dim=1)


import shap

# Use the wrapper from before
wrapped_model = DNNWrapper(model)

# Select background (100 samples)
background = X_shap_train[:100]
X_eval = X_shap_test[:200]

# Use GradientExplainer instead of DeepExplainer
explainer = shap.GradientExplainer(wrapped_model, background)

# Compute SHAP values
shap_values = explainer.shap_values(X_eval)




# Do NOT index with [0]
# Extract and plot
shap_values_np = explainer.shap_values(X_eval)
X_shap_np = X_eval.numpy()


# Just in case: squeeze extra dimensions
shap_values_np = shap_values_np.squeeze()

print("Fixed SHAP shape:", shap_values_np.shape)  # Should now be (200, 26)


feature_names = ["Region_idx", "Technology_idx"] + list(numerical_cols)

shap.summary_plot(shap_values_np, X_shap_np, feature_names=feature_names)



























