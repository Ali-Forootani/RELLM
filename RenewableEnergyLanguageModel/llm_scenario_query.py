#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 23 12:36:30 2025

@author: forootan
"""


from __future__ import annotations

import numpy as np
from scipy.cluster.hierarchy import fcluster

def interpret_stakeholder_query_with_prompt_2(
    query,
    parsed_dict,
    alias_map,
    reverse_alias_map,
    linkage_matrix,
    correlation_matrix,
    threshold=0.5
):
    """
    Matches a stakeholder query to scenarios, finds their cluster, and prepares an LLM-friendly response.

    Returns:
        {
            "matched_scenarios": [...],
            "cluster_scenarios": [...],
            "summary": "...",
            "llm_prompt": "..."
        }
    """
    # Define interpretable keywords and their scenario param keys
    keywords = {
        "CO2 price": "CO2price",
        "carbon price": "CO2price",
        "FM growth": "FMsgrowth",
        "investment level": "costInvLevelFMs",
        "marginal cost": "costMargFMs",
        "beech area": "BeechArea0",
        "grass area": "GrassArea0"
    }

    direction = -0.2 if "decrease" in query.lower() else 0.2 if "increase" in query.lower() else 0.0

    matched_param = None
    for phrase, param in keywords.items():
        if phrase.lower() in query.lower():
            matched_param = param
            break

    if matched_param is None:
        return {
            "summary": "Could not infer parameter from query.",
            "llm_prompt": "The query could not be interpreted because the parameter was not recognized."
        }

    target_value = 1.0 + direction

    # Step 2: Match scenarios with desired parameter change
    matched_scenarios = []
    for alias, param_dict in parsed_dict.items():
        if matched_param in param_dict and np.isclose(param_dict[matched_param], target_value, atol=0.01):
            matched_scenarios.append(alias)

    if not matched_scenarios:
        return {
            "summary": f"No scenario found for {matched_param} = {target_value}.",
            "llm_prompt": f"No scenario in the database corresponds to a ±20% change in {matched_param}."
        }

    # Step 3: Clustering
    num_scenarios = len(parsed_dict)
    cluster_labels = fcluster(linkage_matrix, t=threshold, criterion='distance')
    scenario_clusters = {alias: cluster_labels[i] for i, alias in enumerate(sorted(parsed_dict))}
    cluster_id = scenario_clusters[matched_scenarios[0]]
    cluster_scenarios = [alias for alias, cl in scenario_clusters.items() if cl == cluster_id]

    # Step 4: Correlation summary
    intra_corr_matrix = correlation_matrix.loc[cluster_scenarios, cluster_scenarios]
    avg_corr = intra_corr_matrix.mean().mean()

    # Step 5: Format LLM-friendly prompt
    scenario_descs = "\n".join(
        f"- {alias} corresponds to: {reverse_alias_map[alias]}" for alias in cluster_scenarios
    )

    llm_prompt = f"""You are a scenario analysis assistant.

The user asked: "{query}"

The matched parameter is: **{matched_param}**  
The parameter is assumed to have changed by **{int(direction * 100)}%**  
The scenario(s) corresponding to this change are: {', '.join(matched_scenarios)}  
These belong to cluster #{cluster_id} (with threshold={threshold})  
The average correlation of output metrics in this cluster is: {avg_corr:.4f}

Scenarios in the same cluster:
{scenario_descs}

