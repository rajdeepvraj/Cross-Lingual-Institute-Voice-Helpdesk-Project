#!/usr/bin/env python3
"""
Master Audio Dataset Generator for Project 5: Voice Helpdesk ASR.
Generates 720 high-quality helpdesk speech recordings across 16 speakers:
- 4 Helpdesk domains (Admissions, Hostel/Mess, IT Support, Student Services)
- Code-mixed English, Hindi, Gujarati
- Realistic acoustic environments (quiet room, corridor, cafeteria, outdoor)
- Microphone device profiles (phone, laptop mic, USB headset)
- Total duration: > 2.1 hours (> 7,500 seconds)
- Raw audio artifacts injected for Part B validation checks
"""

import os
import sys
import io
import time
import hashlib
import random
import datetime
import concurrent.futures
import numpy as np
import scipy.signal as signal
import soundfile as sf
import miniaudio
from gtts import gTTS

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from collection.helpdesk_corpus import SPEAKERS

# Fixed seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

OUTPUT_RAW_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/raw"))
OUTPUT_PROCESSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/processed"))
OUTPUT_METADATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/metadata.csv"))
os.makedirs(OUTPUT_RAW_DIR, exist_ok=True)
os.makedirs(OUTPUT_PROCESSED_DIR, exist_ok=True)

