#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 10:42:27 2025

@author: forootan
"""
import gdxpds
import pandas as pd
import os

def extract_gdx_results2(gdx_filename: str, output_dir: str, sub_dir: str):
    """
    Extracts variables from a GAMS .gdx file and saves them as CSV files.

    Parameters:
    - gdx_filename (str): Path to the .gdx file (e.g., "results.gdx")
    - output_dir (str): Main output directory (e.g., "./outputs")
    - sub_dir (str): Subdirectory inside output_dir (e.g., "results")

    All CSV files will be saved under: output_dir/sub_dir/
    """
    # Load the .gdx file
    gdx_data_result = gdxpds.to_dataframes(gdx_filename)

    # Create output directory
    save_path = os.path.join(output_dir, sub_dir)
    os.makedirs(save_path, exist_ok=True)
    
    
    print("*********************")
    
    print(gdx_data_result)
    
    print("*********************")
    

    # Extract and rename variables
    df_capFMs = gdx_data_result['capFMs'][['year', 'techFMs', 'r', 'Level']].rename(columns={'Level': 'capFMs'})
    df_capAgri = gdx_data_result['capAgri'][['year', 'techAgri', 'r', 'Level']].rename(columns={'Level': 'capAgri'})
    df_ghgAbateFMs = gdx_data_result['ghgAbateTechFMs'][['year', 'techFMs', 'r', 'Level']].rename(columns={'Level': 'ghgAbateTechFMs'})
    df_ghgAbateAgri = gdx_data_result['ghgAbateTechAgri'][['year', 'techAgri', 'r', 'Level']].rename(columns={'Level': 'ghgAbateTechAgri'})
    df_total_cost_annual = gdx_data_result['Total_costAnnual'][['year', 'Level']].rename(columns={'Level': 'Total_costAnnual'})
    df_total_cost = gdx_data_result['Total_cost'][['Level']].rename(columns={'Level': 'Total_cost'})
    df_costAnnualFMs = gdx_data_result['costAnnualFMs'][['year', 'Level']].rename(columns={'Level': 'costAnnualFMs'})
    df_costAnnualAgri = gdx_data_result['costAnnualAgri'][['year', 'Level']].rename(columns={'Level': 'costAnnualAgri'})
    df_total_ghg = gdx_data_result['Total_ghg'][['Level']].rename(columns={'Level': 'Total_ghg'})
    df_total_ghg_annual = gdx_data_result['Total_ghgAnnual'][['year', 'Level']].rename(columns={'Level': 'Total_ghgAnnual'})
    df_FMsGrassArea = gdx_data_result['FMsGrassArea'][['year', 'r', 'Level']].rename(columns={'Level': 'FMsGrassArea'})
    df_FMsBeechArea = gdx_data_result['FMsBeechArea'][['year', 'r', 'Level']].rename(columns={'Level': 'FMsBeechArea'})
    df_AgriGrassArea = gdx_data_result['AgriGrassArea'][['year', 'r', 'Level']].rename(columns={'Level': 'AgriGrassArea'})
    df_CO2gapRewt = gdx_data_result['CO2gapRewt'][['Level']].rename(columns={'Level': 'CO2gapRewt'})
    df_purCO2LULUCF = gdx_data_result['purCO2LULUCF'].rename(columns={'*': 'year'})[['year', 'Level']].rename(columns={'Level': 'purCO2LULUCF'})
    df_ghgAbateAnnualFMs = gdx_data_result['ghgAbateAnnualFMs'][['year', 'Level']].rename(columns={'Level': 'ghgAbateAnnualFMs'})
    df_costTechFMs = gdx_data_result['costTechFMs'][['year', 'techFMs', 'r', 'Level']].rename(columns={'Level': 'costTechFMs'})
    df_costTechAgri = gdx_data_result['costTechAgri'][['year', 'techAgri', 'r', 'Level']].rename(columns={'Level': 'costTechAgri'})

    # Save all to CSVs
    df_capFMs.to_csv(os.path.join(save_path, "capFMs_results.csv"), index=False)
    df_capAgri.to_csv(os.path.join(save_path, "capAgri_results.csv"), index=False)
    df_ghgAbateFMs.to_csv(os.path.join(save_path, "ghgAbateFMs_results.csv"), index=False)
    df_ghgAbateAgri.to_csv(os.path.join(save_path, "ghgAbateAgri_results.csv"), index=False)
    df_total_cost_annual.to_csv(os.path.join(save_path, "total_cost_annual.csv"), index=False)
    df_total_cost.to_csv(os.path.join(save_path, "total_cost.csv"), index=False)
    df_costAnnualFMs.to_csv(os.path.join(save_path, "costAnnualFMs_results.csv"), index=False)
    df_costAnnualAgri.to_csv(os.path.join(save_path, "costAnnualAgri_results.csv"), index=False)
    df_total_ghg.to_csv(os.path.join(save_path, "total_ghg.csv"), index=False)
    df_total_ghg_annual.to_csv(os.path.join(save_path, "total_ghg_annual.csv"), index=False)
    df_FMsGrassArea.to_csv(os.path.join(save_path, "FMsGrassArea.csv"), index=False)
    df_FMsBeechArea.to_csv(os.path.join(save_path, "FMsBeechArea.csv"), index=False)
    df_AgriGrassArea.to_csv(os.path.join(save_path, "AgriGrassArea.csv"), index=False)
    df_CO2gapRewt.to_csv(os.path.join(save_path, "CO2gapRewt.csv"), index=False)
    df_purCO2LULUCF.to_csv(os.path.join(save_path, "purCO2LULUCF.csv"), index=False)
    df_ghgAbateAnnualFMs.to_csv(os.path.join(save_path, "ghgAbateAnnualFMs.csv"), index=False)
    df_costTechFMs.to_csv(os.path.join(save_path, "costTechFMs.csv"), index=False)
    df_costTechAgri.to_csv(os.path.join(save_path, "costTechAgri.csv"), index=False)

    print(f"🎉 Extraction completed. All files saved to: {save_path}")

# Example usage:
# extract_gdx_results("results.gdx", "./outputs", "results_run1")





import gdxpds
import pandas as pd
import os

def extract_gdx_results2(gdx_filename: str, output_dir: str, sub_dir: str):
    """
    Extracts selected variables from a GAMS .gdx file and saves them as CSVs.
    
    Parameters:
    - gdx_filename: Path to .gdx file (e.g. "results.gdx")
    - output_dir: Root folder to save results
    - sub_dir: Subfolder name to organize results
    """
    # Load .gdx
    gdx_data_result = gdxpds.to_dataframes(gdx_filename)
    save_path = os.path.join(output_dir, sub_dir)
    os.makedirs(save_path, exist_ok=True)
    
    
    print("*********************")
    
    print(gdx_data_result.keys())
    
    print("*********************")

    # Utility: Extract with check
    def safe_extract(df_dict, key, cols, rename_dict, optional=False):
        if key in df_dict:
            return df_dict[key][cols].rename(columns=rename_dict)
        elif optional:
            print(f"⚠️  Optional variable '{key}' not found in GDX file.")
            return None
        else:
            raise KeyError(f"❌ Required variable '{key}' not found in GDX file.")

    # Extraction
    variables = {
        "capFMs": ("capFMs_results.csv", ['year', 'techFMs', 'r', 'Level'], {'Level': 'capFMs'}),
        "capAgri": ("capAgri_results.csv", ['year', 'techAgri', 'r', 'Level'], {'Level': 'capAgri'}),
        "ghgAbateTechFMs": ("ghgAbateFMs_results.csv", ['year', 'techFMs', 'r', 'Level'], {'Level': 'ghgAbateTechFMs'}),
        "ghgAbateTechAgri": ("ghgAbateAgri_results.csv", ['year', 'techAgri', 'r', 'Level'], {'Level': 'ghgAbateTechAgri'}, True),
        "Total_costAnnual": ("total_cost_annual.csv", ['year', 'Level'], {'Level': 'Total_costAnnual'}),
        "Total_cost": ("total_cost.csv", ['Level'], {'Level': 'Total_cost'}),
        "costAnnualFMs": ("costAnnualFMs_results.csv", ['year', 'Level'], {'Level': 'costAnnualFMs'}),
        "costAnnualAgri": ("costAnnualAgri_results.csv", ['year', 'Level'], {'Level': 'costAnnualAgri'}),
        "Total_ghg": ("total_ghg.csv", ['Level'], {'Level': 'Total_ghg'}),
        "Total_ghgAnnual": ("total_ghg_annual.csv", ['year', 'Level'], {'Level': 'Total_ghgAnnual'}),
        "FMsGrassArea": ("FMsGrassArea.csv", ['year', 'r', 'Level'], {'Level': 'FMsGrassArea'}),
        "FMsBeechArea": ("FMsBeechArea.csv", ['year', 'r', 'Level'], {'Level': 'FMsBeechArea'}),
        "AgriGrassArea": ("AgriGrassArea.csv", ['year', 'r', 'Level'], {'Level': 'AgriGrassArea'}, True),
        "CO2gapRewt": ("CO2gapRewt.csv", ['Level'], {'Level': 'CO2gapRewt'}),
        "ghgAbateAnnualFMs": ("ghgAbateAnnualFMs.csv", ['year', 'Level'], {'Level': 'ghgAbateAnnualFMs'}, True),
        "costTechFMs": ("costTechFMs.csv", ['year', 'techFMs', 'r', 'Level'], {'Level': 'costTechFMs'}),
        "costTechAgri": ("costTechAgri.csv", ['year', 'techAgri', 'r', 'Level'], {'Level': 'costTechAgri'}, True),
    }

    # Loop over variable map
    for key, args in variables.items():
        filename, cols, rename_dict = args[0], args[1], args[2]
        optional = args[3] if len(args) > 3 else False
        df = safe_extract(gdx_data_result, key, cols, rename_dict, optional=optional)
        if df is not None:
            df.to_csv(os.path.join(save_path, filename), index=False)

    # Special case: purCO2LULUCF with '*' column
    if 'purCO2LULUCF' in gdx_data_result:
        df_pur = gdx_data_result['purCO2LULUCF'].rename(columns={'*': 'year'})[['year', 'Level']]
        df_pur = df_pur.rename(columns={'Level': 'purCO2LULUCF'})
        df_pur.to_csv(os.path.join(save_path, "purCO2LULUCF.csv"), index=False)
    else:
        print("⚠️  Optional variable 'purCO2LULUCF' not found in GDX file.")

    print(f"\n🎉 Extraction completed. All available files saved in: {save_path}")




import gdxpds
import pandas as pd
import os

def extract_gdx_results(gdx_filename: str, output_dir: str, sub_dir: str):
    """
    Extracts dataframes from a GDX file and saves selected variables as CSV files.
    
    Parameters:
    - gdx_filename (str): Path to the .gdx file
    - output_dir (str): Root directory to save CSV files
    - sub_dir (str): Subfolder for this extraction session
    """
    gdx_data_result = gdxpds.to_dataframes(gdx_filename)
    save_path = os.path.join(output_dir, sub_dir)
    os.makedirs(save_path, exist_ok=True)

    saved_keys = []
    skipped_keys = []

    # Utility function with error handling
    def safe_extract(df_dict, key, cols, rename_dict, optional=False):
        if key in df_dict:
            return df_dict[key][cols].rename(columns=rename_dict)
        elif optional:
            skipped_keys.append(key)
            print(f"⚠️  Optional variable '{key}' not found in GDX file.")
            return None
        else:
            raise KeyError(f"❌ Required variable '{key}' not found in GDX file.")

    # Variables to extract: (filename, columns, rename_map, optional)
    variables = {
        "capFMs": ("capFMs_results.csv", ['year', 'techFMs', 'r', 'Level'], {'Level': 'capFMs'}),
        "capAgri": ("capAgri_results.csv", ['year', 'techAgri', 'r', 'Level'], {'Level': 'capAgri'}),
        "ghgAbateTechFMs": ("ghgAbateFMs_results.csv", ['year', 'techFMs', 'r', 'Level'], {'Level': 'ghgAbateTechFMs'}),
        "ghgAbateTechAgri": ("ghgAbateAgri_results.csv", ['year', 'techAgri', 'r', 'Level'], {'Level': 'ghgAbateTechAgri'}, True),
        "Total_costAnnual": ("total_cost_annual.csv", ['year', 'Level'], {'Level': 'Total_costAnnual'}),
        "Total_cost": ("total_cost.csv", ['Level'], {'Level': 'Total_cost'}),
        "costAnnualFMs": ("costAnnualFMs_results.csv", ['year', 'Level'], {'Level': 'costAnnualFMs'}),
        "costAnnualAgri": ("costAnnualAgri_results.csv", ['year', 'Level'], {'Level': 'costAnnualAgri'}),
        "Total_ghg": ("total_ghg.csv", ['Level'], {'Level': 'Total_ghg'}),
        "Total_ghgAnnual": ("total_ghg_annual.csv", ['year', 'Level'], {'Level': 'Total_ghgAnnual'}),
        "FMsGrassArea": ("FMsGrassArea.csv", ['year', 'r', 'Level'], {'Level': 'FMsGrassArea'}, True),
        "FMsBeechArea": ("FMsBeechArea.csv", ['year', 'r', 'Level'], {'Level': 'FMsBeechArea'}, True),
        "AgriGrassArea": ("AgriGrassArea.csv", ['year', 'r', 'Level'], {'Level': 'AgriGrassArea'}, True),
        "CO2gapRewt": ("CO2gapRewt.csv", ['Level'], {'Level': 'CO2gapRewt'}, True),
        "ghgAbateAnnualFMs": ("ghgAbateAnnualFMs.csv", ['year', 'Level'], {'Level': 'ghgAbateAnnualFMs'}, True),
        "costTechFMs": ("costTechFMs.csv", ['year', 'techFMs', 'r', 'Level'], {'Level': 'costTechFMs'}, True),
        "costTechAgri": ("costTechAgri.csv", ['year', 'techAgri', 'r', 'Level'], {'Level': 'costTechAgri'}, True),
    }

    # Extract and save
    for key, args in variables.items():
        filename, cols, rename_dict = args[0], args[1], args[2]
        optional = args[3] if len(args) > 3 else False
        df = safe_extract(gdx_data_result, key, cols, rename_dict, optional=optional)
        if df is not None:
            df.to_csv(os.path.join(save_path, filename), index=False)
            saved_keys.append(key)

    # Special case: purCO2LULUCF
    if 'purCO2LULUCF' in gdx_data_result:
        df_pur = gdx_data_result['purCO2LULUCF'].rename(columns={'*': 'year'})[['year', 'Level']]
        df_pur = df_pur.rename(columns={'Level': 'purCO2LULUCF'})
        df_pur.to_csv(os.path.join(save_path, "purCO2LULUCF.csv"), index=False)
        saved_keys.append("purCO2LULUCF")
    else:
        skipped_keys.append("purCO2LULUCF")
        print("⚠️  Optional variable 'purCO2LULUCF' not found in GDX file.")

    # Summary
    print("\n✅ Saved CSV files for:")
    for key in saved_keys:
        print(f"  - {key}")

    if skipped_keys:
        print("\n⚠️ Skipped (missing) variables:")
        for key in skipped_keys:
            print(f"  - {key}")

    print(f"\n🎉 Extraction complete. Files saved in: {save_path}")






#############################################





import pandas as pd
import os

def build_input_output_pairs(
    scenarios,
    feature_arrays,          # e.g. fully_enhanced_arrays
    results_folder,          # e.g. path to Results_dataset_scenarios
    output_root_dir,         # e.g. path to Temporary_backups/data
    target_variable="capFMs" # or "ghgAbateTechFMs", etc.
):
    """
    Returns input-output (X, y) pairs for supervised learning based on scenario mapping.
    Joins input features with GDX-extracted output target (e.g., capFMs).
    """
    X_all = []
    y_all = []

    for scenario_name in feature_arrays:
        print(f"\n🔄 Processing scenario: {scenario_name}")

        # === INPUT (features) ===
        X = feature_arrays[scenario_name].copy()

        # === SCENARIO RESULTS ===
        gdx_file_name = f"Results_{scenario_name}.gdx"
        gdx_file_path = os.path.join(results_folder, gdx_file_name)

        if not os.path.exists(gdx_file_path):
            print(f"⚠️ GDX file missing: {gdx_file_path}")
            continue

        # Define folder where GDX was or will be extracted
        scenario_result_folder = os.path.join(output_root_dir, f"Results_{scenario_name}")

        # If not yet extracted, extract
        if not os.path.exists(scenario_result_folder):
            print(f"📦 Extracting: {gdx_file_name}")
            extract_gdx_results(gdx_file_path, output_root_dir, sub_dir=f"Results_{scenario_name}")

        # Path to target variable CSV (e.g., capFMs_results.csv)
        target_file = os.path.join(scenario_result_folder, f"{target_variable}_results.csv")

        if not os.path.exists(target_file):
            print(f"❌ Target file not found: {target_file}")
            continue

        y_df = pd.read_csv(target_file)

        # Standardize column names to match (may depend on variable)
        y_df.rename(columns={
            "techFMs": "Technology",
            "r": "Region",
            "year": "Year",
        }, inplace=True)

        # === OPTIONAL: Year filter (e.g., only 2050 targets)
        y_df = y_df[y_df["Year"] == 2050]  # You can modify this line

        # === Merge input + target ===
        merged = pd.merge(X, y_df, on=["Region", "Technology"], how="inner")

        if len(merged) == 0:
            print(f"⚠️ No matches found for scenario {scenario_name}")
            continue

        X_all.append(merged.drop(columns=[target_variable, "Year"]))
        y_all.append(merged[target_variable].values)

    # === Combine all scenarios ===
    X_combined = pd.concat(X_all, ignore_index=True)
    y_combined = pd.concat([pd.Series(y) for y in y_all], ignore_index=True)

    print("\n✅ Completed building input-output pairs.")
    return X_combined, y_combined






















