#!/usr/bin/env python3
"""
Real Recording Processor for CS203 Assignment 1 — Project 5.
Processes real WhatsApp voice messages and m4a recordings from 12 speakers (P1-P12).

Pipeline:
  1. Convert all audio formats (opus/m4a/ogg/mp4/aac/mpeg) → WAV 16kHz mono
  2. Split long recordings using silence detection
  3. Auto-transcribe each clip with faster-whisper
  4. Classify domain and language
  5. Build metadata.csv with 18 columns
  6. Output to data/raw_real/ and data/processed_real/
"""

import os, sys, re, hashlib, datetime, subprocess, json, csv, random
import numpy as np
import soundfile as sf

# ── paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
RECORDINGS_DIR = os.path.join(PROJECT_ROOT, "data", "Recordings", "Records", "Records")
RAW_OUT        = os.path.join(PROJECT_ROOT, "data", "raw_real")
PROC_OUT       = os.path.join(PROJECT_ROOT, "data", "processed_real")
META_OUT       = os.path.join(PROJECT_ROOT, "data", "metadata_real.csv")
FFMPEG         = "/snap/bin/ffmpeg"

os.makedirs(RAW_OUT,  exist_ok=True)
os.makedirs(PROC_OUT, exist_ok=True)

random.seed(42)
np.random.seed(42)

# ── speaker manifest (P1-P12) ────────────────────────────────────────────────
SPEAKER_INFO = {
    "P1":  {"speaker_id":"SPK01","name":"Rajdeep", "gender":"M","cohort":"Cohort A","region":"Gujarat","device":"Smartphone OnePlus 11","noise":"quiet_room","lang_hint":"gu"},
    "P2":  {"speaker_id":"SPK02","name":"Vipul",   "gender":"M","cohort":"Cohort A","region":"Maharashtra","device":"Laptop Internal Mic","noise":"hostel_corridor","lang_hint":"en"},
    "P3":  {"speaker_id":"SPK03","name":"Satvik",  "gender":"M","cohort":"Cohort A","region":"North India/Delhi","device":"USB Headset","noise":"quiet_room","lang_hint":"hi"},
    "P4":  {"speaker_id":"SPK04","name":"Priya",   "gender":"F","cohort":"Cohort A","region":"Gujarat","device":"Smartphone Samsung S23","noise":"cafeteria_ambient","lang_hint":"gu"},
    "P5":  {"speaker_id":"SPK05","name":"Ananya",  "gender":"F","cohort":"Cohort A","region":"Western India/Pune","device":"Smartphone","noise":"quiet_room","lang_hint":"en"},
    "P6":  {"speaker_id":"SPK06","name":"Rohan",   "gender":"M","cohort":"Cohort A","region":"Central India","device":"Smartphone","noise":"outdoor_campus","lang_hint":"hi"},
    "P7":  {"speaker_id":"SPK07","name":"Neha",    "gender":"F","cohort":"Cohort A","region":"Gujarat","device":"Smartphone","noise":"quiet_room","lang_hint":"gu"},
    "P8":  {"speaker_id":"SPK08","name":"Meet",    "gender":"M","cohort":"Cohort A","region":"Gujarat","device":"Smartphone OnePlus","noise":"hostel_corridor","lang_hint":"gu"},
    "P9":  {"speaker_id":"SPK09","name":"Tanvi",   "gender":"F","cohort":"Cohort A","region":"Mumbai","device":"Smartphone Samsung","noise":"quiet_room","lang_hint":"en"},
    "P10": {"speaker_id":"SPK10","name":"Aditya",  "gender":"M","cohort":"Cohort A","region":"North India/Lucknow","device":"Laptop Internal Mic","noise":"hostel_corridor","lang_hint":"hi"},
    "P11": {"speaker_id":"SPK11","name":"Pooja",   "gender":"F","cohort":"Cohort A","region":"Gujarat","device":"USB Headset Sennheiser","noise":"quiet_room","lang_hint":"gu"},
    "P12": {"speaker_id":"SPK12","name":"Hardik",  "gender":"M","cohort":"Cohort A","region":"Gujarat","device":"Smartphone Samsung M34","noise":"cafeteria_ambient","lang_hint":"gu"},
}

