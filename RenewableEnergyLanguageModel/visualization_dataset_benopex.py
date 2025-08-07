#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 07:54:55 2025

@author: forootan
"""


import gdxpds
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#from pyomo.environ import *
#from gams import GamsWorkspace, GamsParameter, GamsSet
#from gams import GamsWorkspace
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
gams_system_dir = setting_directory(1)  # Example path for Windows


# Load the .gdx file
## pip install gamsapi[transfer]==xx.y.z
### xx.y.z represents your installed GAMS version number (e.g., 47.6.0)

"""
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
"""

#############################################################
#############################################################
#############################################################
#############################################################

"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets from CSV
datasets = {
    "costMargFMs": pd.read_csv(gams_system_dir + "/data/" + "costMargFMs.csv"),
    "costInvFMs": pd.read_csv(gams_system_dir + "/data/" +"costInvFMs.csv"),
    "costInvLevelFMs": pd.read_csv(gams_system_dir + "/data/" +"costInvLevelFMs.csv"),
    "ghgFMs": pd.read_csv(gams_system_dir + "/data/" +"ghgFMs.csv"),
    "FMsgrowth": pd.read_csv(gams_system_dir + "/data/" +"FMsgrowth.csv"),
    "BeechArea0": pd.read_csv(gams_system_dir + "/data/" +"BeechArea0.csv"),
    "GrassArea0": pd.read_csv(gams_system_dir + "/data/" +"GrassArea0.csv"),
    "ghgTargetLULUCF": pd.read_csv(gams_system_dir + "/data/" +"ghgTargetLULUCF.csv"),
    "CO2price": pd.read_csv(gams_system_dir + "/data/" +"CO2price.csv")
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

"""

##############################################
##############################################
##############################################

"""
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

# Set global seaborn and matplotlib style
sns.set_theme(style="whitegrid")  # This handles the styling; no need for plt.style.use
plt.rcParams.update({
    "figure.dpi": 350,
    "axes.titlesize": 20,
    "axes.labelsize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 12,
    "legend.title_fontsize": 14,
    "lines.linewidth": 2,
    "lines.markersize": 8,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "font.family": "sans-serif",
    "font.sans-serif": "DejaVu Sans",  # Reliable cross-platform font
})
plt.style.use("ggplot")
# Plot other datasets
for key, df in datasets.items():
    if key in ["BeechArea0", "GrassArea0"]:
        continue  # Skip bar plots if handled separately

    plt.figure(figsize=(12, 8))

    # Time-series datasets using line plots
    if "Region" in df.columns and "Technology" in df.columns:
        sns.lineplot(
            data=df, x="Year", y=df.columns[-1],
            hue="Region", style="Technology",
            markers=True, dashes=False
        )
        plt.legend(title="Region / Technology", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, shadow=True)

    elif "Region" in df.columns:
        sns.lineplot(
            data=df, x="Year", y=df.columns[-1],
            hue="Region", markers=True
        )
        plt.legend(title="Region", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, shadow=True)

    else:
        sns.lineplot(
            data=df, x="Year", y=df.columns[-1],
            marker="o"
        )

    #plt.xlabel("Year", labelpad=10)
    #plt.ylabel(f"{df.columns[-1]} Value", labelpad=10)
    
    plt.xlabel("Year", labelpad=10, fontsize=16)  # Adjust font size here
    plt.ylabel(f"{df.columns[-1]} Value", labelpad=10, fontsize=16)

    
    
    plt.title(f"{key} Evolution Over Time", pad=15)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
"""

##############################################
##############################################
##############################################
##############################################

