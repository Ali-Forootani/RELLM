#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 18 16:55:39 2025

@author: forootan
"""


import gdxpds
import pandas as pd
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


from Temporary_backups.feature_construction_fm import compute_global_trend, compute_trend



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
gdx_file_base = gams_system_dir + "/scenarios_neg_emi/CarbonPrice/Data/test_Ali.gdx"  # Change this to the actual path of your GDX file


"""
gdx_co2 = gams_system_dir + "/scenarios_neg_emi/CarbonPrice/Data/ali_carbonPrice_2times.gdx"
gdx_co2_3 = gams_system_dir + "/scenarios_neg_emi/CarbonPrice/Data/ali_carbonPrice_3times.gdx"
gdx_co2_05 = gams_system_dir + "/scenarios_neg_emi/CarbonPrice/Data/ali_carbonPrice_halftimes.gdx"
"""


gdx_base_ali = gams_system_dir + "/test_Ali.gdx"



##########################
##########################

gdx_data = gdxpds.to_dataframes(gdx_file_base)



"""
gdx_co2_data = gdxpds.to_dataframes(gdx_co2)
gdx_co2_3_data = gdxpds.to_dataframes(gdx_co2_3)
gdx_co2_05_data = gdxpds.to_dataframes(gdx_co2_05)
"""


#gdx_base_data = gdxpds.to_dataframes(gdx_base_ali)

#gdx_base_data.keys() 



###########################
###########################
###########################


from Temporary_backups.loading_saving_parms_from_gdx_csv import load_and_save_selected_symbols


gdx_dir = os.path.expanduser("~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/dataset_scenarios")
save_dir = os.path.expanduser("~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/csv_outputs")
target_symbols = ["CO2price", "FMsgrowth", "BeechArea0", "ghgTargetLULUCF"]

load_and_save_selected_symbols(gdx_dir, target_symbols, save_path=save_dir)




###########################
###########################


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



#################################


# Save to CSV for further analysis (optional)
costMargFMs_df.to_csv("costMargFMs.csv", index=False)
costInvFMs_df.to_csv("costInvFMs.csv", index=False)

costInvLevelFMs_df.to_csv("costInvLevelFMs.csv", index=False)

ghgFMs_df.to_csv("ghgFMs.csv", index=False)

FMsgrowth_df.to_csv("FMsgrowth.csv", index=False)

BeechArea0_df.to_csv("BeechArea0.csv", index=False)

GrassArea0_df.to_csv("GrassArea0.csv", index=False)
ghgTargetLULUCF_df.to_csv("ghgTargetLULUCF.csv", index=False)
#ghgTargetLULUCF_df_08_08_08.to_csv("ghgTargetLULUCF_08_08_08.csv", index=False)


CO2price_df.to_csv("CO2price.csv", index=False)




CO2price_df = CO2price_df.rename(columns={"*": "year", "Value": "CO2_price"})





#############################################################
#############################################################
#############################################################
#############################################################



from Temporary_backups.utiles import load_and_rename_csvs, get_dynamic_rename_mapping



csv_directory = os.path.expanduser("~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/csv_outputs")

datasets = load_and_rename_csvs(csv_directory)


################################################
################################################



# Apply dynamic renaming and convert "Year" to numeric
for key, df in datasets.items():
    rename_dict = get_dynamic_rename_mapping(key)
    if rename_dict:
        df.rename(columns=rename_dict, inplace=True)
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors='coerce')






################################################
################################################
"""
# Apply renaming and ensure Year is numeric
for key, df in datasets.items():
    df.rename(columns=rename_columns[key], inplace=True)
    df["Year"] = pd.to_numeric(df["Year"], errors='coerce')
