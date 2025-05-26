#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 15:44:27 2025

@author: forootan
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import numpy as np

def train_and_predict_capFMs(df_capFMs: pd.DataFrame, final_feature_array: pd.DataFrame):
    # Step 1: Cross-join with year
    years_df = pd.DataFrame(df_capFMs["year"].unique(), columns=["year"])
    temp = final_feature_array.copy()
    temp["key"] = 1
    years_df["key"] = 1
    X_all = temp.merge(years_df, on="key").drop("key", axis=1)

    # Step 2: Merge with capFMs target
    df_capFMs_renamed = df_capFMs.rename(columns={
        "techFMs": "Technology",
        "r": "Region"
    })
    training_df = X_all.merge(df_capFMs_renamed, on=["Region", "Technology", "year"], how="left")
    training_df = training_df.dropna(subset=["capFMs"])

    # Step 3: Encode categorical features
    categorical_cols = ["Region", "Technology"]
    encoder = OneHotEncoder(sparse_output=False)
    encoded = encoder.fit_transform(training_df[categorical_cols])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical_cols))

    # Step 4: Assemble input (X) and target (y)
    X = pd.concat([encoded_df, training_df.drop(columns=categorical_cols + ["capFMs"])], axis=1)
    y = training_df["capFMs"]

    # Normalize target
    target_scaler = MinMaxScaler()
    y_scaled = target_scaler.fit_transform(y.values.reshape(-1, 1)).ravel()

    # Step 5: Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y_scaled, test_size=0.1, random_state=42)

    # Step 6: Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Step 7: Predict and evaluate
    y_pred = model.predict(X_test)
    y_pred_original = target_scaler.inverse_transform(y_pred.reshape(-1, 1)).ravel()
    y_test_original = target_scaler.inverse_transform(y_test.reshape(-1, 1)).ravel()

    r2_scaled = r2_score(y_test, y_pred)
    rmse_scaled = np.sqrt(mean_squared_error(y_test, y_pred))
    r2_original = r2_score(y_test_original, y_pred_original)
    rmse_original = np.sqrt(mean_squared_error(y_test_original, y_pred_original))

    return {
        "y_pred_original": y_pred_original,
        "y_test_original": y_test_original,
        "r2_scaled": r2_scaled,
        "rmse_scaled": rmse_scaled,
        "r2_original": r2_original,
        "rmse_original": rmse_original,
        "model": model,
        "encoder": encoder,
        "target_scaler": target_scaler,
        "X_test": X_test,
        "X_train": X_train
    }


from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import numpy as np

