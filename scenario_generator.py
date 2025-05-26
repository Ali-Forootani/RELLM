#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 12:04:36 2025
@author: forootan
"""



import os
import sys
import itertools
import pandas as pd
import gdxpds
from datetime import datetime

# Optional: for trend computation, ensure the file exists
from RenewableEnergyLanguageModel.feature_construction_fm import compute_global_trend, compute_trend


"""
def setting_directory(depth):
    #Dynamically walk up N levels in directory structure
    current_dir = os.path.abspath(os.getcwd())
    root_dir = current_dir
    for _ in range(depth):
        root_dir = os.path.abspath(os.path.join(root_dir, os.pardir))
        sys.path.append(os.path.dirname(root_dir))
    return root_dir

# Get base path to GAMS data
gams_system_dir = setting_directory(1)

# Load base GDX file
gdx_base_file = os.path.join(gams_system_dir, "scenarios_neg_emi", "test_Ali.gdx")
gdx_base_data = gdxpds.to_dataframes(gdx_base_file)

# Output directory (inside user's home directory)
output_dir = os.path.expanduser("~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/dataset_scenarios")
os.makedirs(output_dir, exist_ok=True)

# Variables to scale and their factors
variables = ['FMsgrowth', 'costInvLevelFMs']
scale_factors = [0.8]  # Add more if needed
combinations = list(itertools.product(scale_factors, repeat=len(variables)))

# Filter function to exclude problematic symbols (like 1D sets)
def is_valid_gdx_symbol(df):
    return isinstance(df, pd.DataFrame) and (('Value' in df.columns) or df.shape[1] > 1)

# Iterate over all scaling combinations
for combo in combinations:
    # Copy all valid symbols
    modified_data = {k: df.copy() for k, df in gdx_base_data.items() if is_valid_gdx_symbol(df)}
    
    # Apply scaling to specified variables
    for var_name, scale in zip(variables, combo):
        if var_name in modified_data:
            df = modified_data[var_name]
            if 'Value' in df.columns:
                df['Value'] = df['Value'] * scale
            else:
                print(f"⚠️ Warning: 'Value' column not found in {var_name}")
        else:
            print(f"⚠️ Warning: Variable '{var_name}' not found in GDX data")

    # Generate output file name
    
    # Generate output file name dynamically
    file_parts = [f"{var}_{scale:.1f}" for var, scale in zip(variables, combo)]
    file_name = "_".join(file_parts) + ".gdx"
    output_path = os.path.join(output_dir, file_name)

    
    #file_name = f"CO2price_{combo[0]:.1f}_FMsgrowth_{combo[1]:.1f}_BeechArea0_{combo[2]:.1f}.gdx"
    #output_path = os.path.join(output_dir, file_name)

    # Save modified GDX file
    try:
        gdxpds.to_gdx(modified_data, output_path)
        print(f"✅ Saved: {output_path}")
    except Exception as e:
        print(f"❌ Failed to write {file_name}: {e}")