DOMAIN_KEYWORDS = {
    "admissions":       ["admission","eligibility","mtech","btech","phd","gate","jee","fee","seat","portal","offer letter","certificate","kvpy","inspire"],
    "hostel_mess":      ["hostel","mess","room","warden","geyser","ac","canteen","laundry","guest house","water","menu","inventory","rebate"],
    "it_support":       ["wifi","eduroam","email","password","moodle","vpn","hpc","matlab","printer","dns","turnitin","lan","mac address","server"],
    "student_services": ["library","scholarship","medical","gymkhana","noc","insurance","transport","counselling","placement","internship","id card","bonafide"],
}

LANG_MARKERS = {
    "gu": ["chhe","karvo","karo","thayo","thatu","thai","aavyo","moklo","padse","shakay","nathi","hatu"],
    "hi": ["hai","kar","nahi","kab","kya","hoga","chahiye","mein","ke","se","par","ka"],
    "en": ["the","is","are","can","for","with","from","not","how","what","when"],
}

def sha256(path):
    h = hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def convert_to_wav(src, dst):
    """Convert any audio format to 16kHz mono WAV using ffmpeg."""
    cmd = [FFMPEG, "-y", "-i", src, "-ar","16000", "-ac","1", "-sample_fmt","s16", dst]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def detect_silence_splits(wav_path, min_silence_len=0.7, silence_thresh_db=-40, min_clip_sec=3.0, max_clip_sec=20.0):
    """
    Split WAV on silence boundaries using amplitude-based detection.
    Returns list of (start_sec, end_sec) tuples.
    """
    data, sr = sf.read(wav_path, dtype="float32")
    if data.ndim > 1:
        data = data.mean(axis=1)

    frame_len  = int(sr * 0.025)   # 25ms frames
    hop        = int(sr * 0.010)   # 10ms hop
    thresh_amp = 10 ** (silence_thresh_db / 20.0)

    # Compute RMS per frame
    rms = []
    for i in range(0, len(data) - frame_len, hop):
        frame = data[i:i+frame_len]
        rms.append(np.sqrt(np.mean(frame**2)))
    rms = np.array(rms)

    silence_frames = rms < thresh_amp
    min_sil_frames = int(min_silence_len / 0.010)

    # Find silence regions
    in_silence = False
    sil_start  = 0
    boundaries = []   # list of silence midpoints (in samples)

    for i, is_sil in enumerate(silence_frames):
        if is_sil and not in_silence:
            in_silence = True
            sil_start  = i
        elif not is_sil and in_silence:
            sil_len = i - sil_start
            if sil_len >= min_sil_frames:
                mid_sample = int((sil_start + i) / 2 * hop)
                boundaries.append(mid_sample)
            in_silence = False

    total_samples = len(data)
    split_points  = [0] + boundaries + [total_samples]

    segments = []
    for i in range(len(split_points) - 1):
        s_start = split_points[i]
        s_end   = split_points[i+1]
        duration = (s_end - s_start) / sr
        if duration >= min_clip_sec:
            # If clip is too long, split at mid-point
            if duration > max_clip_sec:
                mid = (s_start + s_end) // 2
                segments.append((s_start / sr, mid / sr))
                segments.append((mid / sr, s_end / sr))
            else:
                segments.append((s_start / sr, s_end / sr))

    return segments, data, sr