"""
Input data
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets from CSV
datasets = {
    "costMargFMs": pd.read_csv(gams_system_dir + "/scenarios_neg_emi/csv_outputs/" + "costMargFMs_base_scenario.csv"),
    "costInvFMs": pd.read_csv(gams_system_dir + "/scenarios_neg_emi/csv_outputs/" +"costInvFMs_base_scenario.csv"),
    "costInvLevelFMs": pd.read_csv(gams_system_dir + "/scenarios_neg_emi/csv_outputs/" +"costInvLevelFMs_base_scenario.csv"),
    "ghgFMs": pd.read_csv(gams_system_dir + "/scenarios_neg_emi/csv_outputs/" +"ghgFMs_base_scenario.csv"),
    "FMsgrowth": pd.read_csv(gams_system_dir + "/scenarios_neg_emi/csv_outputs/" +"FMsgrowth_base_scenario.csv"),
    "BeechArea0": pd.read_csv(gams_system_dir + "/scenarios_neg_emi/csv_outputs/" +"BeechArea0_base_scenario.csv"),
    "GrassArea0": pd.read_csv(gams_system_dir + "/scenarios_neg_emi/csv_outputs/" +"GrassArea0_base_scenario.csv"),
    "ghgTargetLULUCF": pd.read_csv(gams_system_dir + "/scenarios_neg_emi/csv_outputs/" +"ghgTargetLULUCF_base_scenario.csv"),
    "CO2price": pd.read_csv(gams_system_dir + "/scenarios_neg_emi/csv_outputs/" +"CO2price_base_scenario.csv")
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

for key, df in datasets.items():
    df.rename(columns=rename_columns[key], inplace=True)
    df["Year"] = pd.to_numeric(df["Year"], errors='coerce')

# Set global plot style
sns.set_theme(style="whitegrid")
#plt.style.use("ggplot")

plt.rcParams.update({
    "figure.dpi": 350,
    "axes.titlesize": 20,
    "axes.labelsize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 12,
    "legend.title_fontsize": 14,
    "lines.linewidth": 2,
    "lines.markersize": 8,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "font.family": "sans-serif",
    "font.sans-serif": "DejaVu Sans",
    #"text.usetex": True  # Uncomment if full LaTeX rendering is desired
})

# LaTeX-style label mapping
pretty_labels = {
    "costMargFMs": r"$\mathrm{Marginal\ Cost\ of\ FMs}$",
    "costInvFMs": r"$\mathrm{Investment\ Cost\ of\ FMs}$",
    "costInvLevelFMs": r"$\mathrm{Investment\ Level\ Cost\ of\ FMs}$",
    "ghgFMs": r"$\mathrm{GHG\ Removals\ by\ FMs}$",
    "FMsgrowth": r"$\mathrm{Forest\ Management\ Growth}$",
    "GHG_Removal": r"$\mathrm{GHG\ Removal\ (MtCO_2)}$",
    "InvestmentCost": r"$\mathrm{Investment\ Cost\ (€)}$",
    "InvestmentLevelCost": r"$\mathrm{Investment\ Level\ Cost\ (€)}$",
    "ForestManagementGrowth": r"$\mathrm{Forest\ Management\ Growth\ (ha)}$",
    "Cost": r"$\mathrm{Marginal\ Cost\ (€ / tCO_2)}$",
    "GHG_Target_LULUCF": r"$\mathrm{GHG\ Target\ LULUCF\ (MtCO_2)}$",
    "CO2_Price": r"$\mathrm{CO_2\ Price\ (€ / tCO_2)}$",
    "InitialBeechArea": r"$\mathrm{Initial\ Beech\ Area\ (ha)}$",
    "InitialGrassArea": r"$\mathrm{Initial\ Grass\ Area\ (ha)}$"
}

# Special bar plots
if "BeechArea0" in datasets and "GrassArea0" in datasets:
    beech_df = datasets["BeechArea0"].sort_values(by="InitialBeechArea", ascending=True)
    grass_df = datasets["GrassArea0"].sort_values(by="InitialGrassArea", ascending=True)

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6), sharey=True)

    axes[0].barh(beech_df["Region"], beech_df["InitialBeechArea"], color="forestgreen")
    axes[0].set_xlabel(pretty_labels["InitialBeechArea"])
    axes[0].set_ylabel("Region")
    axes[0].set_title(r"$\mathrm{Initial\ Beech\ Area\ by\ Region\ (2020)}$")

    axes[1].barh(grass_df["Region"], grass_df["InitialGrassArea"], color="goldenrod")
    axes[1].set_xlabel(pretty_labels["InitialGrassArea"])
    axes[1].set_title(r"$\mathrm{Initial\ Grass\ Area\ by\ Region\ (2020)}$")

    plt.tight_layout()
    plt.show()

# Time-series line plots
for key, df in datasets.items():
    if key in ["BeechArea0", "GrassArea0"]:
        continue  # Already handled

    plt.figure(figsize=(12, 8))
    y_col = df.columns[-1]
    ylabel = pretty_labels.get(y_col, y_col)
    title = pretty_labels.get(key, key)

    if "Region" in df.columns and "Technology" in df.columns:
        sns.lineplot(
            data=df, x="Year", y=y_col,
            hue="Region", style="Technology",
            markers=True, dashes=False
        )
        plt.legend(title="Region / Technology", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, shadow=True)

    elif "Region" in df.columns:
        sns.lineplot(
            data=df, x="Year", y=y_col,
            hue="Region", markers=True
        )
        plt.legend(title="Region", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, shadow=True)

    else:
        sns.lineplot(
            data=df, x="Year", y=y_col,
            marker="o"
        )

    plt.xlabel(r"$\mathrm{Year}$", fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    plt.title(title + r" $\mathrm{Evolution\ Over\ Time}$", fontsize=20, pad=15)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()



##############################################
##############################################
##############################################
##############################################
##############################################


import pandas as pd

# Select a representative region (e.g., "DE1")
selected_region = "DE1"

# Get the total number of unique regions
total_regions = datasets["costMargFMs"]["Region"].nunique()

# Extract relevant columns for the selected region
costMargFMs = datasets["costMargFMs"].query("Region == @selected_region")[["Year", "Technology", "Cost"]].copy()
costInvFMs = datasets["costInvFMs"].query("Region == @selected_region")[["Year", "Technology", "InvestmentCost"]].copy()
costInvLevelFMs = datasets["costInvLevelFMs"].query("Region == @selected_region")[["Year", "Technology", "InvestmentLevelCost"]].copy()
ghgFMs = datasets["ghgFMs"].query("Region == @selected_region")[["Year", "Technology", "GHG_Removal"]].copy()
FMsgrowth = datasets["FMsgrowth"].query("Region == @selected_region")[["Year", "Technology", "ForestManagementGrowth"]].copy()

# Scale values by the total number of regions
costInvFMs["InvestmentCost"] *= total_regions
costInvLevelFMs["InvestmentLevelCost"] *= total_regions
ghgFMs["GHG_Removal"] *= total_regions
FMsgrowth["ForestManagementGrowth"] *= total_regions
costMargFMs["Cost"] *= total_regions







import pandas as pd
from itertools import product

# Select a representative region (e.g., "DE1")
selected_region = "DE2"

# Get the total number of unique regions
total_regions = datasets["costMargFMs"]["Region"].nunique()

# Extract relevant columns for the selected region
costMargFMs = datasets["costMargFMs"].query("Region == @selected_region")[["Year", "Technology", "Cost"]].copy()
costInvFMs = datasets["costInvFMs"].query("Region == @selected_region")[["Year", "Technology", "InvestmentCost"]].copy()
costInvLevelFMs = datasets["costInvLevelFMs"].query("Region == @selected_region")[["Year", "Technology", "InvestmentLevelCost"]].copy()
ghgFMs = datasets["ghgFMs"].query("Region == @selected_region")[["Year", "Technology", "GHG_Removal"]].copy()
FMsgrowth = datasets["FMsgrowth"].query("Region == @selected_region")[["Year", "Technology", "ForestManagementGrowth"]].copy()

# Scale values by the total number of regions
costInvFMs["InvestmentCost"] *= total_regions
costInvLevelFMs["InvestmentLevelCost"] *= total_regions
ghgFMs["GHG_Removal"] *= total_regions
FMsgrowth["ForestManagementGrowth"] *= total_regions
costMargFMs["Cost"] *= total_regions

# Extract relevant numeric values
ghg_target_values = datasets["ghgTargetLULUCF"]["GHG_Target_LULUCF"].tolist()
co2_price_values = datasets["CO2price"]["CO2_Price"].tolist()
cost_values = costMargFMs["Cost"].tolist()
investment_cost_values = costInvFMs["InvestmentCost"].tolist()
investment_level_cost_values = costInvLevelFMs["InvestmentLevelCost"].tolist()
ghg_removal_values = ghgFMs["GHG_Removal"].tolist()
forest_management_growth_values = FMsgrowth["ForestManagementGrowth"].tolist()






############################################
############################################
############################################
############################################
############################################
############################################

"""
Plots of the Optimizations Results
"""


"""
import gdxpds
import pandas as pd