"""


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


############################################
############################################
############################################
############################################
############################################
############################################



import pandas as pd
from scipy.stats import linregress
from sklearn.preprocessing import MinMaxScaler

# Load datasets
costMargFMs = datasets["costMargFMs"]
costInvFMs = datasets["costInvFMs"]
costInvLevelFMs = datasets["costInvLevelFMs"]
ghgFMs = datasets["ghgFMs"]
FMsgrowth = datasets["FMsgrowth"]

FMsgrowth_08_08_08 = datasets["FMsgrowth_df_sce_08_08_08"]
BeechArea0_08_08_08 = datasets["BeechArea0_df_sce_08_08_08"]
CO2price_08_08_08 = datasets["CO2price_df_sce_08_08_08"]



FMsgrowth_12_12_08 = datasets["FMsgrowth_df_sce_12_12_08"]
BeechArea0_12_12_08 = datasets["BeechArea0_df_sce_12_12_08"]
CO2price_12_12_08 = datasets["CO2price_df_sce_12_12_08"]



FMsgrowth_08_10_08 = datasets["FMsgrowth_df_sce_08_10_08"]
BeechArea0_08_10_08 = datasets["BeechArea0_df_sce_08_10_08"]
CO2price_08_10_08 = datasets["CO2price_df_sce_08_10_08"]



FMsgrowth_08_10_10 = datasets["FMsgrowth_df_sce_08_10_10"]
BeechArea0_08_10_10 = datasets["BeechArea0_df_sce_08_10_10"]
CO2price_08_10_10 = datasets["CO2price_df_sce_08_10_10"]







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




final_feature_array_08_08_08 = final_feature_array.copy()
final_feature_array_12_12_08 = final_feature_array.copy()


final_feature_array_08_10_08 = final_feature_array.copy()
final_feature_array_08_10_10 = final_feature_array.copy()




######################### 
#########################
#########################



"""
CO_2 price 
GHG Target LULUCF
"""

ghgTargetLULUCF = datasets["ghgTargetLULUCF"]
CO2price = datasets["CO2price"]



ghgTargetLULUCF_08_08_08 = datasets["ghgTargetLULUCF_df_sce_08_08_08"] 

ghgTargetLULUCF_12_12_08 = datasets["ghgTargetLULUCF_df_sce_12_12_08"] 


ghgTargetLULUCF_08_10_08 = datasets["ghgTargetLULUCF_df_sce_08_10_08"] 

ghgTargetLULUCF_08_10_10 = datasets["ghgTargetLULUCF_df_sce_08_10_10"] 



from scipy.stats import linregress


# Compute CO2 and GHG trend features
co2_features = compute_global_trend(CO2price, "Year", "CO2_Price", "CO2")


co2_08_08_08_features = compute_global_trend(CO2price_08_08_08, "Year", "CO2_Price", "CO2")
co2_12_12_08_features = compute_global_trend(CO2price_12_12_08, "Year", "CO2_Price", "CO2")


co2_08_10_08_features = compute_global_trend(CO2price_08_10_08, "Year", "CO2_Price", "CO2")
co2_08_10_10_features = compute_global_trend(CO2price_08_10_10, "Year", "CO2_Price", "CO2")



ghg_target_features = compute_global_trend(ghgTargetLULUCF, "Year", "GHG_Target_LULUCF", "GHGTarget")


ghgTargetLULUCF_08_08_08["Year"] = pd.to_numeric(ghgTargetLULUCF_08_08_08["Year"], errors="coerce")
ghgTargetLULUCF_08_08_08["GHG_Target_LULUCF"] = pd.to_numeric(ghgTargetLULUCF_08_08_08["GHG_Target_LULUCF"], errors="coerce")
ghg_target_features_08_08_08 = compute_global_trend(ghgTargetLULUCF_08_08_08, "Year", "GHG_Target_LULUCF", "GHGTarget")



ghgTargetLULUCF_12_12_08["Year"] = pd.to_numeric(ghgTargetLULUCF_12_12_08["Year"], errors="coerce")
ghgTargetLULUCF_12_12_08["GHG_Target_LULUCF"] = pd.to_numeric(ghgTargetLULUCF_12_12_08["GHG_Target_LULUCF"], errors="coerce")
ghg_target_features_12_12_08 = compute_global_trend(ghgTargetLULUCF_12_12_08, "Year", "GHG_Target_LULUCF", "GHGTarget")




ghgTargetLULUCF_08_10_08["Year"] = pd.to_numeric(ghgTargetLULUCF_08_10_08["Year"], errors="coerce")
ghgTargetLULUCF_08_10_08["GHG_Target_LULUCF"] = pd.to_numeric(ghgTargetLULUCF_08_10_08["GHG_Target_LULUCF"], errors="coerce")
ghg_target_features_08_10_08 = compute_global_trend(ghgTargetLULUCF_08_10_08, "Year", "GHG_Target_LULUCF", "GHGTarget")



ghgTargetLULUCF_08_10_10["Year"] = pd.to_numeric(ghgTargetLULUCF_08_10_10["Year"], errors="coerce")
ghgTargetLULUCF_08_10_10["GHG_Target_LULUCF"] = pd.to_numeric(ghgTargetLULUCF_08_10_10["GHG_Target_LULUCF"], errors="coerce")
ghg_target_features_08_10_10 = compute_global_trend(ghgTargetLULUCF_08_10_10, "Year", "GHG_Target_LULUCF", "GHGTarget")






# Broadcast these to all regions in the final_feature_array
unique_regions = final_feature_array["Region"].unique()


broadcast_df = pd.DataFrame(unique_regions, columns=["Region"])



broadcast_df_08_08_08 = pd.DataFrame(unique_regions, columns=["Region"])
broadcast_df_12_12_08 = pd.DataFrame(unique_regions, columns=["Region"])


broadcast_df_08_10_08 = pd.DataFrame(unique_regions, columns=["Region"])
broadcast_df_08_10_10 = pd.DataFrame(unique_regions, columns=["Region"])



# Cross join with co2 and ghg features (same values for all regions)
broadcast_df = broadcast_df.merge(co2_features, how="cross")
broadcast_df = broadcast_df.merge(ghg_target_features, how="cross")




broadcast_df_08_08_08 = broadcast_df_08_08_08.merge(co2_08_08_08_features, how="cross")
broadcast_df_08_08_08 = broadcast_df_08_08_08.merge(ghg_target_features_08_08_08, how="cross")



broadcast_df_12_12_08 = broadcast_df_12_12_08.merge(co2_12_12_08_features, how="cross")
broadcast_df_12_12_08 = broadcast_df_12_12_08.merge(ghg_target_features_12_12_08, how="cross")



broadcast_df_08_10_08 = broadcast_df_08_10_08.merge(co2_08_10_08_features, how="cross")
broadcast_df_08_10_08 = broadcast_df_08_10_08.merge(ghg_target_features_08_10_08, how="cross")


broadcast_df_08_10_10 = broadcast_df_08_10_10.merge(co2_08_10_10_features, how="cross")
broadcast_df_08_10_10 = broadcast_df_08_10_10.merge(ghg_target_features_08_10_10, how="cross")






# Merge with final_feature_array
final_feature_array = final_feature_array.merge(broadcast_df, on="Region", how="left")



# Merge with final_feature_array 08_08_08
final_feature_array_08_08_08 = final_feature_array_08_08_08.merge(broadcast_df_08_08_08, on="Region", how="left")

# Merge with final_feature_array 12_12_08
final_feature_array_12_12_08 = final_feature_array_12_12_08.merge(broadcast_df_12_12_08, on="Region", how="left")




# Merge with final_feature_array 08 10 08
final_feature_array_08_10_08 = final_feature_array_08_10_08.merge(broadcast_df_08_10_08, on="Region", how="left")

# Merge with final_feature_array _08 10 10
final_feature_array_08_10_10 = final_feature_array_08_10_10.merge(broadcast_df_08_10_10, on="Region", how="left")


#####################################
#####################################


import pandas as pd

# Load additional datasets
BeechArea0 = datasets["BeechArea0"]
GrassArea0 = datasets["GrassArea0"]

BeechArea0_08_08_08 = datasets["BeechArea0_df_sce_08_08_08"]
GrassArea0_08_08_08 = datasets["GrassArea0"]

BeechArea0_12_12_08 = datasets["BeechArea0_df_sce_12_12_08"]
GrassArea0_12_12_08 = datasets["GrassArea0"]



BeechArea0_08_10_08 = datasets["BeechArea0_df_sce_08_10_08"]
GrassArea0_08_10_08 = datasets["GrassArea0"]


BeechArea0_08_10_10 = datasets["BeechArea0_df_sce_08_10_10"]
GrassArea0_08_10_10 = datasets["GrassArea0"]


# Drop the "Year" column (not needed) and merge region-wise into final_feature_array
final_feature_array = final_feature_array.merge(
    BeechArea0.drop(columns=["Year"]), on="Region", how="left")


final_feature_array = final_feature_array.merge(
    GrassArea0.drop(columns=["Year"]), on="Region", how="left")



# Drop the "Year" column (not needed) and merge region-wise into final_feature_array
final_feature_array_08_08_08 = final_feature_array_08_08_08.merge(
    BeechArea0_08_08_08.drop(columns=["Year"]), on="Region", how="left")


final_feature_array_08_08_08 = final_feature_array_08_08_08.merge(
    GrassArea0_08_08_08.drop(columns=["Year"]), on="Region", how="left")


# Drop the "Year" column (not needed) and merge region-wise into final_feature_array
final_feature_array_12_12_08 = final_feature_array_12_12_08.merge(
    BeechArea0_12_12_08.drop(columns=["Year"]), on="Region", how="left")


final_feature_array_12_12_08 = final_feature_array_12_12_08.merge(
    GrassArea0_12_12_08.drop(columns=["Year"]), on="Region", how="left")




# Drop the "Year" column (not needed) and merge region-wise into final_feature_array
final_feature_array_08_10_08 = final_feature_array_08_10_08.merge(
    BeechArea0_08_10_08.drop(columns=["Year"]), on="Region", how="left")


final_feature_array_08_10_08 = final_feature_array_08_10_08.merge(
    GrassArea0_08_10_08.drop(columns=["Year"]), on="Region", how="left")


# Drop the "Year" column (not needed) and merge region-wise into final_feature_array
final_feature_array_08_10_10 = final_feature_array_08_10_10.merge(
    BeechArea0_08_10_10.drop(columns=["Year"]), on="Region", how="left")


final_feature_array_08_10_10 = final_feature_array_08_10_10.merge(
    GrassArea0_08_10_10.drop(columns=["Year"]), on="Region", how="left")




#############################
#############################
#############################


# Vertically stack the two DataFrames
final_feature_array_combined_1_2 = pd.concat([final_feature_array,
                                          final_feature_array_08_08_08,
                                          #final_feature_array_co2_3times,
                                          #final_feature_array_co2_05times
                                          ],
                                         ignore_index=True)

final_feature_array_combined_1_4 = pd.concat([
                                          final_feature_array,
                                          #final_feature_array_co2_2times,
                                          #final_feature_array_co2_3times,
                                          #final_feature_array_co2_05times,
                                          final_feature_array_12_12_08
                                          ],
                                         ignore_index=True)


# Vertically stack the two DataFrames
final_feature_array_combined_1_3 = pd.concat([final_feature_array,
                                          final_feature_array_08_10_08,
                                          #final_feature_array_co2_3times,
                                          #final_feature_array_co2_05times
                                          ],
                                         ignore_index=True)

final_feature_array_combined_1_5 = pd.concat([
                                          final_feature_array,
                                          #final_feature_array_co2_2times,
                                          #final_feature_array_co2_3times,
                                          #final_feature_array_co2_05times,
                                          final_feature_array_08_10_10
                                          ],
                                         ignore_index=True)



final_feature_array_combined = pd.concat(
                                [ final_feature_array,
                                final_feature_array_08_08_08,
                                final_feature_array_08_10_08,
                                final_feature_array_08_10_10,
                                #final_feature_array_co2_05times,
                                final_feature_array_12_12_08
                                ],
                               ignore_index=True)



# ---- Apply Min-Max Scaling ----
scaler = MinMaxScaler()
columns_to_scale = [col for col in final_feature_array.columns if col not in ["Region", "Technology"]]
final_feature_array[columns_to_scale] = scaler.fit_transform(final_feature_array[columns_to_scale])




columns_to_scale = [col for col in final_feature_array_combined.columns if col not in ["Region", "Technology"]]

final_feature_array_combined_1_2[columns_to_scale] = scaler.fit_transform(final_feature_array_combined_1_2[columns_to_scale])

final_feature_array_combined_1_3[columns_to_scale] = scaler.fit_transform(final_feature_array_combined_1_3[columns_to_scale])

final_feature_array_combined_1_4[columns_to_scale] = scaler.fit_transform(final_feature_array_combined_1_4[columns_to_scale])

final_feature_array_combined_1_5[columns_to_scale] = scaler.fit_transform(final_feature_array_combined_1_5[columns_to_scale])

final_feature_array_combined = scaler.fit_transform(final_feature_array_combined[columns_to_scale])


############################################
############################################
############################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from Temporary_backups.gdx_to_csv_function import extract_gdx_results


#gdx_filename: str, output_dir: str, sub_dir: str



#######################################################
#######################################################
#######################################################



"""
SHOULD BE refined from here
"""


# Load the .gdx file
gdx_file = gams_system_dir + "/scenarios_neg_emi/CarbonPrice/Results/Ali_results_2times.gdx"  # Change this to the actual path of your GDX file
output_dir = gams_system_dir + "/Temporary_backups/data/CarbonPrice"
extract_gdx_results(gdx_file, output_dir, sub_dir= "2times" )

gdx_file = gams_system_dir + "/scenarios_neg_emi/CarbonPrice/Results/Ali_results_3times.gdx" 

extract_gdx_results(gdx_file, output_dir, sub_dir= "3times" )



gdx_file = gams_system_dir + "/scenarios_neg_emi/CarbonPrice/Results/Ali_results_halftimes.gdx" 

extract_gdx_results(gdx_file, output_dir, sub_dir= "halftimes" )



gdx_file = gams_system_dir + "/scenarios_neg_emi/Results_dataset_scenarios/Results_CO2price_0.8_FMsgrowth_0.8_BeechArea0_0.8.gdx" 
output_dir_08_08_08 = gams_system_dir + "/Temporary_backups/data"
extract_gdx_results(gdx_file, output_dir_08_08_08, sub_dir= "Results_08_08_08" )



gdx_file = gams_system_dir + "/scenarios_neg_emi/Results_dataset_scenarios/Results_CO2price_1.2_FMsgrowth_1.2_BeechArea0_0.8.gdx" 
output_dir_12_12_08 = gams_system_dir + "/Temporary_backups/data"
extract_gdx_results(gdx_file, output_dir_12_12_08, sub_dir= "Results_12_12_08" )



gdx_file = gams_system_dir + "/scenarios_neg_emi/Results_dataset_scenarios/Results_CO2price_0.8_FMsgrowth_1.0_BeechArea0_0.8.gdx" 
output_dir_08_10_08 = gams_system_dir + "/Temporary_backups/data"
extract_gdx_results(gdx_file, output_dir_08_10_08, sub_dir= "Results_08_10_08" )


gdx_file = gams_system_dir + "/scenarios_neg_emi/Results_dataset_scenarios/Results_CO2price_0.8_FMsgrowth_1.0_BeechArea0_1.0.gdx" 
output_dir_08_10_10 = gams_system_dir + "/Temporary_backups/data"
extract_gdx_results(gdx_file, output_dir_08_10_10, sub_dir= "Results_08_10_10" )



df_capFMs_08_08_08 = pd.read_csv(output_dir_08_08_08 + "/Results_08_08_08" + "/capFMs_results.csv")
df_capFMs_12_12_08 = pd.read_csv(output_dir_12_12_08 + "/Results_12_12_08" + "/capFMs_results.csv")



df_capFMs_08_10_08 = pd.read_csv(output_dir_08_10_08 + "/Results_08_10_08" + "/capFMs_results.csv")
df_capFMs_08_10_10 = pd.read_csv(output_dir_08_10_10 + "/Results_08_10_10" + "/capFMs_results.csv")




# Load extracted CSV data
df_capFMs = pd.read_csv(gams_system_dir + "/Temporary_backups/data" + "/capFMs_results.csv")


df_capFMs_combined_1_2 = pd.concat([df_capFMs,
                                #df_capFMs_co2_2times,
                                df_capFMs_08_08_08
                                ], ignore_index=True)



df_capFMs_combined_1_4 = pd.concat([
                                df_capFMs,
                                df_capFMs_12_12_08,
                                ], ignore_index=True)



df_capFMs_combined_1_3 = pd.concat([
                                df_capFMs,
                                df_capFMs_08_10_08,
                                ], ignore_index=True)



df_capFMs_combined_1_5 = pd.concat([
                                df_capFMs,
                                df_capFMs_08_10_10,
                                ], ignore_index=True)



df_capFMs_combined = pd.concat([
                                df_capFMs,
                                df_capFMs_08_08_08,
                                df_capFMs_08_10_08,
                                df_capFMs_08_10_10,
                                df_capFMs_12_12_08,
                                ], ignore_index=True)


"""
final_feature_array_combined = pd.concat(
                                [ final_feature_array,
                                final_feature_array_08_08_08,
                                final_feature_array_08_10_08,
                                final_feature_array_08_10_10,
                                #final_feature_array_co2_05times,
                                final_feature_array_12_12_08
                                ],
                               ignore_index=True)
