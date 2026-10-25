# Explanatory Video — Narration Script

**Video:** [Watch on Google Drive](https://drive.google.com/file/d/1AelLUOuaCpB3-HJONwX6H2OoGNcrfn84/view?usp=sharing) (about 6 minutes)

The video combines a silent screen recording (`video/raw.mp4`) with narration recorded separately as **nine short audio files**, one per section below. `tools/build_video.py` speeds up or slows down each section of the recording to match the length of its narration, adds the parts the recording does not show (policy Sections 11–13, Figures 1 and 2, and the policy check output), and writes `video/final.mp4`. The video and audio files are not stored in this repository.

## How to rebuild the video

1. Record **one audio file per section**, named after the headings below (e.g. `01-intro.m4a` or `intro.m4a`). Any of `.m4a .mp3 .wav .aac .ogg .opus` is fine.
2. Put the files in `video/audio/` and the screen recording at `video/raw.mp4`.
3. Run `python tools/build_video.py` (needs ffmpeg: `winget install Gyan.FFmpeg`).

---

## 01-intro

*On screen: GitHub README header.*

> Hello, I'm Arpit Yadav, Intern ID 2415, at RedKross Research Foundation. My task was security policy writing: drafting an acceptable use policy for a small research organisation.
>
> In this video I'll explain what the task involved, why it matters, how I approached it, what I created, how I checked it, and the limitations of my work.

## 02-why

*On screen: README Objective section.*

> An acceptable use policy, or AUP, sets the rules for how people may use an organisation's systems, devices and data. It turns security goals into everyday behaviour.
>
> This matters because most breaches involve people. Verizon's 2024 Data Breach Investigations Report found that 68 percent of breaches involved a non-malicious human element, such as falling for phishing or simply making a mistake.
>
> Small research organisations are especially exposed. They hold sensitive participant data and unpublished research, they have many short-term users like interns and visiting researchers, and they usually have very few IT staff.
>
> The brief asked me to cover scope, acceptable use, prohibited actions, account and device responsibilities, data handling, reporting, a monitoring notice, and consequences and escalation, and to include a purpose, responsibilities, an exception process and a review date.

## 03-approach

*On screen: Technical Report, Methodology table and key risks.*

> I followed eight steps. First, I broke the brief down into 13 required elements, so I could track each one.
>
> Then I researched the standards: ISO 27002 control 5.10 on acceptable use; NIST SP 800-53 controls such as PL-4, Rules of Behavior, and AC-8, System Use Notification; NIST's password guidance; the CIS Controls; and Indian law, including the IT Act, the DPDP Act 2023 and the CERT-In directions.
>
> I created a fictional organisation, Kestrelwood Research Institute, so the policy could be specific without exposing any real organisation's data. I identified its main risks, drafted the policy, created the supporting material, and finally evaluated everything.

## 04-policy

*On screen: policy PDF, from the cover page through Section 9.*

> This is the finished policy, reference KRI-ISP-001, version 1.0. Like any professional policy, it has an owner, an approver, an effective date and a review date. The next review is due by 1 November 2027.
>
> Sections 1 to 4 set the foundations: the purpose; a scope that covers employees, interns, visitors and contractors, on KRI and personal devices; plain-English definitions; and clear responsibilities for each role.
>
> Section 5 explains what people may do. One part I want to highlight is AI tools: staff may use approved AI tools for public and internal information, but they must never put confidential or restricted data into public AI tools.
>
> Section 6 groups prohibited actions into five categories. Because this is a research organisation, there's also a controlled route for legitimate research, for example malware analysis, which needs an approved exception and an isolated environment.
>
> Sections 7 and 8 cover accounts and devices: passphrases of at least 14 characters, a password manager, multi-factor authentication, and never approving an MFA prompt you didn't start. Updates must be installed within 7 days, and a lost or stolen device must be reported within one hour.
>
> Section 9 classifies information into four levels: Public, Internal, Confidential and Restricted. Each level has examples and clear handling rules.

## 05-reporting

*On screen: Section 10, then Figure 1 (reporting and escalation diagram).*

> Section 10 explains what to report, how, and how quickly. The policy uses a no-blame approach, because people who fear punishment report incidents late, and late reports cause more damage.
>
> This diagram shows the reporting and escalation path. It also covers outside notification, such as CERT-In's six-hour reporting rule.

## 06-monitoring-to-exceptions

*On screen: Sections 11, 12 and 13, ending on Figure 2.*

> Section 11 is the monitoring notice. It's transparent about what is monitored and, just as importantly, what is not. For example, there is no keystroke logging, and accessing the content of someone's messages needs the Executive Director's approval. Logs are kept for 12 months.
>
> Section 12 sets out four graduated breach levels, from a minor mistake to a deliberate serious breach, with a step-by-step escalation process and a right of appeal within 10 working days.
>
> Finally, Section 13 is the exception process. Requests are approved based on risk, decided within 10 working days, limited to a maximum of 12 months, and recorded in an exception register.

## 07-supporting

*On screen: README Deliverables table, forms folder.*

> To make the policy usable in practice, I also created an acknowledgement form that users sign, an exception request form, an onboarding checklist for new users, and an annual review checklist for the policy owner.

## 08-evaluation

*On screen: terminal running `python tools/policy_check.py`.*

> A policy can't be run like software, so I wrote a Python script to check it. Here it is running.
>
> The script confirmed that all of the brief's requirements are present, all 10 internal cross-references are valid, both figures exist, and there is no personal data in the repository. I also checked by hand that timeframes like one hour and ten working days are consistent across the policy, the diagrams and the forms.
>
> The script also measured readability. The Flesch score was 39.2, which means the text is fairly difficult to read. That's typical for policies, but it's an area I'd improve.

## 09-limitations

*On screen: Technical Report, Limitations and Recommendations.*

> To be honest about the limits: the organisation is fictional, the policy hasn't been reviewed by legal or HR professionals, and it hasn't been tested with real users. It also assumes tools like MFA and device management are already in place.
>
> Before a real organisation adopted it, I'd recommend a legal review, a pilot with one team, awareness training, and a tabletop exercise to test the reporting process.
>
> In conclusion, the policy covers every requirement in the brief, is grounded in recognised standards, and is designed to be practical. All the files are in my GitHub repository. Thank you for watching.
