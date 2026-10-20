# In-Depth Analysis of 10 Inter-Annotator Disagreements

This document examines 10 representative disagreements recorded between Annotator 1 (Rajdeep Vraj) and Annotator 2 (Vipul Sunil Patil) during Round 1 annotation.

### Case #1: Clip `AUD_SPK01_0005`
- **Spoken Query**: *"BTech seat acceptance fee payment portal open nathi thatu..."*
- **Annotator 1**: Transcript: *"BTech seat acceptance fee payment portal open nathi thatu..."* | Intent: `it_support`
- **Annotator 2**: Transcript: *"BTech seat acceptance fee payment portal open nthi thatu..."* | Intent: `admissions`
- **Consensus Ground Truth**: `admissions`
- **Disagreement Type**: Keyword heuristic vs root administrative purpose
- **Root Cause Analysis**: A1 saw 'portal open nathi thatu' and classified as IT infrastructure. A2 recognized the query originated from a prospective BTech candidate paying seat acceptance fees.
- **Resolution in Guidelines v2.0**: Guidelines v2 Section 3.3 explicitly rules that seat acceptance and onboarding portals belong to admissions.

### Case #2: Clip `AUD_SPK01_0010`
- **Spoken Query**: *"Admissions portal par offer letter accept karyu hatu pan confirmation email nathi aavyo..."*
- **Annotator 1**: Transcript: *"Admissions portal par offer letter accept karyu hatu pan confirmation email nathi aavyo..."* | Intent: `it_support`
- **Annotator 2**: Transcript: *"Admissions portal par offer letter accept karyu hatu pan confirmation email nthi aavyo..."* | Intent: `admissions`
- **Consensus Ground Truth**: `admissions`
- **Disagreement Type**: Communication failure vs admissions onboarding
- **Root Cause Analysis**: A1 flagged missing automated email as IT mail server issue. A2 focused on admission offer status.
- **Resolution in Guidelines v2.0**: Guidelines v2 mandates admissions office routing for all offer letter acknowledgments.

### Case #3: Clip `AUD_SPK01_0015`
- **Spoken Query**: *"Mess rebate form submit karyu hatu pan monthly bill ma deduction reflect nathi thayo..."*
- **Annotator 1**: Transcript: *"Mess rebate form submit karyu hatu pan monthly bill ma deduction reflect nathi thayo..."* | Intent: `student_services`
- **Annotator 2**: Transcript: *"Mess rebate form submit karyu hatu pan monthly bill ma deduction reflect nthi thayo..."* | Intent: `hostel_mess`
- **Consensus Ground Truth**: `hostel_mess`
- **Disagreement Type**: Accounts/Billing vs dining administration
- **Root Cause Analysis**: A1 treated 'bill deduction' as finance/student affairs accounting. A2 routed to mess rebate committee.
- **Resolution in Guidelines v2.0**: Guidelines v2 Section 3.2 explicitly assigns all dining hall billings and rebates to hostel_mess.

### Case #4: Clip `AUD_SPK01_0020`
- **Spoken Query**: *"Exam week ma night canteen timings extend thase ke usual barah baje close thai jase..."*
- **Annotator 1**: Transcript: *"Exam week ma night canteen timings extend thase ke usual barah baje close thai jase..."* | Intent: `hostel_mess`
- **Annotator 2**: Transcript: *"Exam week ma night canteen timings extend thase ke usual 12 baje close thai jase..."* | Intent: `hostel_mess`
- **Consensus Ground Truth**: `hostel_mess`
- **Disagreement Type**: Transcript numeric format disagreement
- **Root Cause Analysis**: A1 transcribed spoken Hindi number 'barah' in words, while A2 wrote Arabic numeral '12'.
- **Resolution in Guidelines v2.0**: Guidelines v2 Section 4 enforces writing spoken numbers out in words ('barah baje').

### Case #5: Clip `AUD_SPK01_0025`
- **Spoken Query**: *"Eduroam institute wifi connect nathi thatu, incorrect password error show kare chhe laptop ma..."*
- **Annotator 1**: Transcript: *"Eduroam institute wifi connect nathi thatu, incorrect password error show kare che laptop ma..."* | Intent: `it_support`
- **Annotator 2**: Transcript: *"Eduroam institute wifi connect nthi thatu, incorrect password error show kare chhe laptop ma..."* | Intent: `it_support`
- **Consensus Ground Truth**: `it_support`
- **Disagreement Type**: Transcript transliteration variance (che vs chhe, nathi vs nthi)
- **Root Cause Analysis**: Unstandardized phonetic transliteration of Gujarati auxiliary verb 'chhe' and negation 'nathi'.
- **Resolution in Guidelines v2.0**: Normative dictionary in Guidelines v2 mandates 'chhe' and 'nathi' across all annotators.