"""


#######################################################
#######################################################
#######################################################


from Temporary_backups.random_forest_module import train_and_predict_capFMs, train_and_predict_capFMs_ensemble

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import numpy as np




results_1_2 = train_and_predict_capFMs(df_capFMs_combined_1_2, final_feature_array_combined_1_2)

print(f"📈 R² (scaled): {results_1_2['r2_scaled']:.4f}")
print(f"📉 RMSE (scaled): {results_1_2['rmse_scaled']:.4f}")
print(f"📈 R² (original): {results_1_2['r2_original']:.4f}")
print(f"📉 RMSE (original): {results_1_2['rmse_original']:.2f} hectares")

y_pred_original = results_1_2["y_pred_original"]
y_test_original = results_1_2["y_test_original"]

model = results_1_2["model"]
X_train = results_1_2["X_train"]
X_test = results_1_2["X_test"]
encoder = results_1_2["encoder"]



import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(y_test_original, y_pred_original, alpha=0.6, edgecolor='k')
plt.plot([y_test_original.min(), y_test_original.max()],
         [y_test_original.min(), y_test_original.max()], 'r--', lw=2)
plt.xlabel("Actual capFMs (ha)")
plt.ylabel("Predicted capFMs (ha)")
plt.title("Predicted vs Actual capFMs")
plt.grid(True)
plt.tight_layout()
plt.show()



results_1_3 = train_and_predict_capFMs(df_capFMs_combined_1_3, final_feature_array_combined_1_3)

print(f"📈 R² (scaled): {results_1_3['r2_scaled']:.4f}")
print(f"📉 RMSE (scaled): {results_1_3['rmse_scaled']:.4f}")
print(f"📈 R² (original): {results_1_3['r2_original']:.4f}")
print(f"📉 RMSE (original): {results_1_3['rmse_original']:.2f} hectares")

y_pred_original = results_1_3["y_pred_original"]
y_test_original = results_1_3["y_test_original"]

model = results_1_3["model"]
X_train = results_1_3["X_train"]
X_test = results_1_3["X_test"]
encoder = results_1_3["encoder"]



import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(y_test_original, y_pred_original, alpha=0.6, edgecolor='k')
plt.plot([y_test_original.min(), y_test_original.max()],
         [y_test_original.min(), y_test_original.max()], 'r--', lw=2)
plt.xlabel("Actual capFMs (ha)")
plt.ylabel("Predicted capFMs (ha)")
plt.title("Predicted vs Actual capFMs")
plt.grid(True)
plt.tight_layout()
plt.show()






results_1_4 = train_and_predict_capFMs(df_capFMs_combined_1_4, final_feature_array_combined_1_4)

print(f"📈 R² (scaled): {results_1_4['r2_scaled']:.4f}")
print(f"📉 RMSE (scaled): {results_1_4['rmse_scaled']:.4f}")
print(f"📈 R² (original): {results_1_4['r2_original']:.4f}")
print(f"📉 RMSE (original): {results_1_4['rmse_original']:.2f} hectares")

y_pred_original = results_1_4["y_pred_original"]
y_test_original = results_1_4["y_test_original"]

model = results_1_4["model"]
X_train = results_1_4["X_train"]
X_test = results_1_4["X_test"]
encoder = results_1_4["encoder"]



import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(y_test_original, y_pred_original, alpha=0.6, edgecolor='k')
plt.plot([y_test_original.min(), y_test_original.max()],
         [y_test_original.min(), y_test_original.max()], 'r--', lw=2)
plt.xlabel("Actual capFMs (ha)")
plt.ylabel("Predicted capFMs (ha)")
plt.title("Predicted vs Actual capFMs")
plt.grid(True)
plt.tight_layout()
plt.show()




results_1_5 = train_and_predict_capFMs(df_capFMs_combined_1_5, final_feature_array_combined_1_5)

print(f"📈 R² (scaled): {results_1_5['r2_scaled']:.4f}")
print(f"📉 RMSE (scaled): {results_1_5['rmse_scaled']:.4f}")
print(f"📈 R² (original): {results_1_5['r2_original']:.4f}")
print(f"📉 RMSE (original): {results_1_5['rmse_original']:.2f} hectares")

y_pred_original = results_1_5["y_pred_original"]
y_test_original = results_1_5["y_test_original"]

model = results_1_5["model"]
X_train = results_1_5["X_train"]
X_test = results_1_5["X_test"]
encoder = results_1_5["encoder"]



import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(y_test_original, y_pred_original, alpha=0.6, edgecolor='k')
plt.plot([y_test_original.min(), y_test_original.max()],
         [y_test_original.min(), y_test_original.max()], 'r--', lw=2)
plt.xlabel("Actual capFMs (ha)")
plt.ylabel("Predicted capFMs (ha)")
plt.title("Predicted vs Actual capFMs")
plt.grid(True)
plt.tight_layout()
plt.show()



results = train_and_predict_capFMs_ensemble(df_capFMs_combined, final_feature_array_combined, n_folds=5)

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






#######################################
#######################################
#######################################

"""
SHAP analysis
"""


"""
import shap

