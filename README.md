# RE-LLM: Renewable Energy Language Model — Scenario Analytics & Surrogates

A reproducible pipeline for **scenario generation**, **feature engineering**, **correlation & clustering**, **surrogate modeling (RF/DNN/XGBoost)**, and **LLM-assisted stakeholder querying** for land-based GHG mitigation (LULUCF) and forestry/agriculture technologies.

This repository glues together:

* GAMS outputs (GDX) → tidy CSVs
* Structured feature construction (global/regional trends)
* Scenario similarity analysis (correlations, dendrograms)
* Surrogate models + SHAP explanations
* Natural-language scenario reasoning via an LLM

> **Library code:** reusable modules live in `RenewableEnergyLanguageModel/` (e.g., `/home/forootan/Documents/Mohammad_Sadr_files/RenewableEnergyLanguageModel/RenewableEnergyLanguageModel`).
> **Example script:** `ghg_abate_fms_feature_analysis_final.py` demonstrates end-to-end usage.

---

## 📦 Repository layout

```
.
├── agri_caps_feature_analysis.py / _final.py
├── cost_tech_agri_feature_analysis.py / _final.py
├── cost_tech_fm_feature_analysis.py / _mining_final.py
├── fm_caps_feature_analysis_dnn.py / _random_forest.py / _xgboost.py
├── fm_management_feature_analysis.py
├── forest_management_capacity_random_forest_final.py
├── ghg_abate_fms_feature_analysis_final.py      ← start here (full pipeline example)
├── ghg_abate_fms_feature_analysis_random_forest.py
├── ghgAbate_tech_agri_feature_analysis_final.py
├── plots/                                       ← auto-saved figures
├── correlation_matrices/                         ← saved correlation CSVs
├── data/  data_agri/                             ← extracted CSVs / ML datasets
├── scenarios_neg_emi/                            ← base_scenario.gdx + Results_*.gdx
├── shap_outputs/                                 ← SHAP values/plots (optional)
├── Temporary_backups/
└── RenewableEnergyLanguageModel/
    ├── correlations_module.py
    ├── feature_construction_fm.py
    ├── gdx_to_csv_function.py
    ├── llm_scenario_query.py
    ├── loading_saving_parms_from_gdx_csv.py
    ├── random_forest_module.py
    ├── scenario_generator.py
    ├── utiles.py
    └── visualization_dataset_benopex.py
```

### Key modules (import as `RenewableEnergyLanguageModel.<module>`)

* `scenario_generator.py`

  * `GDXScaler`: scale base GDX symbols to generate perturbed scenarios
  * `build_scenario_hierarchy(...)`: organize datasets into scenario groups
* `loading_saving_parms_from_gdx_csv.py`

  * `load_and_save_selected_symbols(...)`: export selected GDX symbols to CSV
* `utiles.py`

  * `load_and_rename_csvs(...)`, `get_dynamic_rename_mapping_fixed(...)`
  * `process_all_results_scenarios(...)`
  * `enhance_with_global_trends_from_scenarios(...)`
  * `enhance_with_region_level_features(...)`
  * `parse_scenario_keys(...)`, `replace_dict_keys(...)`
* `gdx_to_csv_function.py`

  * `extract_gdx_results(...)`, `build_input_output_pairs(...)`
* `correlations_module.py`

  * `plot_scenario_correlations`, `plot_scenario_dendrogram`
  * `plot_ghgAbateFMs_correlation`, `plot_cost_output_correlation_heatmap`
  * `find_most_and_least_similar_scenarios`, `generate_pca_summary_text`
* `random_forest_module.py`

  * `train_and_predict_ghgAbateFMs_ensemble(...)`, `compute_ensemble_shap(...)`
* `llm_scenario_query.py`

  * `interpret_stakeholder_query_with_prompt(...)`: ground “what-if” queries in your scenario clusters/correlations

---

## ⚙️ Requirements

* Python 3.10+ (tested with Conda env `elm`)
* GAMS/GDX tools (needed only to generate/scale new scenarios)
* Python packages:

  * `gdxpds`, `pandas`, `numpy`, `scikit-learn`, `xgboost`
  * `matplotlib`, `seaborn`
  * (optional) `openai` (or compatible client) for LLM demo

**Quick setup**

```bash
conda create -n elm python=3.10 -y
conda activate elm
pip install pandas numpy scikit-learn xgboost matplotlib seaborn gdxpds openai
```

---

## 📂 Data & paths

* **Input GDX**: `scenarios_neg_emi/base_scenario.gdx`
* **Scenario results (GDX)**: `scenarios_neg_emi/Results_dataset_scenarios/Results_<SUFFIX>.gdx`
* **Extracted CSVs (inputs)**: `scenarios_neg_emi/csv_outputs/`
* **ML datasets (outputs)**: `RenewableEnergyLanguageModel/data/Results_<SUFFIX>/...`

Adjust paths inside scripts if your working directory differs.

---

## 🚀 Quick start (full pipeline)

### 1) Run the example

`ghg_abate_fms_feature_analysis_final.py` executes:

