"""Step 01: verify the downloaded original weights against the Hugging Face repo.

Checks every file exists with the right size, and (by default) verifies the SHA256 of
every large (LFS) file. Records the exact commit used, for reproducibility.

    python pipeline/01_verify_download.py [--no-hash]
"""
import argparse
import sys

from huggingface_hub import HfApi

from common import CFG, MODEL_DIR, RESULTS, gb, log, save_json, sha256

ap = argparse.ArgumentParser()
ap.add_argument("--no-hash", action="store_true", help="only check sizes (faster)")
args = ap.parse_args()

repo, rev = CFG["model"]["repo_id"], CFG["model"]["revision"]
info = HfApi().model_info(repo, revision=rev, files_metadata=True)
log(f"{repo} @ {info.sha}: {len(info.siblings)} files")

missing, wrong_size, wrong_hash, total = [], [], [], 0
for s in sorted(info.siblings, key=lambda s: s.rfilename):
    f = MODEL_DIR / s.rfilename
    if not f.is_file():
        missing.append(s.rfilename)
        continue
    size = f.stat().st_size
    total += size
    if s.size is not None and size != s.size:
        wrong_size.append(f"{s.rfilename} (local {size}, remote {s.size})")
        continue
    if s.lfs and not args.no_hash:
        digest = sha256(f)
        ok = digest == s.lfs.sha256
        log(f"  {'OK ' if ok else 'BAD'} {s.rfilename}")
        if not ok:
            wrong_hash.append(s.rfilename)

save_json(RESULTS / "source_manifest.json", {
    "repo_id": repo,
    "commit": info.sha,
    "files": len(info.siblings),
    "total_gb": gb(total),
    "sha256_verified": not args.no_hash,
})

if missing or wrong_size or wrong_hash:
    for label, items in (("Missing", missing), ("Wrong size", wrong_size), ("Hash mismatch", wrong_hash)):
        for i in items:
            print(f"{label}: {i}")
    sys.exit("Download is incomplete or corrupted. Re-run: hf download "
             f"{repo} --local-dir {CFG['model']['local_dir']}")

log(f"All {len(info.siblings)} files verified ({gb(total)} GB). Commit {info.sha}")