# Use TreeExplainer for tree-based models like RandomForest
explainer_shap = shap.TreeExplainer(model)
shap_values = explainer_shap.shap_values(X_test)


shap_values = explainer_shap.shap_values(X_test)

shap.summary_plot(shap_values, X_test)


# SHAP summary plot
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


# Get global SHAP feature importance
mean_abs_shap = np.abs(shap_values).mean(axis=0)
top_indices = np.argsort(mean_abs_shap)[-3:][::-1]

# Extract top 3 feature names and their stats
top_features = [X_test.columns[i] for i in top_indices]
top_shap_vals = [mean_abs_shap[i] for i in top_indices]
top_feature_vals = [X_test.iloc[:, i].mean() for i in top_indices]


"""


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





#####################################################
#####################################################
#####################################################

"""

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
rename_columns_agri = {
    "costMargAgri": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "Cost"},
    "costInvAgri": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "InvestmentCost"},
    "costInvLevelAgri": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "InvestmentLevelCost"},
    "ghgAgri": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "GHG_Removal"},
    "Agrigrowth": {"*": "Year", "*.1": "Technology", "*.2": "Region", "Value": "Agri_Growth"},
    "Agriarea0": {"*": "Year", "*.1": "Region", "Value": "InitialAgriArea"},
    "PeatExtract": {"*": "Year", "Value": "Peat_Extraction"}
}