Using this information, explain to the stakeholder what the likely implications of the change in {matched_param} are based on the modeled scenarios. Focus on trends in outputs (e.g., costs, emissions, or land use), and mention which other scenario results this is most aligned with.
"""

    summary = (
        f"Matched parameter: '{matched_param}' changed by {int(direction * 100)}%.\n"
        f"Matching scenario(s): {matched_scenarios}.\n"
        f"These belong to cluster #{cluster_id} with average intra-cluster correlation: {avg_corr:.4f}.\n"
        f"Cluster includes: {cluster_scenarios}."
    )

    return {
        "matched_scenarios": matched_scenarios,
        "cluster_scenarios": cluster_scenarios,
        "summary": summary,
        "llm_prompt": llm_prompt
    }



# -------------------------------------------------------------

# -------------------------------------------------------------



import re
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster


# ---------------------------------------------------------------------------
# Helper ─────────────────────────────────────────────────────────────────────
# ---------------------------------------------------------------------------
_CHANGE_REGEX = re.compile(
    r"""(?P<verb>increase|decrease|raise|lower|cut|drop|
          boost|reduce|double|halve)\s*         # action word
          (by\s*)?                              # optional 'by'
          (?P<amount>[-+]?\d*\.?\d+)?\s*        # optional number
          (?P<unit>%|percent|percentage|x|times)? # unit (% or factor)
       """,
    re.IGNORECASE | re.VERBOSE,
)


def _parse_change(query: str) -> float:
    """
    Returns the **multiplicative factor** implied by the query.

    Examples
    --------
    >>> _parse_change("CO2 price increases by 15 %")
    1.15
    >>> _parse_change("halve the investment level")
    0.5
    >>> _parse_change("double marginal cost")
    2.0
    >>> _parse_change("cut carbon price")
    0.8            # default 20 % reduction
    """
    m = _CHANGE_REGEX.search(query)
    if m is None:
        return 1.0  # no change recognised

    verb = m["verb"].lower()
    raw_amount = m["amount"]
    unit = (m["unit"] or "").lower()

    # Default magnitudes when no number supplied
    default_pct = 0.20
    default_factor = 2.0 if verb in {"double"} else 0.5 if verb in {"halve"} else 1.0

    if raw_amount:
        val = float(raw_amount)
        if unit in {"%", "percent", "percentage"}:
            factor = 1.0 + (val / 100.0)
        elif unit in {"x", "times"}:
            factor = val
        else:  # no unit → treat as percent
            factor = 1.0 + (val / 100.0)
    else:
        # no explicit amount
        if verb in {"double"}:
            factor = 2.0
        elif verb in {"halve"}:
            factor = 0.5
        elif verb in {"increase", "raise", "boost"}:
            factor = 1.0 + default_pct
        elif verb in {"decrease", "lower", "cut", "drop", "reduce"}:
            factor = 1.0 - default_pct
        else:
            factor = default_factor

    return factor


# ---------------------------------------------------------------------------
# Main function ──────────────────────────────────────────────────────────────
# ---------------------------------------------------------------------------
def interpret_stakeholder_query_with_prompt_3(
    query: str,
    parsed_dict: Dict[str, Dict[str, float]],
    alias_map: Dict[str, str],
    reverse_alias_map: Dict[str, str],
    linkage_matrix: np.ndarray,
    correlation_matrix: pd.DataFrame,
    threshold: float = 0.5,
    k_nearest: int = 3,
) -> Dict[str, Any]:
    """
    Translate a stakeholder query to model scenarios and craft an LLM prompt.

    Parameters
    ----------
    query
        Free-form stakeholder question (e.g. *“What if CO₂ price doubles?”*)
    parsed_dict
        `{scenario_alias: {param_key: value, ...}, ...}`
    alias_map, reverse_alias_map
        Forward/backward dictionaries returned by your `parse_scenario_keys`.
    linkage_matrix
        SciPy linkage matrix built **in the same order** as `parsed_dict`.
    correlation_matrix
        Square DataFrame (scenario × scenario) of output correlations.
    threshold
        Distance threshold for `fcluster` (defaults to *0.5*).
    k_nearest
        Number of closest scenarios to return when no exact match.

    Returns
    -------
    dict
        Keys: ``matched_scenarios``, ``cluster_scenarios``, ``summary``,
        ``llm_prompt``.
    """
    # 1️⃣  Map human phrases to parameter keys ---------------------------------
    keywords = {
        # CO₂ price
        r"\bco2 price\b|\bcarbon price\b": "CO2price",
        # Forestry management
        r"\bfm growth\b": "FMsgrowth",
        r"\binvest(ment)? level\b": "costInvLevelFMs",
        r"\bmarginal cost\b": "costMargFMs",
        # Land use
        r"\b(beech|beechwood) area\b": "BeechArea0",
        r"\bgrass area\b": "GrassArea0",
    }

    matched_param = None
    for pat, param in keywords.items():
        if re.search(pat, query, flags=re.IGNORECASE):
            matched_param = param
            break

    if matched_param is None:
        return {
            "summary": "❌ Could not infer model parameter from the query.",
            "llm_prompt": (
                "The query could not be interpreted; it does not contain a "
                "recognised parameter keyword."
            ),
        }

    # 2️⃣  Desired parameter value ---------------------------------------------
    factor = _parse_change(query)  # multiplicative factor
    target_value = factor

    # 3️⃣  Find matching or nearest scenarios ----------------------------------
    # Convert to list to lock ordering for linkage consistency
    scenario_names: List[str] = list(parsed_dict.keys())

    values = np.array(
        [
            parsed_dict[alias].get(matched_param, np.nan)
            for alias in scenario_names
        ]
    )

    # filter scenarios that actually define the parameter
    valid_mask = ~np.isnan(values)
    if not valid_mask.any():
        return {
            "summary": f"❌ No scenario defines parameter '{matched_param}'.",
            "llm_prompt": "Parameter was recognised but no scenario contains it.",
        }

    values = values[valid_mask]
    valid_names = np.array(scenario_names)[valid_mask]

    # Absolute difference to target
    diffs = np.abs(values - target_value)
    exact_mask = np.isclose(diffs, 0.0, atol=1e-2)

    if exact_mask.any():
        matched_scenarios = valid_names[exact_mask].tolist()
    else:
        # pick k nearest
        idx_sorted = diffs.argsort()[:k_nearest]
        matched_scenarios = valid_names[idx_sorted].tolist()

    # 4️⃣  Cluster membership ---------------------------------------------------
    cluster_labels = fcluster(linkage_matrix, t=threshold, criterion="distance")
    scenario_clusters = dict(zip(scenario_names, cluster_labels))

    # use first match for cluster id
    cluster_id = scenario_clusters[matched_scenarios[0]]
    cluster_scenarios = [
        name for name, cid in scenario_clusters.items() if cid == cluster_id
    ]

    # 5️⃣  Intra-cluster correlation (exclude self) ----------------------------
    intra_corr = correlation_matrix.loc[cluster_scenarios, cluster_scenarios]
    tri_vals = intra_corr.values[np.triu_indices(len(cluster_scenarios), k=1)]
    avg_corr = float(np.nanmean(tri_vals)) if tri_vals.size else np.nan

    # 6️⃣  Craft human summary --------------------------------------------------
    direction_str = (
        f"{(factor - 1) * 100:+.0f} %" if abs(factor - 1) < 3 else f"×{factor:g}"
    )

    summary = (
        f"Matched parameter **{matched_param}** altered by **{direction_str}**.\n"
        f"Matched scenario(s): {', '.join(matched_scenarios)}.\n"
        f"Cluster #{cluster_id} → contains {len(cluster_scenarios)} scenarios "
        f"(average intra-cluster ρ ≈ {avg_corr:.3f})."
    )

    # 7️⃣  Build the LLM prompt -------------------------------------------------
    scenario_descs = "\n".join(
        f"- {alias} → {reverse_alias_map.get(alias, 'no-desc')}"
        for alias in cluster_scenarios
    )

    llm_prompt = f"""You are a scenario-analysis assistant.

