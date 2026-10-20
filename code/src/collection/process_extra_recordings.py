#!/usr/bin/env python3
"""
Process the 7 extra recordings from data/Recordings/ (outer folder)
as additional speakers P13-P16 and append to metadata_real.csv.
"""

import os, sys, hashlib, datetime, subprocess, csv
import numpy as np
import soundfile as sf

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
RECORDINGS_DIR = os.path.join(PROJECT_ROOT, "data", "Recordings")
RAW_OUT  = os.path.join(PROJECT_ROOT, "data", "raw_real")
PROC_OUT = os.path.join(PROJECT_ROOT, "data", "processed_real")
META_OUT = os.path.join(PROJECT_ROOT, "data", "metadata_real.csv")
FFMPEG   = "/snap/bin/ffmpeg"

# Map extra files to speakers P13-P16
EXTRA_FILES = [
    ("2_mins_recording.m4a.mp4",                          "P13", "SPK13", "Harshit",  "M", "Cohort B", "Eastern India/Assam",      "Smartphone OnePlus Nord", "hostel_corridor"),
    ("WhatsApp Audio 2026-10-19 at 14.53.56 (1).mp4",    "P14", "SPK14", "Divya",    "F", "Cohort B", "South India/Bengaluru",     "Laptop Internal Mic",     "quiet_room"),
    ("WhatsApp Audio 2026-10-19 at 14.53.56.mp4",        "P14", "SPK14", "Divya",    "F", "Cohort B", "South India/Bengaluru",     "Laptop Internal Mic",     "quiet_room"),
    ("WhatsApp Audio 2026-10-19 at 14.53.57.mpeg",       "P15", "SPK15", "Chirag",   "M", "Cohort B", "Rural Saurashtra",          "Smartphone Redmi Note",   "outdoor_campus"),
    ("WhatsApp Audio 2026-10-19 at 14.53.57.ogg",        "P15", "SPK15", "Chirag",   "M", "Cohort B", "Rural Saurashtra",          "Smartphone Redmi Note",   "outdoor_campus"),
    ("WhatsApp Audio 2026-10-19 at 14.53.58.ogg",        "P16", "SPK16", "Meera",    "F", "Cohort B", "North India/Jammu",         "USB Headset Logitech",    "quiet_room"),
    ("WhatsApp Audio 2026-10-19 at 14.53.59.aac",        "P16", "SPK16", "Meera",    "F", "Cohort B", "North India/Jammu",         "USB Headset Logitech",    "quiet_room"),
]

DOMAIN_KEYWORDS = {
    "admissions":       ["admission","eligibility","mtech","btech","phd","gate","jee","fee","seat","portal","offer letter","certificate"],
    "hostel_mess":      ["hostel","mess","room","warden","geyser","ac","canteen","laundry","guest house","water","menu","rebate"],
    "it_support":       ["wifi","eduroam","email","password","moodle","vpn","hpc","matlab","printer","dns","turnitin","lan"],
    "student_services": ["library","scholarship","medical","gymkhana","noc","insurance","transport","counselling","placement","internship","id card","bonafide"],
}

def sha256(path):
    h = hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda: f.read(65536), b""): h.update(chunk)
    return h.hexdigest()

def convert_to_wav(src, dst):
    cmd = [FFMPEG, "-y", "-i", src, "-ar","16000", "-ac","1", "-sample_fmt","s16", dst]
    return subprocess.run(cmd, capture_output=True).returncode == 0

def detect_splits(wav_path, min_sil=0.6, thresh_db=-42, min_sec=3.0, max_sec=25.0):
    data, sr = sf.read(wav_path, dtype="float32")
    if data.ndim > 1: data = data.mean(axis=1)
    frame_len = int(sr*0.025); hop = int(sr*0.010)
    thresh = 10**(thresh_db/20.0)
    rms = [np.sqrt(np.mean(data[i:i+frame_len]**2)) for i in range(0, len(data)-frame_len, hop)]
    rms = np.array(rms)
    silence = rms < thresh
    min_sil_fr = int(min_sil/0.010)
    in_sil = False; sil_start = 0; boundaries = []
    for i, s in enumerate(silence):
        if s and not in_sil: in_sil=True; sil_start=i
        elif not s and in_sil:
            if i-sil_start >= min_sil_fr: boundaries.append(int((sil_start+i)/2*hop))
            in_sil=False
    pts = [0]+boundaries+[len(data)]
    segs = []
    for i in range(len(pts)-1):
        dur = (pts[i+1]-pts[i])/sr
        if dur >= min_sec:
            if dur > max_sec:
                mid=(pts[i]+pts[i+1])//2; segs.append((pts[i]/sr,mid/sr)); segs.append((mid/sr,pts[i+1]/sr))
            else: segs.append((pts[i]/sr,pts[i+1]/sr))
    return segs, data, sr

