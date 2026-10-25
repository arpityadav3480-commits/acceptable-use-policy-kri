# Acceptable Use Policy for a Small Research Organisation

**RedKross Research Foundation — Internship Task: Security Policy Writing**

| Field | Detail |
|---|---|
| **Intern** | Arpit Yadav |
| **Intern ID** | 2415 |
| **Task** | Draft an acceptable-use policy for a small research organisation |
| **Deadline** | 25 October 2026 |
| **Explanatory video** | 🎥 **[Watch the video](https://drive.google.com/file/d/1AelLUOuaCpB3-HJONwX6H2OoGNcrfn84/view?usp=sharing)** |

---

## 📌 Objective

The task was to draft an **Acceptable Use Policy (AUP)** for a small research organisation. The policy had to define:

- scope;
- acceptable use;
- prohibited actions;
- account and device responsibilities;
- data handling;
- reporting;
- a monitoring notice;
- consequences and escalation.

It also had to be a professional document with a **purpose, scope, responsibilities, rules, an exception process and a review date**.

The policy is written for **Kestrelwood Research Institute (KRI)**, a *fictional* non-profit research institute with about 30 users. A fictional organisation was used so that no real organisation's data or personal data appears in this repository.

## 📂 Deliverables

| Deliverable | File(s) |
|---|---|
| **Acceptable Use Policy (KRI-ISP-001 v1.0)** | [`policy/KRI-Acceptable-Use-Policy.pdf`](policy/KRI-Acceptable-Use-Policy.pdf) · [`.docx`](policy/KRI-Acceptable-Use-Policy.docx) · [`.md`](policy/KRI-Acceptable-Use-Policy.md) |
| **Technical Report** | [`report/Technical-Report.pdf`](report/Technical-Report.pdf) · [`.docx`](report/Technical-Report.docx) · [`.md`](report/Technical-Report.md) |
| Figure 1: Incident reporting and breach escalation | [`diagrams/incident-reporting-escalation.png`](diagrams/incident-reporting-escalation.png) (SVG source included) |
| Figure 2: Exception request process | [`diagrams/exception-process.png`](diagrams/exception-process.png) (SVG source included) |
| User acknowledgement form | [`forms/acknowledgement-form.md`](forms/acknowledgement-form.md) |
| Exception request form | [`forms/exception-request-form.md`](forms/exception-request-form.md) |
| New user onboarding checklist | [`checklists/user-onboarding-checklist.md`](checklists/user-onboarding-checklist.md) |
| Annual policy review checklist | [`checklists/policy-review-checklist.md`](checklists/policy-review-checklist.md) |
| Evaluation results | [`evaluation/policy-check-results.md`](evaluation/policy-check-results.md) |
| Screenshots of the final documents | [`screenshots/`](screenshots/) |

## 🗂️ Repository Structure

```
.
├── README.md
├── policy/          Acceptable Use Policy (Markdown source, DOCX, PDF)
├── report/          Technical report (Markdown source, DOCX, PDF)
├── diagrams/        Process diagrams (SVG source + PNG)
├── forms/           Acknowledgement and exception request forms
├── checklists/      Onboarding and annual review checklists
├── evaluation/      Output of the automated policy checks
├── screenshots/     Page previews of the final PDFs
├── video/           Narration script for the explanatory video
└── tools/           Build and check scripts
```

## 🧭 What the Policy Covers

| # | Section | Highlights |
|---|---|---|
| 1 | Purpose | Why the rules exist; meaning of *must / should / may* |
| 2 | Scope | Employees, interns, visitors, contractors; KRI and personal devices; on-site, remote and travelling |
| 3 | Definitions | Plain-English definitions of key terms |
| 4 | Roles and responsibilities | Executive Director, Information Security Lead, IT, managers/PIs, data owners, HR, all users |
| 5 | Acceptable use | Personal use, email, cloud services, **AI tools**, code, remote working, social media, clear desk |
| 6 | Prohibited actions | Access abuse, data misuse, harmful content, misuse of resources, concealment |
| 7 | Account responsibilities | Passphrases of 14+ characters, password manager, MFA, admin accounts, joiners/movers/leavers |
| 8 | Device responsibilities | Encryption, updates within 7 days, BYOD rules, report lost devices within **1 hour** |
| 9 | Data handling | Four-level classification (Public / Internal / Confidential / Restricted), participant data |
| 10 | Reporting | What, how and when to report; no-blame reporting; CERT-In and DPDP notification |
| 11 | Monitoring notice | What is monitored, **what is not**, who may approve access to content, log retention |
| 12 | Consequences and escalation | Four breach levels, seven-step escalation, right of appeal |
| 13 | Exception process | Risk-based approval, maximum 12 months, Exception Register |
| 14 | Review | Annual review; next review due **1 November 2027** |
| 15–16 | Acknowledgement, related documents | Plus Appendix A (quick reference) and Appendix B (exception form summary) |

## 🔬 Approach

1. **Requirement analysis.** Broke the task brief down into 13 required elements.
2. **Research.** Reviewed ISO/IEC 27001/27002:2022 (control 5.10), NIST SP 800-53 Rev. 5 (PL-4, AC-8, PS-6, PS-8, IR-6), NIST SP 800-63B-4, SP 800-61 Rev. 3 and SP 800-88 Rev. 2, CIS Controls v8.1, the SANS AUP template, and Indian law (IT Act 2000, DPDP Act 2023, CERT-In Directions 2022).
3. **Organisation profile and risks.** Defined a realistic fictional organisation and its main risks.
4. **Drafting.** Wrote the policy with clear requirement language, specific timeframes, tables and diagrams.
5. **Evaluation.** Wrote and ran an automated check script, and carried out a manual consistency review.
6. **Publishing.** Built DOCX and PDF versions and organised this repository.

Full details are in the [Technical Report](report/Technical-Report.pdf).

## ✅ Evaluation Results

From [`evaluation/policy-check-results.md`](evaluation/policy-check-results.md), generated by `tools/policy_check.py`:

| Check | Result |
|---|---|
| All task-brief elements present | ✅ 14/14 |
| Section cross-references valid | ✅ 10 checked, 0 broken |
| Referenced figures exist | ✅ 2/2 |
| Personal-data scan (emails and phone numbers) | ✅ 0 findings |
| Flesch Reading Ease | 39.2 (difficult). Identified as an area to improve. |

**Not done:** legal review, HR review, testing with real users, and tabletop exercises. See *Limitations* in the report.

## ⚙️ Setup and Usage

The documents are ready to read: open the PDFs in `policy/` and `report/`. To rebuild them or re-run the checks:

**Requirements:** Windows, Microsoft Word, Python 3.10 or later.

```bash
pip install -r tools/requirements.txt

# Run the automated policy checks (writes evaluation/policy-check-results.md)
python tools/policy_check.py

# Rebuild DOCX and PDF from the Markdown sources (uses Microsoft Word)
python tools/build_docs.py

# Rebuild the explanatory video from the screen recording and narration (needs ffmpeg; see video/video-script.md)
python tools/build_video.py
```

## 🎥 Explanatory Video

**Video link:** [Watch on Google Drive](https://drive.google.com/file/d/1AelLUOuaCpB3-HJONwX6H2OoGNcrfn84/view?usp=sharing)

The video explains the task, why acceptable-use policies matter, the approach taken, a walkthrough of the policy and supporting material, the evaluation results, and the limitations. The script is in [`video/video-script.md`](video/video-script.md).

## ⚠️ Disclaimer

- **Kestrelwood Research Institute is fictional.** All contact details use the reserved `.example` domain.
- This policy was written for an internship assignment. It is **not legal advice**. Any real organisation adopting it should have it reviewed by legal and HR professionals.
- No passwords, API keys, confidential information or personal data are stored in this repository.

## 📚 Key References

- ISO/IEC 27001:2022 and ISO/IEC 27002:2022 — Control 5.10, *Acceptable use of information and other associated assets*
- NIST SP 800-53 Rev. 5 — *Security and Privacy Controls for Information Systems and Organizations*
- NIST SP 800-63B-4 (2025), SP 800-61 Rev. 3 (2025) and SP 800-88 Rev. 2 (2025)
- CIS Critical Security Controls v8.1
- Information Technology Act, 2000; Digital Personal Data Protection Act, 2023; CERT-In Directions, 2022

The full reference list is in the [Technical Report](report/Technical-Report.md#11-references).

---

*Arpit Yadav · Intern ID 2415 · RedKross Research Foundation · October 2026*
