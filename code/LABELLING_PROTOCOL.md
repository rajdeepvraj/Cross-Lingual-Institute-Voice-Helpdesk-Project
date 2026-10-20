# Labelling Protocol (LABELLING_PROTOCOL.md)
**Project 5: Cross-Lingual Institute Voice Helpdesk with Drift-Triggered Retraining**  
**Course: CS 203 Software Tools and Techniques in AI**  
**IIT Gandhinagar**

---

## 1. Overview & Anonymised Annotator Roster
This protocol documents the exact operational procedures used to transcribe and label speech helpdesk recordings for Assignment 1.

| Annotator Identifier | Full Name / Institutional Role | Email Identifier | Assigned Annotation Tasks |
|---|---|---|---|
| `A1_RAJDEEP` | Rajdeep Vraj (Group Member) | `rajdeep.vraj@iitgn.ac.in` | Double annotation of Rounds 1 & 2 (120 clips), Guidelines author |
| `A2_VIPUL` | Vipul Sunil Patil (Group Member) | `vipul.patil@iitgn.ac.in` | Independent double annotation of Rounds 1 & 2 (120 clips) |
| `A3_SATVIK` | Satvik Sharma (Group Member) | `satvik.sharma@iitgn.ac.in` | Independent Adjudicator & Disagreement Arbiter |

---

## 2. Tools & Guideline Versions per Round
- **Annotation Software**: `Label Studio 1.13.0`
- **Project Configuration**: `code/label_studio_config.xml` (defining `<AudioPlus>`, verbatim `<TextArea>`, and 4-way `<Choices>`).
- **Round 1**:
  - Sample: 60 audio clips (`AUD_SPK01_0001` through `AUD_SPK02_0060`).
  - Active Guideline: `code/guidelines/guidelines_v1.md`.
  - Export Files: `annotator1_round1.json`, `annotator2_round1.json`.
- **Round 2**:
  - Sample: 60 audio clips (`AUD_SPK02_0061` through `AUD_SPK03_0120`).
  - Active Guideline: `code/guidelines/guidelines_v2.md` (normative transliteration dictionary and intent disambiguation matrix).
  - Export Files: `annotator1_round2.json`, `annotator2_round2.json`.

---

## 3. Order of Multi-Level Annotation (Fixed Hierarchy)
The label levels specified for Project 5 are:
1. **Level 1**: Multilingual Speech Transcript
2. **Level 2**: Administrative Intent Category (`admissions`, `hostel_mess`, `it_support`, `student_services`)

### Strict Sequential Execution Order:
Every annotator followed the exact 3-step sequence:
1. **Auditory Audition**: Listen to the complete speech clip at standard listening volume.
2. **Verbatim Text Transcription**: Type out the exact spoken dialogue in the text area according to the spelling and transliteration dictionary.
3. **Intent Category Selection**: Select the single matching radio choice from the four domains.

### Rationale:
If an annotator selects the intent category first, cognitive confirmation bias induces them to paraphrase or normalize the free-text transcript toward domain keywords (e.g. converting *"room cooler issue"* to *"hostel maintenance"*). Enforcing transcription first ensures auditory fidelity, requiring the annotator to parse every phoneme before deciding administrative routing.

---

## 4. Item Presentation Order & Randomization
- Audio clips were imported into Label Studio in pseudo-randomized order using a deterministic seed (`RANDOM_SEED = 42`).
- Both annotators were presented with clips in the exact same randomized sequence to ensure identical cognitive fatigue patterns.

---

## 5. Annotator Visibility & Information Masking
- **Zero Pre-Annotations**: No ASR model predictions, pre-transcriptions, or automated classifications were shown to annotators. Text boxes started empty.
- **Mutual Blindness**: Annotators worked independently on isolated client instances. Neither annotator could view the other annotator's transcripts, choices, or progress.
- **Metadata Masking**: Annotators were blind to speaker metadata (speaker name, region, demographic cohort).

---

## 6. Disagreement Resolution & Adjudication
- When transcripts differed, edit distance was computed. Transliteration discrepancies were resolved by matching against the Guidelines v2 normative dictionary.
- When intent classifications differed, the clip was escalated to Adjudicator `A3_SATVIK`.
- The adjudicator listened to the clip, evaluated the root cause according to Section 3 of Guidelines v2, and entered the binding consensus label into `data/gold_test_set.csv`.

---

## 7. Annotation Timeline & Provenance
| Phase | Date | Milestones & Activities |
|---|---|---|
| Phase 1: Setup | 2026-10-06 | Label Studio deployment, XML interface validation, Guidelines v1.0 release |
| Phase 2: Round 1 | 2026-10-08 | Independent annotation of 60 clips by A1 and A2 under Guidelines v1.0 |
| Phase 3: Audit | 2026-10-10 | Agreement calculation (WER 8.77%, Kappa 0.686), disagreement analysis of 10 cases |
| Phase 4: Revision | 2026-10-12 | Guidelines v2.0 published with normative dictionary and intent boundary rules |
| Phase 5: Round 2 | 2026-10-14 | Independent annotation of 60 clips under Guidelines v2.0 (WER 0.53%, Kappa 0.955) |
| Phase 6: Freezing | 2026-10-16 | Adjudication of residual conflicts and cryptographic freezing of `gold_test_set.csv` |
