"""Build the explanatory video from the screen recording and the recorded narration.

Pipeline: video/raw.mp4 (silent screen recording) + video/audio/*.m4a (one narration file per
section of video/video-script.md) --(ffmpeg)--> video/final.mp4

Each section of the recording is sped up or slowed down to fit the length of its narration. Parts
missing from the recording (policy Sections 11-13 with Figures 1 and 2, and the policy check run)
are generated from the policy PDF and the evaluation results.

Requirements: ffmpeg (winget install Gyan.FFmpeg), Python 3 with `pip install -r tools/requirements.txt`.
Usage:  python tools/build_video.py              # narration from video/audio/, writes video/final.mp4
        python tools/build_video.py --no-title   # without the 4-second title card
        python tools/build_video.py --audio DIR --out FILE
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "video" / "raw.mp4"
AUDIO_DIR = ROOT / "video" / "audio"
OUT = ROOT / "video" / "final.mp4"
WORK = ROOT / "build" / "video"

W, H = 1906, 1026          # size of the screen recording; everything is drawn at this size
FINAL_PAD = "pad=1920:1080:7:27:black,setsar=1,fps=30,format=yuv420p"
BG = "#0d1117"             # GitHub dark background, to match the recording
FONTS = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
AUDIO_EXT = (".m4a", ".mp3", ".wav", ".aac", ".ogg", ".opus", ".webm", ".flac")

# Speed limits for the recording: 0.5 = twice as fast, 2.0 = half speed. Beyond these the
# clip is trimmed or its last frame is held instead.
MIN_STRETCH, MAX_STRETCH = 0.5, 2.0
ENCODE = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", "30"]


def ffmpeg_bin(name):
    found = shutil.which(name)
    if found:
        return found
    pattern = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\ffmpeg-*\bin")
    for folder in glob.glob(pattern):
        if Path(folder, name + ".exe").exists():
            return str(Path(folder, name + ".exe"))
    sys.exit(f"{name} not found. Install it with: winget install Gyan.FFmpeg")


FFMPEG, FFPROBE = ffmpeg_bin("ffmpeg"), ffmpeg_bin("ffprobe")


def run(args):
    subprocess.run([FFMPEG, "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def duration(path):
    out = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
                         check=True, capture_output=True, text=True).stdout
    return float(json.loads(out)["format"]["duration"])


# ---------------------------------------------------------------------------------------------
# Generated images
# ---------------------------------------------------------------------------------------------

def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def render_policy_strip():
    """Policy pages 13-17 stacked on a dark background. Returns the image path and the scroll
    position (y) that puts each named heading near the top of the screen."""
    doc = pymupdf.open(ROOT / "policy" / "KRI-Acceptable-Use-Policy.pdf")
    page_w, gap, top = 1100, 24, 30
    anchors = {"Figure 1": 13, "11. Monitoring Notice": 13, "11.3 What KRI will not do": 14, "12. Compliance": 14,
               "12.2 Breach levels": 14, "13. Exception Process": 15, "Figure 2": 17}
    pages, y, positions = [], top, {}
    for number in range(13, 18):
        page = doc[number - 1]
        scale = page_w / page.rect.width
        pix = page.get_pixmap(matrix=pymupdf.Matrix(scale, scale))
        pages.append((Image.frombytes("RGB", (pix.width, pix.height), pix.samples), y))
        for text, anchor_page in anchors.items():
            if anchor_page == number:
                # Figures are shown from the top of their page; headings sit 50 px below the top edge.
                hit_y = 0 if text.startswith("Figure") else page.search_for(text)[0].y0 * scale - 50
                positions[text] = int(y + hit_y)
        y += pix.height + gap
    strip = Image.new("RGB", (W, max(y + top, H)), BG)
    for img, page_y in pages:
        strip.paste(img, ((W - page_w) // 2, page_y))
    path = WORK / "policy-strip.png"
    strip.save(path)
    limit = strip.height - H
    return path, {k: max(0, min(v, limit)) for k, v in positions.items()}


def render_terminal():
    """A PowerShell window showing `python tools/policy_check.py` and its output, which is the
    content of evaluation/policy-check-results.md. Returns (full image, command-only image)."""
    output = (ROOT / "evaluation" / "policy-check-results.md").read_text(encoding="utf-8").rstrip().splitlines()
    mono, title_font = font("consola.ttf", 21), font("segoeui.ttf", 18)
    line_h, pad, bar_h, margin = 29, 26, 40, 40
    prompt = r"PS D:\redkross\task 1> "

    def draw(lines):
        win_h = max(bar_h + pad * 2 + line_h * len(lines), H - 2 * margin)
        img = Image.new("RGB", (W, win_h + 2 * margin), BG)
        d = ImageDraw.Draw(img)
        d.rectangle([margin, margin, W - margin, margin + win_h], fill="#0c0c0c", outline="#3a3a3a")
        d.rectangle([margin, margin, W - margin, margin + bar_h], fill="#1f1f1f")
        d.text((margin + 16, margin + 9), "Windows PowerShell", font=title_font, fill="#cccccc")
        for i, line in enumerate(lines):
            x, ly = margin + pad, margin + bar_h + pad + i * line_h
            if line.startswith(prompt):
                d.text((x, ly), prompt, font=mono, fill="#cccccc")
                d.text((x + d.textlength(prompt, font=mono), ly), line[len(prompt):], font=mono, fill="#f9f1a5")
            else:
                d.text((x, ly), line, font=mono, fill="#cccccc")
        return img

    command = prompt + "python tools/policy_check.py"
    full, start = WORK / "terminal.png", WORK / "terminal-command.png"
    draw([command, *output]).save(full)
    draw([command]).crop((0, 0, W, H)).save(start)
    return full, start


def render_title_card():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    lines = [("Acceptable Use Policy for a Small Research Organisation", font("segoeuib.ttf", 54), "#f0f6fc"),
             ("Kestrelwood Research Institute (fictional)  ·  KRI-ISP-001 v1.0", font("segoeui.ttf", 30), "#9da7b3"),
             ("Arpit Yadav  ·  Intern ID 2415  ·  RedKross Research Foundation", font("segoeui.ttf", 30), "#58a6ff")]
    y = H // 2 - 110
    for text, f, colour in lines:
        d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=colour)
        y += 95 if f.size > 40 else 60
    path = WORK / "title.png"
    img.save(path)
    return path


# ---------------------------------------------------------------------------------------------
# Video parts. Each takes the target duration in seconds and writes a silent 1920x1080 clip.
# ---------------------------------------------------------------------------------------------

def raw_part(start, end):
    def make(seconds, out):
        stretch = min(max(seconds / (end - start), MIN_STRETCH), MAX_STRETCH)
        run(["-ss", f"{start}", "-t", f"{end - start}", "-i", str(RAW), "-an", "-vf",
             f"setpts=(PTS-STARTPTS)*{stretch:.4f},tpad=stop_mode=clone:stop_duration={seconds},"
             f"trim=duration={seconds},{FINAL_PAD}", *ENCODE, str(out)])
    return make


def scroll_part(image, keyframes):
    """Scroll over a tall image. keyframes: [(fraction of duration, y), ...]; eased between them."""
    def make(seconds, out):
        points = [(f * seconds, y) for f, y in keyframes]
        expr = str(points[-1][1])
        for (t0, y0), (t1, y1) in reversed(list(zip(points, points[1:]))):
            u = f"((t-{t0:.3f})/{max(t1 - t0, 0.001):.3f})"
            expr = f"if(lt(t,{t1:.3f}),{y0}+({y1 - y0})*(3*{u}*{u}-2*{u}*{u}*{u}),{expr})"
        run(["-loop", "1", "-framerate", "30", "-t", f"{seconds}", "-i", str(image), "-vf",
             f"crop={W}:{H}:0:'{expr}',{FINAL_PAD}", *ENCODE, str(out)])
    return make


def still_part(image, y=0):
    return scroll_part(image, [(0, y)])


# ---------------------------------------------------------------------------------------------

def sections(strip, at, terminal, terminal_start):
    """(narration name, [(share of the narration time, part), ...]). Times in raw.mp4 are in seconds."""
    bottom = Image.open(terminal).height - H
    return [
        ("01-intro", [(1, raw_part(0, 20.3))]),                         # README header
        ("02-why", [(1, raw_part(20.3, 79.3))]),                        # README objective
        ("03-approach", [(1, raw_part(79.3, 149.8))]),                  # report: methodology, key risks
        ("04-policy", [(1, raw_part(149.8, 289.9))]),                   # policy: cover to Section 9
        ("05-reporting", [(0.55, raw_part(289.9, 324.5)),               # policy: Section 10
                          (0.45, still_part(strip, at["Figure 1"]))]),
        ("06-monitoring-to-exceptions", [(1, scroll_part(strip, [       # policy: Sections 11-13
            (0.00, at["11. Monitoring Notice"]), (0.08, at["11. Monitoring Notice"]),
            (0.22, at["11.3 What KRI will not do"]), (0.40, at["11.3 What KRI will not do"]),
            (0.45, at["12. Compliance"]), (0.52, at["12. Compliance"]),
            (0.57, at["12.2 Breach levels"]), (0.70, at["12.2 Breach levels"]),
            (0.74, at["13. Exception Process"]), (0.84, at["13. Exception Process"]),
            (0.89, at["Figure 2"]), (1.00, at["Figure 2"])]))]),
        ("07-supporting", [(1, raw_part(327.4, 341.9))]),               # README deliverables
        ("08-evaluation", [(0.12, still_part(terminal_start)),          # policy check run
                           (0.88, scroll_part(terminal, [(0, 0), (0.40, 0), (0.70, bottom), (1, bottom)]))]),
        ("09-limitations", [(1, raw_part(342.1, 375.1))]),              # report: limitations
    ]


def find_audio(folder, name):
    """Accepts `04-policy.m4a`, `04 policy.mp3`, `policy.m4a`, `04.wav` and similar."""
    number, label = name.split("-", 1)
    simple = lambda text: "".join(c for c in text.lower() if c.isalnum())
    for path in sorted(folder.iterdir()):
        stem = simple(path.stem)
        if path.suffix.lower() in AUDIO_EXT and stem in (simple(name), simple(label), number):
            return path
    sys.exit(f"Missing narration: {folder / name}.m4a (see video/video-script.md)")


def peak_db(path):
    log = subprocess.run([FFMPEG, "-hide_banner", "-nostats", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                         check=True, capture_output=True, text=True).stderr
    return float(log.split("max_volume:")[1].split("dB")[0])


def clean_audio(src, out):
    """Raise quiet recordings to a normal level, remove rumble and hiss, trim silence at both ends,
    even out loudness, and leave a short pause after."""
    gain = min(max(-3 - peak_db(src), 0), 50)
    trim = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.2"
    run(["-i", str(src), "-vn", "-af",
         f"highpass=f=80,volume={gain:.1f}dB,afftdn=nf=-35:tn=1,{trim},areverse,{trim},areverse,"
         "loudnorm=I=-16:TP=-1.5:LRA=11,apad=pad_dur=0.6", "-ar", "48000", "-ac", "2", str(out)])
    return duration(out)


def concat(paths, out, extra=()):
    listing = out.with_suffix(".txt")
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in paths), encoding="utf-8")
    run(["-f", "concat", "-safe", "0", "-i", str(listing), *extra, str(out)])


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-title", action="store_true", help="leave out the title card")
    parser.add_argument("--audio", type=Path, default=AUDIO_DIR, help="folder with the narration files")
    parser.add_argument("--out", type=Path, default=OUT, help="output video file")
    args = parser.parse_args()

    WORK.mkdir(parents=True, exist_ok=True)
    strip, at = render_policy_strip()
    terminal, terminal_start = render_terminal()

    finished = []
    if not args.no_title:
        clip = WORK / "s00.mp4"
        run(["-loop", "1", "-framerate", "30", "-t", "4", "-i", str(render_title_card()),
             "-f", "lavfi", "-t", "4", "-i", "anullsrc=r=48000:cl=stereo",
             "-vf", f"fade=in:d=0.6,fade=out:st=3.4:d=0.6,{FINAL_PAD}", *ENCODE,
             "-c:a", "aac", "-b:a", "160k", "-shortest", str(clip)])
        finished.append(clip)

    for name, parts in sections(strip, at, terminal, terminal_start):
        prefix = name[:2]
        src = find_audio(args.audio, name)
        audio = WORK / f"a{prefix}.wav"
        seconds = clean_audio(src, audio)
        print(f"{name:30} {src.name:32} {seconds:5.1f} s")
        clips = []
        for i, (share, make) in enumerate(parts):
            clip = WORK / f"v{prefix}-{i}.mp4"
            make(round(seconds * share, 3), clip)
            clips.append(clip)
        video = WORK / f"v{prefix}.mp4"
        concat(clips, video, ["-c", "copy"])
        section = WORK / f"s{prefix}.mp4"
        run(["-i", str(video), "-i", str(audio), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
             "-c:a", "aac", "-b:a", "160k", "-shortest", str(section)])
        finished.append(section)

    concat(finished, args.out, ["-c", "copy", "-movflags", "+faststart"])
    minutes = duration(args.out) / 60
    print(f"\nWrote {args.out}  ({minutes:.1f} min, {args.out.stat().st_size / 1e6:.0f} MB)")
    if minutes >= 10:
        print("WARNING: the video must be under 10 minutes. Re-record the longest sections more briefly.")


if __name__ == "__main__":
    main()
