#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 13:27:51 2025

@author: forootan
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def visualize_gdx_outputs2(output_dir: str, sub_dir: str):
    """
    Loads extracted GDX CSV data and generates plots based on available files.
    
    Parameters:
    - output_dir (str): Root directory (e.g., base output folder)
    - sub_dir (str): Subdirectory containing saved .csv files
    """
    sns.set_style("whitegrid")
    data_path = os.path.join(output_dir, sub_dir)

    def load_csv(name):
        path = os.path.join(data_path, name)
        if os.path.exists(path):
            return pd.read_csv(path)
        else:
            print(f"⚠️ Missing file: {name}")
            return None

    # Load files
    df_capFMs = load_csv("capFMs_results.csv")
    df_capAgri = load_csv("capAgri_results.csv")
    df_ghgAbateFMs = load_csv("ghgAbateFMs_results.csv")
    df_ghgAbateAgri = load_csv("ghgAbateAgri_results.csv")
    df_total_cost_annual = load_csv("total_cost_annual.csv")
    df_costAnnualFMs = load_csv("costAnnualFMs_results.csv")
    df_costAnnualAgri = load_csv("costAnnualAgri_results.csv")
    df_total_ghg_annual = load_csv("total_ghg_annual.csv")
    df_FMsGrassArea = load_csv("FMsGrassArea.csv")
    df_FMsBeechArea = load_csv("FMsBeechArea.csv")
    df_purCO2LULUCF = load_csv("purCO2LULUCF.csv")
    df_costTechFMs = load_csv("costTechFMs.csv")
    df_costTechAgri = load_csv("costTechAgri.csv")

    # ----- PLOT 1: Total GHG Reduction Over Time -----
    if df_total_ghg_annual is not None:
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df_total_ghg_annual, x="year", y="Total_ghgAnnual", marker="o")
        plt.title("Total GHG Reduction Over Time")
        plt.xlabel("Year")
        plt.ylabel("Total GHG Reduction (tCO₂eq)")
        plt.grid(True)
        plt.show()

    # ----- PLOT 2: Annual Costs -----
    if df_costAnnualFMs is not None and df_costAnnualAgri is not None:
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df_costAnnualFMs, x="year", y="costAnnualFMs", marker="o", label="FMs")
        sns.lineplot(data=df_costAnnualAgri, x="year", y="costAnnualAgri", marker="s", linestyle="--", label="Agri")
        plt.title("Annual Cost of FMs and Agriculture")
        plt.xlabel("Year")
        plt.ylabel("Cost (€)")
        plt.legend()
        plt.grid(True)
        plt.show()

    # ----- PLOT 3: PurCO2 LULUCF -----
    if df_purCO2LULUCF is not None:
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df_purCO2LULUCF, x="year", y="purCO2LULUCF", marker="D")
        plt.title("CO₂ Purchased from LULUCF Over Time")
        plt.xlabel("Year")
        plt.ylabel("CO₂ Purchase (tCO₂eq)")
        plt.grid(True)
        plt.show()

    # ----- PLOT 4: Land Allocation by Region -----
    if df_capFMs is not None:
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df_capFMs, x="year", y="capFMs", hue="r")
        plt.title("Forest Management Land Allocation by Region")
        plt.xlabel("Year")
        plt.ylabel("Allocated Land (ha)")
        plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

    # ----- PLOT 5: GHG Abatement by Region -----
    if df_ghgAbateFMs is not None:
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df_ghgAbateFMs, x="year", y="ghgAbateTechFMs", hue="r")
        plt.title("GHG Abatement by FM Tech and Region")
        plt.xlabel("Year")
        plt.ylabel("GHG Abatement (tCO₂eq)")
        plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

    # ----- PLOT 6: Agriculture Implementation -----
    if df_capAgri is not None:
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df_capAgri, x="year", y="capAgri", hue="r", marker="o")
        plt.title("Agricultural Land Allocation Over Time by Region")
        plt.xlabel("Year")
        plt.ylabel("Agri Area (ha)")
        plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True)
        plt.show()

    # ----- PLOT 7: FM Cost by Tech -----
    if df_costTechFMs is not None:
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df_costTechFMs, x="year", y="costTechFMs", hue="techFMs", marker="o")
        plt.title("Forest Management Cost by Technology")
        plt.xlabel("Year")
        plt.ylabel("Cost (€)")
        plt.legend(title="Technology", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True)
        plt.show()

        # Stacked area by region
        df_cost_region = df_costTechFMs.groupby(["year", "r"], as_index=False)["costTechFMs"].sum()
        df_cost_stack = df_cost_region.pivot(index="year", columns="r", values="costTechFMs").fillna(0)

        fig, ax = plt.subplots(figsize=(12, 6))
        df_cost_stack.plot.area(ax=ax, colormap="tab20", linewidth=0)
        ax.set_title("Forest Management Cost by Region")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total FM Cost (€)")
        ax.grid(True)
        ax.legend(title="Region", bbox_to_anchor=(0.5, -0.25), loc="upper center", ncol=6)
        plt.tight_layout()
        plt.show()

    # ----- PLOT 8: Agri Cost by Tech -----
    if df_costTechAgri is not None:
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df_costTechAgri, x="year", y="costTechAgri", hue="techAgri", marker="o")
        plt.title("Agriculture Cost by Technology")
        plt.xlabel("Year")
        plt.ylabel("Cost (€)")
        plt.legend(title="Technology", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True)
        plt.show()

        df_agri_region = df_costTechAgri.groupby(["year", "r"], as_index=False)["costTechAgri"].sum()
        df_agri_stack = df_agri_region.pivot(index="year", columns="r", values="costTechAgri").fillna(0)

        fig, ax = plt.subplots(figsize=(12, 6))
        df_agri_stack.plot.area(ax=ax, colormap="tab20", linewidth=0)
        ax.set_title("Agriculture Cost by Region")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Agri Cost (€)")
        ax.grid(True)
        ax.legend(title="Region", bbox_to_anchor=(0.5, -0.25), loc="upper center", ncol=6)
        plt.tight_layout()
        plt.show()

    # ----- PLOT 9: GHG Abatement by Region/Tech Over Time -----
    if df_ghgAbateFMs is not None:
        plt.figure(figsize=(12, 6))
        regions = df_ghgAbateFMs["r"].unique()
        colors = plt.cm.viridis(np.linspace(0, 1, len(regions)))

        for i, region in enumerate(regions):
            region_data = df_ghgAbateFMs[df_ghgAbateFMs["r"] == region]
            plt.plot(region_data["year"], region_data["ghgAbateTechFMs"],
                     label=f"Region {region}", color=colors[i], marker="o")

        plt.title("GHG Abatement by FM Tech and Region")
        plt.xlabel("Year")
        plt.ylabel("GHG Abatement (tCO₂eq)")
        plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True)
        plt.show()

    print("\n✅ Visualization complete.")
    
    
    
