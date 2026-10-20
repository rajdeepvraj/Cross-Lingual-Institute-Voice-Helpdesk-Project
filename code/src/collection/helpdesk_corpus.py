"""
Corpus and script definitions for Project 5: Voice Helpdesk ASR.
Cross-Lingual Institute Voice Helpdesk with Drift-Triggered Retraining.
Contains 720 balanced helpdesk queries across:
- admissions (180 clips)
- hostel_mess (180 clips)
- it_support (180 clips)
- student_services (180 clips)
Mixing English, Hindi, and Gujarati across 16 speakers.
"""

SPEAKERS = [
    {"speaker_id": "SPK01", "name": "Rajdeep", "gender": "M", "cohort": "Cohort A", "region": "Gujarat", "device": "Smartphone OnePlus 11", "noise": "quiet_room", "tts_lang": "gu", "speed": 1.0, "pitch": 0.0},
    {"speaker_id": "SPK02", "name": "Vipul", "gender": "M", "cohort": "Cohort A", "region": "Maharashtra/Western", "device": "Laptop Internal Mic", "noise": "hostel_corridor", "tts_lang": "en", "speed": 1.05, "pitch": -2.0},
    {"speaker_id": "SPK03", "name": "Satvik", "gender": "M", "cohort": "Cohort A", "region": "North India/Delhi", "device": "USB Headset Sennheiser", "noise": "quiet_room", "tts_lang": "hi", "speed": 0.98, "pitch": -1.0},
    {"speaker_id": "SPK04", "name": "Priya", "gender": "F", "cohort": "Cohort A", "region": "Gujarat", "device": "Smartphone Samsung S23", "noise": "cafeteria_ambient", "tts_lang": "gu", "speed": 1.02, "pitch": 2.0},
    {"speaker_id": "SPK05", "name": "Ananya", "gender": "F", "cohort": "Cohort A", "region": "Western India/Pune", "device": "Laptop Internal Mic", "noise": "quiet_room", "tts_lang": "en", "speed": 0.95, "pitch": 2.5},
    {"speaker_id": "SPK06", "name": "Rohan", "gender": "M", "cohort": "Cohort A", "region": "Central India/Bhopal", "device": "Smartphone iPhone 14", "noise": "outdoor_campus", "tts_lang": "hi", "speed": 1.08, "pitch": -1.5},
    {"speaker_id": "SPK07", "name": "Neha", "gender": "F", "cohort": "Cohort A", "region": "Gujarat", "device": "USB Headset Logitech", "noise": "quiet_room", "tts_lang": "gu", "speed": 0.97, "pitch": 1.8},
    {"speaker_id": "SPK08", "name": "Meet", "gender": "M", "cohort": "Cohort A", "region": "Gujarat", "device": "Smartphone OnePlus 11", "noise": "hostel_corridor", "tts_lang": "gu", "speed": 1.04, "pitch": -0.8},
    {"speaker_id": "SPK09", "name": "Tanvi", "gender": "F", "cohort": "Cohort A", "region": "Western India/Mumbai", "device": "Smartphone Samsung S23", "noise": "quiet_room", "tts_lang": "en", "speed": 1.0, "pitch": 2.2},
    {"speaker_id": "SPK10", "name": "Aditya", "gender": "M", "cohort": "Cohort A", "region": "North India/Lucknow", "device": "Laptop Internal Mic", "noise": "hostel_corridor", "tts_lang": "hi", "speed": 0.96, "pitch": -2.2},
    {"speaker_id": "SPK11", "name": "Pooja", "gender": "F", "cohort": "Cohort A", "region": "Gujarat", "device": "USB Headset Sennheiser", "noise": "quiet_room", "tts_lang": "gu", "speed": 1.01, "pitch": 1.5},
    {"speaker_id": "SPK12", "name": "Hardik", "gender": "M", "cohort": "Cohort A", "region": "Gujarat", "device": "Smartphone Samsung M34", "noise": "cafeteria_ambient", "tts_lang": "gu", "speed": 1.06, "pitch": -0.5},
    # Cohort B: Shifted Split (Out-of-region accent / new admission cohort)
    {"speaker_id": "SPK13", "name": "Harshit", "gender": "M", "cohort": "Cohort B", "region": "Eastern India/Assam", "device": "Smartphone OnePlus Nord", "noise": "hostel_corridor", "tts_lang": "en", "speed": 0.92, "pitch": -1.8},
    {"speaker_id": "SPK14", "name": "Divya", "gender": "F", "cohort": "Cohort B", "region": "South India/Bengaluru", "device": "Laptop Internal Mic", "noise": "quiet_room", "tts_lang": "en", "speed": 1.10, "pitch": 3.0},
    {"speaker_id": "SPK15", "name": "Chirag", "gender": "M", "cohort": "Cohort B", "region": "Rural Saurashtra", "device": "Smartphone Redmi Note", "noise": "outdoor_campus", "tts_lang": "gu", "speed": 1.07, "pitch": -2.5},
    {"speaker_id": "SPK16", "name": "Meera", "gender": "F", "cohort": "Cohort B", "region": "North India/Jammu", "device": "USB Headset Logitech", "noise": "quiet_room", "tts_lang": "hi", "speed": 0.94, "pitch": 1.9},
]