# Step 4: Apply renaming and clean duplicates
for key, df in agri_datasets.items():
    # Drop duplicate column names (just in case)
    df = df.loc[:, ~df.columns.duplicated()]
    # Rename columns
    df.rename(columns=rename_columns_agri[key], inplace=True)
    # Re-assign cleaned DataFrame back to dictionary
    agri_datasets[key] = df

# ✅ Done! All agri_datasets now have clean, standardized column names.


print(agri_datasets["costMargAgri"].head())



"""



"""
For the future work on the next week

"""



#df_ghgAbateFMs = pd.read_csv("ghgAbateFMs_results.csv")



"""

df_ghgAbateAgri = pd.read_csv("ghgAbateAgri_results.csv")

df_capAgri = pd.read_csv("capAgri_results.csv")


# First, rename columns to match the function expectations
df_capAgri_renamed = df_capAgri.rename(columns={
    "year": "Year",
    "r": "Region",
    "techAgri": "Technology",
    "capAgri": "Capacity"
})

# Now apply the trend function to capAgri
capAgri_features = compute_trend(df_capAgri_renamed, value_col="Capacity", feature_prefix="CapAgri")

# Output sample
print(capAgri_features.head())


final_feature_array = final_feature_array.merge(capAgri_features, on=["Region", "Technology"], how="outer")

