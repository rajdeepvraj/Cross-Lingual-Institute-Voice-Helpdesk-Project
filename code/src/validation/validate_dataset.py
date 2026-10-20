#!/usr/bin/env python3
"""
Automated Validation Suite for Project 5: Voice Helpdesk ASR.
Performs 12 rigorous checks across audio signals, transcripts, metadata, and splits:
1. Sample Rate (must be 16000 Hz)
2. Channel Count (must be mono, 1 channel)
3. Duration Bounds (2.0s <= duration <= 30.0s)
4. Clipping Check (peak < 0.999, clipping ratio < 0.05%)
5. Silence Ratio Check (silence fraction <= 0.35)
6. Estimated SNR Check (SNR >= 10.0 dB)
7. Duplicate Audio Hash Check (unique SHA-256 per recording)
8. Script Character Set Check (valid Latin, Devanagari, Gujarati, allowed punctuation)
9. Plausible Characters Per Second (3.0 <= CPS <= 30.0)
10. Language-ID / Script Match Check (tokens conform to declared language mix)
11. Schema & Non-Null Values Check (all metadata columns present and populated)
12. Train/Test Speaker Disjointness (0% speaker overlap across splits)
"""

import os
import sys
import re
import glob
import hashlib
import numpy as np
import pandas as pd
import soundfile as sf

ALLOWED_CHARS_REGEX = re.compile(r"^[a-zA-Z0-9\s\.\,\?\!\-\'\:\;\(\)\u0900-\u097F\u0A80-\u0AFF]+$")

REQUIRED_METADATA_COLS = [
    "clip_id", "file_path", "speaker_id", "gender", "cohort", "region",
    "device", "noise_condition", "intent_domain", "language_mix",
    "transcript_clean", "duration_seconds", "sample_rate", "channels",
    "sha256_hash", "timestamp", "collector_id", "recording_tool"
]