* (Optional) Scenario scaling with `GDXScaler`
* Export selected symbols → CSVs
* Build scenario hierarchy & enhanced feature sets
* Extract outputs from `Results_*.gdx`
* Correlation heatmaps & hierarchical clustering
* Ensemble surrogate training & evaluation
* (Optional) LLM stakeholder query

```bash
python ghg_abate_fms_feature_analysis_final.py
```

**Outputs**

* `plots/` — correlation heatmaps & dendrograms
* `correlation_matrices/` — input/output correlation CSVs
* Console — metrics (R²/RMSE); optional LLM answer if configured

### 2) Optional: LLM demo

Use environment variables (don’t hard-code tokens):

```bash
export OPENAI_API_KEY="YOUR_TOKEN"
export OPENAI_API_BASE="https://your-llm-endpoint.example.com/v1"
```

The helper builds a grounded prompt using scenario clusters/correlations and prints the model’s response.

---

## 🧩 Pipeline overview

1. **Scenario generation (optional)**: scale selected symbols (e.g., `CO2price`, `FMsgrowth`, `BeechArea0`, `GrassArea0`, cost/target parameters) → perturbed scenarios with descriptive filenames.
2. **Extraction**:

   * Inputs → CSV via `load_and_save_selected_symbols(...)`
   * Outputs → CSV via `extract_gdx_results(...)`
3. **Feature engineering**: per-(Region, Technology) trends (initial/final/slope), global policy signals, regional static features; Min-Max scaling for numerics.
4. **Scenario similarity**: correlation matrices, dendrograms, and heatmaps for inputs and outputs.
5. **Surrogate modeling + SHAP**: K-fold ensembles (RF/XGB/DNN), evaluate R²/RMSE, optional SHAP attributions.
6. **LLM-assisted queries (optional)**: map natural-language “what-if” to nearest scenarios/clusters and construct a data-grounded prompt.

---

## 🖥️ Minimal usage example (RF)

```python
from RenewableEnergyLanguageModel.loading_saving_parms_from_gdx_csv import load_and_save_selected_symbols
from RenewableEnergyLanguageModel.scenario_generator import build_scenario_hierarchy
from RenewableEnergyLanguageModel.gdx_to_csv_function import extract_gdx_results
from RenewableEnergyLanguageModel.utiles import (
    load_and_rename_csvs, get_dynamic_rename_mapping_fixed,
    process_all_results_scenarios, enhance_with_global_trends_from_scenarios,
    enhance_with_region_level_features
)
from RenewableEnergyLanguageModel.random_forest_module import train_and_predict_ghgAbateFMs_ensemble

# 1) Export selected symbols from scenario GDX to CSV
gdx_dir = "scenarios_neg_emi/dataset_scenarios"
save_dir = "scenarios_neg_emi/csv_outputs"
target_symbols = ["CO2price","FMsgrowth","BeechArea0","ghgTargetLULUCF",
                  "costInvLevelFMs","costMargFMs","costInvFMs","ghgFMs","GrassArea0"]
load_and_save_selected_symbols(gdx_dir, target_symbols, save_path=save_dir)

# 2) Load/rename CSVs and build scenario hierarchy
datasets = load_and_rename_csvs(save_dir)
for k, df in datasets.items():
    rename = get_dynamic_rename_mapping_fixed(k)
    if rename:
        df.rename(columns=rename, inplace=True)
scenarios = build_scenario_hierarchy(datasets)

# 3) Build enhanced features & align outputs
merged = process_all_results_scenarios(scenarios, "scenarios_neg_emi/Results_dataset_scenarios")
enh = enhance_with_global_trends_from_scenarios(merged, scenarios)
features = enhance_with_region_level_features(enh, scenarios, region_feature_keys=["BeechArea0","GrassArea0"])

# 4) Train ensemble RF (see full script for concatenation across scenarios)
res = train_and_predict_ghgAbateFMs_ensemble(
    df_targets=...,   # concatenated outputs across scenarios
    df_features=...,  # concatenated enhanced features
    n_folds=30
)
print(res["metrics"])
```

---

## 🧪 Reproducibility

* Fix random seeds in training scripts for fair comparisons.
* Keep scenario filenames deterministic—they act as keys.
* Export correlation CSVs (`correlation_matrices/*.csv`) for auditing and paper figures.
* Avoid committing large intermediates or private GDX files.

---

## 🔐 Security & secrets

Use environment variables for API keys:

```bash
export OPENAI_API_KEY="..."
export OPENAI_API_BASE="https://..."
```

Never commit tokens or private endpoints.

---

## 📈 Outputs

* **Figures:** `plots/` (heatmaps, dendrograms)
* **Matrices:** `correlation_matrices/` (CSV)
* **SHAP (optional):** `shap_outputs/`

---

## 📄 Citation

If you use this repository or the RE-LLM workflow in academic work, please cite the accompanying manuscript (add bib entry here).

---

## 📝 License

Add a `LICENSE` file (e.g., MIT or Apache-2.0).

---

## 🙌 Acknowledgments

This work integrates optimization outputs (GAMS), data engineering, ML surrogates, and LLMs to make complex scenario outcomes accessible to stakeholders.

