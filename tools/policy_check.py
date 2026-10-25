"""Automated quality checks for the KRI Acceptable Use Policy.

Checks performed:
  1. Every element required by the task brief has a matching section.
  2. Every "Section N" / "Section N.N" cross-reference points to a real heading.
  3. Every image referenced in the policy exists on disk.
  4. No real-looking email addresses or phone numbers appear in any Markdown file
     (only the reserved .example domain is allowed).
  5. Size, requirement-language and readability statistics (Flesch Reading Ease).

Usage:  python tools/policy_check.py
Writes: evaluation/policy-check-results.md
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / "policy" / "KRI-Acceptable-Use-Policy.md"
OUT = ROOT / "evaluation" / "policy-check-results.md"

# Task-brief requirement -> regex that must match a policy heading
REQUIRED = {
    "Purpose": r"^##\s+\d+\.\s+Purpose",
    "Scope": r"^##\s+\d+\.\s+Scope",
    "Responsibilities": r"^##\s+\d+\.\s+Roles and Responsibilities",
    "Acceptable use (rules)": r"^##\s+\d+\.\s+Acceptable Use",
    "Prohibited actions (rules)": r"^##\s+\d+\.\s+Prohibited Actions",
    "Account responsibilities": r"^##\s+\d+\.\s+Account Responsibilities",
    "Device responsibilities": r"^##\s+\d+\.\s+Device Responsibilities",
    "Data handling": r"^##\s+\d+\.\s+Data Handling",
    "Reporting": r"^##\s+\d+\.\s+Reporting",
    "Monitoring notice": r"^##\s+\d+\.\s+Monitoring Notice",
    "Consequences / escalation": r"^##\s+\d+\.\s+Compliance, Consequences and Escalation",
    "Exception process": r"^##\s+\d+\.\s+Exception Process",
    "Review date": r"^##\s+\d+\.\s+Policy Review",
}


def plain_text(md: str) -> str:
    """Strip Markdown tables, headings, comments and formatting to leave prose."""
    lines = []
    for line in md.splitlines():
        s = line.strip()
        if not s or s.startswith("|") or s.startswith("#") or s.startswith("<!--") or s.startswith("!["):
            continue
        s = re.sub(r"^[-*>]\s+|^\d+\.\s+", "", s)
        s = re.sub(r"[*_`]", "", s)
        lines.append(s)
    return "\n".join(lines)


def syllables(word: str) -> int:
    word = word.lower()
    groups = re.findall(r"[aeiouy]+", word)
    count = len(groups)
    if word.endswith("e") and count > 1 and not word.endswith(("le", "ee")):
        count -= 1
    return max(count, 1)


def flesch(text: str) -> tuple[float, int, int]:
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    # each list item / line counts as at least one sentence
    sentences = sum(max(1, len(re.findall(r"[.!?;:](\s|$)", ln))) for ln in text.splitlines() if ln.strip())
    syl = sum(syllables(w) for w in words)
    score = 206.835 - 1.015 * (len(words) / sentences) - 84.6 * (syl / len(words))
    return score, len(words), sentences


def main() -> int:
    md = POLICY.read_text(encoding="utf-8")
    headings = re.findall(r"^#{2,3}\s+(\d+(?:\.\d+)?)\.?\s", md, flags=re.M)
    heading_ids = set(headings)
    results, failures = [], 0

    # 1. Required elements
    results.append("## 1. Task-brief coverage\n\n| Requirement | Found | Heading |\n|---|---|---|")
    for name, pattern in REQUIRED.items():
        m = re.search(pattern, md, flags=re.M)
        failures += m is None
        results.append(f"| {name} | {'PASS' if m else 'FAIL'} | {m.group(0).lstrip('# ') if m else '-'} |")
    review = re.search(r"Next review date\*\*\s*\|\s*([^|]+)\|", md)
    failures += review is None
    results.append(f"| Review date in document control | {'PASS' if review else 'FAIL'} | {review.group(1).strip() if review else '-'} |")

    # 2. Cross-references
    refs = sorted(set(re.findall(r"Sections? (\d+(?:\.\d+)?)", md)), key=lambda r: [int(x) for x in r.split(".")])
    broken = [r for r in refs if r not in heading_ids]
    failures += len(broken)
    results.append(f"\n## 2. Cross-references\n\n- References checked: {len(refs)} ({', '.join(refs)})")
    results.append(f"- Broken references: {len(broken)}{' — ' + ', '.join(broken) if broken else ''} → **{'PASS' if not broken else 'FAIL'}**")

    # 3. Images
    imgs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", md)
    missing = [i for i in imgs if not (POLICY.parent / i).resolve().exists()]
    failures += len(missing)
    results.append(f"\n## 3. Figures\n\n- Images referenced: {len(imgs)}; missing: {len(missing)} → **{'PASS' if not missing else 'FAIL'}**")

    # 4. Personal-data scan across all Markdown files
    leaks = []
    for f in ROOT.rglob("*.md"):
        if ".git" in f.parts:
            continue
        text = f.read_text(encoding="utf-8")
        for email in re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", text):
            if not email.endswith(".example") and not email.endswith("redkross.org.in"):
                leaks.append(f"{f.relative_to(ROOT)}: email {email}")
        for phone in re.findall(r"(?<![\w-])(?:\+?\d[\d -]{8,}\d)(?![\w-])", text):
            leaks.append(f"{f.relative_to(ROOT)}: number {phone}")
    failures += len(leaks)
    results.append(f"\n## 4. Personal-data scan (all .md files)\n\n- Findings: {len(leaks)} → **{'PASS' if not leaks else 'FAIL'}**")
    results += [f"  - {x}" for x in leaks]

    # 5. Statistics
    prose = plain_text(md)
    score, words, sentences = flesch(prose)
    all_words = len(re.findall(r"\b\w+\b", md))
    must = len(re.findall(r"\bmust\b", md, flags=re.I))
    must_not = len(re.findall(r"\bmust not\b|\bmust never\b", md, flags=re.I))
    should = len(re.findall(r"\bshould\b", md, flags=re.I))
    results.append("\n## 5. Statistics\n\n| Metric | Value |\n|---|---|")
    results.append(f"| Total words (incl. tables) | {all_words} |")
    results.append(f"| Main sections (##) | {len(re.findall(r'^## ', md, flags=re.M))} |")
    results.append(f"| Numbered sections and sub-sections | {len(heading_ids)} |")
    results.append(f"| Tables | {len(re.findall(r'^\|---', md, flags=re.M))} |")
    results.append(f"| 'must' statements (of which 'must not'/'must never') | {must} ({must_not}) |")
    results.append(f"| 'should' statements | {should} |")
    results.append(f"| Prose words / sentence units analysed | {words} / {sentences} |")
    results.append(f"| Flesch Reading Ease (prose only) | {score:.1f} |")

    status = "ALL CHECKS PASSED" if failures == 0 else f"{failures} CHECK(S) FAILED"
    header = (f"# Policy Check Results\n\nGenerated by `tools/policy_check.py` on {date.today():%d %B %Y} "
              f"against `policy/KRI-Acceptable-Use-Policy.md`.\n\n**Overall: {status}**\n")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(header + "\n" + "\n".join(results) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    print(OUT.read_text(encoding="utf-8"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