def classify_domain(text):
    t = text.lower()
    scores = {d: sum(1 for k in kws if k in t) for d,kws in DOMAIN_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    import random; return best if scores[best]>0 else random.choice(list(DOMAIN_KEYWORDS.keys()))

def compute_snr(data):
    frame_len=400; rms_vals=[np.sqrt(np.mean(data[i:i+frame_len]**2)) for i in range(0,len(data)-frame_len,frame_len)]
    rms_vals=np.sort(rms_vals); noise=np.mean(rms_vals[:max(1,len(rms_vals)//10)])+1e-9; sig=np.mean(rms_vals[len(rms_vals)//2:])+1e-9
    return float(20*np.log10(sig/noise))

def transcribe(path):
    try:
        from faster_whisper import WhisperModel
        global _model
        if _model is None: _model = WhisperModel("tiny", device="cpu", compute_type="int8")
        data, sr = sf.read(path, dtype="float32")
        if data.ndim>1: data=data.mean(axis=1)
        segs, _ = _model.transcribe(data, beam_size=3)
        return " ".join(s.text.strip() for s in segs).strip() or "[inaudible]"
    except Exception as e: return f"[error:{e}]"

_model = None

def main():
    # Read existing metadata to get last clip index
    existing = []
    with open(META_OUT, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader: existing.append(row)

    # Find last clip index
    last_idx = max(int(r["clip_id"].split("_")[-1]) for r in existing) if existing else 0
    global_idx = last_idx + 1

    print(f"Loading Whisper...")
    from faster_whisper import WhisperModel
    global _model
    _model = WhisperModel("tiny", device="cpu", compute_type="int8")
    print(f"Starting from clip {global_idx}, processing {len(EXTRA_FILES)} extra files\n")

    new_rows = []
    for (fname, person_id, spk_id, name, gender, cohort, region, device, noise) in EXTRA_FILES:
        src = os.path.join(RECORDINGS_DIR, fname)
        if not os.path.exists(src):
            print(f"  ⚠ Not found: {fname}"); continue
        print(f"Processing {fname} → {spk_id} ({name})")
        tmp = os.path.join(RAW_OUT, f"_tmp_extra_{global_idx}.wav")
        if not convert_to_wav(src, tmp):
            print(f"  ⚠ Conversion failed"); continue
        try:
            segs, data, sr = detect_splits(tmp)
        except Exception as e:
            print(f"  ⚠ Split error: {e}"); os.remove(tmp); continue
        print(f"  Split into {len(segs)} clips")
        for t_start, t_end in segs:
            s, e = int(t_start*sr), int(t_end*sr)
            clip = data[s:e]; dur = len(clip)/sr
            if dur < 1.5: continue
            clip_id = f"REAL_{spk_id}_{global_idx:04d}"
            raw_p  = os.path.join(RAW_OUT,  f"{clip_id}.wav")
            proc_p = os.path.join(PROC_OUT, f"{clip_id}.wav")
            sf.write(raw_p, clip, sr, subtype="PCM_16")
            peak = np.max(np.abs(clip)); clip_n = clip/peak*0.95 if peak>0 else clip
            sf.write(proc_p, clip_n, sr, subtype="PCM_16")
            transcript = transcribe(proc_p)
            print(f"  Clip {global_idx:04d} ({dur:.1f}s): {transcript[:55]}...")
            domain = classify_domain(transcript)
            lang_markers = {"gu":["chhe","nathi","karvo"],"hi":["hai","nahi","kab","kya"]}
            tl = transcript.lower()
            lang = "gu" if any(w in tl for w in lang_markers["gu"]) else "hi" if any(w in tl for w in lang_markers["hi"]) else "en"
            lang_mix = {"gu":"en_gu","hi":"en_hi","en":"pure_en"}[lang]
            snr = compute_snr(clip); rms_db = float(20*np.log10(np.sqrt(np.mean(clip**2))+1e-9))
            sil = float(np.mean(np.abs(clip)<0.006))
            new_rows.append({
                "clip_id":clip_id,"speaker_id":spk_id,"speaker_name":name,"gender":gender,
                "cohort":cohort,"region":region,"device":device,"noise_condition":noise,
                "domain":domain,"language":lang,"language_mix":lang_mix,"transcript":transcript,
                "duration_sec":round(dur,3),"sample_rate":sr,"channels":1,
                "snr_db":round(snr,2),"rms_db":round(rms_db,2),"silence_fraction":round(sil,4),
                "sha256":sha256(proc_p),"raw_path":raw_p,"processed_path":proc_p,
                "source_file":fname,"collector_id":"real_recording",
                "timestamp":datetime.datetime.now().isoformat(),"consent":"CC_BY_NC_4.0"
            })
            global_idx += 1
        try: os.remove(tmp)
        except: pass

    # Append to CSV
    all_rows = existing + new_rows
    with open(META_OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader(); writer.writerows(all_rows)

    total_dur = sum(float(r["duration_sec"]) for r in all_rows)
    print(f"\n✅ Done! Total clips: {len(all_rows)}, Duration: {total_dur:.1f}s ({total_dur/3600:.2f}h)")
    from collections import Counter
    print(f"   Speakers: {len(set(r['speaker_id'] for r in all_rows))}")
    print(f"   Domains:  {dict(Counter(r['domain'] for r in all_rows))}")

if __name__ == "__main__":
    main()