final_feature_array.fillna(0, inplace=True)








######################################################
######################################################
######################################################
######################################################




df_total_cost_annual = pd.read_csv("total_cost_annual.csv")
df_costAnnualFMs = pd.read_csv("costAnnualFMs_results.csv")
df_costAnnualAgri = pd.read_csv("costAnnualAgri_results.csv")
df_total_ghg_annual = pd.read_csv("total_ghg_annual.csv")
df_FMsGrassArea = pd.read_csv("FMsGrassArea.csv")
df_FMsBeechArea = pd.read_csv("FMsBeechArea.csv")
df_purCO2LULUCF = pd.read_csv("purCO2LULUCF.csv")






import pandas as pd
import numpy as np
from scipy.stats import linregress
from sklearn.preprocessing import MinMaxScaler
from numpy.polynomial.polynomial import Polynomial

# Load optimization results (Replace these with actual file paths if needed)
df_capFMs = pd.read_csv("capFMs_results.csv")
df_capAgri = pd.read_csv("capAgri_results.csv")
df_ghgAbateFMs = pd.read_csv("ghgAbateFMs_results.csv")
df_ghgAbateAgri = pd.read_csv("ghgAbateAgri_results.csv")

# Function to compute various statistical and trend-based features

def compute_features(df, value_col, feature_prefix, group_by=["techFMs", "r"]):
    extracted_features = []

    for group_key, group in df.groupby(group_by):
        # Handle cases where group_by has only one value (e.g., "year")
        if isinstance(group_key, tuple):
            tech, region = group_key
        else:
            tech, region = group_key, None  # Assign None when there's no second key

        years = group["year"].values
        values = group[value_col].values

        # Compute slope using linear regression
        slope, _, _, _, _ = linregress(years, values)

        # Compute polynomial fits
        poly_2 = Polynomial.fit(years, values, 2).convert().coef
        poly_3 = Polynomial.fit(years, values, 3).convert().coef

        # Ensure polynomial coefficients have correct length
        poly_2_c1 = poly_2[1] if len(poly_2) > 1 else 0
        poly_2_c2 = poly_2[2] if len(poly_2) > 2 else 0

        poly_3_c1 = poly_3[1] if len(poly_3) > 1 else 0
        poly_3_c2 = poly_3[2] if len(poly_3) > 2 else 0
        poly_3_c3 = poly_3[3] if len(poly_3) > 3 else 0

        # Compute additional statistical features
        initial_value = values[0]
        final_value = values[-1]
        mean_value = np.mean(values)
        std_value = np.std(values)
        range_value = np.max(values) - np.min(values)

        # Store extracted features
        extracted_features.append([
            tech, region, initial_value, final_value, slope, 
            poly_2_c1, poly_2_c2,  # Quadratic coefficients
            poly_3_c1, poly_3_c2, poly_3_c3,  # Cubic coefficients
            mean_value, std_value, range_value
        ])

    # Convert to DataFrame
    feature_df = pd.DataFrame(extracted_features, columns=[
        "Technology", "Region", f"{feature_prefix}_2020", f"{feature_prefix}_2050", f"{feature_prefix}_Slope",
        f"{feature_prefix}_Poly2_C1", f"{feature_prefix}_Poly2_C2",
        f"{feature_prefix}_Poly3_C1", f"{feature_prefix}_Poly3_C2", f"{feature_prefix}_Poly3_C3",
        f"{feature_prefix}_Mean", f"{feature_prefix}_Std", f"{feature_prefix}_Range"
    ])
    
    return feature_df



