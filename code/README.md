# CS 203: Voice Helpdesk ASR (Assignment 1)
**Project 5: Cross-Lingual Institute Voice Helpdesk with Drift-Triggered Retraining**  
**Indian Institute of Technology Gandhinagar**  
**Group Members**: Rajdeep Vraj (22110215), Vipul Sunil Patil, Satvik Sharma  
**GitHub Repository**: `https://github.com/rajdeepvraj/cs203-voice-helpdesk-asr`  
**Git Tag**: `a1-final`

---

## 1. Quickstart: Rebuild Dataset in 5 Commands
To reproduce the entire dataset, validation suite, and supporting figures from scratch:

```bash
# 1. Clone repository and navigate to code directory
git clone https://github.com/rajdeepvraj/cs203-voice-helpdesk-asr.git && cd cs203-voice-helpdesk-asr/code

# 2. Initialize and activate Python virtual environment
python3 -m venv .venv && source .venv/bin/activate

# 3. Install pinned dependencies
pip install -r requirements.txt

# 4. Execute the master automated end-to-end pipeline
python3 pipeline.py

# 5. Run automated test suite verifying corruption detection
pytest tests/ -v
```

---

## 2. Repository Architecture & Layout
```
code/
├── src/
│   ├── collection/        # Speech corpus, dataset synthesizer, and splitters
│   ├── validation/        # Automated 12-check validation suite and audio cleaner
│   ├── labelling/         # Dual-round inter-annotator agreement engine
│   ├── augmentation/      # 4 audio augmentations & off-the-shelf Whisper evaluation
│   └── active_learning/   # Informative vs. random pool-based active learning
├── tests/                 # Pytest test suite asserting deliberate corruptions fail
├── guidelines/            # Annotation Guidelines v1.0 and Revised v2.0
├── prompts/               # Verbatim model prompts for generation & audit
├── label_studio_config.xml # XML interface definition for Label Studio
├── pipeline.py            # Master reproducible pipeline script
├── requirements.txt       # Pinned library dependencies
├── requirements_freeze.txt# Environment snapshot (pip freeze)
├── ENVIRONMENT.md         # Hardware, OS, runtime, and seed documentation
├── LABELLING_PROTOCOL.md  # Detailed labelling protocol and annotator orders
├── HANDOFF_A2.md          # Frozen splits, label schema, and gold checksum
└── CONSENT_LICENSING.md   # Consent terms, PII anonymisation, and CC BY-NC 4.0
```

---

## 3. Dataset Summary
- **Total Speech Duration**: 9,850.54 seconds (2.74 hours) across 720 clips
- **Speakers**: 16 disjoint speakers (Cohort A: SPK01 - SPK12, Cohort B: SPK13 - SPK16)
- **Acoustic Standards**: 16,000 Hz, Mono (1-channel), 16-bit PCM WAV
- **Domain Balance**: 180 clips per domain (`admissions`, `hostel_mess`, `it_support`, `student_services`)
- **Languages Spoken**: Code-mixed Indian English, Hindi, and Gujarati
- **Inter-Annotator Agreement**:
  - Round 1 (v1 Guidelines): WER = 8.77%, Cohen's $\kappa = 0.686$
  - Round 2 (v2 Guidelines): WER = 0.53%, Cohen's $\kappa = 0.955$
- **Frozen Gold Test Checksum**: `c5e195975ce089bffbdd6bc1899e3be90c0ad759ae1dabec60d2f34b870357bc`

---

## 4. Verification & Testing
The validation suite enforces 12 technical constraints:
- Sample rate (16kHz), mono channels, duration bounds (2-30s), clipping peak < 0.999, silence ratio < 35%, SNR >= 10dB, audio hash uniqueness, valid script characters, plausible speech rate (3-30 CPS), language match, metadata schema, and 0% split speaker leakage.
- Run `pytest tests/test_validation_corrupted.py` to confirm that all 8 deliberate corruptions are caught by the suite.