def train_and_predict_capFMs_ensemble(
    df_capFMs: pd.DataFrame,
    final_feature_array,
    n_folds: int = 5
):
    # Step 0: Ensure final_feature_array is a DataFrame
    if isinstance(final_feature_array, np.ndarray):
        raise ValueError("final_feature_array is a numpy array. Please convert it to a pandas DataFrame with columns ['Region', 'Technology', feature1, feature2, ...].")
    elif not isinstance(final_feature_array, pd.DataFrame):
        raise ValueError("final_feature_array must be a pandas DataFrame.")

    # Step 1: Cross-join final_feature_array with years
    years_df = pd.DataFrame(df_capFMs["year"].unique(), columns=["year"])
    temp = final_feature_array.copy()
    temp["key"] = 1
    years_df["key"] = 1
    X_all = temp.merge(years_df, on="key").drop("key", axis=1)

    # Step 2: Merge with capFMs target
    df_capFMs_renamed = df_capFMs.rename(columns={
        "techFMs": "Technology",
        "r": "Region"
    })
    training_df = X_all.merge(df_capFMs_renamed, on=["Region", "Technology", "year"], how="left")
    training_df = training_df.dropna(subset=["capFMs"])

    # Step 3: Encode categorical features
    categorical_cols = ["Region", "Technology"]
    encoder = OneHotEncoder(sparse_output=False)
    encoded = encoder.fit_transform(training_df[categorical_cols])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical_cols), index=training_df.index)

    # Step 4: Assemble input (X) and target (y)
    X = pd.concat([encoded_df, training_df.drop(columns=categorical_cols + ["capFMs"])], axis=1)
    y = training_df["capFMs"]

    # Normalize target
    target_scaler = MinMaxScaler()
    y_scaled = target_scaler.fit_transform(y.values.reshape(-1, 1)).ravel()

    # Step 5: Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y_scaled, test_size=0.1, random_state=42)

    # Step 6: Split X_train into n_folds
    indices = np.arange(len(X_train))
    np.random.shuffle(indices)  # shuffle indices first
    fold_sizes = np.full(n_folds, len(X_train) // n_folds, dtype=int)
    fold_sizes[:len(X_train) % n_folds] += 1
    current = 0

    models = []
    for fold_size in fold_sizes:
        start, stop = current, current + fold_size
        fold_idx = indices[start:stop]
        X_fold = X_train.iloc[fold_idx]
        y_fold = y_train[fold_idx]

        model = RandomForestRegressor(n_estimators=50, random_state=42 + len(models))
        model.fit(X_fold, y_fold)
        models.append(model)
        current = stop

    # Step 7: Ensemble prediction
    preds = []
    for model in models:
        preds.append(model.predict(X_test))
    preds = np.array(preds)
    y_pred = preds.mean(axis=0)  # Average voting

    # Unscale
    y_pred_original = target_scaler.inverse_transform(y_pred.reshape(-1, 1)).ravel()
    y_test_original = target_scaler.inverse_transform(y_test.reshape(-1, 1)).ravel()

    # Metrics
    r2_scaled = r2_score(y_test, y_pred)
    rmse_scaled = np.sqrt(mean_squared_error(y_test, y_pred))
    r2_original = r2_score(y_test_original, y_pred_original)
    rmse_original = np.sqrt(mean_squared_error(y_test_original, y_pred_original))

    return {
        "y_pred_original": y_pred_original,
        "y_test_original": y_test_original,
        "r2_scaled": r2_scaled,
        "rmse_scaled": rmse_scaled,
        "r2_original": r2_original,
        "rmse_original": rmse_original,
        "models": models,
        "encoder": encoder,
        "target_scaler": target_scaler,
        "X_test": X_test,
        "X_train": X_train
    }





import shap
import numpy as np

def compute_ensemble_shap(models, X_test, sample_size= 100, n_samples= 10):
    """
    Apply SHAP on random subsets of X_test for each model in the ensemble and aggregate the results.

    Parameters:
    - models: List of trained models (ensemble of RandomForestRegressor).
    - X_test: Test set to be explained.
    - sample_size: Number of samples to take from X_test in each iteration.
    - n_samples: Number of random samples (subsets) to take and apply SHAP.

    Returns:
    - aggregated_shap_values: Aggregated SHAP values across all models and samples.
    """
    all_shap_values = []

    # Loop through each model in the ensemble
    for model_idx, model in enumerate(models):
        shap_values_list = []
        
        # Create a SHAP explainer for tree-based models (using TreeSHAP)
        explainer = shap.TreeExplainer(model)
        
        # Loop through and sample the data
        for _ in range(n_samples):
            # Randomly sample the data
            sampled_indices = np.random.choice(X_test.index, size=sample_size, replace=False)
            X_test_sample = X_test.loc[sampled_indices]
            
            # Compute SHAP values for the sampled data
            shap_values = explainer.shap_values(X_test_sample)
            shap_values_list.append(shap_values)
        
        # Convert the list of SHAP values into a numpy array for easier aggregation
        shap_values_array = np.array(shap_values_list)
        
        # Aggregate SHAP values for the current model by averaging across the samples
        aggregated_shap_values_model = shap_values_array.mean(axis=0)
        
        # Add the aggregated SHAP values for the current model to the overall list
        all_shap_values.append(aggregated_shap_values_model)
    
    # Now aggregate across all models in the ensemble by averaging the SHAP values
    aggregated_shap_values_ensemble = np.mean(np.array(all_shap_values), axis=0)
    
    return aggregated_shap_values_ensemble


##########################################################
##########################################################
##########################################################
##########################################################



from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import numpy as np

def train_and_predict_costTechFMs_ensemble(
    df_costTechFMs: pd.DataFrame,
    final_feature_array_all,
    n_folds: int = 5
):
    # Step 0: Ensure final_feature_array_all is a DataFrame
    if isinstance(final_feature_array_all, np.ndarray):
        raise ValueError("final_feature_array_all is a numpy array. Please convert it to a pandas DataFrame with columns ['Region', 'Technology', feature1, feature2, ...].")
    elif not isinstance(final_feature_array_all, pd.DataFrame):
        raise ValueError("final_feature_array_all must be a pandas DataFrame.")

    # Step 1: Cross-join final_feature_array_all with years
    years_df = pd.DataFrame(df_costTechFMs["year"].unique(), columns=["year"])
    temp = final_feature_array_all.copy()
    temp["key"] = 1
    years_df["key"] = 1
    X_all = temp.merge(years_df, on="key").drop("key", axis=1)

    # Step 2: Merge with costTechFMs target
    df_costTechFMs_renamed = df_costTechFMs.rename(columns={
        "techFMs": "Technology",
        "r": "Region"
    })
    training_df = X_all.merge(df_costTechFMs_renamed, on=["Region", "Technology", "year"], how="left")
    training_df = training_df.dropna(subset=["costTechFMs"])

    # Step 3: Encode categorical features
    categorical_cols = ["Region", "Technology"]
    encoder = OneHotEncoder(sparse_output=False)
    encoded = encoder.fit_transform(training_df[categorical_cols])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical_cols), index=training_df.index)

    # Step 4: Assemble input (X) and target (y)
    X = pd.concat([encoded_df, training_df.drop(columns=categorical_cols + ["costTechFMs"])], axis=1)
    y = training_df["costTechFMs"]

    # Normalize target
    target_scaler = MinMaxScaler()
    y_scaled = target_scaler.fit_transform(y.values.reshape(-1, 1)).ravel()

    # Step 5: Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y_scaled, test_size=0.1, random_state=42)

    # Step 6: Split X_train into n_folds
    indices = np.arange(len(X_train))
    np.random.shuffle(indices)  # shuffle indices first
    fold_sizes = np.full(n_folds, len(X_train) // n_folds, dtype=int)
    fold_sizes[:len(X_train) % n_folds] += 1
    current = 0

    models = []
    for fold_size in fold_sizes:
        start, stop = current, current + fold_size
        fold_idx = indices[start:stop]
        X_fold = X_train.iloc[fold_idx]
        y_fold = y_train[fold_idx]

        #model = RandomForestRegressor(n_estimators=80, random_state=42 + len(models))
        
        model = RandomForestRegressor(
                            n_estimators=50,  # Increase number of trees
                            max_depth=10,      # Set max depth to prevent overfitting
                            min_samples_split=5, # Minimum samples to split a node
                            min_samples_leaf=2,  # Minimum samples required at a leaf node
                            random_state=42 + len(models)
                            )
        
        
        model.fit(X_fold, y_fold)
        models.append(model)
        current = stop

    # Step 7: Ensemble prediction
    preds = []
    for model in models:
        preds.append(model.predict(X_test))
    preds = np.array(preds)
    y_pred = preds.mean(axis=0)  # Average voting

    # Unscale
    y_pred_original = target_scaler.inverse_transform(y_pred.reshape(-1, 1)).ravel()
    y_test_original = target_scaler.inverse_transform(y_test.reshape(-1, 1)).ravel()

    # Metrics
    r2_scaled = r2_score(y_test, y_pred)
    rmse_scaled = np.sqrt(mean_squared_error(y_test, y_pred))
    r2_original = r2_score(y_test_original, y_pred_original)
    rmse_original = np.sqrt(mean_squared_error(y_test_original, y_pred_original))

    return {
        "y_pred_original": y_pred_original,
        "y_test_original": y_test_original,
        "r2_scaled": r2_scaled,
        "rmse_scaled": rmse_scaled,
        "r2_original": r2_original,
        "rmse_original": rmse_original,
        "models": models,
        "encoder": encoder,
        "target_scaler": target_scaler,
        "X_test": X_test,
        "X_train": X_train
    }





















