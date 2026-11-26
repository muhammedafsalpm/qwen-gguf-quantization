"""Step 05: quantize BF16 into every type in config.yaml, then write SHA256 checksums.

    python pipeline/05_quantize.py [--force] [--only Q4_K_M ...]
"""
import argparse

from common import (BF16, CFG, IMATRIX, MMPROJ, OUT, RESULTS, gb, gguf, load_json, log,
                    require, run, save_json, sha256, tool)

ap = argparse.ArgumentParser()
ap.add_argument("--force", action="store_true")
ap.add_argument("--only", nargs="*", help="quant types to (re)build")
args = ap.parse_args()

qc = CFG["quantize"]
types = args.only or qc["types"]
require(BF16, "Run step 02 first.")

for t in types:
    target = gguf(t)
    if target.exists() and not args.force:
        log(f"skip: {target.name} exists ({gb(target.stat().st_size)} GB)")
        continue
    cmd = [tool("llama-quantize")]
    if t not in qc["no_imatrix"]:
        require(IMATRIX, "Run step 04 first.")
        cmd += ["--imatrix", IMATRIX]
    tmp = target.with_suffix(".partial.gguf")
    run(cmd + [BF16, tmp, t], f"05_quantize_{t}")
    tmp.replace(target)
    log(f"wrote {target.name} ({gb(target.stat().st_size)} GB)")

# Checksums for everything that will be published (cached by size + mtime)
cache = load_json(RESULTS / "checksums.json", {})
files = [gguf(t) for t in qc["types"]] + ([MMPROJ] if MMPROJ else []) + [IMATRIX]
result = {}
for f in files:
    if not f.exists():
        continue
    st = f.stat()
    c = cache.get(f.name)
    if not c or c["size"] != st.st_size or c["mtime"] != int(st.st_mtime):
        log(f"sha256 {f.name}")
        c = {"size": st.st_size, "mtime": int(st.st_mtime), "sha256": sha256(f)}
    result[f.name] = c
save_json(RESULTS / "checksums.json", result)
(OUT / "SHA256SUMS.txt").write_text(  # LF endings, so `sha256sum -c` works on Linux too
    "".join(f"{v['sha256']}  {k}\n" for k, v in result.items()), encoding="utf-8", newline="\n")
log(f"checksums written for {len(result)} files")
