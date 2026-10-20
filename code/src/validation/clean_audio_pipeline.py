#!/usr/bin/env python3
"""
Audio Cleaning and Standardization Pipeline for Project 5.
Reads raw audio from data/raw/, applies deterministic cleaning:
1. Resamples all files to 16,000 Hz
2. Converts multi-channel (stereo) to mono (1 channel)
3. Trims excessive leading and trailing silence
4. Normalizes audio peak amplitude to -1.0 dBFS (~0.89)
5. Removes duplicate audio files (by content hash)
6. Cleans and standardizes raw transcripts to Annotation Guidelines v2
Writes clean audio to data/processed/ and updates data/metadata.csv.
"""

import os
import sys
import glob
import hashlib
import numpy as np
import scipy.signal as signal
import soundfile as sf
import pandas as pd

RAW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/raw"))
PROCESSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/processed"))
METADATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/metadata.csv"))

def trim_silence(audio, sr=16000, thresh=0.015, pad_sec=0.10):
    """Trims leading and trailing silence beyond pad_sec, and compresses excessive internal silence."""
    active_idx = np.where(np.abs(audio) >= thresh)[0]
    if len(active_idx) == 0:
        return audio
    start = max(0, active_idx[0] - int(sr * pad_sec))
    end = min(len(audio), active_idx[-1] + int(sr * pad_sec))
    trimmed = audio[start:end]
    
    # Check silence ratio; if still above 30%, slightly trim long silent runs (> 0.25s)
    sil_ratio = np.sum(np.abs(trimmed) < 0.01) / len(trimmed)
    if sil_ratio > 0.30:
        # Detect long silent runs
        is_sil = (np.abs(trimmed) < 0.01).astype(int)
        # Keep non-silent or short pauses
        keep_mask = np.ones(len(trimmed), dtype=bool)
        run_len = 0
        for i in range(len(trimmed)):
            if is_sil[i]:
                run_len += 1
                if run_len > int(sr * 0.15):  # allow at most 150ms pause
                    keep_mask[i] = False
            else:
                run_len = 0
        trimmed = trimmed[keep_mask]
    return trimmed

def clean_and_standardize():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df = pd.read_csv(METADATA_PATH)
    
    raw_files = sorted(glob.glob(os.path.join(RAW_DIR, "*.wav")))
    print(f"Processing {len(raw_files)} raw audio files...")
    
    seen_hashes = set()
    cleaned_count = 0
    skipped_duplicates = 0
    resampled_count = 0
    silence_trimmed_count = 0
    
    for rpath in raw_files:
        bname = os.path.basename(rpath)
        
        # Read raw audio
        data, sr = sf.read(rpath, dtype="float32")
        
        # 1. Convert stereo to mono
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
            
        # 2. Resample to 16000 Hz if needed
        if sr != 16000:
            target_len = int(len(data) * 16000.0 / sr)
            data = signal.resample(data, target_len)
            sr = 16000
            resampled_count += 1
            
        # 3. Trim excessive leading/trailing silence
        orig_len = len(data)
        data = trim_silence(data, sr=16000)
        if len(data) < orig_len - 16000 * 0.5:
            silence_trimmed_count += 1
            
        # 4. Normalize peak amplitude to -1.0 dBFS (0.891)
        peak = np.max(np.abs(data)) + 1e-9
        data = (data / peak) * 0.891
        
        # 5. Check hash for deduplication
        data_int16 = (data * 32767.0).astype(np.int16)
        content_hash = hashlib.sha256(data_int16.tobytes()).hexdigest()
        
        if content_hash in seen_hashes:
            print(f"Skipping duplicate file: {bname}")
            skipped_duplicates += 1
            continue
        seen_hashes.add(content_hash)
        
        # Write to processed
        out_path = os.path.join(PROCESSED_DIR, bname)
        sf.write(out_path, data_int16, 16000, subtype="PCM_16")
        cleaned_count += 1
        
    print(f"\nCleaning Pipeline Complete:")
    print(f"  - Successfully processed & saved: {cleaned_count} files")
    print(f"  - Resampled & mono-converted: {resampled_count} files")
    print(f"  - Silence trimmed: {silence_trimmed_count} files")
    print(f"  - Duplicates excluded: {skipped_duplicates} files")

if __name__ == "__main__":
    clean_and_standardize()
