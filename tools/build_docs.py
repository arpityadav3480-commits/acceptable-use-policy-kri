"""Build DOCX and PDF versions of the policy and the technical report.

Pipeline: Markdown --(python-markdown)--> styled HTML --(Microsoft Word via export_word.ps1)--> DOCX + PDF

Requirements: Windows, Microsoft Word, Python 3 with `pip install -r tools/requirements.txt`.
Usage:  python tools/build_docs.py
"""
import re
import subprocess
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"

DOCS = [
    {
        "src": ROOT / "policy" / "KRI-Acceptable-Use-Policy.md",
        "header": "KRI-ISP-001  |  Acceptable Use Policy  |  Version 1.0  |  Classification: Internal",
    },
    {
        "src": ROOT / "report" / "Technical-Report.md",
        "header": "Technical Report  |  Arpit Yadav (Intern ID 2415)  |  RedKross Research Foundation",
    },
]

CSS = """
body { font-family: Calibri, 'Segoe UI', Arial, sans-serif; font-size: 11pt; color: #1A1A1A; }
h1 { font-size: 22pt; color: #1F3B57; border-bottom: 2px solid #2F5D8A; padding-bottom: 4pt; margin-bottom: 12pt; }
h2 { font-size: 15pt; color: #1F3B57; margin-top: 18pt; margin-bottom: 6pt; }
h3 { font-size: 12pt; color: #2F5D8A; margin-top: 12pt; margin-bottom: 4pt; }
p  { margin-top: 3pt; margin-bottom: 6pt; }
li { margin-bottom: 2pt; }
table { border-collapse: collapse; width: 100%; margin-top: 6pt; margin-bottom: 8pt; }
th, td { border: 1px solid #A6B4C3; padding: 4pt 6pt; vertical-align: top; font-size: 10pt; }
th { background: #DCE6F1; text-align: left; color: #1F3B57; }
blockquote { border-left: 3pt solid #2F5D8A; background: #F2F6FA; margin-left: 0; padding: 6pt 10pt; }
code { font-family: Consolas, monospace; font-size: 9.5pt; }
.toc-title { font-size: 15pt; color: #1F3B57; font-weight: bold; }
.caption { font-size: 9.5pt; color: #555555; text-align: center; }
"""


def to_html(src: Path) -> str:
    md = src.read_text(encoding="utf-8")
    md = md.replace("<!-- WORDTOC -->", '<p class="toc-title">Contents</p>\n\n<p>WORDTOC</p>')
    md = md.replace("<!-- pagebreak -->", "<br clear=all style='page-break-before:always'>")
    body = markdown.markdown(md, extensions=["tables", "sane_lists"])

    # Resolve image paths to absolute file paths so Word can embed them.
    def fix_img(m: re.Match) -> str:
        path = (src.parent / m.group(1)).resolve()
        return f'<img src="{path.as_uri()}" width="620"'
    body = re.sub(r'<img src="([^"]+)"', fix_img, body)
    # Centre figures and their captions.
    body = re.sub(r"<p>(<img [^>]+>)</p>", r'<p align="center">\1</p>', body)
    body = re.sub(r"<p><em>(Figure \d[^<]*)</em></p>", r'<p class="caption"><em>\1</em></p>', body)

    title = re.search(r"^# (.+)$", md, flags=re.M).group(1)
    return (f"<!DOCTYPE html><html><head><meta charset='utf-8'><title>{title}</title>"
            f"<style>{CSS}</style></head><body>{body}</body></html>")


def main() -> None:
    BUILD.mkdir(exist_ok=True)
    script = ROOT / "tools" / "export_word.ps1"
    for doc in DOCS:
        html_path = BUILD / (doc["src"].stem + ".html")
        html_path.write_text(to_html(doc["src"]), encoding="utf-8")
        out_base = doc["src"].with_suffix("")
        print(f"Exporting {doc['src'].name} -> .docx/.pdf")
        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script),
             "-Html", str(html_path), "-OutBase", str(out_base), "-Header", doc["header"]],
            check=True,
        )


if __name__ == "__main__":
    main()
