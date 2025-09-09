#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 20 07:42:38 2025

@author: forootan
"""


"""
Finding corrolations between scenarios
"""




import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)  # Reset to Matplotlib defaults



def plot_scenario_correlations_sns(fully_enhanced_arrays, annot_fontsize=12, label_fontsize=14, title_fontsize=18):
    """
    Plot a heatmap showing correlations between scenarios based on numeric features,
    with increased font sizes for better readability.

    Parameters:
    - fully_enhanced_arrays (dict): Dictionary where keys are scenario names and
      values are DataFrames with numeric features.

    Returns:
    - scenario_corr (pd.DataFrame): Correlation matrix between scenarios.
    """
    scenario_vectors = {}

    # Extract and flatten numeric arrays
    for scenario, df in fully_enhanced_arrays.items():
        arr = df.select_dtypes(include=[float, int]).values.flatten()
        scenario_vectors[scenario] = arr

    # Align all vectors to the shortest length
    min_len = min(len(arr) for arr in scenario_vectors.values())
    for k in scenario_vectors:
        scenario_vectors[k] = scenario_vectors[k][:min_len]

    # Create DataFrame from aligned vectors
    scenario_matrix = pd.DataFrame(scenario_vectors)

    # Compute correlation matrix
    scenario_corr = scenario_matrix.corr()

    # Plot heatmap with larger fonts
    plt.figure(figsize=(18, 18))
    sns.set(font_scale=1.4)  # General scaling
    ax = sns.heatmap(
        scenario_corr,
        annot=True,
        fmt=".2f",
        cmap="viridis",
        annot_kws={"size": annot_fontsize},
        cbar_kws={"shrink": 0.8, "label": "Correlation"}
    )
    ax.set_title("Correlation Between Scenarios (All Numeric Features)", fontsize=title_fontsize)
    ax.set_xlabel("Scenario", fontsize=label_fontsize)
    ax.set_ylabel("Scenario", fontsize=label_fontsize)
    ax.tick_params(axis='both', which='major', labelsize=label_fontsize)

    # Also set colorbar font size
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=label_fontsize)
    cbar.set_label("Correlation", size=label_fontsize)

    plt.tight_layout()
    plt.show()

    return scenario_corr





import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_scenario_correlations(fully_enhanced_arrays, annot_fontsize=12, label_fontsize=14, title_fontsize=18):
    """
    Plot a heatmap showing correlations between scenarios based on numeric features,
    using matplotlib only (no seaborn).

    Parameters:
    - fully_enhanced_arrays (dict): keys are scenario names; values are DataFrames with numeric features.

    Returns:
    - scenario_corr (pd.DataFrame): Correlation matrix between scenarios.
    """
    scenario_vectors = {}

    # Extract and flatten numeric arrays
    for scenario, df in fully_enhanced_arrays.items():
        arr = df.select_dtypes(include=[float, int]).values.flatten()
        scenario_vectors[scenario] = arr

    # Align all vectors to the shortest length
    min_len = min(len(arr) for arr in scenario_vectors.values())
    for k in scenario_vectors:
        scenario_vectors[k] = scenario_vectors[k][:min_len]

    # Create DataFrame from aligned vectors
    scenario_matrix = pd.DataFrame(scenario_vectors)

    # Compute correlation matrix
    scenario_corr = scenario_matrix.corr()

    # --- Plot with matplotlib only ---
    fig, ax = plt.subplots(figsize=(18, 18))

    im = ax.imshow(scenario_corr.values, interpolation='nearest', cmap='viridis', vmin=-1, vmax=1)
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.ax.tick_params(labelsize=label_fontsize)
    cbar.set_label("Correlation", size=label_fontsize)

    # Axis ticks and labels
    labels = scenario_corr.columns.tolist()
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, fontsize=label_fontsize, rotation=45, ha='right')
    ax.set_yticklabels(labels, fontsize=label_fontsize)

    # Titles and axes labels
    ax.set_title("Correlation Between Scenarios (All Numeric Features)", fontsize=title_fontsize, pad=12)
    ax.set_xlabel("Scenario", fontsize=label_fontsize)
    ax.set_ylabel("Scenario", fontsize=label_fontsize)

    # Grid-like separators (optional)
    ax.set_xticks(np.arange(-.5, len(labels), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(labels), 1), minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=0.5)
    ax.tick_params(which="minor", bottom=False, left=False)

    # Annotate each cell
    data = scenario_corr.values
    nrows, ncols = data.shape
    for i in range(nrows):
        for j in range(ncols):
            ax.text(j, i, f"{data[i, j]:.2f}",
                    ha="center", va="center", fontsize=annot_fontsize, color="black")

    fig.tight_layout()
    plt.show()

    return scenario_corr







# ----------------------------------------------------------
# ----------------------------------------------------------


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler




import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

def plot_scenario_correlations_better(
    fully_enhanced_arrays,
    annot_fontsize=12,
    label_fontsize=14,
    title_fontsize=18,
    scale_features=True,
    return_matrix=True
):
    """
    Computes and plots a heatmap of scenario correlations with robust alignment and feature scaling,
    using matplotlib only (no seaborn).
    """
    # Step 1: Collect and align numeric DataFrames
    scenario_names = list(fully_enhanced_arrays.keys())
    numeric_dfs = []
    for scenario in scenario_names:
        df = fully_enhanced_arrays[scenario]
        # Sort rows and columns for strict alignment
        df_sorted = df.sort_values(['Region', 'Technology']).sort_index(axis=1)
        numeric_df = df_sorted.select_dtypes(include=[np.number])
        numeric_dfs.append(numeric_df)
    
    # Step 2: Restrict to common columns (features) across all scenarios
    common_columns = set(numeric_dfs[0].columns)
    for df in numeric_dfs[1:]:
        common_columns &= set(df.columns)
    common_columns = sorted(list(common_columns))
    numeric_dfs = [df[common_columns] for df in numeric_dfs]

    # Step 3: Check that all shapes match, restrict to minimum shape if not
    nrows = min(df.shape[0] for df in numeric_dfs)
    ncols = len(common_columns)
    numeric_dfs = [df.iloc[:nrows, :] for df in numeric_dfs]

    # Step 4: Feature scaling (z-score per feature, per scenario)
    arrs = []
    if scale_features:
        for df in numeric_dfs:
            scaler = StandardScaler()
            arr = scaler.fit_transform(df.values)  # shape: (nrows, ncols)
            arrs.append(arr.flatten())
    else:
        arrs = [df.values.flatten() for df in numeric_dfs]

    # Step 5: Build matrix for correlation
    scenario_matrix = pd.DataFrame({k: v for k, v in zip(scenario_names, arrs)})

    # Step 6: Compute correlation matrix
    scenario_corr = scenario_matrix.corr()

    # Step 7: Plot heatmap with matplotlib
    fig, ax = plt.subplots(figsize=(12, 12))
    im = ax.imshow(scenario_corr.values, interpolation='nearest', cmap='viridis', vmin=-1, vmax=1)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.ax.tick_params(labelsize=label_fontsize)
    cbar.set_label("Correlation", size=label_fontsize)

    # Axis ticks and labels
    labels = scenario_corr.columns.tolist()
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, fontsize=label_fontsize, rotation=45, ha='right')
    ax.set_yticklabels(labels, fontsize=label_fontsize)

    # Title and axis labels
    ax.set_title("Correlation Between Scenarios (Aligned, Scaled Numeric Features)", fontsize=title_fontsize, pad=16)
    ax.set_xlabel("Scenario", fontsize=label_fontsize)
    ax.set_ylabel("Scenario", fontsize=label_fontsize)

    # Grid-like separators
    ax.set_xticks(np.arange(-.5, len(labels), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(labels), 1), minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=0.5)
    ax.tick_params(which="minor", bottom=False, left=False)

    # Cell annotations
    data = scenario_corr.values
    nrows_corr, ncols_corr = data.shape
    for i in range(nrows_corr):
        for j in range(ncols_corr):
            ax.text(j, i, f"{data[i, j]:.2f}", ha="center", va="center",
                    fontsize=annot_fontsize, color="black")

    fig.tight_layout()
    plt.show()

    if return_matrix:
        return scenario_corr







def plot_scenario_correlations_better_sns(
    fully_enhanced_arrays,
    annot_fontsize=12,
    label_fontsize=14,
    title_fontsize=18,
    scale_features=True,
    return_matrix=True
):
    """
    Computes and plots a heatmap of scenario correlations with robust alignment and feature scaling.
    
    Parameters
    ----------
    fully_enhanced_arrays : dict
        Dict where keys are scenario names and values are DataFrames (must have identical structure).
    annot_fontsize : int
        Font size for heatmap annotation numbers.
    label_fontsize : int
        Font size for axis labels and tick labels.
    title_fontsize : int
        Font size for the plot title.
    scale_features : bool
        If True, applies z-score normalization per feature before flattening.
    return_matrix : bool
        If True, returns the scenario correlation matrix as a DataFrame.
    
    Returns
    -------
    scenario_corr : pd.DataFrame
        DataFrame containing the correlation matrix between scenarios.
    """
    # Step 1: Collect and align numeric DataFrames
    scenario_names = list(fully_enhanced_arrays.keys())
    numeric_dfs = []
    for scenario in scenario_names:
        df = fully_enhanced_arrays[scenario]
        # Sort rows and columns for strict alignment
        df_sorted = df.sort_values(['Region', 'Technology']).sort_index(axis=1)
        numeric_df = df_sorted.select_dtypes(include=[np.number])
        numeric_dfs.append(numeric_df)
    
    # Step 2: Restrict to common columns (features) across all scenarios
    common_columns = set(numeric_dfs[0].columns)
    for df in numeric_dfs[1:]:
        common_columns &= set(df.columns)
    common_columns = sorted(list(common_columns))
    numeric_dfs = [df[common_columns] for df in numeric_dfs]

    # Step 3: Check that all shapes match, restrict to minimum shape if not
    nrows = min(df.shape[0] for df in numeric_dfs)
    ncols = len(common_columns)
    numeric_dfs = [df.iloc[:nrows, :] for df in numeric_dfs]

    # Step 4: Feature scaling (z-score per feature, per scenario)
    # Option 1: Scale per-scenario (across all their rows)
    arrs = []
    if scale_features:
        for df in numeric_dfs:
            scaler = StandardScaler()
            arr = scaler.fit_transform(df.values)  # shape: (nrows, ncols)
            arrs.append(arr.flatten())
    else:
        arrs = [df.values.flatten() for df in numeric_dfs]

    # Step 5: Build matrix for correlation
    scenario_matrix = pd.DataFrame(
        {k: v for k, v in zip(scenario_names, arrs)}
    )

    # Step 6: Compute correlation matrix
    scenario_corr = scenario_matrix.corr()

    # Step 7: Plot heatmap with robust fonts, ticks, and colorbar
    plt.figure(figsize=(12, 12))
    sns.set(font_scale=1.4)
    ax = sns.heatmap(
        scenario_corr,
        annot=True,
        fmt=".2f",
        cmap="viridis",
        annot_kws={"size": annot_fontsize},
        cbar_kws={"shrink": 0.8, "label": "Correlation"}
    )
    ax.set_title("Correlation Between Scenarios (Aligned, Scaled Numeric Features)", fontsize=title_fontsize, pad=16)
    ax.set_xlabel("Scenario", fontsize=label_fontsize)
    ax.set_ylabel("Scenario", fontsize=label_fontsize)
    ax.tick_params(axis='both', which='major', labelsize=label_fontsize)
    # Also set colorbar font size
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=label_fontsize)
    cbar.set_label("Correlation", size=label_fontsize)
    plt.tight_layout()
    plt.show()

    if return_matrix:
        return scenario_corr

# ====== Example Usage ======
# scenario_corr = plot_scenario_correlations_better(fully_enhanced_arrays_aliased)




# ----------------------------------------------------------
# ----------------------------------------------------------


from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import numpy as np

def plot_scenario_dendrogram(
    scenario_corr, 
    figsize=(8, 8), 
    title_fontsize=20, 
    label_fontsize=15, 
    tick_fontsize=13,
    line_width=5.5,
    color_threshold=None
):
    """
    Plot a hierarchical clustering dendrogram from a correlation matrix,
    with customizable fonts and line widths.

    Parameters:
    - scenario_corr (pd.DataFrame): Correlation matrix between scenarios.
    - figsize (tuple): Figure size.
    - title_fontsize (int): Font size for the title.
    - label_fontsize (int): Font size for axis labels.
    - tick_fontsize (int): Font size for tick labels.
    - line_width (float): Width of dendrogram lines.
    - color_threshold (float or None): Threshold for color in dendrogram.

    Returns:
    - Z (ndarray): Linkage matrix used for dendrogram.
    """
    import matplotlib as mpl
    mpl.rcParams.update(mpl.rcParamsDefault)  # Reset to Matplotlib defaults
    
    # Compute distance matrix (1 - correlation)
    distance = 1 - scenario_corr
    # Convert to condensed distance matrix for linkage
    condensed_distance = distance.values[np.triu_indices_from(distance, k=1)]

    # Perform hierarchical/agglomerative clustering
    Z = linkage(condensed_distance, method='average')

    # Plot dendrogram
    plt.figure(figsize=figsize)
    dendro = dendrogram(
        Z,
        labels=scenario_corr.columns,
        leaf_rotation=90,
        leaf_font_size=tick_fontsize,
        color_threshold=color_threshold,
        above_threshold_color='black'
    )

    plt.title("Scenario Clustering (Hierarchical Dendrogram)", fontsize=title_fontsize, pad=20)
    plt.xlabel("Scenario", fontsize=label_fontsize, labelpad=10)
    plt.ylabel("Distance", fontsize=label_fontsize, labelpad=10)

    # Increase line widths
    ax = plt.gca()
    for line in ax.get_lines():
        line.set_linewidth(line_width)

    # Increase tick label size (redundant if leaf_font_size above, but ensures y-ticks are bigger too)
    plt.xticks(fontsize=tick_fontsize)
    plt.yticks(fontsize=tick_fontsize)
    plt.tight_layout()
    plt.show()

    return Z



# --------------------------------------------------------
# --------------------------------------------------------

import numpy as np

def find_most_and_least_similar_scenarios(correlation_matrix):
    """
    Identify the most and least similar scenarios based on a correlation matrix.

    Parameters:
    - correlation_matrix (pd.DataFrame): Correlation matrix between scenarios.

    Returns:
    - most_similar (tuple): Pair of most similar scenarios.
    - max_corr (float): Correlation value for most similar pair.
    - least_similar (tuple): Pair of least similar scenarios.
    - min_corr (float): Correlation value for least similar pair.
    """
    # Avoid considering self-correlation by masking the diagonal
    corr_copy = correlation_matrix.copy()
    np.fill_diagonal(corr_copy.values, np.nan)

    # Find max and min correlation pairs
    max_corr = corr_copy.max().max()
    min_corr = corr_copy.min().min()
    most_similar = corr_copy.stack().idxmax()
    least_similar = corr_copy.stack().idxmin()

    print(f"Most similar scenarios: {most_similar} with correlation {max_corr:.4f}")
    print(f"Least similar scenarios: {least_similar} with correlation {min_corr:.4f}")

    return most_similar, max_corr, least_similar, min_corr





import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_costTechFMs_correlation(costTechFMs_dict):
    """
    Compute and plot correlation matrix across scenarios based on `costTechFMs` values.
    """
    scenario_vectors = {}
    
    for scenario, df in costTechFMs_dict.items():
        vec = df["costTechFMs"].values.flatten()
        scenario_vectors[scenario] = vec

    # Align vectors to the shortest length
    min_len = min(len(v) for v in scenario_vectors.values())
    for k in scenario_vectors:
        scenario_vectors[k] = scenario_vectors[k][:min_len]

    scenario_matrix = pd.DataFrame(scenario_vectors)
    corr_matrix = scenario_matrix.corr()

    plt.figure(figsize=(35, 35))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="viridis")
    plt.title("Correlation Between Scenarios (costTechFMs)")
    plt.tight_layout()
    plt.show()

    return corr_matrix


from scipy.cluster.hierarchy import linkage, dendrogram


def plot_scenario_dendrogram_2(correlation_matrix):
    """
    Plot a dendrogram using 1 - correlation as distance metric.
    """
    distance = 1 - correlation_matrix
    Z = linkage(distance, method='average')

    plt.figure(figsize=(20, 12))
    dendrogram(Z, labels=correlation_matrix.columns, leaf_rotation=90)
    plt.title("Scenario Clustering (Hierarchical Dendrogram)")
    plt.tight_layout()
    plt.show()

    return Z


def plot_capAgri_correlation(capAgri_dict):
    """
    Compute and plot correlation matrix across scenarios based on `capAgri` values.
    """
    scenario_vectors = {}
    
    for scenario, df in capAgri_dict.items():
        vec = df["capAgri"].values.flatten()
        scenario_vectors[scenario] = vec

    # Align vectors to the shortest length
    min_len = min(len(v) for v in scenario_vectors.values())
    for k in scenario_vectors:
        scenario_vectors[k] = scenario_vectors[k][:min_len]

    scenario_matrix = pd.DataFrame(scenario_vectors)
    corr_matrix = scenario_matrix.corr()

    plt.figure(figsize=(15, 15))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="viridis")
    plt.title("Correlation Between Scenarios (capAgri)")
    plt.tight_layout()
    plt.show()

    return corr_matrix




def plot_costTechAgri_correlation(capAgri_dict):
    """
    Compute and plot correlation matrix across scenarios based on `costTechAgri` values.
    """
    scenario_vectors = {}
    
    for scenario, df in capAgri_dict.items():
        vec = df["costTechAgri"].values.flatten()
        scenario_vectors[scenario] = vec

    # Align vectors to the shortest length
    min_len = min(len(v) for v in scenario_vectors.values())
    for k in scenario_vectors:
        scenario_vectors[k] = scenario_vectors[k][:min_len]

    scenario_matrix = pd.DataFrame(scenario_vectors)
    corr_matrix = scenario_matrix.corr()

    plt.figure(figsize=(15, 15))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="viridis")
    plt.title("Correlation Between Scenarios (costTechAgri)")
    plt.tight_layout()
    plt.show()

    return corr_matrix






def plot_ghgAbateFMs_correlation(ghgAbateFMs_dict):
    """
    Compute and plot correlation matrix across scenarios based on `ghgAbateFMs` values.
    """
    scenario_vectors = {}
    
    for scenario, df in ghgAbateFMs_dict.items():
        vec = df["ghgAbateTechFMs"].values.flatten()
        scenario_vectors[scenario] = vec

    # Align vectors to the shortest length
    min_len = min(len(v) for v in scenario_vectors.values())
    for k in scenario_vectors:
        scenario_vectors[k] = scenario_vectors[k][:min_len]

    scenario_matrix = pd.DataFrame(scenario_vectors)
    corr_matrix = scenario_matrix.corr()

    plt.figure(figsize=(20, 20))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="viridis")
    plt.title("Correlation Between Scenarios (ghgAbateFMs)")
    plt.tight_layout()
    plt.show()

    return corr_matrix





def plot_ghgAbateTechAgri_correlation(ghgAbateTechAgri_dict):
    """
    Compute and plot correlation matrix across scenarios based on `ghgAbateTechAgri` values.
    """
    scenario_vectors = {}
    
    for scenario, df in ghgAbateTechAgri_dict.items():
        vec = df["ghgAbateTechAgri"].values.flatten()
        scenario_vectors[scenario] = vec

    # Align vectors to the shortest length
    min_len = min(len(v) for v in scenario_vectors.values())
    for k in scenario_vectors:
        scenario_vectors[k] = scenario_vectors[k][:min_len]

    scenario_matrix = pd.DataFrame(scenario_vectors)
    corr_matrix = scenario_matrix.corr()

    plt.figure(figsize=(20, 20))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="viridis")
    plt.title("Correlation Between Scenarios (ghgAbateTechAgri)")
    plt.tight_layout()
    plt.show()

    return corr_matrix





from scipy.cluster.hierarchy import linkage, dendrogram




# --------------------------------------------------------
# --------------------------------------------------------



from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def pca_projection(
    scenario_dict, 
    value_column=None, 
    title="PCA Projection",
    figsize=(18, 12),
    marker_size=150,
    label_fontsize=16,
    text_fontsize=17,
    title_fontsize=22,
    axis_fontsize=18,
    legend_fontsize=15
):
    """
    Apply PCA to input or output vectors of scenario_dict with customizable font and marker sizes.

    Parameters:
    - scenario_dict (dict): Dictionary of DataFrames per scenario.
    - value_column (str or None): If set, extract only this column from each DataFrame (e.g., "costTechFMs").
                                  If None, use all numeric values.
    - title (str): Title of the plot.
    - figsize (tuple): Figure size.
    - marker_size (int): Size of scatter markers.
    - label_fontsize (int): Font size for axis labels.
    - text_fontsize (int): Font size for scenario name annotations.
    - title_fontsize (int): Font size for the plot title.
    - axis_fontsize (int): Font size for axis ticks.
    - legend_fontsize (int): Font size for the legend.
    """
    scenario_vectors = {}

    for scenario, df in scenario_dict.items():
        if value_column:
            vec = df[value_column].values
        else:
            vec = df.select_dtypes(include=[float, int]).values.flatten()
        scenario_vectors[scenario] = vec

    # Align lengths
    min_len = min(len(v) for v in scenario_vectors.values())
    aligned_vectors = {k: v[:min_len] for k, v in scenario_vectors.items()}
    matrix = np.vstack(list(aligned_vectors.values()))
    scenario_names = list(aligned_vectors.keys())

    # PCA to 2D
    pca = PCA(n_components=3)
    projected = pca.fit_transform(matrix)

    # Plot
    plt.figure(figsize=figsize)
    ax = plt.gca()
    for i, name in enumerate(scenario_names):
        ax.scatter(projected[i, 0], projected[i, 1], s=marker_size, label=name)
        ax.text(projected[i, 0], projected[i, 1], name, fontsize=text_fontsize, fontweight='bold')

    ax.set_title(title, fontsize=title_fontsize, pad=20)
    ax.set_xlabel("PC1", fontsize=label_fontsize, labelpad=10)
    ax.set_ylabel("PC2", fontsize=label_fontsize, labelpad=10)
    ax.tick_params(axis='both', which='major', labelsize=axis_fontsize)
    ax.grid(True, linestyle='--', alpha=0.5)

    # Show a legend outside the plot if there are many scenarios
    if len(scenario_names) <= 15:
        ax.legend(fontsize=legend_fontsize, loc='best')
    else:
        ax.legend(fontsize=legend_fontsize, bbox_to_anchor=(1.01, 1), loc='upper left')

    plt.tight_layout()
    plt.show()


#####################################




from sklearn.manifold import MDS
def mds_projection(scenario_dict, value_column=None, title="MDS Projection"):
    import numpy as np
    from sklearn.metrics import pairwise_distances
    vectors = []
    names = []
    for k, df in scenario_dict.items():
        vec = df[value_column].values if value_column else df.select_dtypes(include=[float, int]).values.flatten()
        vectors.append(vec)
        names.append(k)
    min_len = min(len(v) for v in vectors)
    vectors = [v[:min_len] for v in vectors]
    matrix = np.vstack(vectors)
    dist = pairwise_distances(matrix)
    embedding = MDS(n_components=2, dissimilarity='precomputed')
    proj = embedding.fit_transform(dist)
    plt.figure(figsize=(30,15))
    for i, name in enumerate(names):
        plt.scatter(proj[i,0], proj[i,1], s=200)
        plt.text(proj[i,0], proj[i,1], name, fontsize=16, weight='bold')
    plt.title(title, fontsize=20)
    plt.xlabel('MDS1')
    plt.ylabel('MDS2')
    plt.grid(True)
    plt.show()



from sklearn.metrics import silhouette_score, silhouette_samples
def compute_silhouette(scenario_matrix, cluster_labels):
    score = silhouette_score(scenario_matrix, cluster_labels)
    print(f"Mean silhouette score: {score:.3f}")
    return score


# ------------------------------------------------
# ------------------------------------------------

import numpy as np
import pandas as pd
from sklearn.cross_decomposition import CCA
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def scenario_cca(
    input_dict, 
    output_dict, 
    input_value_column=None,
    output_value_column="costTechFMs",
    n_components=2,
    pca_reduce=None,      # Tuple: (n_pca_input, n_pca_output) or None
    plot=True,
    figsize=(10,6),
    annotate_points=True,
):
    """
    Performs Canonical Correlation Analysis (CCA) between scenario inputs and outputs.
    
    Parameters:
        input_dict (dict): scenario_name -> DataFrame of input features
        output_dict (dict): scenario_name -> DataFrame of output (should match inputs)
        input_value_column (str or None): If set, use only this input column; else all numeric features
        output_value_column (str): Column name in output dict (e.g., "costTechFMs")
        n_components (int): Number of CCA canonical dimensions
        pca_reduce (tuple or None): If set, (n_input_PCs, n_output_PCs) to use before CCA
        plot (bool): Whether to plot the canonical variables
        figsize (tuple): Figure size for plot
        annotate_points (bool): Add scenario names to plot

    Returns:
        cca (CCA object)
        X_c (ndarray): Canonical variables for inputs
        Y_c (ndarray): Canonical variables for outputs
        scenario_names (list)
        corrs (list): List of canonical correlations
    """
    # 1. Align scenario names
    scenario_names = sorted(list(set(input_dict) & set(output_dict)))
    if not scenario_names:
        raise ValueError("No overlapping scenario keys between input_dict and output_dict.")

    # 2. Assemble scenario matrices
    input_vectors = []
    output_vectors = []
    for name in scenario_names:
        if input_value_column:
            x = input_dict[name][input_value_column].values.flatten()
        else:
            x = input_dict[name].select_dtypes(include=[float, int]).values.flatten()
        y = output_dict[name][output_value_column].values.flatten()
        min_len = min(len(x), len(y))
        input_vectors.append(x[:min_len])
        output_vectors.append(y[:min_len])

    X = np.stack(input_vectors)
    Y = np.stack(output_vectors)

    # 3. (Optional) PCA reduction
    if pca_reduce:
        n_pca_x, n_pca_y = pca_reduce
        if X.shape[1] > n_pca_x:
            X = PCA(n_components=n_pca_x).fit_transform(X)
        if Y.shape[1] > n_pca_y:
            Y = PCA(n_components=n_pca_y).fit_transform(Y)

    # 4. Standardize (mean 0, std 1) for CCA
    X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-12)
    Y = (Y - Y.mean(axis=0)) / (Y.std(axis=0) + 1e-12)

    # 5. CCA
    cca = CCA(n_components=n_components, max_iter=5000)
    X_c, Y_c = cca.fit_transform(X, Y)

    # 6. Canonical correlations
    corrs = [np.corrcoef(X_c[:,i], Y_c[:,i])[0,1] for i in range(n_components)]

    # 7. Visualization
    if plot:
        plt.figure(figsize=figsize)
        plt.scatter(X_c[:,0], Y_c[:,0], s=120)
        if annotate_points:
            for i, name in enumerate(scenario_names):
                plt.text(X_c[i,0], Y_c[i,0], name, fontsize=12)
        plt.xlabel('Input Canonical Var 1')
        plt.ylabel('Output Canonical Var 1')
        plt.title(f'CCA: Canonical Correlation = {corrs[0]:.2f}')
        plt.grid(True)
        plt.show()

        if n_components >= 2:
            plt.figure(figsize=figsize)
            plt.scatter(X_c[:,1], Y_c[:,1], s=120)
            if annotate_points:
                for i, name in enumerate(scenario_names):
                    plt.text(X_c[i,1], Y_c[i,1], name, fontsize=12)
            plt.xlabel('Input Canonical Var 2')
            plt.ylabel('Output Canonical Var 2')
            plt.title(f'CCA: Canonical Correlation (2nd pair) = {corrs[1]:.2f}')
            plt.grid(True)
            plt.show()

    # 8. Print canonical correlations
    for i, c in enumerate(corrs, 1):
        print(f"Canonical correlation {i}: {c:.4f}")

    return cca, X_c, Y_c, scenario_names, corrs

# Usage example:
# cca, X_c, Y_c, names, corrs = scenario_cca(
#     fully_enhanced_arrays, costTechFMs_dict, 
#     input_value_column=None, output_value_column="costTechFMs", 
#     n_components=2, pca_reduce=None, plot=True)


# ---------------------------------------------------------------
# ---------------------------------------------------------------

import numpy as np
import pandas as pd

def cca_feature_importance(
    cca,                      # fitted CCA object
    scenario_names,           # list of scenario names, as returned by scenario_cca
    fully_enhanced_arrays,    # input scenario dictionary (for feature names)
    costTechFMs_dict,         # output scenario dictionary (for output names)
    pca_X=None,               # fitted PCA object for inputs, or None if not used
    pca_Y=None,               # fitted PCA object for outputs, or None if not used
    canonical_index=0,        # which canonical variate to analyze
    topn=10                   # how many features to display
):
    """
    Returns and prints importance of original input and output features for the given canonical variate.
    
    Parameters:
        cca: trained sklearn CCA object
        scenario_names: names of scenarios (as in scenario_cca return)
        fully_enhanced_arrays: dict of scenario -> input DataFrame
        costTechFMs_dict: dict of scenario -> output DataFrame
        pca_X: fitted PCA object for inputs (or None if not used)
        pca_Y: fitted PCA object for outputs (or None if not used)
        canonical_index: index of canonical dimension (0 for first, 1 for second, etc.)
        topn: number of top features to display

    Returns:
        (input_importance: pd.Series, output_importance: pd.Series)
    """

    # -- Get input feature names
    example_input_df = fully_enhanced_arrays[scenario_names[0]]
    input_feature_names = example_input_df.select_dtypes(include=[float, int]).columns

    # -- Get output feature names (costTechFMs is usually a vector)
    example_output_vec = costTechFMs_dict[scenario_names[0]]["costTechFMs"]
    if hasattr(example_output_vec, "index"):
        output_feature_names = example_output_vec.index
    else:
        output_feature_names = [f"costTechFMs_{i}" for i in range(len(example_output_vec))]

    # -- Map weights back to original input features
    if pca_X is not None:
        # CCA weights are in PCA space: project back to original
        input_weights = np.dot(pca_X.components_.T, cca.x_weights_[:, canonical_index])
    else:
        input_weights = cca.x_weights_[:, canonical_index]

    input_importance = pd.Series(input_weights, index=input_feature_names)
    print(f"\nTop {topn} original input features for canonical variate {canonical_index+1}:")
    print(input_importance.sort_values(key=np.abs, ascending=False).head(topn))

    # -- Map weights back to original output features
    if pca_Y is not None:
        output_weights = np.dot(pca_Y.components_.T, cca.y_weights_[:, canonical_index])
    else:
        output_weights = cca.y_weights_[:, canonical_index]

    output_importance = pd.Series(output_weights, index=output_feature_names)
    print(f"\nTop {topn} original output features for canonical variate {canonical_index+1}:")
    print(output_importance.sort_values(key=np.abs, ascending=False).head(topn))

    return input_importance, output_importance

# Example usage (assume you did pca_X and pca_Y before CCA, or set to None if not used):
# input_importance, output_importance = cca_feature_importance(
#     cca, scenario_names, fully_enhanced_arrays, costTechFMs_dict,
#     pca_X=pca_X, pca_Y=pca_Y, canonical_index=0, topn=10
# )




def cca_feature_importance_flat(
    cca, pca_X, pca_Y, canonical_index=0, topn=10,
    input_vec_length=None, output_vec_length=None
):
    """
    Map CCA weights on PCA components back to original flattened vector indices.
    """
    # Get weights for the chosen canonical dimension
    input_weights = np.dot(pca_X.components_.T, cca.x_weights_[:, canonical_index])
    output_weights = np.dot(pca_Y.components_.T, cca.y_weights_[:, canonical_index])

    # Create generic feature names if not provided
    if input_vec_length is None:
        input_vec_length = input_weights.shape[0]
    if output_vec_length is None:
        output_vec_length = output_weights.shape[0]

    input_indices = [f"input_{i}" for i in range(input_vec_length)]
    output_indices = [f"output_{i}" for i in range(output_vec_length)]

    input_importance = pd.Series(input_weights, index=input_indices)
    output_importance = pd.Series(output_weights, index=output_indices)

    print(f"\nTop {topn} input vector indices for canonical variate {canonical_index+1}:")
    print(input_importance.sort_values(key=np.abs, ascending=False).head(topn))

    print(f"\nTop {topn} output vector indices for canonical variate {canonical_index+1}:")
    print(output_importance.sort_values(key=np.abs, ascending=False).head(topn))

    return input_importance, output_importance

"""
# Usage:
input_imp, output_imp = cca_feature_importance_flat(
    cca, pca_X, pca_Y, canonical_index=0, topn=10,
    input_vec_length=X.shape[1],
    output_vec_length=Y.shape[1]
)
"""

# --------------------------------------------------------
# --------------------------------------------------------


from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def pca_features(df_features, n_components=2):
    numeric_cols = df_features.select_dtypes(include=[np.number]).columns
    X = df_features[numeric_cols].values

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)

    # Plot
    plt.figure(figsize=(8, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.6)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA of Input Features")
    plt.grid(True)
    plt.show()

    return pca, X_pca


def pca_outputs(df_outputs, value_column="costTechFMs", n_components=2):
    pivot = df_outputs.pivot_table(
        index=["r", "techFMs"], columns="year", values=value_column, fill_value=0
    )
    X = pivot.values

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)

    plt.figure(figsize=(8, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.6)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA of Output costTechFMs Over Years")
    plt.grid(True)
    plt.show()

    return pca, X_pca, pivot




def pca_features_per_scenario(feature_dict, n_components=2):
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt

    for scenario, df in feature_dict.items():
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        X = df[numeric_cols].values

        if X.shape[0] > n_components:
            pca = PCA(n_components=n_components)
            X_pca = pca.fit_transform(X)

            plt.figure(figsize=(6, 5))
            plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.6)
            plt.xlabel("PC1")
            plt.ylabel("PC2")
            plt.title(f"PCA: {scenario}")
            plt.grid(True)
            plt.tight_layout()
            plt.show()


import seaborn as sns

def pca_features_colored(df_features, color_by="Region", n_components=2):
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt

    df = df_features.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    X = df[numeric_cols].values

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)

    df_pca = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
    df_pca[color_by] = df[color_by].values

    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df_pca, x="PC1", y="PC2", hue=color_by, palette="tab10", s=40)
    plt.title(f"PCA of Input Features Colored by {color_by}")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()






import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def pca_features_colored_by_region_tech(df_features, n_components=2):
    df = df_features.copy()

    # 1. Select numeric features
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    X = df[numeric_cols].values

    # 2. Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3. PCA
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)

    # 4. Create combined label
    df_pca = pd.DataFrame(X_pca, columns=[f"PC{i+1}" for i in range(n_components)])
    df_pca["Region_Tech"] = df["Region"].astype(str) + "_" + df["Technology"].astype(str)

    # Optional: reduce number of unique labels if too many
    unique_labels = df_pca["Region_Tech"].nunique()
    if unique_labels > 40:
        print(f"⚠️ Warning: {unique_labels} unique Region_Tech labels. Consider filtering or clustering first.")

    # 5. Plot
    plt.figure(figsize=(12, 7))
    sns.scatterplot(data=df_pca, x="PC1", y="PC2", hue="Region_Tech", palette="tab20", s=40, legend=False)
    plt.title("PCA of Input Features Colored by Region and Technology")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return pca, df_pca





import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def pca_outputs_colored_by_region_tech(df_features, n_components=2):
    df = df_features.copy()

    # 1. Select numeric features
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    X = df[numeric_cols].values

    # 2. Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 3. PCA
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)

    # 4. Create combined label
    df_pca = pd.DataFrame(X_pca, columns=[f"PC{i+1}" for i in range(n_components)])
    df_pca["Region_Tech"] = df["r"].astype(str) + "_" + df["techFMs"].astype(str)

    # Optional: reduce number of unique labels if too many
    unique_labels = df_pca["Region_Tech"].nunique()
    if unique_labels > 40:
        print(f"⚠️ Warning: {unique_labels} unique Region_Tech labels. Consider filtering or clustering first.")

    # 5. Plot
    plt.figure(figsize=(12, 7))
    sns.scatterplot(data=df_pca, x="PC1", y="PC2", hue="Region_Tech", palette="tab20", s=40, legend=False)
    plt.title("PCA of Input Features Colored by Region and Technology")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return pca, df_pca


from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def get_pca_embedding(df_features, n_components=5):
    df = df_features.copy()
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    X = df[numeric_cols].values
    X_scaled = StandardScaler().fit_transform(X)

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)

    return X_pca, df  # original df to use labels if needed


from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

def plot_dendrogram_pca(X_pca, labels=None, method='ward'):
    linkage_matrix = linkage(X_pca, method=method)

    plt.figure(figsize=(30, 6))
    dendrogram(linkage_matrix, labels=labels, leaf_rotation=90, leaf_font_size=8)
    plt.title("Hierarchical Clustering Dendrogram (PCA-reduced Features)")
    plt.xlabel("Sample Index or Label")
    plt.ylabel("Distance")
    plt.tight_layout()
    plt.show()



##############################################################


from sklearn.decomposition import KernelPCA
from sklearn.preprocessing import StandardScaler

def kernel_pca_projection_sampled(df_features, color_by="r", kernel="rbf", gamma=1e-4, n_components=2, sample_size=5000):
    df = df_features.copy()

    # Randomly sample without replacement
    df_sampled = df.sample(n=sample_size, random_state=42)

    numeric_cols = df_sampled.select_dtypes(include=[float, int]).columns
    X = df_sampled[numeric_cols].values

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kpca = KernelPCA(n_components=n_components, kernel=kernel, gamma=gamma)
    X_kpca = kpca.fit_transform(X_scaled)

    df_kpca = pd.DataFrame(X_kpca, columns=["KPC1", "KPC2"])
    df_kpca[color_by] = df_sampled[color_by].values

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_kpca, x="KPC1", y="KPC2", hue=color_by, palette="tab10", s=40)
    plt.title(f"Kernel PCA (sampled {sample_size}) - Colored by {color_by}")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()

    return kpca, df_kpca


###############################################################


import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage

def plot_cost_output_correlation_heatmap(correlation_matrix, method='average', figsize=(8, 8), cmap="coolwarm"):
    """
    Plots a clustered heatmap with dendrogram for a cost output correlation matrix.

    Parameters:
    - correlation_matrix (pd.DataFrame): Correlation matrix of cost outputs between scenarios.
    - method (str): Linkage method to use for hierarchical clustering. Default is 'average'.
    - figsize (tuple): Size of the figure. Default is (12, 12).
    - cmap (str): Colormap for the heatmap. Default is 'coolwarm'.

    Returns:
    - linkage_matrix (np.ndarray): Linkage matrix used for clustering.
    """
    sns.set(style="white", font_scale=1.2)

    # Compute linkage matrix
    linkage_matrix = linkage(correlation_matrix, method=method)

    # Create clustermap
    g = sns.clustermap(correlation_matrix,
                       row_linkage=linkage_matrix,
                       col_linkage=linkage_matrix,
                       cmap=cmap,
                       figsize=figsize,
                       center=0.5)

    # Optional: add title to the figure
    g.fig.suptitle("Cost Output Correlation Heatmap with Dendrogram", y=1.02)

    plt.show()
    return linkage_matrix


#############################################################

def generate_pca_summary_text(df_pca_output, top_k=5):
    df_summary = df_pca_output.groupby("Region_Tech")[["PC1", "PC2"]].mean().reset_index()
    top_extremes = df_summary.reindex(df_summary["PC1"].abs().sort_values(ascending=False).head(top_k).index)

    summary_lines = []
    for _, row in top_extremes.iterrows():
        summary_lines.append(
            f"- {row['Region_Tech']}: PC1 = {row['PC1']:.2f}, PC2 = {row['PC2']:.2f}"
        )

    return (
        "Principal Component Analysis reveals that the most significant contributors "
        "to variance in this scenario are:\n" + "\n".join(summary_lines)
    )









