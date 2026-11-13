"""Run the pipeline steps 01-07 in order. Upload (08) is always a separate, manual step.

Every step skips work that is already done, so re-running continues where it stopped.

    python run_all.py               # steps 01-07
    python run_all.py --from 4      # start at step 04
    python run_all.py --only 6      # just step 06
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

STEPS = sorted(p for p in (Path(__file__).parent / "pipeline").glob("0*.py") if not p.name.startswith("08"))

ap = argparse.ArgumentParser()
ap.add_argument("--from", dest="start", type=int, default=1)
ap.add_argument("--only", type=int)
args = ap.parse_args()

t0 = time.time()
for step in STEPS:
    n = int(step.name[:2])
    if (args.only and n != args.only) or n < args.start:
        continue
    print(f"\n{'=' * 70}\n  STEP {step.stem}\n{'=' * 70}", flush=True)
    if subprocess.call([sys.executable, str(step)], cwd=step.parent) != 0:
        sys.exit(f"\nStopped at {step.name}. Fix the problem, then: python run_all.py --from {n}")
print(f"\nAll done in {(time.time() - t0) / 3600:.1f} h. Review release/README.md, then:")
print("  python pipeline/08_upload.py        (dry run)")
print("  python pipeline/08_upload.py --yes  (upload)")