"""


##############################################################

import os
import sys
import itertools
import pandas as pd
import gdxpds

class GDXScaler_2:
    def __init__(self, gdx_base_file, output_dir, variables, scale_factors, directory_depth=1):
        self.gdx_base_file = gdx_base_file
        self.output_dir = os.path.expanduser(output_dir)
        self.variables = variables
        self.scale_factors = scale_factors
        self.combinations = list(itertools.product(scale_factors, repeat=len(variables)))
        self.directory_depth = directory_depth

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Prepare GAMS system directory and load base GDX file
        self.gams_system_dir = self._setting_directory(self.directory_depth)
        self.gdx_data = gdxpds.to_dataframes(self.gdx_base_file)

    def _setting_directory(self, depth):
        """Dynamically walk up N levels in directory structure"""
        current_dir = os.path.abspath(os.getcwd())
        root_dir = current_dir
        for _ in range(depth):
            root_dir = os.path.abspath(os.path.join(root_dir, os.pardir))
            sys.path.append(os.path.dirname(root_dir))
        return root_dir

    def _is_valid_gdx_symbol(self, df):
        """Filter function to exclude problematic symbols (like 1D sets)"""
        return isinstance(df, pd.DataFrame) and (('Value' in df.columns) or df.shape[1] > 1)

    def scale_and_save(self):
        """Perform scaling and save modified GDX files"""
        for combo in self.combinations:
            # Copy valid symbols
            modified_data = {k: df.copy() for k, df in self.gdx_data.items() if self._is_valid_gdx_symbol(df)}

            # Apply scaling to specified variables
            for var_name, scale in zip(self.variables, combo):
                if var_name in modified_data:
                    df = modified_data[var_name]
                    if 'Value' in df.columns:
                        df['Value'] = df['Value'] * scale
                    else:
                        print(f" Warning: 'Value' column not found in {var_name}")
                else:
                    print(f" Warning: Variable '{var_name}' not found in GDX data")

            # Generate output file name
            file_parts = [f"{var}_{scale:.1f}" for var, scale in zip(self.variables, combo)]
            file_name = "_".join(file_parts) + ".gdx"
            output_path = os.path.join(self.output_dir, file_name)

            # Save modified GDX file
            try:
                gdxpds.to_gdx(modified_data, output_path)
                print(f"✅ Saved: {output_path}")
            except Exception as e:
                print(f"❌ Failed to write {file_name}: {e}")

############################################


import os
import sys
import itertools
import pandas as pd
import gdxpds

class GDXScaler:
    def __init__(self, gdx_base_file, output_dir, variables=None, scale_factors=None, directory_depth=1):
        self.gdx_base_file = gdx_base_file
        self.output_dir = os.path.expanduser(output_dir)
        self.variables = variables if variables is not None else []
        self.scale_factors = scale_factors if scale_factors is not None else [1]
        self.directory_depth = directory_depth

        # Prepare combinations only if variables exist
        if self.variables:
            self.combinations = list(itertools.product(self.scale_factors, repeat=len(self.variables)))
        else:
            self.combinations = [()]  # Single combination for base scenario

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Prepare GAMS system directory and load base GDX file
        self.gams_system_dir = self._setting_directory(self.directory_depth)
        self.gdx_data = gdxpds.to_dataframes(self.gdx_base_file)

    def _setting_directory(self, depth):
        """Dynamically walk up N levels in directory structure"""
        current_dir = os.path.abspath(os.getcwd())
        root_dir = current_dir
        for _ in range(depth):
            root_dir = os.path.abspath(os.path.join(root_dir, os.pardir))
            sys.path.append(os.path.dirname(root_dir))
        return root_dir

    def _is_valid_gdx_symbol(self, df):
        """Filter function to exclude problematic symbols (like 1D sets)"""
        return isinstance(df, pd.DataFrame) and (('Value' in df.columns) or df.shape[1] > 1)

    def scale_and_save(self):
        """Perform scaling and save modified GDX files"""
        for combo in self.combinations:
            # Copy valid symbols
            modified_data = {k: df.copy() for k, df in self.gdx_data.items() if self._is_valid_gdx_symbol(df)}

            # Apply scaling to specified variables if any
            if self.variables:
                for var_name, scale in zip(self.variables, combo):
                    if var_name in modified_data:
                        df = modified_data[var_name]
                        if 'Value' in df.columns:
                            df['Value'] = df['Value'] * scale
                        else:
                            print(f"⚠️ Warning: 'Value' column not found in {var_name}")
                    else:
                        print(f"⚠️ Warning: Variable '{var_name}' not found in GDX data")

                # Generate filename based on scaling factors
                file_parts = [f"{var}_{scale:.1f}" for var, scale in zip(self.variables, combo)]
                file_name = "_".join(file_parts) + ".gdx"
            else:
                # No variables → Save as base scenario
                file_name = "base_scenario.gdx"

            output_path = os.path.join(self.output_dir, file_name)

            # Save modified GDX file
            try:
                gdxpds.to_gdx(modified_data, output_path)
                print(f"✅ Saved: {output_path}")
            except Exception as e:
                print(f"❌ Failed to write {file_name}: {e}")



############################################
############################################


from collections import defaultdict
import re

def build_scenario_hierarchy(datasets):
    """
    Build hierarchical scenario dictionary from dataset keys.
    
    Output structure:
    
    scenarios = {
        'CO2price_0.8_FMsgrowth_0.8_BeechArea0_0.8': {
            'costInvFMs': dataset,
            'FMsgrowth': dataset,
            'BeechArea0': dataset,
            ...
        },
        ...
    }
    """
    scenarios = defaultdict(dict)
    
    pattern = re.compile(r"(?P<variable>^[^_]+)(?:_(?P<params>.+))?")
    
    for key in datasets.keys():
        match = pattern.match(key)
        if match:
            variable = match.group("variable")
            params = match.group("params")

            # If there are params, build scenario key
            if params:
                scenario = params
            else:
                scenario = "base"  # for base scenarios

            scenarios[scenario][variable] = datasets[key]

    return scenarios





############################################
############################################

"""
# Example usage:

if __name__ == "__main__":
    gdx_base_file = os.path.join(os.path.abspath(os.getcwd()), "..", "scenarios_neg_emi", "test_Ali.gdx")
    output_dir = "~/Documents/Mohammad_Sadr_files/scenarios_neg_emi/dataset_scenarios"
    variables = ['FMsgrowth', 'costInvLevelFMs']
    scale_factors = [0.8]  # Example scale factors

    scaler = GDXScaler(gdx_base_file, output_dir, variables, scale_factors)
    scaler.scale_and_save()
"""