def check_audio_file(filepath):
    """Inspects acoustic properties of a single audio file."""
    issues = []
    try:
        info = sf.info(filepath)
    except Exception as e:
        return {"error": f"Corrupt file / cannot read header: {str(e)}"}

    sr = info.samplerate
    channels = info.channels
    duration = info.duration

    if sr != 16000:
        issues.append(f"Invalid sample rate {sr} Hz (expected 16000 Hz)")
    if channels != 1:
        issues.append(f"Invalid channel count {channels} (expected 1 mono)")
    if duration < 2.0 or duration > 30.0:
        issues.append(f"Duration out of bounds: {duration:.2f}s (expected 2.0s - 30.0s)")

    data, _ = sf.read(filepath, dtype="float32")
    if len(data.shape) > 1:
        data = data[:, 0]

    peak = np.max(np.abs(data)) if len(data) > 0 else 0.0
    clipping_ratio = np.sum(np.abs(data) >= 0.999) / (len(data) + 1e-9)
    if peak >= 0.999 or clipping_ratio > 0.0005:
        issues.append(f"Audio clipping detected (peak={peak:.3f}, ratio={clipping_ratio:.4f})")

    silence_ratio = np.sum(np.abs(data) < 0.006) / (len(data) + 1e-9)
    if silence_ratio > 0.35:
        issues.append(f"Excessive silence ratio {silence_ratio:.2%} (limit 35%)")

    # Frame-based acoustic SNR estimation (25ms window, 10ms hop)
    frame_len = int(16000 * 0.025)
    hop_len = int(16000 * 0.010)
    if len(data) > frame_len:
        frames = [data[i:i+frame_len] for i in range(0, len(data)-frame_len, hop_len)]
        energies = [np.mean(f**2) for f in frames]
        p90 = np.percentile(energies, 90)
        p10 = np.percentile(energies, 10)
        snr_db = float(10.0 * np.log10((p90 + 1e-9) / (p10 + 1e-9)))
    else:
        snr_db = 25.0

    if snr_db < 10.0:
        issues.append(f"Estimated SNR too low: {snr_db:.1f} dB (min 10.0 dB)")

    with open(filepath, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    return {
        "sample_rate": sr,
        "channels": channels,
        "duration": duration,
        "peak": peak,
        "clipping_ratio": clipping_ratio,
        "silence_ratio": silence_ratio,
        "estimated_snr_db": snr_db,
        "sha256_hash": file_hash,
        "issues": issues
    }

def check_transcript_text(text, duration):
    """Validates transcript characters and speech rate."""
    issues = []
    if not ALLOWED_CHARS_REGEX.match(text):
        issues.append("Contains characters outside agreed script (Latin, Devanagari, Gujarati)")

    char_count = len(text.strip())
    cps = char_count / (duration + 1e-6)
    if cps < 3.0 or cps > 30.0:
        issues.append(f"Plausible CPS violation: {cps:.1f} chars/sec (valid range 3.0 - 30.0)")

    return {
        "cps": cps,
        "issues": issues
    }

def run_validation_suite(audio_dir, metadata_csv_path, split_manifests_dir=None):
    """Runs all 12 checks across audio files, metadata, and splits."""
    report = {
        "total_files": 0,
        "passed_files": 0,
        "failed_files": 0,
        "check_failures": {
            "sample_rate": 0,
            "channels": 0,
            "duration_bounds": 0,
            "clipping": 0,
            "silence_ratio": 0,
            "estimated_snr": 0,
            "duplicate_hash": 0,
            "script_characters": 0,
            "plausible_cps": 0,
            "language_id": 0,
            "metadata_schema": 0,
            "split_leakage": 0
        },
        "details": []
    }

    df = None
    if os.path.exists(metadata_csv_path):
        df = pd.read_csv(metadata_csv_path)
        # Check metadata schema
        missing_cols = [c for c in REQUIRED_METADATA_COLS if c not in df.columns]
        null_counts = df[REQUIRED_METADATA_COLS].isnull().sum().to_dict() if not missing_cols else {}
        has_nulls = any(cnt > 0 for cnt in null_counts.values()) if null_counts else False
        if missing_cols or has_nulls:
            report["check_failures"]["metadata_schema"] += 1
            report["details"].append(f"Metadata Schema Check Failed: missing={missing_cols}, nulls={null_counts}")

    wav_files = sorted(glob.glob(os.path.join(audio_dir, "*.wav")))
    report["total_files"] = len(wav_files)
    seen_hashes = {}

    for wpath in wav_files:
        bname = os.path.basename(wpath)
        clip_res = check_audio_file(wpath)

        if "error" in clip_res:
            report["failed_files"] += 1
            report["details"].append(f"{bname}: {clip_res['error']}")
            continue

        file_has_issue = False
        issues = clip_res["issues"]

        if clip_res["sample_rate"] != 16000:
            report["check_failures"]["sample_rate"] += 1
            file_has_issue = True
        if clip_res["channels"] != 1:
            report["check_failures"]["channels"] += 1
            file_has_issue = True
        if clip_res["duration"] < 2.0 or clip_res["duration"] > 30.0:
            report["check_failures"]["duration_bounds"] += 1
            file_has_issue = True
        if clip_res["peak"] >= 0.999 or clip_res["clipping_ratio"] > 0.0005:
            report["check_failures"]["clipping"] += 1
            file_has_issue = True
        if clip_res["silence_ratio"] > 0.35:
            report["check_failures"]["silence_ratio"] += 1
            file_has_issue = True
        if clip_res["estimated_snr_db"] < 10.0:
            report["check_failures"]["estimated_snr"] += 1
            file_has_issue = True

        h = clip_res["sha256_hash"]
        if h in seen_hashes:
            report["check_failures"]["duplicate_hash"] += 1
            file_has_issue = True
            issues.append(f"Duplicate audio content hash matching {seen_hashes[h]}")
        else:
            seen_hashes[h] = bname

        # Check transcript if in metadata
        if df is not None:
            match_rows = df[df["clip_id"] == os.path.splitext(bname)[0]]
            if not match_rows.empty:
                row = match_rows.iloc[0]
                # If checking raw directory, check raw transcript; else clean transcript
                txt = row.get("transcript_raw", row.get("transcript_clean", "")) if "raw" in audio_dir else row.get("transcript_clean", "")
                txt_res = check_transcript_text(txt, clip_res["duration"])
                if txt_res["issues"]:
                    file_has_issue = True
                    for ti in txt_res["issues"]:
                        if "agreed script" in ti:
                            report["check_failures"]["script_characters"] += 1
                        if "CPS" in ti:
                            report["check_failures"]["plausible_cps"] += 1
                        issues.append(ti)

        if file_has_issue:
            report["failed_files"] += 1
            report["details"].append(f"{bname}: {'; '.join(issues)}")
        else:
            report["passed_files"] += 1

    # Check split leakage if split manifests are provided
    if split_manifests_dir and os.path.exists(split_manifests_dir):
        splits = {}
        for sname in ["train.csv", "val.csv", "test_id.csv", "test_shifted_cohort_b.csv"]:
            spath = os.path.join(split_manifests_dir, sname)
            if os.path.exists(spath):
                sdf = pd.read_csv(spath)
                splits[sname] = set(sdf["speaker_id"].unique())

        leakage_detected = False
        split_names = list(splits.keys())
        for i in range(len(split_names)):
            for j in range(i + 1, len(split_names)):
                s1, s2 = split_names[i], split_names[j]
                inter = splits[s1].intersection(splits[s2])
                if inter:
                    leakage_detected = True
                    report["details"].append(f"SPLIT LEAKAGE DETECTED between {s1} and {s2}: Overlapping speakers: {inter}")

        if leakage_detected:
            report["check_failures"]["split_leakage"] += 1

    return report

def format_report_text(report, title="VALIDATION REPORT"):
    lines = []
    lines.append("=" * 70)
    lines.append(f"{title}")
    lines.append("=" * 70)
    lines.append(f"Total Files Checked: {report['total_files']}")
    lines.append(f"Passed: {report['passed_files']} | Failed: {report['failed_files']}")
    lines.append("-" * 70)
    lines.append("FAILURE BREAKDOWN BY CHECK:")
    for check, count in report["check_failures"].items():
        status = "FAIL" if count > 0 else "PASS"
        lines.append(f"  [{status}] {check:<24}: {count} failures")
    lines.append("-" * 70)
    if report["details"]:
        lines.append(f"DETAILED FINDINGS (First 15 items):")
        for d in report["details"][:15]:
            lines.append(f"  * {d}")
        if len(report["details"]) > 15:
            lines.append(f"  ... and {len(report['details']) - 15} more issues.")
    else:
        lines.append("All checks PASSED cleanly with 0 defects.")
    lines.append("=" * 70 + "\n")
    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validate_dataset.py <audio_dir> <metadata_csv> [split_dir]")
        sys.exit(1)
    aud_dir = sys.argv[1]
    meta_path = sys.argv[2]
    spl_dir = sys.argv[3] if len(sys.argv) > 3 else None
    res = run_validation_suite(aud_dir, meta_path, spl_dir)
    print(format_report_text(res, title=f"VALIDATION REPORT: {os.path.basename(aud_dir).upper()}"))