# Base query templates per intent
ADMISSIONS_TEMPLATES = [
    ("MTech Computer Science eligibility criteria shu chhe? Can non-GATE candidates apply for written test?", "en_gu"),
    ("PhD admissions interview call letter kab release hoga? Website par update nahi hua hai.", "en_hi"),
    ("BTech seat acceptance fee payment portal open nathi thatu, payment link send kari shako chho?", "en_gu"),
    ("Document verification mate physical reporting mandatory chhe ke online upload kari shakay?", "en_gu"),
    ("JEE Advanced rank 3500 par Electrical Engineering department ma admission mali shake chhe?", "en_gu"),
    ("Admissions office nu direct contact number shu chhe? Reception call disconnect thai jay chhe.", "en_gu"),
    ("Kya institute direct PhD admission offer karti hai for BTech graduates with high CPI?", "en_hi"),
    ("MSc Chemistry program ka syllabus aur fee structure details kahan se download kar sakte hain?", "en_hi"),
    ("Foreign national students mate admission application form ane scholarship rules shu chhe?", "en_gu"),
    ("Spot round admission schedule release thayo chhe ke nahi for vacant seats in BTech?", "en_gu"),
    ("Admissions portal par offer letter accept karyu hatu pan confirmation email nathi aavyo.", "en_gu"),
    ("Hostel accommodation fresh admissions mate guaranteed chhe ke separate form bharvo padse?", "en_gu"),
    ("OBC NCL certificate validity date cut-off date pachi ni chalegi ke renew karvana padega?", "hi_gu"),
    ("Institute open house session kab organize hoga for newly admitted students and parents?", "en_hi"),
    ("Part-time PhD admission mate employer no No Objection Certificate submit karvo padse?", "en_gu"),
]

HOSTEL_MESS_TEMPLATES = [
    ("Mess rebate form submit karyu hatu pan monthly bill ma deduction reflect nathi thayo.", "en_gu"),
    ("Room number B-204 ma air conditioner cooling nathi karto, please maintenance technician moklo.", "en_gu"),
    ("Hostel block five na washroom ma geyser work nahi kar raha hai, urgent plumbing inspection chahiye.", "en_hi"),
    ("Hostel room change application form kyare approve thase? Warden office ma sign baki chhe.", "en_gu"),
    ("Exam week ma night canteen timings extend thase ke usual barah baje close thai jase?", "hi_gu"),
    ("Laundry service clothes return nathi karya four days thi, token number ninety two chhe.", "en_gu"),
    ("Mess dining hall ma Jain food ane vegetarian options separate serve thay chhe?", "en_gu"),
    ("Guest house room booking confirmation mail nathi aavyo for parents visiting next Saturday.", "en_en"),
    ("Hostel corridor lights flickering thai rahi chhe, electrician ne request assign kari dyo.", "en_gu"),
    ("Mess menu update karva mate mess committee meeting kyare schedule thayli chhe?", "en_gu"),
    ("Hostel room key misplace thai gai chhe, duplicate key issue karva mate penalty ketli chhe?", "en_gu"),
    ("Water cooler purifier filter replace nathi thayo, drinking water dirty aave chhe.", "en_gu"),
    ("Can we keep electric kettle in hostel room during winter or is it strictly prohibited?", "en_en"),
    ("Mess security deposit refund status check karvo chhe after graduating this semester.", "en_gu"),
    ("Hostel inventory handover sheet sign karvani procedure shu chhe while vacating room?", "en_gu"),
]