### Case #6: Clip `AUD_SPK01_0030`
- **Spoken Query**: *"Computer lab printers offline show kare chhe, pan printing quota credits account thi deduct thai gaya..."*
- **Annotator 1**: Transcript: *"Computer lab printers offline show kare chhe, pan printing quota credits account thi deduct thai gaya..."* | Intent: `student_services`
- **Annotator 2**: Transcript: *"Computer lab printers offline show kare chhe, pan printing quota credits account thi deduct thai gaya..."* | Intent: `it_support`
- **Consensus Ground Truth**: `it_support`
- **Disagreement Type**: Account credits monetary charge vs lab printing hardware
- **Root Cause Analysis**: A1 interpreted 'quota credits deduct' as financial accounting issue. A2 treated as IT printer infrastructure.
- **Resolution in Guidelines v2.0**: Guidelines v2 Section 3.1 classifies all computer center quota and lab printers as it_support.

### Case #7: Clip `AUD_SPK01_0035`
- **Spoken Query**: *"Official academic transcript and consolidated grade sheet status check karvo chhe for foreign university application..."*
- **Annotator 1**: Transcript: *"Official academic transcript and consolidated grade sheet status check karvo chhe for foreign university application..."* | Intent: `student_services`
- **Annotator 2**: Transcript: *"Official academic transcript and consolidated grade sheet status check karvo che for foreign university application..."* | Intent: `admissions`
- **Consensus Ground Truth**: `student_services`
- **Disagreement Type**: Outbound admission transcript vs institute admissions office
- **Root Cause Analysis**: A2 caught the keyword 'university application' and tagged admissions. A1 realized it is an enrolled student requesting academic records.
- **Resolution in Guidelines v2.0**: Guidelines v2 clarifies that outbound grade sheets and transcripts belong exclusively to student_services.

### Case #8: Clip `AUD_SPK01_0040`
- **Spoken Query**: *"Duplicate student identity card issue karva mate fine ketli bharvani chhe ane photo kya upload karvani..."*
- **Annotator 1**: Transcript: *"Duplicate student identity card issue karva mate fine ketli bharvani chhe ane photo kya upload karvani..."* | Intent: `it_support`
- **Annotator 2**: Transcript: *"Duplicate student identity card issue karva mate fine ketli bharvani chhe ane photo kya upload karvani..."* | Intent: `student_services`
- **Consensus Ground Truth**: `student_services`
- **Disagreement Type**: Identity credential administration vs IT photo portal
- **Root Cause Analysis**: A1 focused on 'photo kya upload karvani' as IT web portal task. A2 focused on student ID card fine and re-issuance.
- **Resolution in Guidelines v2.0**: Guidelines v2 Section 3.1 rules that lost card re-issuance and fines belong to student_services.

### Case #9: Clip `AUD_SPK01_0045`
- **Spoken Query**: *"Library digital repository papers download karta time gateway timeout error aave chhe..."*
- **Annotator 1**: Transcript: *"Library digital repository papers download karta time gateway timeout error aave chhe..."* | Intent: `student_services`
- **Annotator 2**: Transcript: *"Library digital repository papers download karta time gateway timeout error awe chhe..."* | Intent: `it_support`
- **Consensus Ground Truth**: `it_support`
- **Disagreement Type**: Library services vs network gateway error
- **Root Cause Analysis**: A1 considered library facilities as student services. A2 correctly recognized network HTTP 504 gateway timeout.
- **Resolution in Guidelines v2.0**: Guidelines v2 establishes that all gateway, DNS, and server errors route to it_support.

### Case #10: Clip `AUD_SPK01_0050`
- **Spoken Query**: *"Fee concession and merit scholarship reimbursement amount bank account ma kab transfer hoga..."*
- **Annotator 1**: Transcript: *"Fee concession and merit scholarship reimbursement amount bank account ma kab transfer hoga..."* | Intent: `student_services`
- **Annotator 2**: Transcript: *"Fee concession and merit scholarship reimbursement amount bank account ma kab transfer hoga..."* | Intent: `admissions`
- **Consensus Ground Truth**: `student_services`
- **Disagreement Type**: Entrance merit scholarship vs ongoing financial welfare
- **Root Cause Analysis**: A2 associated merit scholarship with admissions merit scholarships. A1 recognized student welfare bursary disbursement.
- **Resolution in Guidelines v2.0**: Guidelines v2 routes all ongoing semester bursaries and disbursements to student_services.