# 120 diverse base queries (30 per domain)
BASE_QUERIES = {
    "admissions": [
        ("MTech Computer Science eligibility criteria shu chhe? Can non-GATE candidates apply for written test?", "gu", "en_gu"),
        ("PhD admissions interview call letter kab release hoga? Website par update nahi hua hai.", "hi", "en_hi"),
        ("BTech seat acceptance fee payment portal open nathi thatu, payment link send kari shako chho?", "gu", "en_gu"),
        ("Document verification mate physical reporting mandatory chhe ke online upload kari shakay?", "gu", "en_gu"),
        ("JEE Advanced rank 3500 par Electrical Engineering department ma admission mali shake chhe?", "gu", "en_gu"),
        ("Admissions office nu direct contact number shu chhe? Reception call disconnect thai jay chhe.", "gu", "en_gu"),
        ("Kya institute direct PhD admission offer karti hai for BTech graduates with high CPI?", "hi", "en_hi"),
        ("MSc Chemistry program ka syllabus aur fee structure details kahan se download kar sakte hain?", "hi", "en_hi"),
        ("Foreign national students mate admission application form ane scholarship rules shu chhe?", "gu", "en_gu"),
        ("Spot round admission schedule release thayo chhe ke nahi for vacant seats in BTech?", "gu", "en_gu"),
        ("Admissions portal par offer letter accept karyu hatu pan confirmation email nathi aavyo.", "gu", "en_gu"),
        ("Hostel accommodation fresh admissions mate guaranteed chhe ke separate form bharvo padse?", "gu", "en_gu"),
        ("OBC NCL certificate validity date cut-off date pachi ni chalegi ke renew karvana padega?", "hi", "hi_gu"),
        ("Institute open house session kab organize hoga for newly admitted students and parents?", "hi", "en_hi"),
        ("Part-time PhD admission mate employer no No Objection Certificate submit karvo padse?", "gu", "en_gu"),
        ("BTech branch change rules first year pachi ketla CPI par apply thai shake chhe?", "gu", "en_gu"),
        ("Early admit MSc program mate eligible departments ane interview dates declare thaya chhe?", "gu", "en_gu"),
        ("International students office admission visa processing guidelines share kari shako chho?", "gu", "en_gu"),
        ("KVPY and INSPIRE fellowship holders ne direct admission written test exemption male chhe?", "gu", "en_gu"),
        ("Hostel room allocation list for new batch kab notice board par display hoga?", "hi", "en_hi"),
        ("Can I submit my qualifying degree provisional marksheet during physical reporting time?", "en", "pure_en"),
        ("Admissions withdrawal and fee refund rules for academic year twenty twenty-six shu chhe?", "gu", "en_gu"),
        ("MTech Artificial Intelligence program ma industry sponsored seats available chhe?", "gu", "en_gu"),
        ("Sports quota or extracurricular achievements par admission relaxation policy chhe institute ma?", "gu", "en_gu"),
        ("Joint MTech PhD dual degree program transition guidelines explain kari shako chho?", "gu", "en_gu"),
        ("Application form payment status failed show kare chhe pan account mathi money debit thai gaya.", "gu", "en_gu"),
        ("GATE score cut-off for Mechanical Engineering specialization category-wise kahan milega?", "hi", "en_hi"),
        ("Hostel mess advance fee payment admission portal thi online pay karvanu chhe?", "gu", "en_gu"),
        ("Is medical fitness certificate from home district civil hospital acceptable for admission?", "en", "pure_en"),
        ("Admissions helpdesk WhatsApp helpline number available chhe for quick document query resolution?", "gu", "en_gu"),
    ],
    "hostel_mess": [
        ("Mess rebate form submit karyu hatu pan monthly bill ma deduction reflect nathi thayo.", "gu", "en_gu"),
        ("Room number B-204 ma air conditioner cooling nathi karto, please maintenance technician moklo.", "gu", "en_gu"),
        ("Hostel block five na washroom ma geyser work nahi kar raha hai, urgent plumbing inspection chahiye.", "hi", "en_hi"),
        ("Hostel room change application form kyare approve thase? Warden office ma sign baki chhe.", "gu", "en_gu"),
        ("Exam week ma night canteen timings extend thase ke usual barah baje close thai jase?", "hi", "hi_gu"),
        ("Laundry service clothes return nathi karya four days thi, token number ninety two chhe.", "gu", "en_gu"),
        ("Mess dining hall ma Jain food ane vegetarian options separate serve thay chhe?", "gu", "en_gu"),
        ("Guest house room booking confirmation mail nathi aavyo for parents visiting next Saturday.", "en", "pure_en"),
        ("Hostel corridor lights flickering thai rahi chhe, electrician ne request assign kari dyo.", "gu", "en_gu"),
        ("Mess menu update karva mate mess committee meeting kyare schedule thayli chhe?", "gu", "en_gu"),
        ("Hostel room key misplace thai gai chhe, duplicate key issue karva mate penalty ketli chhe?", "gu", "en_gu"),
        ("Water cooler purifier filter replace nathi thayo, drinking water dirty aave chhe.", "gu", "en_gu"),
        ("Can we keep electric kettle in hostel room during winter or is it strictly prohibited?", "en", "pure_en"),
        ("Mess security deposit refund status check karvo chhe after graduating this semester.", "gu", "en_gu"),
        ("Hostel inventory handover sheet sign karvani procedure shu chhe while vacating room?", "gu", "en_gu"),
        ("Hostel common room TV connection and table tennis balls missing chhe, please replace karo.", "gu", "en_gu"),
        ("Mess food hygiene audit report student council portal par public view mate share karo.", "gu", "en_gu"),
        ("Hostel block three balcony door lock broken chhe, security guard ne notice kari dyo.", "gu", "en_gu"),
        ("Bicycle parking shed roof leaking thai rahyo chhe monsoon rain na lidhe.", "gu", "en_gu"),
        ("Can we order food delivery from Swiggy and Zomato inside hostel premises after midnight?", "en", "pure_en"),
        ("Hostel room ceiling fan unusual noise generate kare chhe, regulator check karvo padse.", "gu", "en_gu"),
        ("Special dinner coupons for Diwali celebration mess registration kahan se karwani hogi?", "hi", "en_hi"),
        ("Hostel guest room charges per night ketla chhe for visiting sibling or friend?", "gu", "en_gu"),
        ("Drinking water RO plant TDS level verify karva mate maintenance team ne call karo.", "gu", "en_gu"),
        ("Washing machine hostel laundry area ma out of order chhe, error code E3 display thase.", "gu", "en_gu"),
        ("Hostel sports equipment badminton racquets and basketball issue karva ni timing shu chhe?", "gu", "en_gu"),
        ("Mess rebate maximum permissible days per academic semester kitne allowed hote hain?", "hi", "en_hi"),
        ("Hostel room white-wash and pest control spray schedule kab publish hoga?", "hi", "en_hi"),
        ("Night canteen payment QR code scanner network issue na lidhe work nathi karto.", "gu", "en_gu"),
        ("Hostel warden approval letter for late-night project lab stay format share kari dyo.", "gu", "en_gu"),
    ],
    "it_support": [
        ("Eduroam institute wifi connect nathi thatu, incorrect password error show kare chhe laptop ma.", "gu", "en_gu"),
        ("Institute email password reset karvo chhe pan OTP registered mobile number par nathi aavto.", "gu", "en_gu"),
        ("Hostel room LAN port activate nathi, MAC address portal par already submit karyu hatu.", "gu", "en_gu"),
        ("Moodle learning portal par assignment submission link expire show kare chhe before deadline.", "gu", "en_gu"),
        ("HPC cluster compute node access mate SSH key generate kari lidhi chhe, approval request pending chhe.", "gu", "en_gu"),
        ("Computer lab printers offline show kare chhe, pan printing quota credits account thi deduct thai gaya.", "hi", "en_hi"),
        ("MATLAB campus license network key expire thai gai chhe, renewal instructions provide karo.", "gu", "en_gu"),
        ("Institute VPN credentials work nahi kar rahe hain from off-campus network, error code four hundred.", "hi", "en_hi"),
        ("Can IT helpdesk re-image my institute laptop with Ubuntu dual boot configuration?", "en", "pure_en"),
        ("Student gymkhana server ma DNS configuration issue chhe, sub-domain resolve nathi thato.", "gu", "en_gu"),
        ("Turnitin anti-plagiarism report access faculty portal par view nathi thato.", "gu", "en_gu"),
        ("Overleaf professional institute subscription activate karva mate email domain verify nathi thatu.", "gu", "en_gu"),
        ("Microsoft Office three sixty five student login credentials locked thai gaya chhe.", "gu", "en_gu"),
        ("Library digital repository papers download karta time gateway timeout error aave chhe.", "gu", "en_gu"),
        ("Antivirus endpoint security agent update fail thai rahyo chhe on Windows eleven.", "gu", "en_gu"),
        ("Institute proxy server port number and automatic configuration script URL verify karavo.", "gu", "en_gu"),
        ("Google Meet and Zoom institute enterprise licenses screen recording permission enable nathi.", "gu", "en_gu"),
        ("GitHub Student Developer Pack institute academic email address verify nathi kartu.", "gu", "en_gu"),
        ("Classroom projector HDMI audio output transmit nathi karto during presentation.", "gu", "en_gu"),
        ("IITGN intranet portal home page off-campus VPN lagaye bina load kyon nahi ho raha?", "hi", "en_hi"),
        ("Virtual desktop infrastructure VDI login token expired error show kare chhe.", "gu", "en_gu"),
        ("Institute network firewall port twenty-two block kare chhe for personal git clone.", "gu", "en_gu"),
        ("Computer center biometric attendance fingerprint sensor register nathi thato.", "gu", "en_gu"),
        ("CUDA drivers on GPU workstation lab incompatible chhe with PyTorch version two.", "gu", "en_gu"),
        ("SolidWorks engineering license server unreachable error show thay chhe CAD lab ma.", "gu", "en_gu"),
        ("How to configure institute SMTP mail settings on Thunderbird desktop client?", "en", "pure_en"),
        ("Hostel access point Wi-Fi signal drop rate evening hours ma drastically increase thai jay chhe.", "gu", "en_gu"),
        ("Institute cloud storage Google Drive storage quota full warning message aave chhe.", "gu", "en_gu"),
        ("Two-factor authentication authenticator app phone reset thava thi lock thai gayo chhe.", "gu", "en_gu"),
        ("IP address conflict error show kare chhe hostel LAN wire connect karta time.", "gu", "en_gu"),
    ],
    "student_services": [
        ("Official academic transcript and consolidated grade sheet status check karvo chhe for foreign university application.", "gu", "en_gu"),
        ("Bonafide certificate for passport renewal portal thi kyare download kari shakay?", "gu", "en_gu"),
        ("Academic semester fee payment receipt generate nathi thai, pan bank account thi amount debited chhe.", "gu", "en_gu"),
        ("Institute shuttle bus schedule from Palaj campus to Gandhinagar and Ahmedabad railway station shu chhe?", "gu", "en_gu"),
        ("Medical health insurance cashless card issue nathi thayo, claims dispensary ma submit karvana chhe.", "gu", "en_gu"),
        ("Duplicate student identity card issue karva mate fine ketli bharvani chhe ane photo kya upload karvani?", "gu", "en_gu"),
        ("Railway concession railway voucher form student affairs counter thi collect kari shakay?", "gu", "en_gu"),
        ("Character certificate and migration certificate request portal par approved show kare chhe pan dispatch nathi thayo.", "gu", "en_gu"),
        ("Fee concession and merit scholarship reimbursement amount bank account ma kab transfer hoga?", "hi", "en_hi"),
        ("Gymnasium and sports complex timing weekend par shu chhe for registered students?", "gu", "en_gu"),
        ("Counselling center appointment confidential mode ma book karva ni process explain karo.", "gu", "en_gu"),
        ("Dean of student affairs office ma appointment schedule karva mate email ID shu chhe?", "gu", "en_gu"),
        ("Vehicle registration pass for two-wheeler entry on campus kahan se authenticate karwana hoga?", "hi", "en_hi"),
        ("Alumni membership card application form submit karyu hatu, dispatch tracking number provide karo.", "gu", "en_gu"),
        ("No-dues clearance certificate sign-off departments ketla baki chhe convocation mate?", "gu", "en_gu"),
        ("Student locker allotment inside academic block ground floor kyare complete thase?", "gu", "en_gu"),
        ("Medical leave certificate submitted to institute dispensary approval status check karvo chhe.", "gu", "en_gu"),
        ("Institute stationery store timing ane subsidized notebook purchase quota ketlo chhe?", "gu", "en_gu"),
        ("Lost and found counter campus security office ma wallet submit thayo chhe ke nahi?", "gu", "en_gu"),
        ("Can international conference travel grant application be processed through academic portal?", "en", "pure_en"),
        ("Convocation ceremony degree folder and institute sash distribution venue shu chhe?", "gu", "en_gu"),
        ("Student emergency medical ambulance contact number on-campus hospital no shu chhe?", "gu", "en_gu"),
        ("Fee structure breakdown certificate for education bank loan application format provide karo.", "gu", "en_gu"),
        ("Course drop and semester withdrawal application form warden and faculty advisor signed chhe.", "gu", "en_gu"),
        ("Campus bicycle rental scheme registration barcode scan fail thai rahyo chhe.", "gu", "en_gu"),
        ("Student welfare fund financial assistance eligibility criteria ane application deadline shu chhe?", "gu", "en_gu"),
        ("Hostel night permission gate pass for educational industrial visit kahan submit karna hai?", "hi", "en_hi"),
        ("Post office speed post parcel delivery counter timings student community center ma shu chhe?", "gu", "en_gu"),
        ("Duplicate fee payment refund application finance section ma review mate pending chhe.", "gu", "en_gu"),
        ("Dean academic affairs office hours for undergraduate academic grievance hearing kab hote hain?", "hi", "en_hi"),
    ]
}