#######################

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def visualize_gdx_outputs(output_dir: str, sub_dir: str):
    """
    Loads extracted GDX CSV data and generates plots based on available files.
    
    Parameters:
    - output_dir (str): Root directory (e.g., base output folder)
    - sub_dir (str): Subdirectory containing saved .csv files
    """
    sns.set_style("whitegrid")
    data_path = os.path.join(output_dir, sub_dir)

    def load_csv(name):
        path = os.path.join(data_path, name)
        if os.path.exists(path):
            return pd.read_csv(path)
        else:
            print(f"⚠️ Missing file: {name}")
            return None

    # Load files
    df_capFMs = load_csv("capFMs_results.csv")
    df_capAgri = load_csv("capAgri_results.csv")
    df_ghgAbateFMs = load_csv("ghgAbateFMs_results.csv")
    df_ghgAbateAgri = load_csv("ghgAbateAgri_results.csv")
    df_total_cost_annual = load_csv("total_cost_annual.csv")
    df_costAnnualFMs = load_csv("costAnnualFMs_results.csv")
    df_costAnnualAgri = load_csv("costAnnualAgri_results.csv")
    df_total_ghg_annual = load_csv("total_ghg_annual.csv")
    df_FMsGrassArea = load_csv("FMsGrassArea.csv")
    df_FMsBeechArea = load_csv("FMsBeechArea.csv")
    df_purCO2LULUCF = load_csv("purCO2LULUCF.csv")
    df_costTechFMs = load_csv("costTechFMs.csv")
    df_costTechAgri = load_csv("costTechAgri.csv")

    # ----- PLOT 1: Total GHG Reduction Over Time -----
    if df_total_ghg_annual is not None:
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df_total_ghg_annual, x="year", y="Total_ghgAnnual", marker="o")
        plt.title("Total GHG Reduction Over Time")
        plt.xlabel("Year")
        plt.ylabel("Total GHG Reduction (tCO₂eq)")
        plt.grid(True)
        plt.show()

    # ----- PLOT 2: Annual Costs -----
    if df_costAnnualFMs is not None and df_costAnnualAgri is not None:
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df_costAnnualFMs, x="year", y="costAnnualFMs", marker="o", label="FMs")
        sns.lineplot(data=df_costAnnualAgri, x="year", y="costAnnualAgri", marker="s", linestyle="--", label="Agri")
        plt.title("Annual Cost of FMs and Agriculture")
        plt.xlabel("Year")
        plt.ylabel("Cost (€)")
        plt.legend()
        plt.grid(True)
        plt.show()

    # ----- PLOT 3: PurCO2 LULUCF -----
    if df_purCO2LULUCF is not None:
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df_purCO2LULUCF, x="year", y="purCO2LULUCF", marker="D")
        plt.title("CO₂ Purchased from LULUCF Over Time")
        plt.xlabel("Year")
        plt.ylabel("CO₂ Purchase (tCO₂eq)")
        plt.grid(True)
        plt.show()

    # ----- PLOT 4: Land Allocation by Region -----
    if df_capFMs is not None:
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df_capFMs, x="year", y="capFMs", hue="r")
        plt.title("Forest Management Land Allocation by Region")
        plt.xlabel("Year")
        plt.ylabel("Allocated Land (ha)")
        plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

    # ----- PLOT 5: GHG Abatement by Region -----
    if df_ghgAbateFMs is not None:
        plt.figure(figsize=(12, 6))
        sns.barplot(data=df_ghgAbateFMs, x="year", y="ghgAbateTechFMs", hue="r")
        plt.title("GHG Abatement by FM Tech and Region")
        plt.xlabel("Year")
        plt.ylabel("GHG Abatement (tCO₂eq)")
        plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

        # ----- NEW PLOT: GHG Abatement (stacked area by region) -----
        df_ghg_region = df_ghgAbateFMs.groupby(["year", "r"], as_index=False)["ghgAbateTechFMs"].sum()
        df_ghg_stack_region = df_ghg_region.pivot(index="year", columns="r", values="ghgAbateTechFMs").fillna(0)

        fig, ax = plt.subplots(figsize=(12, 6))
        df_ghg_stack_region.plot.area(ax=ax, colormap="tab20", linewidth=0)

        ax.set_xlabel(r"$\mathrm{Year}$", fontsize=14)
        ax.set_ylabel(r"$\mathrm{GHG\ Abatement\ (tCO_2eq)}$", fontsize=14)
        ax.set_title(r"$\mathrm{GHG\ Abatement\ by\ Region}$", fontsize=18)
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles=handles, labels=labels, title=r"$\mathrm{Region}$",
                  bbox_to_anchor=(0.5, -0.25), loc="upper center", ncol=6,
                  frameon=True, fontsize=10, title_fontsize=12)

        plt.tight_layout()
        plt.show()

    # ----- PLOT 6: Agriculture Implementation -----
    if df_capAgri is not None:
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df_capAgri, x="year", y="capAgri", hue="r", marker="o")
        plt.title("Agricultural Land Allocation Over Time by Region")
        plt.xlabel("Year")
        plt.ylabel("Agri Area (ha)")
        plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True)
        plt.show()

    # ----- PLOT 7: FM Cost by Tech -----
    if df_costTechFMs is not None:
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df_costTechFMs, x="year", y="costTechFMs", hue="techFMs", marker="o")
        plt.title("Forest Management Cost by Technology")
        plt.xlabel("Year")
        plt.ylabel("Cost (€)")
        plt.legend(title="Technology", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True)
        plt.show()

        # Stacked area by region
        df_cost_region = df_costTechFMs.groupby(["year", "r"], as_index=False)["costTechFMs"].sum()
        df_cost_stack = df_cost_region.pivot(index="year", columns="r", values="costTechFMs").fillna(0)

        fig, ax = plt.subplots(figsize=(12, 6))
        df_cost_stack.plot.area(ax=ax, colormap="tab20", linewidth=0)
        ax.set_title("Forest Management Cost by Region")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total FM Cost (€)")
        ax.grid(True)
        ax.legend(title="Region", bbox_to_anchor=(0.5, -0.25), loc="upper center", ncol=6)
        plt.tight_layout()
        plt.show()

    # ----- PLOT 8: Agri Cost by Tech -----
    if df_costTechAgri is not None:
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=df_costTechAgri, x="year", y="costTechAgri", hue="techAgri", marker="o")
        plt.title("Agriculture Cost by Technology")
        plt.xlabel("Year")
        plt.ylabel("Cost (€)")
        plt.legend(title="Technology", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True)
        plt.show()

        df_agri_region = df_costTechAgri.groupby(["year", "r"], as_index=False)["costTechAgri"].sum()
        df_agri_stack = df_agri_region.pivot(index="year", columns="r", values="costTechAgri").fillna(0)

        fig, ax = plt.subplots(figsize=(12, 6))
        df_agri_stack.plot.area(ax=ax, colormap="tab20", linewidth=0)
        ax.set_title("Agriculture Cost by Region")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Agri Cost (€)")
        ax.grid(True)
        ax.legend(title="Region", bbox_to_anchor=(0.5, -0.25), loc="upper center", ncol=6)
        plt.tight_layout()
        plt.show()

    # ----- PLOT 9: GHG Abatement Time Series per Region -----
    if df_ghgAbateFMs is not None:
        plt.figure(figsize=(12, 6))
        regions = df_ghgAbateFMs["r"].unique()
        colors = plt.cm.viridis(np.linspace(0, 1, len(regions)))

        for i, region in enumerate(regions):
            region_data = df_ghgAbateFMs[df_ghgAbateFMs["r"] == region]
            plt.plot(region_data["year"], region_data["ghgAbateTechFMs"],
                     label=f"Region {region}", color=colors[i], marker="o")

        plt.title("GHG Abatement by Forest Management Tech and Region")
        plt.xlabel("Year")
        plt.ylabel("GHG Abatement (tCO₂eq)")
        plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True)
        plt.show()
        
        
        
    # ----- PLOT 10: GHG Abatement Aggregated by Region-Year (Stacked Area Plot) -----
    if df_ghgAbateFMs is not None:
        # Aggregate GHG abatement per region-year
        df_ghg_region = df_ghgAbateFMs.groupby(["year", "r"], as_index=False)["ghgAbateTechFMs"].sum()
        df_ghg_stack_region = df_ghg_region.pivot(index="year", columns="r", values="ghgAbateTechFMs").fillna(0)

        # Plot stacked area chart
        fig, ax = plt.subplots(figsize=(12, 6))
        df_ghg_stack_region.plot.area(ax=ax, colormap="tab20", linewidth=0)

        ax.set_xlabel(r"$\mathrm{Year}$", fontsize=14)
        ax.set_ylabel(r"$\mathrm{GHG\ Abatement\ (tCO_2eq)}$", fontsize=14)
        ax.set_title(r"$\mathrm{GHG\ Abatement\ by\ Region}$", fontsize=18)
        ax.grid(axis="y", linestyle="--", alpha=0.5)

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles=handles, labels=labels, title=r"$\mathrm{Region}$",
                  bbox_to_anchor=(0.5, -0.25), loc="upper center", ncol=6,
                  frameon=True, fontsize=10, title_fontsize=12)

        plt.tight_layout()
        plt.show()
    
        
    

    print("\n✅ Visualization complete.")
    
    
    
    
    
    
    
    
    

