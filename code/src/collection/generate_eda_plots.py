#!/usr/bin/env python3
"""
Exploratory Data Analysis and Plot Generator for Project 5.
Generates:
1. Duration distribution histogram
2. Estimated SNR distribution by noise condition
3. Domain and language mix distribution
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

METADATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/metadata.csv"))
PLOTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../supporting_files/plots"))
os.makedirs(PLOTS_DIR, exist_ok=True)

df = pd.read_csv(METADATA_PATH)

# Plot 1: Duration Distribution
plt.figure(figsize=(7, 4.5))
plt.hist(df["duration_seconds"], bins=25, color="#2b5c8f", edgecolor="black", alpha=0.85)
plt.axvline(df["duration_seconds"].mean(), color="red", linestyle="--", linewidth=2, label=f"Mean Duration: {df['duration_seconds'].mean():.2f}s")
plt.title("Speech Clip Duration Distribution (720 Helpdesk Clips)", fontsize=12, fontweight="bold")
plt.xlabel("Duration (seconds)", fontsize=10)
plt.ylabel("Number of Clips", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "duration_distribution.png"), dpi=300)
plt.close()

# Plot 2: Estimated SNR by Noise Condition
plt.figure(figsize=(7, 4.5))
conditions = df["noise_condition"].unique()
snr_data = [df[df["noise_condition"] == c]["estimated_snr_db"] for c in conditions]
plt.boxplot(snr_data, tick_labels=[c.replace("_", "\n") for c in conditions], patch_artist=True,
            boxprops=dict(facecolor="#5da5da", color="black"),
            medianprops=dict(color="darkred", linewidth=2))
plt.title("Acoustic SNR Distribution Across Recording Environments", fontsize=12, fontweight="bold")
plt.xlabel("Environmental Noise Condition", fontsize=10)
plt.ylabel("Estimated SNR (dB)", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "snr_distribution.png"), dpi=300)
plt.close()

# Plot 3: Domain and Language Distribution
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

domain_counts = df["intent_domain"].value_counts()
ax1.bar(domain_counts.index, domain_counts.values, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"], edgecolor="black")
ax1.set_title("Clips per Administrative Domain", fontsize=11, fontweight="bold")
ax1.set_ylabel("Count", fontsize=10)
ax1.set_xticks(range(len(domain_counts)))
ax1.set_xticklabels([d.replace("_", "\n") for d in domain_counts.index], rotation=0, fontsize=9)
ax1.grid(True, linestyle="--", alpha=0.4)

lang_counts = df["language_mix"].value_counts()
ax2.bar(lang_counts.index, lang_counts.values, color=["#9467bd", "#8c564b", "#e377c2", "#7f7f7f"], edgecolor="black")
ax2.set_title("Clips by Language Mix", fontsize=11, fontweight="bold")
ax2.set_ylabel("Count", fontsize=10)
ax2.set_xticks(range(len(lang_counts)))
ax2.set_xticklabels(lang_counts.index, rotation=25, ha="right", fontsize=9)
ax2.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "domain_language_distribution.png"), dpi=300)
plt.close()

print(f"All EDA plots saved to {PLOTS_DIR}")