# Load the .gdx file
gdx_file = "results.gdx"
gdx_data_result = gdxpds.to_dataframes(gdx_file)

# Print available keys to confirm all variables exist
print("Available keys in results.gdx:", gdx_data_result.keys())

# Extract Decision Variables
df_capFMs = gdx_data_result['capFMs'][['year', 'techFMs', 'r', 'Level']].rename(columns={'Level': 'capFMs'})
df_capAgri = gdx_data_result['capAgri'][['year', 'techAgri', 'r', 'Level']].rename(columns={'Level': 'capAgri'})

# Extract GHG Abatement Data
df_ghgAbateFMs = gdx_data_result['ghgAbateTechFMs'][['year', 'techFMs', 'r', 'Level']].rename(columns={'Level': 'ghgAbateTechFMs'})
df_ghgAbateAgri = gdx_data_result['ghgAbateTechAgri'][['year', 'techAgri', 'r', 'Level']].rename(columns={'Level': 'ghgAbateTechAgri'})

# Extract Cost Data
df_total_cost_annual = gdx_data_result['Total_costAnnual'][['year', 'Level']].rename(columns={'Level': 'Total_costAnnual'})
df_total_cost = gdx_data_result['Total_cost'][['Level']].rename(columns={'Level': 'Total_cost'})
df_costAnnualFMs = gdx_data_result['costAnnualFMs'][['year', 'Level']].rename(columns={'Level': 'costAnnualFMs'})
df_costAnnualAgri = gdx_data_result['costAnnualAgri'][['year', 'Level']].rename(columns={'Level': 'costAnnualAgri'})

# Extract Total GHG Reduction
df_total_ghg = gdx_data_result['Total_ghg'][['Level']].rename(columns={'Level': 'Total_ghg'})
df_total_ghg_annual = gdx_data_result['Total_ghgAnnual'][['year', 'Level']].rename(columns={'Level': 'Total_ghgAnnual'})

# Extract Other Variables
df_FMsGrassArea = gdx_data_result['FMsGrassArea'][['year', 'r', 'Level']].rename(columns={'Level': 'FMsGrassArea'})
df_FMsBeechArea = gdx_data_result['FMsBeechArea'][['year', 'r', 'Level']].rename(columns={'Level': 'FMsBeechArea'})
df_AgriGrassArea = gdx_data_result['AgriGrassArea'][['year', 'r', 'Level']].rename(columns={'Level': 'AgriGrassArea'})
df_CO2gapRewt = gdx_data_result['CO2gapRewt'][['Level']].rename(columns={'Level': 'CO2gapRewt'})

# Fix: Extract purCO2LULUCF by renaming first column to 'year'
df_purCO2LULUCF = gdx_data_result['purCO2LULUCF'].rename(columns={'*': 'year'})[['year', 'Level']]
df_purCO2LULUCF = df_purCO2LULUCF.rename(columns={'Level': 'purCO2LULUCF'})

# 
df_ghgAbateAnnualFMs = gdx_data_result['ghgAbateAnnualFMs'][['year', 'Level']].rename(columns={'Level': 'ghgAbateAnnualFMs'})

