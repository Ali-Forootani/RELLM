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
gams_system_dir = setting_directory(0)  # Example path for Windows


##############################################
##############################################
##############################################
##############################################

"""
Input data
"""

"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---- Load datasets from CSV ----
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

# ---- Rename columns to ensure consistency ----
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

# ---- Set global plot style ----
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "figure.dpi": 600,
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
    # "text.usetex": True,  # Uncomment for LaTeX rendering (if LaTeX is installed)
})

# ---- LaTeX-style label and title mapping ----
pretty_labels = {
    "costMargFMs": r"$\mathrm{Marginal\ Cost\ of\ FMs}$",
    "costInvFMs": r"$\mathrm{Investment\ Cost\ of\ FMs}$",
    "costInvLevelFMs": r"$\mathrm{Investment\ Level\ Cost\ of\ FMs}$",
    "ghgFMs": r"$\mathrm{Green House Gases (GHG) \ Removals\ by\ FMs}$",
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

# Use this dict to map keys to pretty LaTeX titles for time series plots
pretty_titles = {
    "CO2price": r"$\mathrm{CO_2\ Price\ Evolution\ Over\ Time}$",
    "ghgTargetLULUCF": r"$\mathrm{GHG\ Target\ LULUCF\ Evolution\ Over\ Time}$",
    "costMargFMs": r"$\mathrm{Marginal\ Cost\ of\ FMs\ Evolution}$",
    "costInvFMs": r"$\mathrm{Investment\ Cost\ of\ FMs\ Evolution}$",
    "costInvLevelFMs": r"$\mathrm{Investment\ Level\ Cost\ of\ FMs\ Evolution}$",
    "ghgFMs": r"$\mathrm{GHG\ Removals\ by\ FMs\ Evolution}$",
    "FMsgrowth": r"$\mathrm{Forest\ Management\ Growth\ Evolution}$",
    # ... add more as needed ...
}

# ---- Special bar plots for Initial Beech/Grass Area ----
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

# ---- Time-series line plots (with LaTeX titles!) ----
for key, df in datasets.items():
    if key in ["BeechArea0", "GrassArea0"]:
        continue  # Already handled

    plt.figure(figsize=(12, 8))
    y_col = df.columns[-1]
    ylabel = pretty_labels.get(y_col, y_col)
    title = pretty_titles.get(key, pretty_labels.get(key, key))

    # Multi-region/multi-tech handling
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
    plt.title(title, fontsize=20, pad=15)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()


"""




#############################################################



import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker


# ---- Create output folder for plots ----
output_dir = "plots"
os.makedirs(output_dir, exist_ok=True)

# ---- Load datasets from CSV ----
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

# ---- Rename columns to ensure consistency ----
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

# ---- Set global plot style ----
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "figure.dpi": 600,
    "axes.titlesize": 20,
    "axes.labelsize": 22,
    "xtick.labelsize": 18,
    "ytick.labelsize": 18,
    "legend.fontsize": 14,
    "legend.title_fontsize": 16,
    "lines.linewidth": 3,
    "lines.markersize": 10,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "font.family": "sans-serif",
    "font.sans-serif": "DejaVu Sans",
    # "text.usetex": True,  # Uncomment for LaTeX rendering (if LaTeX is installed)
})

pretty_labels = {
    "costMargFMs": r"$\mathrm{Marginal\ Cost\ of\ Forest\ Management\ (FMs)}$",
    "costInvFMs": r"$\mathrm{Investment\ Cost\ of\ Forest\ Management\ (FMs)}$",
    "costInvLevelFMs": r"$\mathrm{Investment\ Level\ Cost\ of\ Forest\ Management\ (FMs)}$",
    "ghgFMs": r"$\mathrm{Green House Gases\ (GHG) \ Removals\ by\ Forest\ Management\ (FMs)}$",
    "FMsgrowth": r"$\mathrm{Forest\ Management\ (FM)\ Growth}$",
    "GHG_Removal": r"$\mathrm{GHG\ Removal\ (MtCO_2)}$",
    "InvestmentCost": r"$\mathrm{Investment\ Cost\ (€)}$",
    "InvestmentLevelCost": r"$\mathrm{Investment\ Level\ Cost\ (€)}$",
    "ForestManagementGrowth": r"$\mathrm{Forest\ Managements\ (FMs)\ Growth\ (ha)}$",
    "Cost": r"$\mathrm{Marginal\ Cost\ (€ / tCO_2)}$",
    "GHG_Target_LULUCF": r"$\mathrm{Green\ House\ Gas\ (GHG)\ Target\ LULUCF\ (MtCO_2)}$",
    "CO2_Price": r"$\mathrm{CO_2\ Price\ (€ / tCO_2)}$",
    "InitialBeechArea": r"$\mathrm{Initial\ Beech\ Area\ (ha)}$",
    "InitialGrassArea": r"$\mathrm{Initial\ Grass\ Area\ (ha)}$"
}

pretty_titles = {
    "CO2price": r"$\mathrm{CO_2\ Price\ Evolution\ Over\ Time}$",
    "ghgTargetLULUCF": r"$\mathrm{GHG\ Target\ LULUCF\ Evolution\ Over\ Time}$",
    "costMargFMs": r"$\mathrm{Marginal\ Cost\ of\ Forest Managements\ (FMs)\ Evolution}$",
    "costInvFMs": r"$\mathrm{Investment\ Cost\ of\ Forest Managements\ (FMs)\ Evolution}$",
    "costInvLevelFMs": r"$\mathrm{Investment\ Level\ Cost\ of\ Forest\ Management\ (FMs)\ Evolution}$",
    "ghgFMs": r"$\mathrm{Green\ House\ Gas\ (GHG)\ Removals\ by\ FMs\ Evolution}$",
    "FMsgrowth": r"$\mathrm{Forest\ Management (FM)\ Growth\ Evolution}$",
    # ... add more as needed ...
}

# ---- Special bar plots for Initial Beech/Grass Area ----
if "BeechArea0" in datasets and "GrassArea0" in datasets:
    beech_df = datasets["BeechArea0"].sort_values(by="InitialBeechArea", ascending=True)
    grass_df = datasets["GrassArea0"].sort_values(by="InitialGrassArea", ascending=True)

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 7), sharey=True)

    axes[0].barh(beech_df["Region"], beech_df["InitialBeechArea"], color="forestgreen")
    axes[0].set_xlabel(pretty_labels["InitialBeechArea"])
    axes[0].set_ylabel("Region")
    axes[0].set_title(r"$\mathrm{Initial\ Beech\ Area\ by\ Region\ (2020)}$")

    axes[1].barh(grass_df["Region"], grass_df["InitialGrassArea"], color="goldenrod")
    axes[1].set_xlabel(pretty_labels["InitialGrassArea"])
    axes[1].set_title(r"$\mathrm{Initial\ Grass\ Area\ by\ Region\ (2020)}$")
    
    
    # Set font size for ticks
    for ax in axes:
        ax.tick_params(axis='x', labelsize=15)
        ax.tick_params(axis='y', labelsize=15)

        # Scientific notation for x-axis
        formatter = mticker.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-2, 2))  # Scientific if < 0.01 or > 100
        ax.xaxis.set_major_formatter(formatter)

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "InitialBeechArea_GrassArea.png"), dpi=600, bbox_inches="tight")
    fig.savefig(os.path.join(output_dir, "InitialBeechArea_GrassArea.pdf"), dpi=600, bbox_inches="tight")
    plt.close(fig)  # Close so next plots don't overlap

# ---- Time-series line plots (with LaTeX titles!) ----
for key, df in datasets.items():
    if key in ["BeechArea0", "GrassArea0"]:
        continue  # Already handled

    plt.figure(figsize=(12, 9))
    y_col = df.columns[-1]
    ylabel = pretty_labels.get(y_col, y_col)
    title = pretty_titles.get(key, pretty_labels.get(key, key))

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

    plt.xlabel(r"$\mathrm{Year}$", fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.title(title, fontsize=20, pad=15)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # ---- Save plot as both PNG and PDF ----
    png_path = os.path.join(output_dir, f"{key}.png")
    pdf_path = os.path.join(output_dir, f"{key}.pdf")
    plt.savefig(png_path, dpi=600, bbox_inches="tight")
    plt.savefig(pdf_path, dpi=600, bbox_inches="tight")
    plt.close()  # Do not display, just save





import matplotlib.ticker as mticker

if "BeechArea0" in datasets and "GrassArea0" in datasets:
    beech_df = datasets["BeechArea0"].sort_values(by="InitialBeechArea", ascending=True)
    grass_df = datasets["GrassArea0"].sort_values(by="InitialGrassArea", ascending=True)

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 7), sharey=True)

    axes[0].barh(beech_df["Region"], beech_df["InitialBeechArea"], color="forestgreen")
    axes[0].set_xlabel(pretty_labels["InitialBeechArea"])
    axes[0].set_ylabel("Region")
    axes[0].set_title(r"$\mathrm{Initial\ Beech\ Area\ by\ Region\ (2020)}$")

    axes[1].barh(grass_df["Region"], grass_df["InitialGrassArea"], color="goldenrod")
    axes[1].set_xlabel(pretty_labels["InitialGrassArea"])
    axes[1].set_title(r"$\mathrm{Initial\ Grass\ Area\ by\ Region\ (2020)}$")

    # Set font size for ticks
    for ax in axes:
        ax.tick_params(axis='x', labelsize=15)
        ax.tick_params(axis='y', labelsize=15)

        # Scientific notation for x-axis
        formatter = mticker.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-2, 2))  # Scientific if < 0.01 or > 100
        ax.xaxis.set_major_formatter(formatter)

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "InitialBeechArea_GrassArea.png"), dpi=600, bbox_inches="tight")
    fig.savefig(os.path.join(output_dir, "InitialBeechArea_GrassArea.pdf"), dpi=600, bbox_inches="tight")
    plt.close(fig)










############################################################
############################################################
############################################################
############################################################
############################################################
############################################################

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

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data (same as before)
df_capFMs = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"capFMs_results.csv")
df_capAgri = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"capAgri_results.csv")
df_ghgAbateFMs = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"ghgAbateFMs_results.csv")
df_ghgAbateAgri = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"ghgAbateAgri_results.csv")
df_total_cost_annual = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"total_cost_annual.csv")
df_costAnnualFMs = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"costAnnualFMs_results.csv")
df_costAnnualAgri = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"costAnnualAgri_results.csv")
df_total_ghg_annual = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"total_ghg_annual.csv")
df_FMsGrassArea = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"FMsGrassArea.csv")
df_FMsBeechArea = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"FMsBeechArea.csv")
df_purCO2LULUCF = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"purCO2LULUCF.csv")

df_costTechFMs = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" + "costTechFMs.csv")
df_costTechAgri = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" + "costTechAgri.csv")
df_CO2gapRewt = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" + "CO2gapRewt.csv")
df_total_cost = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" + "total_cost.csv")
df_total_ghg = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" + "total_ghg.csv")


# Set consistent style
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "figure.dpi": 600,
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


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load extracted CSV data
df_capFMs = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"capFMs_results.csv")
df_capAgri = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"capAgri_results.csv")
df_ghgAbateFMs = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"ghgAbateFMs_results.csv")
df_ghgAbateAgri = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"ghgAbateAgri_results.csv")
df_total_cost_annual = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"total_cost_annual.csv")
df_costAnnualFMs = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"costAnnualFMs_results.csv")
df_costAnnualAgri = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"costAnnualAgri_results.csv")
df_total_ghg_annual = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"total_ghg_annual.csv")
df_FMsGrassArea = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"FMsGrassArea.csv")
df_FMsBeechArea = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"FMsBeechArea.csv")
df_purCO2LULUCF = pd.read_csv(gams_system_dir + "/data/Results_base_scenario/" +"purCO2LULUCF.csv")

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


