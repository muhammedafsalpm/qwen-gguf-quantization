"""Step 04: make the Q8_0 reference quant, then compute the importance matrix.

The imatrix is computed on Q8_0 by default (practically identical to BF16, and it fits in
48 GB VRAM where BF16 of a 27B model does not), or on BF16 itself when `imatrix.source: bf16`
is set for a model small enough to fit. It uses the chat-formatted calibration text from step 03.

    python pipeline/04_imatrix.py [--force]
"""
import argparse

from common import BF16, CALIB, CFG, IMATRIX, gb, gguf, log, require, run, tool

ap = argparse.ArgumentParser()
ap.add_argument("--force", action="store_true")
args = ap.parse_args()

require(BF16, "Run step 02 first.")
require(CALIB, "Run step 03 first.")

ref_type = CFG["quantize"]["reference"]
ref = gguf(ref_type)
if ref.exists() and not args.force:
    log(f"skip: {ref.name} exists")
else:
    tmp = ref.with_suffix(".partial.gguf")
    run([tool("llama-quantize"), BF16, tmp, ref_type], f"04_quantize_{ref_type}")
    tmp.replace(ref)
    log(f"wrote {ref.name} ({gb(ref.stat().st_size)} GB)")

if IMATRIX.exists() and not args.force:
    log(f"skip: {IMATRIX.name} exists")
else:
    ic = CFG["imatrix"]
    source = BF16 if ic.get("source", "reference") == "bf16" else ref
    log(f"importance matrix computed on {source.name}")
    tmp = IMATRIX.with_suffix(".partial.gguf")
    run([tool("llama-imatrix"), "-m", source, "-f", CALIB, "-o", tmp,
         "-c", ic["ctx"], "-ngl", ic["ngl"], "--chunks", ic["chunks"],
         "--parse-special"],  # chat-template tokens in the calibration text are real special tokens
        "04_imatrix")
    tmp.replace(IMATRIX)
    log(f"wrote {IMATRIX.name}")