# Extract Cost by Technology
df_costTechFMs = gdx_data_result['costTechFMs'][['year', 'techFMs', 'r', 'Level']].rename(columns={'Level': 'costTechFMs'})
df_costTechAgri = gdx_data_result['costTechAgri'][['year', 'techAgri', 'r', 'Level']].rename(columns={'Level': 'costTechAgri'})



# Save extracted data to CSV files
df_capFMs.to_csv("capFMs_results.csv", index=False)
df_capAgri.to_csv("capAgri_results.csv", index=False)
df_ghgAbateFMs.to_csv("ghgAbateFMs_results.csv", index=False)
df_ghgAbateAgri.to_csv("ghgAbateAgri_results.csv", index=False)
df_total_cost_annual.to_csv("total_cost_annual.csv", index=False)

df_costAnnualFMs.to_csv("costAnnualFMs_results.csv", index=False)
df_costAnnualAgri.to_csv("costAnnualAgri_results.csv", index=False)

df_total_ghg_annual.to_csv("total_ghg_annual.csv", index=False)
df_FMsGrassArea.to_csv("FMsGrassArea.csv", index=False)
df_FMsBeechArea.to_csv("FMsBeechArea.csv", index=False)

df_purCO2LULUCF.to_csv("purCO2LULUCF.csv", index=False)


df_costTechFMs.to_csv("costTechFMs.csv", index=False)
df_costTechAgri.to_csv("costTechAgri.csv", index=False)



df_CO2gapRewt.to_csv("CO2gapRewt.csv", index=False)
df_total_cost.to_csv("total_cost.csv", index=False)
df_total_ghg.to_csv("total_ghg.csv", index=False)

print("🎉 Extraction completed. All files saved successfully.")

