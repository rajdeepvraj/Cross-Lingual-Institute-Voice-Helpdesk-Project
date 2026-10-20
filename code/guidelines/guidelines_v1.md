# Voice Helpdesk ASR Annotation Guidelines (Version 1.0)
**Project 5: Cross-Lingual Institute Voice Helpdesk with Drift-Triggered Retraining**  
**Course: CS 203 Software Tools and Techniques in AI**  
**IIT Gandhinagar**

---

## 1. Objectives & Scope
These guidelines define the protocol for dual-level annotation of spoken helpdesk audio queries at IIT Gandhinagar:
1. **Level 1 (Transcription)**: Verbatim text representation of multilingual code-mixed speech (Indian English, Hindi, and Gujarati).
2. **Level 2 (Intent Classification)**: Multi-class routing destination among four institute administrative domains.

Every audio clip is evaluated independently by two annotators without viewing each other's work or prior model predictions.

---

## 2. Order of Annotation
Annotators must strictly execute annotations in the following sequence:
1. **Listen to full audio** at standard volume without interruptions.
2. **Transcribe Level 1**: Type the verbatim transcript matching spoken words.
3. **Assign Level 2**: Select the single best intent routing category.

*Rationale*: Transcribing first forces the annotator to parse every word and phoneme attentively, preventing premature categorization bias based solely on the greeting.

---

## 3. Level 1: Transcription Rules (v1)

### 3.1 Script & Transliteration
- Spoken English words must be transcribed in standard English Latin orthography (e.g., `admission`, `hostel`, `wifi`, `certificate`).
- Spoken Hindi and Gujarati words must be transliterated into Latin characters phonetically according to common Indian Romanization:
  - Examples: `nathi`, `chhe`, `karyu`, `hata`, `kyare`, `kaise`, `kahan`, `kripya`.
- Do not mix Devanagari or Gujarati native scripts within the same Latin transcript.

### 3.2 Spoken Numbers & Codes
- Transcribe numbers as words (e.g., `four hundred`, `twenty twenty-six`).
- Alphanumeric codes, block names, and room numbers retain hyphenated capital notation (e.g., `B-204`, `CS203`, `AB1`).

### 3.3 Filler Words & Hesitations
- Transcribe audible hesitations as `[uh]`, `[um]`, `[ah]`.
- False starts should be transcribed as spoken (e.g., `hu hu apply karva mangu chhu`).

### 3.4 Punctuation
- Use standard sentence punctuation (`.`, `,`, `?`) to capture prosodic boundaries.

---

## 4. Level 2: Intent Taxonomy (v1)

| Intent Category | Primary Scope | Typical Queries |
|---|---|---|
| `admissions` | Inquiries regarding entrance exams, eligibility, application forms, seat acceptance, cutoff ranks, open house, and physical reporting. | BTech/MTech/MSc/PhD eligibility, GATE/JEE score cutoff, seat acceptance fee, document verification. |
| `hostel_mess` | Residential life, room allocation, maintenance, dining halls, rebates, laundry, and amenities. | Room AC repair, mess rebate deduction, geyser issues, mess food menu, late night canteen. |
| `it_support` | Campus computing infrastructure, network, software licenses, lab servers, email, and institute portal access. | Eduroam Wi-Fi credentials, institute email password reset, Moodle upload issue, HPC node access. |
| `student_services` | Academic office, student affairs, certificates, identity cards, transport, and welfare services. | Transcript issuance, bonafide certificate, bus schedule to Gandhinagar, medical insurance card, lost ID card. |

---

## 5. Ambiguities & Edge Cases (Known in v1)
- **ID Cards**: If a student asks about their ID card, mark it according to their question.
- **Fees**: Tuition fee is academic, hostel fee is residential.
- **Portals**: If a portal error occurs while paying fees, mark whichever seems most relevant.
