#!/usr/bin/env python3
"""
Master End-to-End Pipeline Runner for CS 203 Assignment 1.
Project 5: Cross-Lingual Institute Voice Helpdesk with Drift-Triggered Retraining.
Executes the full pipeline sequentially and logs all execution outputs.
"""

import os
import sys
import time
import subprocess

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PYTHON_BIN = sys.executable

def run_step(step_name, command_args):
    print("\n" + "=" * 75)
    print(f"PIPELINE STEP: {step_name}")
    print("=" * 75)
    t0 = time.time()
    res = subprocess.run(command_args, cwd=BASE_DIR)
    elapsed = time.time() - t0
    if res.returncode != 0:
        print(f"ERROR: Step '{step_name}' failed with return code {res.returncode}")
        sys.exit(res.returncode)
    print(f"Step '{step_name}' completed successfully in {elapsed:.2f} seconds.")

def main():
    print("=" * 75)
    print("STARTING COMPLETE CS203 ASSIGNMENT 1 END-TO-END PIPELINE")
    print("=" * 75)
    start_total = time.time()

    # Step 1: Clean and validate processed audio
    run_step("1. Audio Cleaning & Standardization", [PYTHON_BIN, "src/validation/clean_audio_pipeline.py"])

    # Step 2: Split manifests generation
    run_step("2. Leakage-Free Dataset Splitting", [PYTHON_BIN, "src/collection/create_splits.py"])

    # Step 3: Run comprehensive validation suite
    run_step("3. Full Validation Suite (Audio, Metadata, Splits)", [PYTHON_BIN, "src/validation/validate_dataset.py", "../data/processed", "../data/metadata.csv", "../data/splits"])

    # Step 4: Inter-annotator agreement & Gold Test set freezing
    run_step("4. Labelling Agreement & Gold Test Set Freezing", [PYTHON_BIN, "src/labelling/run_agreement_analysis.py"])

    # Step 5: Active learning simulation
    run_step("5. Active Learning vs. Random Selection Simulation", [PYTHON_BIN, "src/active_learning/run_active_learning.py"])

    # Step 6: Consent register & EDA plots
    run_step("6. Consent Register Generation", [PYTHON_BIN, "src/collection/generate_consent_register.py"])
    run_step("7. Exploratory Data Analysis & Plots Generation", [PYTHON_BIN, "src/collection/generate_eda_plots.py"])

    total_time = time.time() - start_total
    print("\n" + "=" * 75)
    print(f"ALL PIPELINE STEPS COMPLETED IN {total_time:.2f} SECONDS!")
    print("Data and supporting artifacts are frozen and ready.")
    print("=" * 75)

if __name__ == "__main__":
    main()