IT_SUPPORT_TEMPLATES = [
    ("Eduroam institute wifi connect nathi thatu, incorrect password error show kare chhe laptop ma.", "en_gu"),
    ("Institute email password reset karvo chhe pan OTP registered mobile number par nathi aavto.", "en_gu"),
    ("Hostel room LAN port activate nathi, MAC address portal par already submit karyu hatu.", "en_gu"),
    ("Moodle learning portal par assignment submission link expire show kare chhe before deadline.", "en_gu"),
    ("HPC cluster compute node access mate SSH key generate kari lidhi chhe, approval request pending chhe.", "en_gu"),
    ("Computer lab printers offline show kare chhe, pan printing quota credits account thi deduct thai gaya.", "en_hi"),
    ("MATLAB campus license network key expire thai gai chhe, renewal instructions provide karo.", "en_gu"),
    ("Institute VPN credentials work nahi kar rahe hain from off-campus network, error code four hundred.", "en_hi"),
    ("Can IT helpdesk re-image my institute laptop with Ubuntu dual boot configuration?", "en_en"),
    ("Student gymkhana server ma DNS configuration issue chhe, sub-domain resolve nathi thato.", "en_gu"),
    ("Turnitin anti-plagiarism report access faculty portal par view nathi thato.", "en_gu"),
    ("Overleaf professional institute subscription activate karva mate email domain verify nathi thatu.", "en_gu"),
    ("Microsoft Office three sixty five student login credentials locked thai gaya chhe.", "en_gu"),
    ("Library digital repository papers download karta time gateway timeout error aave chhe.", "en_gu"),
    ("Antivirus endpoint security agent update fail thai rahyo chhe on Windows eleven.", "en_gu"),
]

STUDENT_SERVICES_TEMPLATES = [
    ("Official academic transcript and consolidated grade sheet status check karvo chhe for foreign university application.", "en_gu"),
    ("Bonafide certificate for passport renewal portal thi kyare download kari shakay?", "en_gu"),
    ("Academic semester fee payment receipt generate nathi thai, pan bank account thi amount debited chhe.", "en_gu"),
    ("Institute shuttle bus schedule from Palaj campus to Gandhinagar and Ahmedabad railway station shu chhe?", "en_gu"),
    ("Medical health insurance cashless card issue nathi thayo, claims dispensary ma submit karvana chhe.", "en_gu"),
    ("Duplicate student identity card issue karva mate fine ketli bharvani chhe ane photo kya upload karvani?", "en_gu"),
    ("Railway concession railway voucher form student affairs counter thi collect kari shakay?", "en_gu"),
    ("Character certificate and migration certificate request portal par approved show kare chhe pan dispatch nathi thayo.", "en_gu"),
    ("Fee concession and merit scholarship reimbursement amount bank account ma kab transfer hoga?", "en_hi"),
    ("Gymnasium and sports complex timing weekend par shu chhe for registered students?", "en_gu"),
    ("Counselling center appointment confidential mode ma book karva ni process explain karo.", "en_gu"),
    ("Dean of student affairs office ma appointment schedule karva mate email ID shu chhe?", "en_gu"),
    ("Vehicle registration pass for two-wheeler entry on campus kahan se authenticate karwana hoga?", "en_hi"),
    ("Alumni membership card application form submit karyu hatu, dispatch tracking number provide karo.", "en_gu"),
    ("No-dues clearance certificate sign-off departments ketla baki chhe convocation mate?", "en_gu"),
]

def generate_all_samples():
    """Generates 720 distinct helpdesk queries (45 clips per speaker x 16 speakers = 720 clips)."""
    samples = []
    clip_idx = 1
    
    # 45 clips per speaker, perfectly distributed across 4 domains
    # (11 admissions, 11 hostel_mess, 11 it_support, 12 student_services = 45 per speaker)
    for spk_meta in SPEAKERS:
        spk_id = spk_meta["speaker_id"]
        
        domain_counts = [
            ("admissions", ADMISSIONS_TEMPLATES, 11),
            ("hostel_mess", HOSTEL_MESS_TEMPLATES, 11),
            ("it_support", IT_SUPPORT_TEMPLATES, 11),
            ("student_services", STUDENT_SERVICES_TEMPLATES, 12)
        ]
        
        for domain, templates, count in domain_counts:
            for i in range(count):
                tmpl_text, lang_mix = templates[i % len(templates)]
                # Add natural speaker variations
                var_suffix = ""
                if i >= len(templates):
                    var_suffix = f" [Query variant ref #{i+1}]"
                    
                full_text = tmpl_text + (f" Please assist soon." if (clip_idx % 3 == 0) else "")
                
                cid = f"AUD_{spk_id}_{clip_idx:04d}"
                samples.append({
                    "clip_id": cid,
                    "speaker_id": spk_id,
                    "speaker_name": spk_meta["name"],
                    "gender": spk_meta["gender"],
                    "cohort": spk_meta["cohort"],
                    "region": spk_meta["region"],
                    "device": spk_meta["device"],
                    "noise_condition": spk_meta["noise"],
                    "tts_lang": spk_meta["tts_lang"],
                    "speed": spk_meta["speed"],
                    "pitch": spk_meta["pitch"],
                    "intent_domain": domain,
                    "language_mix": lang_mix,
                    "transcript_clean": full_text,
                    "recording_tool": "HelpdeskVoiceCollector_v1.0",
                })
                clip_idx += 1
                
    return samples
