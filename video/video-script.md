# Explanatory Video — Script and Outline

**Target length:** 6–8 minutes · **Format:** screen recording with voice-over (webcam optional)
**Upload:** YouTube (Unlisted) or Google Drive (anyone with the link can view) → paste the link into `README.md`

**Tips**

- Record with OBS Studio, the Xbox Game Bar (Windows + Alt + R), or Loom.
- Close email and chat apps, and hide any personal notifications before recording.
- Speak naturally. You don't need to read this script word for word.

---

## 1. Introduction (0:00–0:40)

**Show:** the GitHub repository README.

> "Hello, I'm Arpit Yadav, Intern ID 2415, at RedKross Research Foundation. My task was security policy writing. Specifically, I drafted an acceptable use policy for a small research organisation. In this video I'll explain what the task involved, why it matters, how I approached it, what I created, and the limitations of my work."

## 2. What the task is and why it matters (0:40–1:40)

**Show:** the task requirements (the README *Objective* section).

> "An acceptable use policy, or AUP, sets the rules for how people may use an organisation's systems, devices and data. It turns security goals into everyday behaviour.
>
> It matters because most breaches involve people. Verizon's 2024 Data Breach Investigations Report found that 68 percent of breaches involved a non-malicious human element, such as phishing or a simple mistake.
>
> Small research organisations are especially exposed. They hold sensitive participant data and unpublished research, they have many short-term users like interns and visiting researchers, and they usually have very few IT staff.
>
> The brief asked me to cover scope, acceptable use, prohibited actions, account and device responsibilities, data handling, reporting, a monitoring notice, and consequences and escalation, with a purpose, responsibilities, an exception process and a review date."

## 3. My approach (1:40–2:40)

**Show:** the Technical Report, *Methodology* table.

> "I followed eight steps. First I broke the brief down into 13 required elements. Then I researched the standards: ISO 27002 control 5.10 on acceptable use, NIST SP 800-53 controls such as PL-4 Rules of Behavior and AC-8 System Use Notification, NIST's password guidance, CIS Controls, and Indian law, including the IT Act, the DPDP Act 2023 and the CERT-In directions.
>
> I created a fictional organisation, Kestrelwood Research Institute, so the policy could be specific without exposing any real organisation's data. I identified its main risks, drafted the policy, created the supporting material, and then evaluated everything."

## 4. Walkthrough of the policy (2:40–5:00)

**Show:** the policy PDF. Scroll to each section as you talk about it.

- **Document control** (cover page): "Every professional policy has an owner, an approver, an effective date and a review date. The next review is due on 1 November 2027."
- **Sections 1–4:** "The purpose, a scope covering interns, visitors and personal devices, definitions, and seven defined roles."
- **Section 5, Acceptable use:** "This includes a section on AI tools. You must not put confidential data into public AI tools."
- **Section 6, Prohibited actions:** "Five categories. There's also a controlled route for legitimate research, such as malware analysis."
- **Sections 7–8, Accounts and devices:** "Passphrases of 14 or more characters, MFA, never approving an MFA prompt you didn't start, and reporting a lost device within one hour."
- **Section 9, Data handling:** *show the classification table.* "Four levels: Public, Internal, Confidential and Restricted, each with examples and handling rules."
- **Section 10, Reporting:** *show Figure 1.* "Clear timeframes, and a no-blame approach, because people who fear punishment report incidents late."
- **Section 11, Monitoring notice:** "It is transparent about what is monitored and, importantly, about what is *not* monitored. For example, there is no keystroke logging, and access to message content needs the Executive Director's approval."
- **Section 12, Consequences:** *show the breach-levels table.* "Four graduated levels, an escalation process and a right of appeal."
- **Section 13, Exceptions:** *show Figure 2.* "Risk-based approval, a 12-month maximum, and a register of exceptions."

## 5. Supporting material (5:00–5:40)

**Show:** the `forms/` and `checklists/` folders on GitHub.

> "To make the policy usable in practice, I also created an acknowledgement form, an exception request form, an onboarding checklist for new users, and an annual review checklist for the policy owner."

## 6. Evaluation and results (5:40–6:40)

**Show:** run `python tools/policy_check.py` in a terminal, then show `evaluation/policy-check-results.md`.

> "A policy can't be run like software, so I wrote a Python script to check it. The script confirmed that all of the brief's requirements are covered, all 10 internal cross-references are valid, both figures exist, and there is no personal data in the repository. I also checked by hand that timeframes such as 'one hour' and 'ten working days' are consistent across the policy, the diagrams and the forms.
>
> The script also measured readability. The Flesch score was 39.2, which means the text is fairly difficult to read. That's typical for policies, but it's something to improve."

## 7. Limitations and conclusion (6:40–7:30)

**Show:** the report's *Limitations* and *Recommendations* sections.

> "To be honest about the limits: the organisation is fictional, the policy hasn't been reviewed by legal or HR professionals, and it hasn't been tested with real users. Before a real organisation adopted it, I'd recommend legal review, a pilot with one team, awareness training, and a tabletop exercise to test the reporting process.
>
> In conclusion, the policy covers every requirement in the brief, is grounded in recognised standards, and is designed to be practical. Thank you for watching. All files are in my GitHub repository."