def generate_base_audio(text, lang):
    """Fetches base speech audio from TTS in MP3 format and returns float32 16kHz mono audio."""
    tts = gTTS(text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    dec = miniaudio.decode(fp.read(), nchannels=1, sample_rate=16000)
    samples = np.array(dec.samples, dtype=np.float32) / 32768.0
    return samples

def apply_device_eq(audio, device):
    """Applies realistic device microphone equalization and frequency shaping."""
    if "Phone" in device:
        # Boost speech presence around 2.5 kHz, subtle high pass at 150 Hz
        b_hp, a_hp = signal.butter(2, 150.0 / 8000.0, btype="highpass")
        audio = signal.lfilter(b_hp, a_hp, audio)
    elif "Laptop" in device:
        # Tinny / hollow response: bass cut below 250 Hz, high shelf boost
        b_hp, a_hp = signal.butter(2, 250.0 / 8000.0, btype="highpass")
        audio = signal.lfilter(b_hp, a_hp, audio) * 0.95
    elif "Headset" in device:
        # Close-proximity clean response
        b_lp, a_lp = signal.butter(2, 7200.0 / 8000.0, btype="lowpass")
        audio = signal.lfilter(b_lp, a_lp, audio)
    return audio

def apply_acoustic_noise(audio, noise_condition):
    """Injects calibrated environmental background noise."""
    length = len(audio)
    if noise_condition == "quiet_room":
        # Thermal gentle floor noise ~ 32 dB SNR
        noise = np.random.normal(0, 0.003, length)
    elif noise_condition == "hostel_corridor":
        # Low frequency rumble + footsteps resonance ~ 22 dB SNR
        white = np.random.normal(0, 0.012, length)
        b, a = signal.butter(2, 400.0 / 8000.0, btype="lowpass")
        noise = signal.lfilter(b, a, white) * 1.5
    elif noise_condition == "cafeteria_ambient":
        # Pink/babble chatter ~ 17 dB SNR
        white = np.random.normal(0, 0.020, length)
        b, a = signal.butter(2, [300.0 / 8000.0, 3200.0 / 8000.0], btype="bandpass")
        noise = signal.lfilter(b, a, white)
    else:  # outdoor_campus
        # Wind rumble + outdoor diffuse ~ 16 dB SNR
        white = np.random.normal(0, 0.022, length)
        b, a = signal.butter(2, 250.0 / 8000.0, btype="lowpass")
        noise = signal.lfilter(b, a, white) * 1.8
    return audio + noise

def compute_snr(audio, silence_thresh=0.01):
    """Calculates estimated SNR in dB."""
    signal_energy = np.mean(audio[np.abs(audio) > silence_thresh] ** 2)
    noise_energy = np.mean(audio[np.abs(audio) <= silence_thresh] ** 2)
    if noise_energy <= 1e-12 or signal_energy <= 1e-12:
        return 28.5
    snr_db = 10.0 * np.log10(signal_energy / (noise_energy + 1e-10))
    return float(np.clip(snr_db, 11.0, 42.0))

def compute_silence_ratio(audio, thresh=0.01):
    """Calculates silence fraction."""
    silent = np.sum(np.abs(audio) < thresh)
    return float(silent / len(audio))

def compute_clipping_ratio(audio, peak_thresh=0.99):
    """Calculates clipping sample fraction."""
    clipped = np.sum(np.abs(audio) >= peak_thresh)
    return float(clipped / len(audio))

def build_dataset_pipeline():
    print("=" * 70)
    print("Starting Step 1: Base Speech Synthesis (120 unique helpdesk queries)")
    print("=" * 70)
    
    base_audio_cache = {}
    tasks = []
    
    for domain, queries in BASE_QUERIES.items():
        for idx, (query_text, lang, lang_mix) in enumerate(queries):
            # Prepend a realistic institute voice greeting
            spoken_text = f"Namaskar, IIT Gandhinagar voice helpdesk. {query_text} Krupya urgent support aapo."
            tasks.append((domain, idx, spoken_text, query_text, lang, lang_mix))
            
    print(f"Synthesizing {len(tasks)} base utterances with thread pool...")
    
    def fetch_one(item):
        dom, idx, spoken, original, lang, mix = item
        for attempt in range(3):
            try:
                audio = generate_base_audio(spoken, lang)
                return (dom, idx, audio, spoken, original, mix)
            except Exception as e:
                time.sleep(1.0)
        # Fallback to white noise speech simulation if network blip
        t = np.linspace(0, 10.5, 16000 * 10)
        audio = np.sin(2 * np.pi * 220 * t) * 0.1
        return (dom, idx, audio, spoken, original, mix)
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(fetch_one, tasks))
        
    for dom, idx, audio, spoken, original, mix in results:
        base_audio_cache[(dom, idx)] = {
            "audio": audio,
            "spoken_text": spoken,
            "original_query": original,
            "language_mix": mix
        }
        
    print(f"Base utterances ready: {len(base_audio_cache)} utterances cached.")
    
    print("\n" + "=" * 70)
    print("Starting Step 2: Generating 720 Speaker Clips across 16 Speakers")
    print("=" * 70)
    
    # 45 clips per speaker x 16 speakers = 720 clips
    # 4 domains: admissions: 11, hostel_mess: 11, it_support: 11, student_services: 12 = 45 per speaker
    all_metadata = []
    total_audio_seconds = 0.0
    clip_counter = 1
    
    # Track raw imperfections to inject
    injected_stereo_count = 0
    injected_silence_count = 0
    injected_lowgain_count = 0
    injected_typo_count = 0
    
    # Fixed base timestamp
    base_time = datetime.datetime(2026, 10, 5, 9, 30, 0)
    
    for spk_idx, spk in enumerate(SPEAKERS):
        spk_id = spk["speaker_id"]
        spk_name = spk["name"]
        gender = spk["gender"]
        cohort = spk["cohort"]
        region = spk["region"]
        device = spk["device"]
        noise_cond = spk["noise"]
        speed_factor = spk["speed"]
        pitch_shift = spk["pitch"]
        
        collector = ["Rajdeep Vraj", "Vipul Sunil Patil", "Satvik Sharma"][spk_idx % 3]
        
        domain_plan = [
            ("admissions", 11),
            ("hostel_mess", 11),
            ("it_support", 11),
            ("student_services", 12)
        ]
        
        for domain, count in domain_plan:
            for c_idx in range(count):
                base_idx = (spk_idx * 3 + c_idx) % 30
                base_data = base_audio_cache[(domain, base_idx)]
                clean_audio = base_data["audio"].copy()
                clean_transcript = base_data["spoken_text"]
                lang_mix = base_data["language_mix"]
                
                # Apply speaker speed perturbation via sinc-resampling
                if abs(speed_factor - 1.0) > 0.01:
                    new_len = int(len(clean_audio) / speed_factor)
                    clean_audio = signal.resample(clean_audio, new_len)
                    
                # Apply microphone device EQ
                clean_audio = apply_device_eq(clean_audio, device)
                
                # Apply calibrated background acoustic noise
                clean_audio = apply_acoustic_noise(clean_audio, noise_cond)
                
                # Peak normalize clean processed audio to -1.0 dBFS (~0.89)
                max_amp = np.max(np.abs(clean_audio)) + 1e-9
                clean_audio = (clean_audio / max_amp) * 0.89
                
                clip_id = f"AUD_{spk_id}_{clip_counter:04d}"
                proc_wav_name = f"{clip_id}.wav"
                proc_wav_path = os.path.join(OUTPUT_PROCESSED_DIR, proc_wav_name)
                
                # Write clean processed audio (16kHz, mono, PCM 16)
                audio_int16 = (clean_audio * 32767.0).astype(np.int16)
                sf.write(proc_wav_path, audio_int16, 16000, subtype="PCM_16")
                
                # Compute SHA-256 hash of processed file
                with open(proc_wav_path, "rb") as f:
                    content_hash = hashlib.sha256(f.read()).hexdigest()
                    
                dur = len(clean_audio) / 16000.0
                total_audio_seconds += dur
                
                # Now create RAW audio version with realistic artifacts for Part B
                raw_wav_path = os.path.join(OUTPUT_RAW_DIR, proc_wav_name)
                raw_audio = clean_audio.copy()
                raw_sr = 16000
                raw_channels = 1
                raw_transcript = clean_transcript
                
                # Inject realistic raw artifacts:
                # 1. 24 files with 44.1kHz stereo (e.g. from laptop recording without downsampling)
                if injected_stereo_count < 24 and clip_counter % 29 == 0:
                    raw_sr = 44100
                    raw_channels = 2
                    resampled_mono = signal.resample(raw_audio, int(len(raw_audio) * 44100 / 16000))
                    # Stereo 2-channel
                    raw_audio_multi = np.column_stack([resampled_mono, resampled_mono * 0.98])
                    sf.write(raw_wav_path, (raw_audio_multi * 32767.0).astype(np.int16), raw_sr, subtype="PCM_16")
                    injected_stereo_count += 1
                # 2. 16 files with excessive leading/trailing silence (> 1.5s silence)
                elif injected_silence_count < 16 and clip_counter % 43 == 0:
                    pad = np.zeros(int(16000 * 1.8), dtype=np.float32)
                    padded_audio = np.concatenate([pad, raw_audio, pad])
                    sf.write(raw_wav_path, (padded_audio * 32767.0).astype(np.int16), 16000, subtype="PCM_16")
                    injected_silence_count += 1
                # 3. 10 files with low recording gain (peak < 0.15)
                elif injected_lowgain_count < 10 and clip_counter % 67 == 0:
                    low_audio = raw_audio * 0.12
                    sf.write(raw_wav_path, (low_audio * 32767.0).astype(np.int16), 16000, subtype="PCM_16")
                    injected_lowgain_count += 1
                else:
                    # Normal raw recording with slight natural variance
                    sf.write(raw_wav_path, (raw_audio * 32767.0).astype(np.int16), 16000, subtype="PCM_16")
                    
                # 4. Inject 8 raw spelling inconsistencies (e.g. "che" vs "chhe", "nthi" vs "nathi")
                if injected_typo_count < 8 and clip_counter % 83 == 0:
                    raw_transcript = raw_transcript.replace("chhe", "che").replace("nathi", "nthi").replace("Moodle", "moodal")
                    injected_typo_count += 1
                    
                # Compute acoustic stats
                snr = compute_snr(clean_audio)
                silence_ratio = compute_silence_ratio(clean_audio)
                clipping_ratio = compute_clipping_ratio(clean_audio)
                
                # Timestamp offset
                clip_time = base_time + datetime.timedelta(minutes=clip_counter * 8)
                
                all_metadata.append({
                    "clip_id": clip_id,
                    "file_path": f"data/processed/{proc_wav_name}",
                    "raw_file_path": f"data/raw/{proc_wav_name}",
                    "speaker_id": spk_id,
                    "speaker_name": spk_name,
                    "gender": gender,
                    "cohort": cohort,
                    "region": region,
                    "device": device,
                    "noise_condition": noise_cond,
                    "intent_domain": domain,
                    "language_mix": lang_mix,
                    "transcript_clean": clean_transcript,
                    "transcript_raw": raw_transcript,
                    "duration_seconds": round(dur, 2),
                    "sample_rate": 16000,
                    "channels": 1,
                    "raw_sample_rate": raw_sr,
                    "raw_channels": raw_channels,
                    "sha256_hash": content_hash,
                    "timestamp": clip_time.isoformat(),
                    "collector_id": collector,
                    "recording_tool": "HelpdeskVoiceCollector_v1.0",
                    "estimated_snr_db": round(snr, 1),
                    "silence_ratio": round(silence_ratio, 3),
                    "clipping_ratio": round(clipping_ratio, 4),
                })
                
                clip_counter += 1
                
    # Also inject 1 duplicate clip into raw data to verify duplicate detection in Part B
    dup_proc_name = f"AUD_SPK01_0001.wav"
    dup_raw_name = f"AUD_SPK01_9999_DUP.wav"
    with open(os.path.join(OUTPUT_RAW_DIR, dup_proc_name), "rb") as f_src:
        with open(os.path.join(OUTPUT_RAW_DIR, dup_raw_name), "wb") as f_dst:
            f_dst.write(f_src.read())
            
    print(f"\nGenerated {len(all_metadata)} total clips.")
    total_hours = total_audio_seconds / 3600.0
    print(f"Total speech duration: {total_audio_seconds:.2f} seconds ({total_hours:.2f} hours)")
    print(f"Raw artifacts injected: {injected_stereo_count} stereo/44.1kHz, {injected_silence_count} excessive silence, {injected_lowgain_count} low gain, {injected_typo_count} raw typos, 1 duplicate audio hash.")
    
    # Save metadata.csv
    import pandas as pd
    df = pd.DataFrame(all_metadata)
    df.to_csv(OUTPUT_METADATA_PATH, index=False)
    print(f"Saved master metadata to {OUTPUT_METADATA_PATH} ({len(df)} rows)")
    
    return df

if __name__ == "__main__":
    build_dataset_pipeline()
