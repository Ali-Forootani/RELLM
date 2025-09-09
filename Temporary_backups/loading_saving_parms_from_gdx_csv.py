#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 11:43:15 2025

@author: forootan
"""



import gdxpds
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pyomo.environ import *
#from gams import GamsWorkspace, GamsParameter, GamsSet
#from gams import GamsWorkspace
import os

import sys
import os
import json
from datetime import datetime



###################################


import os
import re
import gdxpds
import pandas as pd

def normalize_filename_to_code_4(filename):
    """
    Extract all variable-value pairs from a filename like 
    'CO2price_0.8_FMsgrowth_1.0_BeechArea0_1.2.gdx' 
    and return a code like '08_10_12' (i.e. scaled and zero-padded values).
    
    If no variable-value pairs found, return None.
    """
    matches = re.findall(r'_(\d(?:\.\d)?)', filename)

    if matches:
        parts = [int(float(x) * 10) for x in matches]
        return '_'.join([f"{p:02d}" for p in parts])
    
    return None  # no code

def load_and_save_selected_symbols_4(directory, symbols, save_path=None):
    """
    Loads specified symbols from all .gdx files in a directory and saves them as CSVs.

    Parameters:
        directory (str): Path where .gdx files are located.
        symbols (list): List of GAMS parameter names to extract.
        save_path (str): Optional. Path to save the .csv files. Defaults to current directory.
    """
    if save_path is None:
        save_path = os.getcwd()
    else:
        os.makedirs(save_path, exist_ok=True)

    gdx_files = [f for f in os.listdir(directory) if f.endswith(".gdx")]

    for gdx_file in gdx_files:
        scenario_code = normalize_filename_to_code_4(gdx_file)
        full_path = os.path.join(directory, gdx_file)

        try:
            dataframes = gdxpds.to_dataframes(full_path)
            for symbol in symbols:
                if symbol in dataframes:
                    df = dataframes[symbol]

                    # Determine filename
                    if scenario_code:
                        var_name = f"{symbol}_df_sce_{scenario_code}"
                        file_name = f"{var_name}.csv"
                    else:
                        var_name = symbol
                        file_name = f"{symbol}.csv"

                    file_path = os.path.join(save_path, file_name)
                    globals()[var_name] = df
                    df.to_csv(file_path, index=False)
                    print(f" Saved {file_path}")
                else:
                    print(f" Symbol '{symbol}' not found in {gdx_file}")
        except Exception as e:
            print(f"✘ Error reading {gdx_file}: {e}")

###########################################
###########################################


import os
import re
import gdxpds
import pandas as pd

def extract_scenario_suffix(filename):
    """
    Extract variable-value pairs from filename, e.g. 
    'CO2price_0.8_FMsgrowth_1.0_BeechArea0_1.2.gdx' -> 'CO2price_0.8_FMsgrowth_1.0_BeechArea0_1.2'
    
    If no variable-value pattern is found, return 'base_scenario'.
    """
    base = os.path.splitext(filename)[0]
    matches = re.findall(r'([A-Za-z0-9]+_\d+(?:\.\d+)?)', base)

    if matches:
        return "_".join(matches)
    return "base_scenario"

def load_and_save_selected_symbols(directory, symbols, save_path=None):
    """
    Loads specified symbols from all .gdx files in a directory and saves them as CSVs.

    Parameters:
        directory (str): Path where .gdx files are located.
        symbols (list): List of GAMS parameter names to extract.
        save_path (str): Optional. Path to save the .csv files. Defaults to current directory.
    """
    if save_path is None:
        save_path = os.getcwd()
    else:
        os.makedirs(save_path, exist_ok=True)

    gdx_files = [f for f in os.listdir(directory) if f.endswith(".gdx")]

    for gdx_file in gdx_files:
        scenario_suffix = extract_scenario_suffix(gdx_file)
        full_path = os.path.join(directory, gdx_file)

        try:
            dataframes = gdxpds.to_dataframes(full_path)
            for symbol in symbols:
                if symbol in dataframes:
                    df = dataframes[symbol]

                    # Build file name with full scenario suffix
                    file_name = f"{symbol}_{scenario_suffix}.csv"
                    file_path = os.path.join(save_path, file_name)
                    globals()[symbol] = df

                    df.to_csv(file_path, index=False)
                    print(f" Saved {file_path}")
                else:
                    print(f" Symbol '{symbol}' not found in {gdx_file}")
        except Exception as e:
            print(f" Error reading {gdx_file}: {e}")