# Compute features for various outputs
capFMs_features = compute_features(df_capFMs, "capFMs", "capFMs")
capAgri_features = compute_features(df_capAgri, "capAgri", "capAgri", group_by=["techAgri", "r"])
ghgAbateFMs_features = compute_features(df_ghgAbateFMs, "ghgAbateTechFMs", "ghgAbateFMs")
ghgAbateAgri_features = compute_features(df_ghgAbateAgri, "ghgAbateTechAgri", "ghgAbateAgri", group_by=["techAgri", "r"])




# Merge all feature sets
final_output_features = capFMs_features.merge(capAgri_features, on=["Technology", "Region"], how="outer") \
                                       .merge(ghgAbateFMs_features, on=["Technology", "Region"], how="outer") \
                                       .merge(ghgAbateAgri_features, on=["Technology", "Region"], how="outer")

# Fill NaNs with zero
final_output_features.fillna(0, inplace=True)

# Apply Min-Max Scaling
scaler = MinMaxScaler()
columns_to_scale = [col for col in final_output_features.columns if col not in ["Technology", "Region"]]
final_output_features[columns_to_scale] = scaler.fit_transform(final_output_features[columns_to_scale])

# Save the extracted features
final_output_features.to_csv("final_output_features.csv", index=False)

print("✅ Extracted ML features from optimization results and saved successfully! 🚀")


"""

#######################################
#######################################
#######################################
#######################################