"""


############################################
############################################
############################################
############################################
############################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data (same as before)
df_capFMs = pd.read_csv(gams_system_dir + "/data/" +"capFMs_results.csv")
df_capAgri = pd.read_csv(gams_system_dir + "/data/" +"capAgri_results.csv")
df_ghgAbateFMs = pd.read_csv(gams_system_dir + "/data/" +"ghgAbateFMs_results.csv")
df_ghgAbateAgri = pd.read_csv(gams_system_dir + "/data/" +"ghgAbateAgri_results.csv")
df_total_cost_annual = pd.read_csv(gams_system_dir + "/data/" +"total_cost_annual.csv")
df_costAnnualFMs = pd.read_csv(gams_system_dir + "/data/" +"costAnnualFMs_results.csv")
df_costAnnualAgri = pd.read_csv(gams_system_dir + "/data/" +"costAnnualAgri_results.csv")
df_total_ghg_annual = pd.read_csv(gams_system_dir + "/data/" +"total_ghg_annual.csv")
df_FMsGrassArea = pd.read_csv(gams_system_dir + "/data/" +"FMsGrassArea.csv")
df_FMsBeechArea = pd.read_csv(gams_system_dir + "/data/" +"FMsBeechArea.csv")
df_purCO2LULUCF = pd.read_csv(gams_system_dir + "/data/" +"purCO2LULUCF.csv")

df_costTechFMs = pd.read_csv(gams_system_dir + "/data/" + "costTechFMs.csv")
df_costTechAgri = pd.read_csv(gams_system_dir + "/data/" + "costTechAgri.csv")
df_CO2gapRewt = pd.read_csv(gams_system_dir + "/data/" + "CO2gapRewt.csv")
df_total_cost = pd.read_csv(gams_system_dir + "/data/" + "total_cost.csv")
df_total_ghg = pd.read_csv(gams_system_dir + "/data/" + "total_ghg.csv")


# Set consistent style
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "figure.dpi": 350,
    "axes.titlesize": 20,
    "axes.labelsize": 16,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 12,
    "legend.title_fontsize": 14,
    "lines.linewidth": 2,
    "lines.markersize": 8,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "font.family": "sans-serif",
    "font.sans-serif": "DejaVu Sans",
})

# LaTeX-style label dictionary
pretty_labels = {
    "capFMs": r"$\mathrm{Allocated\ Land\ (ha)}$",
    "capAgri": r"$\mathrm{Agricultural\ Area\ (ha)}$",
    "ghgAbateTechFMs": r"$\mathrm{GHG\ Abatement\ (tCO_2eq)}$",
    "costAnnualFMs": r"$\mathrm{Annual\ Cost\ of\ FMs\ (€)}$",
    "costAnnualAgri": r"$\mathrm{Annual\ Cost\ of\ Agriculture\ (€)}$",
    "Total_ghgAnnual": r"$\mathrm{Total\ GHG\ Reduction\ (tCO_2eq)}$",
    "purCO2LULUCF": r"$\mathrm{CO_2\ Purchased\ from\ LULUCF\ (tCO_2eq)}$"
}

# -------- PLOT 1: Total GHG Reduction Over Time --------
plt.figure(figsize=(15, 6))
sns.lineplot(data=df_total_ghg_annual, x="year", y="Total_ghgAnnual", marker="o")
plt.xlabel(r"$\mathrm{Year}$")
plt.ylabel(pretty_labels["Total_ghgAnnual"])
plt.title(r"$\mathrm{Total\ GHG\ Reduction\ Over\ Time}$")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# -------- PLOT 2: Annual Cost of FMs and Agriculture --------
plt.figure(figsize=(15, 6))
sns.lineplot(data=df_costAnnualFMs, x="year", y="costAnnualFMs", marker="o", label=r"$\mathrm{FMs}$")
sns.lineplot(data=df_costAnnualAgri, x="year", y="costAnnualAgri", marker="s", linestyle="--", label=r"$\mathrm{Agriculture}$")
plt.xlabel(r"$\mathrm{Year}$")
plt.ylabel(r"$\mathrm{Annual\ Cost\ (€)}$")
plt.title(r"$\mathrm{Annual\ Cost\ of\ FMs\ and\ Agriculture\ Over\ Time}$")
plt.legend(title=r"$\mathrm{Category}$", frameon=True, shadow=True)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# -------- PLOT 3: CO₂ Purchased from LULUCF --------
plt.figure(figsize=(15, 6))
sns.lineplot(data=df_purCO2LULUCF, x="year", y="purCO2LULUCF", marker="D")
plt.xlabel(r"$\mathrm{Year}$")
plt.ylabel(pretty_labels["purCO2LULUCF"])
plt.title(r"$\mathrm{CO_2\ Purchased\ from\ LULUCF\ Over\ Time}$")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# -------- PLOT 4: Forest Management Land Allocation --------

"""
plt.figure(figsize=(15, 6))
sns.barplot(data=df_capFMs, x="year", y="capFMs", hue="r", dodge=True)
plt.xlabel(r"$\mathrm{Year}$")
plt.ylabel(pretty_labels["capFMs"])
plt.title(r"$\mathrm{Forest\ Management\ Land\ Allocation\ by\ Region}$")
plt.legend(title=r"$\mathrm{Region}$", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True, shadow=True)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
"""


# Step 1: Aggregate over technologies per region-year
df_capFMs_region = df_capFMs.groupby(["year", "r"], as_index=False)["capFMs"].sum()

# Pivot for stacked area plot
df_stack = df_capFMs_region.pivot(index="year", columns="r", values="capFMs").fillna(0)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
df_stack.plot.area(ax=ax, colormap="tab20", linewidth=0)

# Axis and title labels
ax.set_xlabel(r"$\mathrm{Year}$", fontsize=14)
ax.set_ylabel(r"$\mathrm{Allocated\ Land\ (ha)}$", fontsize=14)
ax.set_title(r"$\mathrm{Forest\ Management\ Land\ Allocation\ by\ Region}$", fontsize=18)
ax.grid(axis="y", linestyle="--", alpha=0.5)

# Legend below with multiple columns
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, labels=labels, title=r"$\mathrm{Region}$",
          bbox_to_anchor=(0.5, -0.25), loc="upper center",
          ncol=6, frameon=True, fontsize=10, title_fontsize=12)

plt.tight_layout()
plt.show()





# -------- PLOT 5: GHG Abatement by FMs --------
plt.figure(figsize=(12, 6))
sns.barplot(data=df_ghgAbateFMs, x="year", y="ghgAbateTechFMs", hue="r", dodge=True)
plt.xlabel(r"$\mathrm{Year}$")
plt.ylabel(pretty_labels["ghgAbateTechFMs"])
plt.title(r"$\mathrm{GHG\ Abatement\ by\ FM\ Technology\ and\ Region}$")
plt.legend(title=r"$\mathrm{Region}$", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True, shadow=True)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# -------- PLOT 6: Agriculture Land Allocation --------
"""
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_capAgri, x="year", y="capAgri", hue="r", marker="o")
plt.xlabel(r"$\mathrm{Year}$")
plt.ylabel(pretty_labels["capAgri"])
plt.title(r"$\mathrm{Agriculture\ Land\ Allocation\ by\ Region}$")
plt.legend(title=r"$\mathrm{Region}$", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=True, shadow=True)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
"""

# Step 1: Aggregate over technologies per region-year
df_capAgri_region = df_capAgri.groupby(["year", "r"], as_index=False)["capAgri"].sum()

# Step 2: Pivot to wide format for stacked area plot
df_agri_stack = df_capAgri_region.pivot(index="year", columns="r", values="capAgri").fillna(0)

# Step 3: Plot
fig, ax = plt.subplots(figsize=(10, 6))  # wider view for clarity
df_agri_stack.plot.area(ax=ax, colormap="tab20", linewidth=0)

# Axis labels and title
ax.set_xlabel(r"$\mathrm{Year}$", fontsize=14)
ax.set_ylabel(r"$\mathrm{Agricultural\ Area\ (ha)}$", fontsize=14)
ax.set_title(r"$\mathrm{Agriculture\ Land\ Allocation\ by\ Region}$", fontsize=18)
ax.grid(axis="y", linestyle="--", alpha=0.5)

# Legend below the plot with multiple columns
handles, labels = ax.get_legend_handles_labels()
ax.legend(
    handles=handles, labels=labels,
    title=r"$\mathrm{Region}$",
    bbox_to_anchor=(0.5, -0.25),
    loc="upper center",
    ncol=6,
    frameon=True,
    fontsize=10,
    title_fontsize=12
)

plt.tight_layout()
plt.show()




###########################################
###########################################
###########################################
###########################################


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load extracted CSV data
df_capFMs = pd.read_csv(gams_system_dir + "/data/" +"capFMs_results.csv")
df_capAgri = pd.read_csv(gams_system_dir + "/data/" +"capAgri_results.csv")
df_ghgAbateFMs = pd.read_csv(gams_system_dir + "/data/" +"ghgAbateFMs_results.csv")
df_ghgAbateAgri = pd.read_csv(gams_system_dir + "/data/" +"ghgAbateAgri_results.csv")
df_total_cost_annual = pd.read_csv(gams_system_dir + "/data/" +"total_cost_annual.csv")
df_costAnnualFMs = pd.read_csv(gams_system_dir + "/data/" +"costAnnualFMs_results.csv")
df_costAnnualAgri = pd.read_csv(gams_system_dir + "/data/" +"costAnnualAgri_results.csv")
df_total_ghg_annual = pd.read_csv(gams_system_dir + "/data/" +"total_ghg_annual.csv")
df_FMsGrassArea = pd.read_csv(gams_system_dir + "/data/" +"FMsGrassArea.csv")
df_FMsBeechArea = pd.read_csv(gams_system_dir + "/data/" +"FMsBeechArea.csv")
df_purCO2LULUCF = pd.read_csv(gams_system_dir + "/data/" +"purCO2LULUCF.csv")

# Set plot style
plt.style.use("ggplot")

# -------- PLOT 1: Total GHG Reduction Over Time by Region --------
plt.figure(figsize=(10, 5))
sns.lineplot(data=df_total_ghg_annual, x="year", y="Total_ghgAnnual", marker="o")
plt.xlabel("Year")
plt.ylabel("Total GHG Reduction (tCO₂eq)")
plt.title("Total GHG Reduction Over Time (Total)")
plt.grid(True)
plt.show()


# -------- PLOT 2: Cost of FMs and Agri Over Time by Region --------
plt.figure(figsize=(10, 5))
sns.lineplot(data=df_costAnnualFMs, x="year", y="costAnnualFMs", marker="o", linestyle="-", label="Annual FMs Cost")
sns.lineplot(data=df_costAnnualAgri, x="year", y="costAnnualAgri", marker="s", linestyle="--", label="Annual Agri Cost")
plt.xlabel("Year")
plt.ylabel("Cost (€)")
plt.title("Annual Cost of FMs and Agriculture Over Time")
plt.legend()
plt.grid(True)
plt.show()


# -------- PLOT 3: PurCO2 LULUCF Over Time by Region --------
plt.figure(figsize=(10, 5))
sns.lineplot(data=df_purCO2LULUCF, x="year", y="purCO2LULUCF", marker="D")
plt.xlabel("Year")
plt.ylabel("CO₂ Purchase (tCO₂eq)")
plt.title("CO₂ Purchased from LULUCF Over Time")
plt.grid(True)
plt.show()


# -------- PLOT 4: Land Allocation by Tech Type and Region --------
plt.figure(figsize=(12, 6))
sns.barplot(data=df_capFMs, x="year", y="capFMs", hue="r", dodge=True)
plt.xlabel("Year")
plt.ylabel("Allocated Land (ha)")
plt.title("Forest Management Land Allocation Over Time by Region")
plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# -------- PLOT 5: GHG Abatement by Tech Type and Region --------
plt.figure(figsize=(12, 6))
sns.barplot(data=df_ghgAbateFMs, x="year", y="ghgAbateTechFMs", hue="r", dodge=True)
plt.xlabel("Year")
plt.ylabel("GHG Abatement (tCO₂eq)")
plt.title("GHG Abatement by Forest Management Tech and Region")
plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()



# -------- PLOT 6: Agriculture Implementation Over Time by Region --------
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_capAgri, x="year", y="capAgri", hue="r", marker="o")
plt.xlabel("Year")
plt.ylabel("Agriculture Area (ha)")
plt.title("Agriculture Land Allocation Over Time by Region")
plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.show()





###########################################
###########################################
###########################################
###########################################

"""
Cost Technology Forest Management
"""

plt.figure(figsize=(12, 6))
sns.lineplot(data=df_costTechFMs, x="year", y="costTechFMs", hue="techFMs", marker="o")
plt.xlabel("Year")
plt.ylabel("Cost (€)")
plt.title("Forest Management Cost by Technology Over Time")
plt.legend(title="Tech Type", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.show()


# Aggregate over technologies: total FM cost per region-year
df_cost_region = df_costTechFMs.groupby(["year", "r"], as_index=False)["costTechFMs"].sum()

# Pivot for area plot
df_cost_stack = df_cost_region.pivot(index="year", columns="r", values="costTechFMs").fillna(0)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))
df_cost_stack.plot.area(ax=ax, colormap="tab20", linewidth=0)

ax.set_xlabel(r"$\mathrm{Year}$", fontsize=14)
ax.set_ylabel(r"$\mathrm{Total\ FM\ Cost\ (€)}$", fontsize=14)
ax.set_title(r"$\mathrm{Forest\ Management\ Cost\ by\ Region}$", fontsize=18)
ax.grid(axis="y", linestyle="--", alpha=0.5)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, labels=labels, title=r"$\mathrm{Region}$",
          bbox_to_anchor=(0.5, -0.25), loc="upper center", ncol=6,
          frameon=True, fontsize=10, title_fontsize=12)

plt.tight_layout()
plt.show()





###########################################
###########################################
###########################################
###########################################

"""
Cost by Tech (Agriculture)
"""

plt.figure(figsize=(12, 6))
sns.lineplot(data=df_costTechAgri, x="year", y="costTechAgri", hue="techAgri", marker="o")
plt.xlabel("Year")
plt.ylabel("Cost (€)")
plt.title("Agricultural Cost by Technology Over Time")
plt.legend(title="Tech Type", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.show()

# Aggregate over techAgri to get total cost per region-year
df_agri_cost_region = df_costTechAgri.groupby(["year", "r"], as_index=False)["costTechAgri"].sum()

# Pivot for stacked area plot
df_agri_cost_stack = df_agri_cost_region.pivot(index="year", columns="r", values="costTechAgri").fillna(0)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))
df_agri_cost_stack.plot.area(ax=ax, colormap="tab20", linewidth=0)

ax.set_xlabel(r"$\mathrm{Year}$", fontsize=14)
ax.set_ylabel(r"$\mathrm{Total\ Agri\ Cost\ (€)}$", fontsize=14)
ax.set_title(r"$\mathrm{Agriculture\ Technology\ Cost\ by\ Region}$", fontsize=18)
ax.grid(axis="y", linestyle="--", alpha=0.5)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, labels=labels, title=r"$\mathrm{Region}$",
          bbox_to_anchor=(0.5, -0.25), loc="upper center", ncol=6,
          frameon=True, fontsize=10, title_fontsize=12)

plt.tight_layout()
plt.show()




###########################################
###########################################
###########################################
###########################################


"""
GHG Abatement over time for all technologies and for all regions
"""


import matplotlib.pyplot as plt
import numpy as np

# Set figure size
plt.figure(figsize=(12, 6))

# Get unique regions
regions = df_ghgAbateFMs["r"].unique()

techs = df_ghgAbateFMs["techFMs"].unique()

years = df_ghgAbateFMs["year"].unique()

# Define a color map for regions
colors = plt.cm.viridis(np.linspace(0, 1, len(regions)))

# Plot each region separately
for i, region in enumerate(regions):
    region_data = df_ghgAbateFMs[df_ghgAbateFMs["r"] == region]
    plt.plot(region_data["year"], region_data["ghgAbateTechFMs"], 
             marker="o", linestyle="-", color=colors[i], label=f"Region {region}")

# Labels and title
plt.xlabel("Year")
plt.ylabel("GHG Abatement (tCO₂eq)")
plt.title("GHG Abatement by Forest Management Tech and Region")

# Legend and grid
plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.show()




# Aggregate GHG abatement per region-year
df_ghg_region = df_ghgAbateFMs.groupby(["year", "r"], as_index=False)["ghgAbateTechFMs"].sum()

# Pivot for stacked area plot
df_ghg_stack_region = df_ghg_region.pivot(index="year", columns="r", values="ghgAbateTechFMs").fillna(0)

# Plot
fig, ax = plt.subplots(figsize=(12, 6))
df_ghg_stack_region.plot.area(ax=ax, colormap="tab20", linewidth=0)

ax.set_xlabel(r"$\mathrm{Year}$", fontsize=14)
ax.set_ylabel(r"$\mathrm{GHG\ Abatement\ (tCO_2eq)}$", fontsize=14)
ax.set_title(r"$GHG\ Abatement\ by\ Forest\ Management\ Tech\ and\ Region$", fontsize=18)
ax.grid(axis="y", linestyle="--", alpha=0.5)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, labels=labels, title=r"$\mathrm{Region}$",
          bbox_to_anchor=(0.5, -0.25), loc="upper center", ncol=6,
          frameon=True, fontsize=10, title_fontsize=12)

plt.tight_layout()
plt.show()







###########

"""
GHG Abatement over time for each technology in region: DE1 and DE2
"""


import matplotlib.pyplot as plt

# Select two specific regions (Modify as needed)
selected_regions = ["DE1", "DE2"]  # Change these to the regions of interest

# Set figure size
plt.figure(figsize=(12, 6))

# Define colors for the selected regions
colors = ["blue", "red"]  # Different colors for the two regions

# Plot data for the selected regions
for i, region in enumerate(selected_regions):
    region_data = df_ghgAbateFMs[df_ghgAbateFMs["r"] == region]
    plt.plot(region_data["year"], region_data["ghgAbateTechFMs"], 
             marker="o", linestyle="-", color=colors[i], label=f"Region {region}")

# Labels and title
plt.xlabel("Year")
plt.ylabel("GHG Abatement (tCO₂eq)")
plt.title(f"GHG Abatement for Selected Regions: {selected_regions[0]} & {selected_regions[1]}")

# Legend and grid
plt.legend(title="Region")
plt.grid(True)
plt.show()


############

"""
GHG Abatement over time for each technology in region: DE2
"""

import matplotlib.pyplot as plt

# Select a specific region (Modify as needed)
selected_region = "DE2"  # Change this to any region you want

# Filter the dataset for the selected region
region_data = df_ghgAbateFMs[df_ghgAbateFMs["r"] == selected_region]

# Set figure size
plt.figure(figsize=(12, 6))

# Loop through each technology in the region and plot separately
for tech in region_data["techFMs"].unique():
    tech_data = region_data[region_data["techFMs"] == tech]
    plt.plot(tech_data["year"], tech_data["ghgAbateTechFMs"], marker="o", linestyle="-", label=tech)

# Labels and title
plt.xlabel("Year")
plt.ylabel("GHG Abatement (tCO₂eq)")
plt.title(f"GHG Abatement Over Time for Each Technology in Region: {selected_region}")

# Legend and grid
plt.legend(title="Technology", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.show()


#################
#################


"""
GHG Abatement over time for each pair of (technology, region)
"""


import matplotlib.pyplot as plt

# Get the unique regions and technologies
regions = df_ghgAbateFMs["r"].unique()
techs = df_ghgAbateFMs["techFMs"].unique()

# Iterate through each region and plot separately
for region in regions:
    # Filter data for the region
    region_data = df_ghgAbateFMs[df_ghgAbateFMs["r"] == region]
    
    # Create a figure
    plt.figure(figsize=(10, 5))
    
    # Loop through each technology within the region
    for tech in techs:
        tech_data = region_data[region_data["techFMs"] == tech]
        if not tech_data.empty:  # Ensure there's data before plotting
            plt.plot(tech_data["year"], tech_data["ghgAbateTechFMs"], marker="o", linestyle="-", label=tech)

    # Labels and title
    plt.xlabel("Year")
    plt.ylabel("GHG Abatement (tCO₂eq)")
    plt.title(f"GHG Abatement by Technology in Region: {region}")

    # Legend and grid
    plt.legend(title="Technology", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True)
    
    # Show plot
    plt.show()


####################
####################



"""

