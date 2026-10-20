#!/usr/bin/env python3
"""
Leakage-Free Dataset Splitter for Project 5 (Part E).
Creates disjoint speaker partitions:
- Train: SPK01 - SPK08 (360 clips, Cohort A, 8 speakers)
- Validation: SPK09 - SPK10 (90 clips, Cohort A, 2 speakers)
- In-Distribution Test: SPK11 - SPK12 (90 clips, Cohort A, 2 speakers)
- Out-of-Distribution Shifted Test (Cohort B): SPK13 - SPK16 (180 clips, 4 speakers, out-of-region accents)

Guarantees 0% speaker overlap between all splits.
"""

import os
import pandas as pd

METADATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/metadata.csv"))
SPLITS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/splits"))
os.makedirs(SPLITS_DIR, exist_ok=True)

df = pd.read_csv(METADATA_PATH)

train_spk = [f"SPK{i:02d}" for i in range(1, 9)]
val_spk = ["SPK09", "SPK10"]
test_id_spk = ["SPK11", "SPK12"]
shifted_spk = ["SPK13", "SPK14", "SPK15", "SPK16"]

train_df = df[df["speaker_id"].isin(train_spk)].copy().reset_index(drop=True)
val_df = df[df["speaker_id"].isin(val_spk)].copy().reset_index(drop=True)
test_id_df = df[df["speaker_id"].isin(test_id_spk)].copy().reset_index(drop=True)
shifted_df = df[df["speaker_id"].isin(shifted_spk)].copy().reset_index(drop=True)

train_path = os.path.join(SPLITS_DIR, "train.csv")
val_path = os.path.join(SPLITS_DIR, "val.csv")
test_id_path = os.path.join(SPLITS_DIR, "test_id.csv")
shifted_path = os.path.join(SPLITS_DIR, "test_shifted_cohort_b.csv")

train_df.to_csv(train_path, index=False)
val_df.to_csv(val_path, index=False)
test_id_df.to_csv(test_id_path, index=False)
shifted_df.to_csv(shifted_path, index=False)

print("=" * 60)
print("DATASET SPLITS SUMMARY:")
print("=" * 60)
print(f"Train Set:               {len(train_df):3d} clips | Speakers: {train_spk}")
print(f"Validation Set:          {len(val_df):3d} clips | Speakers: {val_spk}")
print(f"Test Set (In-Dist):      {len(test_id_df):3d} clips | Speakers: {test_id_spk}")
print(f"Test Set (Shifted B):    {len(shifted_df):3d} clips | Speakers: {shifted_spk}")
print(f"Total Clips in Splits:   {len(train_df) + len(val_df) + len(test_id_df) + len(shifted_df):3d} / {len(df)}")
print("-" * 60)

# Verify 0% speaker leakage
spk_sets = {
    "Train": set(train_spk),
    "Validation": set(val_spk),
    "Test_ID": set(test_id_spk),
    "Shifted_Cohort_B": set(shifted_spk)
}

leakage_found = False
names = list(spk_sets.keys())
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        overlap = spk_sets[names[i]].intersection(spk_sets[names[j]])
        if overlap:
            print(f"ERROR: Overlap between {names[i]} and {names[j]}: {overlap}")
            leakage_found = True

if not leakage_found:
    print("VERIFICATION SUCCESSFUL: 0% speaker leakage across all splits!")
print("=" * 60)
