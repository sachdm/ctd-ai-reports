#!/usr/bin/env python3
"""
CTD shot iterator — batch-generate show shots on Krea (Nano Banana Pro).

Usage:
  export KREA_API_KEY=your_key_here          # from krea.ai -> API Tokens
  pip install requests pyyaml

  python generate.py                          # all shots, default variations
  python generate.py CTD_AI_WheelsDerail      # one shot
  python generate.py CTD_AI_WheelsDerail -n 8 # 8 variations of one shot
  python generate.py --ref livery.png         # attach a reference image
                                              # (e.g. your locked livery frame)
  python generate.py --list                   # print composed prompts, no API calls

Outputs land in renders/<SHOT_CODE>/  and a contact_sheet.html is rebuilt
after every run — open it in a browser to review everything at once.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import os
import re
import sys
import time
from pathlib import Path

try:
    import requests
    import yaml
except ImportError:
    sys.exit("Missing deps. Run:  pip install requests pyyaml")

API = "https://api.krea.ai"
MODEL_ENDPOINT = "/generate/image/google/nano-banana-pro"
HERE = Path(__file__).parent
RENDERS = HERE / "renders"

POLL_INTERVAL = 4          # seconds between job status checks
POLL_TIMEOUT = 600         # give up on a job after 10 min
TERMINAL = {"completed", "failed", "cancelled"}


def auth_headers():
    key = os.environ.get("KREA_API_KEY")
    if not key:
        key_file = HERE / ".krea_key"
        if key_file.exists():
            key = key_file.read_text().strip()
    if not key:
        sys.exit("Set KREA_API_KEY or put the key in krea-pipeline/.krea_key")
    return {"Authorization": f"Bearer {key}"}


def load_config():
    with open(HERE / "shots.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def compose_prompt(brief: str, blocks: dict) -> str:
    """Inject locked {BLOCK} placeholders into a shot brief."""
    def sub(match):
        name = match.group(1)
        if name not in blocks:
            sys.exit(f"Unknown block {{{name}}} in shots.yaml")
        return blocks[name].strip()
    text = re.sub(r"\{([A-Z_]+)\}", sub, brief)
    return re.sub(r"\s+", " ", text).strip()


def image_to_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    data = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{data}"


def submit(prompt: str, aspect: str, resolution: str, ref_uri: str | None):
    body = {"prompt": prompt, "aspect_ratio": aspect, "resolution": resolution}
    if ref_uri:
        body["image_urls"] = [ref_uri]
    r = requests.post(API + MODEL_ENDPOINT, json=body, headers=auth_headers(), timeout=60)
    if r.status_code == 402:
        sys.exit("Krea says: out of API credits. Top up in API settings.")
    if r.status_code == 429:
        return None  # too many concurrent jobs — caller retries
    r.raise_for_status()
    return r.json()["job_id"]


def poll(job_id: str) -> dict:
    deadline = time.time() + POLL_TIMEOUT
    while time.time() < deadline:
        r = requests.get(f"{API}/jobs/{job_id}", headers=auth_headers(), timeout=60)
        r.raise_for_status()
        job = r.json()
        if job.get("status") in TERMINAL:
            return job
        time.sleep(POLL_INTERVAL)
    return {"status": "timeout", "job_id": job_id}


def extract_urls(obj) -> list[str]:
    """Find every image URL in the job result, whatever shape it has."""
    urls = []
    def walk(x):
        if isinstance(x, str) and x.startswith("http"):
            urls.append(x)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(obj.get("result"))
    return urls


def download(url: str, dest: Path):
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    dest.write_bytes(r.content)


def contact_sheet():
    rows = []
    for shot_dir in sorted(RENDERS.iterdir()):
        if not shot_dir.is_dir():
            continue
        imgs = sorted(p for p in shot_dir.iterdir()
                      if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"))
        if not imgs:
            continue
        cells = "".join(
            f'<a href="{shot_dir.name}/{p.name}" target="_blank">'
            f'<img src="{shot_dir.name}/{p.name}" loading="lazy"></a>'
            for p in imgs
        )
        prompt_file = shot_dir / "prompt.txt"
        prompt = html.escape(prompt_file.read_text()) if prompt_file.exists() else ""
        rows.append(
            f"<section><h2>{shot_dir.name}</h2>"
            f"<details><summary>prompt</summary><pre>{prompt}</pre></details>"
            f'<div class="grid">{cells}</div></section>'
        )
    page = f"""<!doctype html><meta charset="utf-8"><title>CTD contact sheet</title>
<style>
 body{{background:#111;color:#ddd;font:14px/1.4 system-ui;margin:2rem}}
 h2{{border-bottom:1px solid #333;padding-bottom:.3rem}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:10px}}
 img{{width:100%;border-radius:6px;display:block}}
 pre{{white-space:pre-wrap;background:#1a1a1a;padding:1rem;border-radius:6px}}
 summary{{cursor:pointer;color:#8ab}}
</style>
{''.join(rows)}"""
    (RENDERS / "contact_sheet.html").write_text(page, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("shots", nargs="*", help="shot codes to run (default: all)")
    ap.add_argument("-n", "--variations", type=int, help="variations per shot")
    ap.add_argument("--ref", type=Path, help="reference image (e.g. locked livery frame)")
    ap.add_argument("--resolution", choices=["1K", "2K", "4K"])
    ap.add_argument("--list", action="store_true", help="print composed prompts and exit")
    args = ap.parse_args()

    cfg = load_config()
    blocks = cfg["blocks"]
    defaults = cfg.get("defaults", {})
    wanted = {s.upper() for s in args.shots}
    shots = [s for s in cfg["shots"]
             if not wanted or s["code"].upper() in wanted]
    if not shots:
        sys.exit(f"No shots matched {args.shots}. Codes: "
                 + ", ".join(s["code"] for s in cfg["shots"]))

    ref_uri = image_to_data_uri(args.ref) if args.ref else None
    n = args.variations or defaults.get("variations", 4)
    aspect = defaults.get("aspect_ratio", "16:9")
    resolution = args.resolution or defaults.get("resolution", "2K")

    for shot in shots:
        prompt = compose_prompt(shot["brief"], blocks)
        if args.list:
            print(f"\n=== {shot['code']} ===\n{prompt}")
            continue

        out = RENDERS / shot["code"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "prompt.txt").write_text(prompt, encoding="utf-8")
        existing = len(list(out.glob("*.png"))) + len(list(out.glob("*.jpg")))

        print(f"\n=== {shot['code']}  ({n} variations, {resolution}) ===")
        job_ids = []
        for i in range(n):
            jid = None
            while jid is None:
                jid = submit(prompt, aspect, resolution, ref_uri)
                if jid is None:
                    print("  concurrency cap hit, waiting 10s...")
                    time.sleep(10)
            job_ids.append(jid)
            print(f"  submitted {i + 1}/{n}  job {jid[:8]}")

        for i, jid in enumerate(job_ids):
            job = poll(jid)
            if job.get("status") != "completed":
                print(f"  job {jid[:8]} -> {job.get('status')}"
                      f"  {json.dumps(job.get('error') or {})}")
                continue
            for k, url in enumerate(extract_urls(job)):
                idx = existing + i + 1
                suffix = f"_{k}" if k else ""
                dest = out / f"{shot['code']}_v{idx:03d}{suffix}.png"
                download(url, dest)
                print(f"  saved {dest.name}")

    if not args.list:
        contact_sheet()
        print(f"\nContact sheet: {RENDERS / 'contact_sheet.html'}")


if __name__ == "__main__":
    main()
