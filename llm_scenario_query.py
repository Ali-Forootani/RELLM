#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 23 12:36:30 2025

@author: forootan
"""



import numpy as np
from scipy.cluster.hierarchy import fcluster

def interpret_stakeholder_query_with_prompt(
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