**Stakeholder query**  
> {query}

| Item | Value |
|------|-------|
| Matched parameter | `{matched_param}` |
| Requested change | {direction_str} |
| Matching scenario(s) | {', '.join(matched_scenarios)} |
| Cluster ID (t={threshold}) | {cluster_id} |
| Avg. intra-cluster correlation | {avg_corr:.3f} |

**Scenarios in the same cluster**  
{scenario_descs}

Please explain to the stakeholder the anticipated implications of the change in \
`{matched_param}` on key outputs (costs, emissions, land use, …).  Highlight \
trends shared across the cluster and point out the most closely aligned scenarios."""
    # 8️⃣  Return bundle --------------------------------------------------------
    return {
        "matched_scenarios": matched_scenarios,
        "cluster_scenarios": cluster_scenarios,
        "summary": summary,
        "llm_prompt": llm_prompt,
    }




#--------------------------------------
#--------------------------------------
#--------------------------------------


def fuzzy_parameter_match(query: str, param_keys: List[str], threshold: float = 70) -> str:
    """
    Fuzzy match query tokens to available parameter keys.
    Returns best-matching param_key or None.
    """
    try:
        from rapidfuzz import process
    except ImportError:
        try:
            from fuzzywuzzy import process
        except ImportError:
            raise ImportError("Install rapidfuzz or fuzzywuzzy for fuzzy matching support.")

    # Tokenize query and params to lower
    query_lower = query.lower()
    best_param, best_score = None, 0
    for param in param_keys:
        # Compare each param name with query (could extend to more tokens)
        result = process.extractOne(param.lower(), [query_lower])
        score = result[1] if result else 0
        if score > best_score and score >= threshold:
            best_param, best_score = param, score
    return best_param



import re
import numpy as np
import pandas as pd
from typing import Dict, Any, List
from scipy.cluster.hierarchy import fcluster

def interpret_stakeholder_query_with_prompt(
    query: str,
    parsed_dict: Dict[str, Dict[str, float]],
    alias_map: Dict[str, str],
    reverse_alias_map: Dict[str, str],
    linkage_matrix: np.ndarray,
    correlation_matrix: pd.DataFrame,
    threshold: float = 0.5,
    k_nearest: int = 3,
) -> Dict[str, Any]:
    """
    Translate a stakeholder query to model scenarios and craft an LLM prompt.
    Extended for agri-parameters and improved matching.
    """
    # 1️⃣ Map human phrases to parameter keys ---------------------------------
    keywords = {
        r"\bmarginal (cost|agri|agriculture)\b": "costMargAgri",
        r"\binvest(ment)? (cost|agri|agriculture)\b": "costInvAgri",
        r"\binvest(ment)? level\b": "costInvLevelAgri",
        r"\bghg( emission(s)?)? (agri|agriculture)?\b": "ghgAgri",
        r"\bgrowth\b": "Agrigrowth",
        r"\barea\b": "Agriarea0",
        r"\bpeat( extract(ion)?)?\b": "PeatExtract",
        # Legacy forestry/CO2 patterns for compatibility:
        r"\bco2 price\b|\bcarbon price\b": "CO2price",
        r"\bfm growth\b": "FMsgrowth",
        r"\binvest(ment)? level (fm|forestry)?\b": "costInvLevelFMs",
        r"\bmarginal cost (fm|forestry)?\b": "costMargFMs",
        r"\bbeech(wood)? area\b": "BeechArea0",
        r"\bgrass area\b": "GrassArea0",
    }

    # Try keyword-based matching
    matched_param = None
    for pat, param in keywords.items():
        if re.search(pat, query, flags=re.IGNORECASE):
            matched_param = param
            break

    # Optionally, try fuzzy fallback if no regex matched
    if matched_param is None:
        # Fuzzy fallback (see function #2 below)
        matched_param = fuzzy_parameter_match(query, list(set(keywords.values())))

    if matched_param is None:
        return {
            "summary": "❌ Could not infer model parameter from the query.",
            "llm_prompt": (
                "The query could not be interpreted; it does not contain a "
                "recognised parameter keyword."
            ),
        }

    # 2️⃣ Parse desired parameter change --------------------------------------
    factor = _parse_change(query)  # <--- assumes this is defined elsewhere!
    target_value = factor

    # 3️⃣ Find matching or nearest scenarios ----------------------------------
    scenario_names: List[str] = list(parsed_dict.keys())

    values = np.array(
        [
            parsed_dict[alias].get(matched_param, np.nan)
            for alias in scenario_names
        ]
    )

    valid_mask = ~np.isnan(values)
    if not valid_mask.any():
        return {
            "summary": f"❌ No scenario defines parameter '{matched_param}'.",
            "llm_prompt": "Parameter was recognised but no scenario contains it.",
        }

    values = values[valid_mask]
    valid_names = np.array(scenario_names)[valid_mask]

    diffs = np.abs(values - target_value)
    exact_mask = np.isclose(diffs, 0.0, atol=1e-2)
    if exact_mask.any():
        matched_scenarios = valid_names[exact_mask].tolist()
    else:
        idx_sorted = diffs.argsort()[:k_nearest]
        matched_scenarios = valid_names[idx_sorted].tolist()

    # 4️⃣ Cluster membership ---------------------------------------------------
    cluster_labels = fcluster(linkage_matrix, t=threshold, criterion="distance")
    scenario_clusters = dict(zip(scenario_names, cluster_labels))
    cluster_id = scenario_clusters[matched_scenarios[0]]
    cluster_scenarios = [
        name for name, cid in scenario_clusters.items() if cid == cluster_id
    ]

    # 5️⃣ Intra-cluster correlation --------------------------------------------
    intra_corr = correlation_matrix.loc[cluster_scenarios, cluster_scenarios]
    tri_vals = intra_corr.values[np.triu_indices(len(cluster_scenarios), k=1)]
    avg_corr = float(np.nanmean(tri_vals)) if tri_vals.size else np.nan

    # 6️⃣ Human summary --------------------------------------------------------
    direction_str = (
        f"{(factor - 1) * 100:+.0f} %" if abs(factor - 1) < 3 else f"×{factor:g}"
    )

    summary = (
        f"Matched parameter **{matched_param}** altered by **{direction_str}**.\n"
        f"Matched scenario(s): {', '.join(matched_scenarios)}.\n"
        f"Cluster #{cluster_id} → contains {len(cluster_scenarios)} scenarios "
        f"(average intra-cluster ρ ≈ {avg_corr:.3f})."
    )

    # 7️⃣ Build LLM prompt -----------------------------------------------------
    scenario_descs = "\n".join(
        f"- {alias} → {reverse_alias_map.get(alias, 'no-desc')}"
        for alias in cluster_scenarios
    )

    llm_prompt = f"""You are a scenario-analysis assistant.

**Stakeholder query**  
> {query}

| Item | Value |
|------|-------|
| Matched parameter | `{matched_param}` |
| Requested change | {direction_str} |
| Matching scenario(s) | {', '.join(matched_scenarios)} |
| Cluster ID (t={threshold}) | {cluster_id} |
| Avg. intra-cluster correlation | {avg_corr:.3f} |

**Scenarios in the same cluster**  
{scenario_descs}

Please explain to the stakeholder the anticipated implications of the change in \
`{matched_param}` on key outputs (costs, emissions, land use, …).  Highlight \
trends shared across the cluster and point out the most closely aligned scenarios."""

    return {
        "matched_scenarios": matched_scenarios,
        "cluster_scenarios": cluster_scenarios,
        "summary": summary,
        "llm_prompt": llm_prompt,
    }










































