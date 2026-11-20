"""Step 08: upload release/ to Hugging Face. Never runs automatically.

Without --yes it only prints what would be uploaded.

    python pipeline/08_upload.py              # dry run: show the plan
    python pipeline/08_upload.py --yes        # upload (resumable)
    python pipeline/08_upload.py --collection # also add the repo to your collection
"""
import argparse
import sys

from huggingface_hub import HfApi

from common import CFG, OUT, RELEASE, gb, log, require, single_instance

ap = argparse.ArgumentParser()
ap.add_argument("--yes", action="store_true", help="actually upload")
ap.add_argument("--collection", action="store_true", help="add the repo to the configured collection")
args = ap.parse_args()

hf = CFG["hf"]
require(RELEASE / "README.md", "Run step 07 first.")
api = HfApi()

who = api.whoami()["name"]  # uses the token saved by `hf auth login`
if who != hf["username"]:
    sys.exit(f"Logged in as '{who}', but config.yaml expects '{hf['username']}'. Run: hf auth login")

files = sorted(f for f in RELEASE.iterdir() if f.is_file())
total = sum(f.stat().st_size for f in files)
print(f"\nRepository : https://huggingface.co/{hf['repo_id']}  ({'private' if hf['private'] else 'PUBLIC'})")
print(f"Account    : {who}")
for f in files:
    print(f"  {gb(f.stat().st_size):>7.2f} GB  {f.name}")
print(f"  {gb(total):>7.2f} GB  total\n")

if args.yes:
    # Two uploads at once compete for bandwidth and share one progress cache. The lock lives
    # in out/, not release/, so it is never uploaded; it is released when this process ends.
    lock = single_instance(OUT / ".upload.lock", "upload")
    api.create_repo(hf["repo_id"], repo_type="model", private=hf["private"], exist_ok=True)
    log("uploading (resumable; re-run the same command if it stops)")
    api.upload_large_folder(repo_id=hf["repo_id"], folder_path=RELEASE, repo_type="model")
    log(f"done: https://huggingface.co/{hf['repo_id']}")
elif not args.collection:
    print("Dry run only. Re-run with --yes to upload.")

if args.collection:
    col = api.create_collection(title=hf["collection_title"], namespace=who,
                                description="Quantized GGUF models with measured quality", exists_ok=True)
    api.add_collection_item(col.slug, item_id=hf["repo_id"], item_type="model", exists_ok=True)
    log(f"collection: https://huggingface.co/collections/{col.slug}")