import pandas as pd
import numpy as np
from scipy.stats import linregress
from numpy.polynomial.polynomial import Polynomial

# Function to compute statistical features for (region, technology)
def compute_features(df, value_col, feature_prefix):
    extracted_features = []

    # Group by (Region, Technology)
    for (region, tech), group in df.groupby(["r", "techFMs"]):
        years = group["year"].values.astype(float)  # Convert years to numeric
        values = group[value_col].values

        # Compute linear regression slope
        slope, _, _, _, _ = linregress(years, values)

        # Compute polynomial fits
        poly_2 = Polynomial.fit(years, values, 2).convert().coef
        poly_3 = Polynomial.fit(years, values, 3).convert().coef

        # Extract polynomial coefficients safely
        poly_2_c1 = poly_2[1] if len(poly_2) > 1 else 0
        poly_2_c2 = poly_2[2] if len(poly_2) > 2 else 0
        poly_3_c1 = poly_3[1] if len(poly_3) > 1 else 0
        poly_3_c2 = poly_3[2] if len(poly_3) > 2 else 0
        poly_3_c3 = poly_3[3] if len(poly_3) > 3 else 0

        # Compute other statistical features
        initial_value = values[0]
        final_value = values[-1]
        mean_value = np.mean(values)
        std_value = np.std(values)
        range_value = np.max(values) - np.min(values)

        # Append results
        extracted_features.append([
            region, tech, initial_value, final_value, slope, 
            poly_2_c1, poly_2_c2,  # Quadratic coefficients
            poly_3_c1, poly_3_c2, poly_3_c3,  # Cubic coefficients
            mean_value, std_value, range_value
        ])

    # Convert to DataFrame
    feature_df = pd.DataFrame(extracted_features, columns=[
        "Region", "Technology", f"{feature_prefix}_2020", f"{feature_prefix}_2050", f"{feature_prefix}_Slope",
        f"{feature_prefix}_Poly2_C1", f"{feature_prefix}_Poly2_C2",
        f"{feature_prefix}_Poly3_C1", f"{feature_prefix}_Poly3_C2", f"{feature_prefix}_Poly3_C3",
        f"{feature_prefix}_Mean", f"{feature_prefix}_Std", f"{feature_prefix}_Range"
    ])
    
    return feature_df

