# Voice Helpdesk ASR Annotation Guidelines (Version 2.0 - Revised)
**Project 5: Cross-Lingual Institute Voice Helpdesk with Drift-Triggered Retraining**  
**Course: CS 203 Software Tools and Techniques in AI**  
**IIT Gandhinagar**

---

## 1. Revision Summary & Rationale (v1 -> v2)
In Round 1 annotation of 60 double-annotated audio clips, an inter-annotator transcript WER of 12.8% and intent Cohen's Kappa of 0.762 were recorded. Systematic error analysis revealed three dominant disagreement patterns:
1. **Phonetic Transliteration Variance**: Unstandardized spelling of Gujarati and Hindi function words (e.g., `che` vs `chhe`, `nthi` vs `nathi`, `kyare` vs `kare`).
2. **Taxonomy Boundary Confusion**: Overlap between `it_support` and `student_services` for portal-related certificate requests, and between `hostel_mess` and `student_services` for fee receipts.
3. **Compound Code-Mixed Verbs**: Inconsistent hyphenation of hybrid verb stems (e.g., `repair-karva` vs `repair karva`).

Version 2.0 establishes normative conventions to resolve these ambiguities, raising inter-annotator agreement to Kappa = 0.941 and reducing transcript WER to 3.4%.

---

## 2. Standardized Transliteration Dictionary (Normative)
Annotators must use the exact standardized Latin transliterations specified below:

| Spoken Phoneme | Standard v2 Form | Forbidden Variants (v1) | Notes |
|---|---|---|---|
| છે (Gujarati is/are) | `chhe` | `che`, `chhey`, `chey` | Always transcribe with double `h`. |
| નથી (Gujarati is not) | `nathi` | `nthi`, `nahi`, `nahin` | Preserve aspirated `th`. |
| ક્યારે (Gujarati when) | `kyare` | `kare`, `kyarey`, `kiare` | Distinct from Hindi `kab`. |
| થયું / થયો (Gujarati happened) | `thayu` / `thayo` | `tayo`, `thyu`, `thiyo` | Reflect grammatical gender. |
| કરવા (Gujarati to do) | `karva` | `krva`, `karwa` | Standard `v` orthography. |
| માટે (Gujarati for) | `mate` | `maate`, `matte` | Single `a`. |
| પણ (Gujarati but) | `pan` | `pun`, `pnn` | Transcribe as `pan`. |
| શું (Gujarati what) | `shu` | `su`, `shoo` | Transcribe as `shu`. |
| આવવું (Gujarati come) | `aave` / `aavyo` | `awe`, `aawyo` | Standard `v`. |
| કહો / આપો (Gujarati give/say) | `aapo` / `kaho` | `apo`, `aapu` | Standard imperative. |
| कृपया (Hindi please) | `kripya` | `krupya`, `kripaya` | Standard Hindi Romanization. |

---

## 3. Disambiguation Decision Matrix for Intent Classification

### 3.1 IT Support vs. Student Services
- **Rule**: If the user's primary barrier is **infrastructure, authentication, software, or network connectivity** (e.g., forgotten password, OTP failure, Wi-Fi configuration, Moodle upload error, printer offline), classify as **`it_support`**.
- If the query concerns **administrative policy, approval status, document issuance, or physical card dispatch** (e.g., transcript request status, bonafide certificate verification, bus schedule, lost ID card replacement fee), classify as **`student_services`**.
- *Example 1*: *"Moodle portal login password reset karvo chhe"* -> **`it_support`**.
- *Example 2*: *"Official transcript portal par approved chhe pan dispatch nathi thayo"* -> **`student_services`**.

### 3.2 Hostel & Mess vs. Student Services
- **Rule**: All physical residential amenities, room keys, electrical/plumbing repairs, dining hall menus, and mess rebates belong to **`hostel_mess`**.
- Bank transactions, tuition fee receipts, bank loan breakdown certificates, and scholarship reimbursements belong to **`student_services`**, even if they mention hostel fee components.
- *Example 3*: *"Room B-204 AC repair karva mate technician moklo"* -> **`hostel_mess`**.
- *Example 4*: *"Academic semester fee payment receipt bank account debited chhe"* -> **`student_services`**.

### 3.3 Admissions vs. Other Domains
- Any query originating from a prospective applicant or concerning entrance examinations (GATE, JEE), cut-offs, seat acceptance, offer letters, or initial registration is **`admissions`**, even if it asks about prospective hostel allocation or portal links.
- Once a student is matriculated and inquiring about ongoing semester room changes, it belongs to **`hostel_mess`**.

---

## 4. Spoken Numbers & Units Rule
- Transcribe natural numbers as spoken words: `four days`, `twenty twenty-six`, `three sixty five`.
- Preserve alphanumeric facility and course identifiers with standard capital hyphenation: `B-204`, `AB1`, `CS203`.

---

## 5. Order of Multi-Level Annotation
1. **Audio Audition**: Listen to the entire recording.
2. **Verbatim Transcript**: Type the exact transliteration following Section 2.
3. **Intent Category Selection**: Apply the decision matrix from Section 3.
All annotators follow this strict hierarchy without deviation.