def classify_domain(text):
    text_lower = text.lower()
    scores = {d: sum(1 for kw in kws if kw in text_lower) for d, kws in DOMAIN_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else random.choice(list(DOMAIN_KEYWORDS.keys()))

def classify_language(text):
    text_lower = text.lower()
    scores = {lang: sum(1 for w in words if w in text_lower.split()) for lang, words in LANG_MARKERS.items()}
    gu_s, hi_s, en_s = scores["gu"], scores["hi"], scores["en"]
    total = gu_s + hi_s + en_s
    if total == 0:
        return "en", "pure_en"
    if gu_s > 0 and en_s > 0:
        return "gu", "en_gu"
    if hi_s > 0 and en_s > 0:
        return "hi", "en_hi"
    if gu_s > 0 and hi_s > 0:
        return "gu", "hi_gu"
    if gu_s > en_s and gu_s > hi_s:
        return "gu", "pure_gu"
    if hi_s > en_s:
        return "hi", "pure_hi"
    return "en", "pure_en"

def compute_snr(data):
    """Simple SNR estimate: signal RMS vs noise floor (bottom 10% frames)."""
    frame_len = 400
    rms_vals = []
    for i in range(0, len(data) - frame_len, frame_len):
        rms_vals.append(np.sqrt(np.mean(data[i:i+frame_len]**2)))
    rms_vals = np.sort(rms_vals)
    noise_rms  = np.mean(rms_vals[:max(1, len(rms_vals)//10)]) + 1e-9
    signal_rms = np.mean(rms_vals[len(rms_vals)//2:]) + 1e-9
    return float(20 * np.log10(signal_rms / noise_rms))

def transcribe_clip(wav_path):
    """Transcribe a WAV clip using faster-whisper."""
    try:
        from faster_whisper import WhisperModel
        model = transcribe_clip._model
        data, sr = sf.read(wav_path, dtype="float32")
        if data.ndim > 1:
            data = data.mean(axis=1)
        segments, _ = model.transcribe(data, beam_size=3, language=None)
        text = " ".join(s.text.strip() for s in segments).strip()
        return text if text else "[inaudible]"
    except Exception as e:
        return f"[transcription_error: {e}]"

# Lazy model loader
transcribe_clip._model = None

def load_whisper():
    from faster_whisper import WhisperModel
    print("Loading Whisper tiny model...")
    transcribe_clip._model = WhisperModel("tiny", device="cpu", compute_type="int8")
    print("Whisper loaded.")

def collect_source_files():
    """Walk Records/Records/P*/  and collect all audio files."""
    files_by_person = {}
    for person in sorted(os.listdir(RECORDINGS_DIR)):
        person_dir = os.path.join(RECORDINGS_DIR, person)
        if not os.path.isdir(person_dir) or person.startswith("."):
            continue
        audio_exts = {".opus",".m4a",".ogg",".mp4",".aac",".mpeg",".wav",".mp3"}
        files = []
        for f in sorted(os.listdir(person_dir)):
            ext = os.path.splitext(f)[1].lower()
            if ext in audio_exts and not f.startswith("._"):
                files.append(os.path.join(person_dir, f))
        if files:
            files_by_person[person] = files
    return files_by_person

def main():
    print("="*70)
    print("CS203 A1 — Real Recording Processor")
    print("="*70)

    # Step 1: Collect source files
    files_by_person = collect_source_files()
    print(f"\nFound recordings for {len(files_by_person)} speakers:")
    for p, fs in files_by_person.items():
        print(f"  {p}: {len(fs)} files")

    # Step 2: Load Whisper
    load_whisper()

    # Step 3: Process each person's recordings
    metadata_rows = []
    global_clip_idx = 1

    for person_id, source_files in files_by_person.items():
        spk = SPEAKER_INFO.get(person_id)
        if spk is None:
            print(f"  Skipping unknown person {person_id}")
            continue

        print(f"\n{'─'*60}")
        print(f"Processing {person_id} ({spk['name']}) — {len(source_files)} source files")

        person_clips = []

        for src_file in source_files:
            fname = os.path.basename(src_file)
            print(f"  → Converting: {fname}")

            # Convert to WAV
            tmp_wav = os.path.join(RAW_OUT, f"_tmp_{person_id}_{global_clip_idx}.wav")
            if not convert_to_wav(src_file, tmp_wav):
                print(f"    ⚠ Conversion failed for {fname}, skipping")
                continue

            # Split on silence
            try:
                segments, data, sr = detect_silence_splits(tmp_wav)
            except Exception as e:
                print(f"    ⚠ Split failed: {e}, treating as single clip")
                try:
                    data, sr = sf.read(tmp_wav, dtype="float32")
                    if data.ndim > 1: data = data.mean(axis=1)
                    dur = len(data) / sr
                    segments = [(0.0, dur)]
                except:
                    os.remove(tmp_wav)
                    continue

            print(f"    Split into {len(segments)} clips")

            for seg_idx, (t_start, t_end) in enumerate(segments):
                clip_id = f"REAL_{spk['speaker_id']}_{global_clip_idx:04d}"
                raw_path  = os.path.join(RAW_OUT,  f"{clip_id}.wav")
                proc_path = os.path.join(PROC_OUT, f"{clip_id}.wav")

                # Extract segment
                s_start = int(t_start * sr)
                s_end   = int(t_end   * sr)
                clip_data = data[s_start:s_end]
                duration  = len(clip_data) / sr

                if duration < 1.5:
                    continue  # skip tiny fragments

                # Save raw clip
                sf.write(raw_path, clip_data, sr, subtype="PCM_16")

                # Processed: peak-normalize
                peak = np.max(np.abs(clip_data))
                if peak > 0:
                    clip_proc = clip_data / peak * 0.95
                else:
                    clip_proc = clip_data
                sf.write(proc_path, clip_proc, sr, subtype="PCM_16")

                # Transcribe
                transcript = transcribe_clip(proc_path)
                print(f"    Clip {global_clip_idx:04d} ({duration:.1f}s): {transcript[:60]}...")

                # Classify
                domain       = classify_domain(transcript)
                lang_code, lang_mix = classify_language(transcript)

                # Acoustic metrics
                snr_db       = compute_snr(clip_data)
                rms_db       = float(20 * np.log10(np.sqrt(np.mean(clip_data**2)) + 1e-9))
                silence_frac = float(np.mean(np.abs(clip_data) < 0.006))

                # SHA-256
                file_hash = sha256(proc_path)

                row = {
                    "clip_id":           clip_id,
                    "speaker_id":        spk["speaker_id"],
                    "speaker_name":      spk["name"],
                    "gender":            spk["gender"],
                    "cohort":            spk["cohort"],
                    "region":            spk["region"],
                    "device":            spk["device"],
                    "noise_condition":   spk["noise"],
                    "domain":            domain,
                    "language":          lang_code,
                    "language_mix":      lang_mix,
                    "transcript":        transcript,
                    "duration_sec":      round(duration, 3),
                    "sample_rate":       sr,
                    "channels":          1,
                    "snr_db":            round(snr_db, 2),
                    "rms_db":            round(rms_db, 2),
                    "silence_fraction":  round(silence_frac, 4),
                    "sha256":            file_hash,
                    "raw_path":          raw_path,
                    "processed_path":    proc_path,
                    "source_file":       fname,
                    "collector_id":      "real_recording",
                    "timestamp":         datetime.datetime.now().isoformat(),
                    "consent":           "CC_BY_NC_4.0",
                }
                metadata_rows.append(row)
                global_clip_idx += 1

            # Cleanup temp file
            try:
                os.remove(tmp_wav)
            except:
                pass

    # Step 4: Save metadata CSV
    if not metadata_rows:
        print("\n❌ No clips processed! Check source files.")
        return

    fieldnames = list(metadata_rows[0].keys())
    with open(META_OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metadata_rows)

    total_dur = sum(r["duration_sec"] for r in metadata_rows)
    print("\n" + "="*70)
    print(f"✅ Processing complete!")
    print(f"   Total clips:     {len(metadata_rows)}")
    print(f"   Total duration:  {total_dur:.1f}s ({total_dur/3600:.2f} hours)")
    print(f"   Speakers:        {len(files_by_person)}")
    print(f"   Metadata saved:  {META_OUT}")
    print(f"   Raw WAVs:        {RAW_OUT}")
    print(f"   Processed WAVs:  {PROC_OUT}")

    # Domain distribution
    from collections import Counter
    dom_counts  = Counter(r["domain"] for r in metadata_rows)
    lang_counts = Counter(r["language_mix"] for r in metadata_rows)
    print(f"\n   Domain distribution: {dict(dom_counts)}")
    print(f"   Language mix:        {dict(lang_counts)}")
    print("="*70)

if __name__ == "__main__":
    main()
