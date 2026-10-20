# Consent, Privacy, and Licensing Statement (CONSENT_LICENSING.md)
**Project 5: Cross-Lingual Institute Voice Helpdesk with Drift-Triggered Retraining**  
**Course: CS 203 Software Tools and Techniques in AI**  
**IIT Gandhinagar**

---

## 1. Data Providers & Terms of Consent
- **Participants**: Speech recordings were gathered from 16 student and researcher volunteers representing diverse Indian regional accents (Gujarat, Maharashtra, Delhi NCR, Madhya Pradesh, Uttar Pradesh, Assam, Karnataka, and Jammu & Kashmir).
- **Consent Execution**: Each participant signed an institutional informed consent form prior to audio recording.
- **Terms of Agreement**:
  1. The collected voice samples are used strictly for academic research, coursework evaluation, and machine learning model benchmarking.
  2. Data will never be commercialized, monetized, or shared with third-party advertising entities.
  3. Participants hold the irrevocable right to request data inspection or deletion prior to final project publication.
- **Consent Register**: An anonymised consent log is maintained in `supporting_files/consent_register.csv`. In adherence to institutional ethics, raw contact details and signed hard copies are stored securely in offline department archives.

---

## 2. Personal Identifiable Information (PII) Anonymisation
To guarantee privacy:
1. **Speaker Identifiers**: Names and personal identifiers are permanently replaced with anonymised tokens (`SPK01` to `SPK16`).
2. **Cryptographic Salt**: Each participant record is associated with a 16-character SHA-256 salted hash (`IITGN_SALT_<spk_id>_<name>`) to verify consent validity without exposing identities.
3. **Audio Scrubbing**: Scripts are designed strictly around generic campus helpdesk FAQs (e.g. course codes, building names, IT services). No personal student roll numbers, home addresses, phone numbers, or passwords were recorded in the audio.

---

## 3. External Materials & Public Knowledge Sources
- **Helpdesk Seed Queries**: Seed topics and queries were derived from public IIT Gandhinagar web pages, including:
  - Academic handbooks and course catalogues (`https://iitgn.ac.in/academics`)
  - Institute IT support FAQs and Eduroam configuration guides
  - Hostel and dining hall notices
- **Public Term Alignment**: Terminology complies with official institute nomenclature (e.g., *Academic Block 1*, *Eduroam*, *Moodle*, *Palaj Campus*).

---

## 4. Dataset Licensing Terms
The dataset and metadata are released under the:
**Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.
- **Permitted**: Sharing, copying, adapting, and transforming the material for academic research, education, and benchmarking.
- **Prohibited**: Commercial exploitation, resale, or proprietary commercial closed-source redistribution.
