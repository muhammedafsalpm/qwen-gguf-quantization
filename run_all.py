"""Run the pipeline steps 01-07 in order. Upload (08) is always a separate, manual step.

Every step skips work that is already done, so re-running continues where it stopped.

    python run_all.py               # steps 01-07 for config.yaml (Qwen3.8-27B)
    python run_all.py --from 4      # start at step 04
    python run_all.py --only 6      # just step 06
    python run_all.py --config configs/qwen3-8b.yaml   # another model
"""
import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STEPS = sorted(p for p in (ROOT / "pipeline").glob("0*.py") if not p.name.startswith("08"))

ap = argparse.ArgumentParser()
ap.add_argument("--from", dest="start", type=int, default=1)
ap.add_argument("--only", type=int)
ap.add_argument("--config", default="config.yaml", help="model config (default: config.yaml)")
args = ap.parse_args()
cfg = Path(args.config) if Path(args.config).is_absolute() else ROOT / args.config
if not cfg.exists():
    sys.exit(f"Config file not found: {cfg}")
os.environ["QUANT_CONFIG"] = str(cfg)  # every step reads the same model config
extra = [] if args.config == "config.yaml" else [f" --config {args.config}"]

t0 = time.time()
for step in STEPS:
    n = int(step.name[:2])
    if (args.only and n != args.only) or n < args.start:
        continue
    print(f"\n{'=' * 70}\n  STEP {step.stem}\n{'=' * 70}", flush=True)
    if subprocess.call([sys.executable, str(step)], cwd=step.parent) != 0:
        sys.exit(f"\nStopped at {step.name}. Fix the problem, then: python run_all.py --from {n}{''.join(extra)}")
release = __import__("yaml").safe_load(cfg.read_text(encoding="utf-8"))["paths"]["release"]
print(f"\nAll done in {(time.time() - t0) / 3600:.1f} h. Review {release}/README.md, then:")
print(f"  python pipeline/08_upload.py{''.join(extra)}        (dry run)")
print(f"  python pipeline/08_upload.py{''.join(extra)} --yes  (upload)")
