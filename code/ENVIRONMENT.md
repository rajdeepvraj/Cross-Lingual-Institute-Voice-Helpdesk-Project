# System and Runtime Environment Specification
**Project 5: Cross-Lingual Institute Voice Helpdesk with Drift-Triggered Retraining**  
**Course: CS 203 Software Tools and Techniques in AI (Assignment 1)**  
**Indian Institute of Technology Gandhinagar**

---

## 1. Operating System and Hardware
- **Operating System**: Ubuntu Linux (GNU/Linux)
- **Kernel Version**: `7.0.0-38-generic #38-Ubuntu SMP PREEMPT_DYNAMIC`
- **Architecture**: `x86_64` (64-bit Intel/AMD)
- **Host Platform**: ASUS VivoBook
- **GPU Acceleration**: None (CPU Execution with `int8` quantization)
- **System Memory**: 16 GB DDR4 RAM
- **Audio Subsystem**: ALSA / PulseAudio interface, `libsndfile` backend

---

## 2. Core Runtimes & CLI Tools
- **Python Runtime**: `Python 3.14.4` (`/home/rajdeepvraj/Documents/STT AI/Project/.venv/bin/python3`)
- **Package Manager**: `pip 26.2.1`
- **Version Control**: `git 2.43.0`
- **Data Version Control**: `dvc 3.67.1`
- **Annotation Tool**: `Label Studio 1.13.0` (Docker container / local server deployment with XML config)
- **Testing Framework**: `pytest 9.1.1`

---

## 3. Pretrained Models & Model Registries
| Model Name | Version / Revision Tag | Source / Repository | Checksum / Architecture |
|---|---|---|---|
| `faster-whisper-tiny` | `Systran/faster-whisper-tiny` | Hugging Face Hub | CTranslate2 `int8` CPU quantization, 39M parameters |
| `gTTS Base Engine` | `gTTS 2.5.4` | Google Translate TTS API | Multilingual acoustic synthesis (`en-IN`, `hi`, `gu`) |
| `Intent Classifier Baseline` | Scikit-Learn 1.9.1 | In-repo trained model | TF-IDF (1500 n-grams) + LogisticRegression (`C=5.0`) |

---

## 4. Deterministic Random Seeds
To ensure bitwise exact reproducibility across all experimental pipelines, random seeds are strictly pinned:
- **Global Random Seed**: `42` (`random.seed(42)`)
- **NumPy Random Generator**: `np.random.seed(42)`
- **Audio DSP Perturbation Seed**: `42` (reverberation RIR synthesis and noise floor)
- **Split Partitioner Seed**: `42` (disjoint speaker allocation)
- **Active Learning Seed Model**: `42` (initial seed classifier)
- **Random Baseline Multi-Run Seeds**: `[13, 20, 27, 34, 41, 48, 55, 62, 69, 76]` (10 independent Monte Carlo folds)
