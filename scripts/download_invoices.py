"""Download invoices: the Câmara expense quota (CEAP) annual JSON and a sample of receipt PDFs.

uv run scripts/download_invoices.py --year 2026 --limit 50
"""

import argparse
import io
import json
import random
import time
import urllib.request
import zipfile
from pathlib import Path

ZIP_URL = "https://www.camara.leg.br/cotas/Ano-{year}.json.zip"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "closer-look/0.1"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--year", type=int, default=2026)
    p.add_argument("--limit", type=int, default=50, help="number of PDFs to sample")
    p.add_argument("--seed", type=int, default=42, help="sample seed, for reproducibility")
    p.add_argument("--out", type=Path, default=Path("data/invoices"))
    args = p.parse_args()

    out = args.out / str(args.year)
    pdf_dir = out / "pdf"
    pdf_dir.mkdir(parents=True, exist_ok=True)

    json_path = out / f"Ano-{args.year}.json"
    if not json_path.exists():
        print(f"downloading {ZIP_URL.format(year=args.year)}")
        with zipfile.ZipFile(io.BytesIO(fetch(ZIP_URL.format(year=args.year)))) as z:
            z.extract(f"Ano-{args.year}.json", out)

    rows = json.loads(json_path.read_text(encoding="utf-8"))["dados"]
    with_pdf = [r for r in rows if r["urlDocumento"].endswith(".pdf")]
    sample = random.Random(args.seed).sample(with_pdf, min(args.limit, len(with_pdf)))
    print(f"{len(rows)} expenses, {len(with_pdf)} with PDF, sampling {len(sample)}")

    for i, r in enumerate(sample, 1):
        path = pdf_dir / f"{r['idDocumento']}.pdf"
        if path.exists():
            continue
        try:
            path.write_bytes(fetch(r["urlDocumento"]))
            print(f"[{i}/{len(sample)}] {path.name}")
        except OSError as e:
            print(f"[{i}/{len(sample)}] {path.name} failed: {e}")
        time.sleep(0.5)  # be polite to the server


if __name__ == "__main__":
    main()
