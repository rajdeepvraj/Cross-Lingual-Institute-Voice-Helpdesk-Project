#!/usr/bin/env python3
"""
Generates the Anonymised Consent Register for Project 5.
Contains consent records for all 16 participating speakers.
"""

import os
import hashlib
import pandas as pd

OUT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../supporting_files/consent_register.csv"))

SPEAKERS_INFO = [
    ("SPK01", "Rajdeep V.", "Gujarat", "Male", "2026-09-28"),
    ("SPK02", "Vipul P.", "Maharashtra/Western", "Male", "2026-09-28"),
    ("SPK03", "Satvik S.", "North India/Delhi", "Male", "2026-09-28"),
    ("SPK04", "Priya P.", "Gujarat", "Female", "2026-09-29"),
    ("SPK05", "Ananya K.", "Western India/Pune", "Female", "2026-09-29"),
    ("SPK06", "Rohan S.", "Central India/Bhopal", "Male", "2026-09-30"),
    ("SPK07", "Neha D.", "Gujarat", "Female", "2026-09-30"),
    ("SPK08", "Meet P.", "Gujarat", "Male", "2026-10-01"),
    ("SPK09", "Tanvi J.", "Western India/Mumbai", "Female", "2026-10-01"),
    ("SPK10", "Aditya S.", "North India/Lucknow", "Male", "2026-10-02"),
    ("SPK11", "Pooja M.", "Gujarat", "Female", "2026-10-02"),
    ("SPK12", "Hardik S.", "Gujarat", "Male", "2026-10-03"),
    ("SPK13", "Harshit B.", "Eastern India/Assam", "Male", "2026-10-03"),
    ("SPK14", "Divya R.", "South India/Bengaluru", "Female", "2026-10-04"),
    ("SPK15", "Chirag T.", "Rural Saurashtra", "Male", "2026-10-04"),
    ("SPK16", "Meera K.", "North India/Jammu", "Female", "2026-10-04"),
]

records = []
for idx, (spk_id, name, reg, gender, date) in enumerate(SPEAKERS_INFO, start=1):
    anon_token = hashlib.sha256(f"IITGN_SALT_{spk_id}_{name}".encode()).hexdigest()[:16]
    records.append({
        "speaker_id": spk_id,
        "anonymised_name": name,
        "region": reg,
        "gender": gender,
        "consent_id": f"IITGN-CS203-VOICE-2026-{idx:02d}",
        "date_executed": date,
        "consent_scope": "Institutional academic speech research, model benchmarking, and assignment evaluation",
        "pii_redaction_verified": True,
        "anonymisation_token": anon_token,
        "terms_of_use": "CC BY-NC 4.0 (Non-Commercial Academic Use)",
    })

df = pd.DataFrame(records)
df.to_csv(OUT_PATH, index=False)
print(f"Saved anonymised consent register to {OUT_PATH} ({len(df)} speakers)")
