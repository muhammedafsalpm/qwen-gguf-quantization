"""Step 02: convert the original safetensors to GGUF.

Produces:
  out/<name>-BF16.gguf          full-precision text model (source for every quant)
  out/mmproj-<name>-F16.gguf    vision projector (needed for image input)

    python pipeline/02_convert.py [--force]
"""
import argparse
import sys

from common import BF16, CFG, LLAMA_SRC, MMPROJ, MODEL_DIR, OUT, gb, log, require, run

ap = argparse.ArgumentParser()
ap.add_argument("--force", action="store_true", help="re-create files that already exist")
args = ap.parse_args()

require(MODEL_DIR / "config.json", "Run step 01 first.")
convert = LLAMA_SRC / "convert_hf_to_gguf.py"


def convert_to(target, outtype, extra, log_name):
    if target.exists() and not args.force:
        log(f"skip: {target.name} exists ({gb(target.stat().st_size)} GB)")
        return
    tmp = target.with_suffix(".partial.gguf")
    before = set(OUT.glob("*.gguf"))
    try:
        run([sys.executable, convert, MODEL_DIR, "--outtype", outtype, "--outfile", tmp, *extra], log_name)
        if not tmp.exists():  # some converter versions add a prefix to the name
            new = sorted(set(OUT.glob("*.gguf")) - before)
            if len(new) != 1:
                sys.exit(f"Could not find the converter output for {target.name}: {new}")
            tmp = new[0]
        tmp.replace(target)
    except BaseException:
        for f in set(OUT.glob("*.gguf")) - before:
            f.unlink(missing_ok=True)  # never leave a half-written file behind
        raise
    log(f"wrote {target.name} ({gb(target.stat().st_size)} GB)")


convert_to(BF16, CFG["convert"]["outtype"], [], "02_convert_text")
convert_to(MMPROJ, CFG["convert"]["mmproj_outtype"], ["--mmproj"], "02_convert_mmproj")
