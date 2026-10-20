#!/usr/bin/env python3
"""
Pytest Suite for Corrupted Data Detection (Part B).
Deliberately feeds corrupted audio, transcripts, and split definitions to the validation suite
to prove that every single check detects corruption and fails as expected.
"""

import os
import sys
import tempfile
import numpy as np
import soundfile as sf
import pandas as pd
import pytest

# Add validation module to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/validation")))
from validate_dataset import check_audio_file, check_transcript_text, run_validation_suite

def test_corrupted_sample_rate():
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        t = np.linspace(0, 3.0, int(22050 * 3.0))
        audio = np.sin(2 * np.pi * 440 * t) * 0.5
        sf.write(f.name, audio.astype(np.float32), 22050)
        res = check_audio_file(f.name)
        os.unlink(f.name)
        assert any("sample rate" in iss.lower() for iss in res["issues"])

def test_corrupted_stereo_channels():
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        t = np.linspace(0, 3.0, int(16000 * 3.0))
        mono = np.sin(2 * np.pi * 440 * t) * 0.5
        stereo = np.column_stack([mono, mono])
        sf.write(f.name, stereo.astype(np.float32), 16000)
        res = check_audio_file(f.name)
        os.unlink(f.name)
        assert any("channel count" in iss.lower() for iss in res["issues"])

def test_corrupted_duration_bounds():
    # Too short (< 2.0s)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        audio = np.zeros(int(16000 * 0.8), dtype=np.float32)
        sf.write(f.name, audio, 16000)
        res = check_audio_file(f.name)
        os.unlink(f.name)
        assert any("duration out of bounds" in iss.lower() for iss in res["issues"])

def test_corrupted_clipping():
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        audio = np.ones(int(16000 * 3.0), dtype=np.float32) * 1.5  # overdriven
        audio = np.clip(audio, -1.0, 1.0)
        sf.write(f.name, audio, 16000)
        res = check_audio_file(f.name)
        os.unlink(f.name)
        assert any("clipping detected" in iss.lower() for iss in res["issues"])

def test_corrupted_excessive_silence():
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        audio = np.zeros(int(16000 * 4.0), dtype=np.float32)
        # only tiny beep
        audio[:100] = 0.5
        sf.write(f.name, audio, 16000)
        res = check_audio_file(f.name)
        os.unlink(f.name)
        assert any("excessive silence ratio" in iss.lower() for iss in res["issues"])

def test_corrupted_severe_noise():
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        # Pure heavy white noise with 0 speech
        audio = np.random.normal(0, 0.4, int(16000 * 3.0)).astype(np.float32)
        sf.write(f.name, audio, 16000)
        res = check_audio_file(f.name)
        os.unlink(f.name)
        # SNR should be near 0 dB
        assert res["estimated_snr_db"] < 10.0 or any("snr too low" in iss.lower() for iss in res["issues"])

def test_corrupted_script_characters():
    bad_text = "IITGN admission status \x00\x08 \uFFFF check karvo chhe! $$$$$$$"
    res = check_transcript_text(bad_text, 5.0)
    assert any("outside agreed script" in iss.lower() for iss in res["issues"])

def test_corrupted_split_leakage():
    with tempfile.TemporaryDirectory() as tmpdir:
        train_df = pd.DataFrame([{"clip_id": "c1", "speaker_id": "SPK01"}, {"clip_id": "c2", "speaker_id": "SPK02"}])
        test_df = pd.DataFrame([{"clip_id": "c3", "speaker_id": "SPK02"}, {"clip_id": "c4", "speaker_id": "SPK03"}])
        train_df.to_csv(os.path.join(tmpdir, "train.csv"), index=False)
        test_df.to_csv(os.path.join(tmpdir, "test_id.csv"), index=False)
        
        # Audio file dummy
        sf.write(os.path.join(tmpdir, "dummy.wav"), np.zeros(16000*3, dtype=np.float32), 16000)
        meta_df = pd.DataFrame([{"clip_id": "dummy", "file_path": "dummy.wav", "speaker_id": "SPK01", "gender": "M", "cohort": "A", "region": "GJ", "device": "P", "noise_condition": "Q", "intent_domain": "adm", "language_mix": "en", "transcript_clean": "test query", "duration_seconds": 3.0, "sample_rate": 16000, "channels": 1, "sha256_hash": "abc", "timestamp": "2026-10-10", "collector_id": "RV", "recording_tool": "t"}])
        meta_df.to_csv(os.path.join(tmpdir, "meta.csv"), index=False)
        
        res = run_validation_suite(tmpdir, os.path.join(tmpdir, "meta.csv"), split_manifests_dir=tmpdir)
        assert res["check_failures"]["split_leakage"] > 0