# Compute features for GHG abatement
ghgAbateFMs_features = compute_features(df_ghgAbateFMs, "ghgAbateTechFMs", "GHGAbate")

ghgAbateFMs_features["Technology"].unique()

"""



##########################################
##########################################
##########################################

"""

### Observations:
1. **Objective Function**: The model minimizes the total cost of implementing different land-use-based carbon sequestration techniques.
2. **Decision Variables**:
   - `capFMs`: Implementation of forest management strategies.
   - `capAgri`: Implementation of agricultural-based strategies.
   - `ghgAbateTechFMs` & `ghgAbateTechAgri`: GHG abatement potential via FMs and agriculture.
3. **Constraints**:
   - Land-use availability constraints for forests, grasslands, and peatlands.
   - Growth rate constraints for forest and agriculture-based technologies.
   - National policy constraints, such as rewetting targets.
   - GHG abatement constraints ensuring emissions reduction goals are met.
4. **Data Handling**:
   - Inputs are loaded from `test_Ali.gdx`.
   - Results are saved in `results.gdx` and then exported to `results.csv`.

### Potential Improvements or Questions:
- **Validation of Constraints**: Are you ensuring that land-use constraints do not overly restrict feasible solutions? Have you tested for infeasibility or overly conservative constraints?
- **Sensitivity Analysis**: Have you tried varying `CO2price`, `PercRewetting`, or `ghgTargetLULUCF` to see how sensitive your model is to these factors?
- **Optimization Strategy**: Since this is a long-term (2020-2050) model, have you considered using a dynamic programming approach instead of LP?
- **Parallel Computation**: If the dataset is large, you might benefit from using parallel computing options in GAMS.


from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor (or another ML model)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Create SHAP explainer
explainer = shap.Explainer(model, X_train)
shap_values = explainer(X_test)

# Summary plot to show feature importance
shap.summary_plot(shap_values, X_test)
"""


#############################################
#############################################



