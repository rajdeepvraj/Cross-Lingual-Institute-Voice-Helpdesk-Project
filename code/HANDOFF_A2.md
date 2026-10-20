# Handoff to Assignment 2

## Dataset Summary (Real Recordings)

| Item | Value |
|------|-------|
| Total clips | 284 (after silence-split) |
| Total duration | 4,486 s (1.25 hours) |
| Speakers | 16 (SPK01–SPK16) |
| Cohort A | SPK01–SPK12 (WhatsApp opus + m4a) |
| Cohort B | SPK13–SPK16 (outer recordings, out-of-region) |
| Source format | .opus, .m4a, .ogg, .mpeg, .aac, .mp4 → 16 kHz mono WAV |
| Transcription | Whisper-tiny (auto), reviewed by 2 annotators |

## Data Source

All audio is **real human speech** collected from 16 student volunteers:
- WhatsApp PTT voice messages (`.opus`, `.ogg`)  
- Smartphone voice memos (`.m4a`, `.aac`, `.mpeg`, `.mp4`)

No TTS synthesis was used. Recordings are in code-mixed English/Hindi/Gujarati.

## Frozen Gold Test Set

| Field | Value |
|-------|-------|
| File | `data/gold_test_set_real.csv` |
| Clips | 14 (SPK11 + SPK12, Cohort A) |
| SHA-256 | `8602554090ddbf8ed2701108e94cab000b95df585ddbd3a5a570cd7fd1fce022` |
| ⚠️ | **DO NOT modify or train on this set** |

## Split Schema

| Split | Speakers | Clips | Duration |
|-------|----------|-------|----------|
| `data/splits_real/train.csv` | SPK01–SPK08 | 136 | 43 min |
| `data/splits_real/val.csv` | SPK09–SPK10 | 48 | 10 min |
| `data/splits_real/test_id.csv` | SPK11–SPK12 | 14 | 6 min |
| `data/splits_real/test_shifted_cohort_b.csv` | SPK13–SPK16 | 86 | 15 min |

## Label Schema

- **Domain** (4 classes): `admissions`, `hostel_mess`, `it_support`, `student_services`
- **Transcript**: Whisper-tiny auto-transcript, reviewed in Label Studio (2 annotators)
- **Language mix**: `pure_en`, `en_hi`, `pure_hi`, `en_gu`
- **Cohen's κ** (Round 2): 0.955

## Git

- Repo: `code/`
- Tag: `a1-final-real`
- Clean working tree

## Key Files

| File | Description |
|------|-------------|
| `data/metadata_real.csv` | 284 rows × 24 columns |
| `data/raw_real/` | Original converted WAVs |
| `data/processed_real/` | Peak-normalized WAVs |
| `supporting_files/real_dataset_summary.json` | Full pipeline summary |
| `supporting_files/validation_logs_real/` | 12-check validation report |
| `supporting_files/augmentation_real/` | WER CSV + sample augmented clips |
| `supporting_files/active_learning_real/` | AL vs random comparison |
