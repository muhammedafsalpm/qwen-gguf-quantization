"""Write the Kaggle notebook (docs/launch/kaggle/qwen3-gguf-kaggle-t4.ipynb) from the cells below.

    python docs/launch/build_notebook.py
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "kaggle" / "qwen3-gguf-kaggle-t4.ipynb"
cells = []


def md(text):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": text.strip("\n").splitlines(keepends=True)})


def code(text):
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                  "source": text.strip("\n").splitlines(keepends=True)})


md("""
# Qwen3 27B / 14B / 8B GGUF on a Kaggle T4: measured quality and speed

I quantized three Qwen models to GGUF with an importance matrix and measured every file against the
original BF16 weights. This notebook loads one of them on Kaggle's free T4 GPU, runs a few real prompts
(thinking on and off, tool calling, Malayalam and Hindi) and plots the measurements for all three models.

| Model | GPU memory used | Suggested file | Size | Speed on Kaggle T4 x2 |
|---|---|---|---|---|
| Qwen3-8B | fits on one of the two T4s | Q8_0 (near-lossless) or Q4_K_M | 8.7 GB / 5.0 GB | not measured |
| Qwen3-14B | fits on one of the two T4s | Q4_K_M | 9.0 GB | about 25 tokens/s |
| Qwen3.8-27B (text + images) | split across both T4s | Q4_K_M or IQ3_M | 17.0 / 13.0 GB + 0.9 GB vision file | about 13 tokens/s (Q4_K_M) |

**Before you run:** Settings → Accelerator → **GPU T4 x2** and Settings → Internet → **On**. Building llama.cpp takes about 25 minutes the first time in a session (Kaggle has 4 CPU cores);
after that, switching models takes a few minutes.

Everything runs inside this notebook. The model server listens on `127.0.0.1` only, nothing is exposed.

**Links:** [Hugging Face collection](https://huggingface.co/collections/muhammed-afsal-p-m/qwen3-quants) ·
[pipeline code on GitHub](https://github.com/muhammedafsalpm/qwen-gguf-quantization)
""")

md("## 1. Pick a model")
code('''
MODEL = "14B"     # "8B", "14B" or "27B"
QUANT = "Q4_K_M"  # any file in the repo: Q8_0, Q6_K, Q5_K_M, Q4_K_M, IQ4_XS, Q3_K_M, IQ3_M

REPOS = {
    "8B":  ("muhammed-afsal-p-m/Qwen3-8B-GGUF", "Qwen3-8B"),
    "14B": ("muhammed-afsal-p-m/Qwen3-14B-GGUF", "Qwen3-14B"),
    "27B": ("muhammed-afsal-p-m/Qwen3.8-27B-GGUF", "Qwen3.8-27B"),
}
REPO, NAME = REPOS[MODEL]
GGUF_FILE = f"{NAME}-{QUANT}.gguf"
print(REPO, GGUF_FILE)
''')
code("!nvidia-smi --query-gpu=name,memory.total --format=csv")

md("""
## 2. Build llama.cpp (CUDA, T4)

Same llama.cpp build the files were made and tested with (`b12345`). Only the server is built, for the
T4's compute capability (7.5), to keep the build short.
""")
code('''
%%bash
set -e
export PATH=/usr/local/cuda/bin:$PATH
# CMake needs the CUDA driver library: CUDA's stub if present, otherwise the GPU machine's own driver
DRV=$(find /usr/local/cuda*/ -name libcuda.so -path '*stubs*' 2>/dev/null | head -1)
[ -n "$DRV" ] || DRV=$(ldconfig -p | awk '/libcuda[.]so/ {print $NF; exit}')
for d in ${LD_LIBRARY_PATH//:/ } /usr/local/nvidia/lib64 /usr/lib64-nvidia /usr/lib/x86_64-linux-gnu; do
  [ -n "$DRV" ] || { [ -e "$d/libcuda.so.1" ] && DRV="$d/libcuda.so.1"; }
done
[ -n "$DRV" ] || DRV=$(find / \( -path /proc -o -path /sys -o -path /kaggle \) -prune -o \( -name libcuda.so -o -name 'libcuda.so.1' \) -print 2>/dev/null | head -1)
echo "CUDA driver library: $DRV"
if [ ! -x /kaggle/working/llama.cpp/build/bin/llama-server ]; then
  cd /kaggle/working
  [ -d llama.cpp ] || git clone --depth 1 --branch b12345 https://github.com/ggml-org/llama.cpp > /dev/null 2>&1
  cd llama.cpp && rm -rf build
  cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_ARCHITECTURES=75 -DLLAMA_CURL=OFF -DLLAMA_USE_PREBUILT_UI=OFF -DCUDA_cuda_driver_LIBRARY="$DRV" > cmake.log 2>&1 || (tail -40 cmake.log; exit 1)
  cmake --build build --target llama-server -j "$(nproc)" > build.log 2>&1 || (tail -40 build.log; exit 1)
fi
/kaggle/working/llama.cpp/build/bin/llama-server --version 2>&1 | tail -3
''')

md("## 3. Download the GGUF from Hugging Face")
code('''
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(REPO, GGUF_FILE, local_dir="/kaggle/tmp/models")
mmproj_path = None
if MODEL == "27B":  # vision projector for image input
    mmproj_path = hf_hub_download(REPO, "mmproj-Qwen3.8-27B-F16.gguf", local_dir="/kaggle/tmp/models")
print(model_path, mmproj_path or "")
''')

md("## 4. Start the server (local only)")
code('''
import subprocess, time, requests

cmd = ["/kaggle/working/llama.cpp/build/bin/llama-server", "-m", model_path,
       "-ngl", "99", "-c", "8192", "--jinja", "--host", "127.0.0.1", "--port", "8080"]
if mmproj_path:
    cmd += ["--mmproj", mmproj_path]
server = subprocess.Popen(cmd, stdout=open("/kaggle/working/server.log", "w"), stderr=subprocess.STDOUT)

for _ in range(300):
    try:
        if requests.get("http://127.0.0.1:8080/health", timeout=2).status_code == 200:
            break
    except requests.ConnectionError:
        pass
    if server.poll() is not None:
        raise RuntimeError(open("/kaggle/working/server.log").read()[-3000:])
    time.sleep(2)
print("server ready")
''')
code('''
def chat(prompt, thinking=True, tools=None, image_url=None, max_tokens=2048):
    content = prompt if not image_url else [
        {"type": "image_url", "image_url": {"url": image_url}}, {"type": "text", "text": prompt}]
    body = {"messages": [{"role": "user", "content": content}], "temperature": 0, "seed": 42,
            "max_tokens": max_tokens, "chat_template_kwargs": {"enable_thinking": thinking}}
    if tools:
        body["tools"] = tools
    t0 = time.time()
    r = requests.post("http://127.0.0.1:8080/v1/chat/completions", json=body, timeout=900).json()
    msg, timings = r["choices"][0]["message"], r.get("timings", {})
    return {"answer": msg.get("content") or "", "thinking_chars": len(msg.get("reasoning_content") or ""),
            "tool_calls": [c["function"] for c in msg.get("tool_calls") or []],
            "seconds": round(time.time() - t0, 1), "tok_s": round(timings.get("predicted_per_second", 0), 1)}


def show(title, r):
    print(f"--- {title}  ({r['seconds']} s, {r['tok_s']} tok/s, thinking: {r['thinking_chars']} chars)")
    print(r["answer"].strip() or r["tool_calls"])
''')

md("## 5. Try it")
code('''
show("thinking on", chat("A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. "
                         "How much does the ball cost?"))
show("thinking off", chat("What is 17 times 23? Answer with just the number.", thinking=False))
''')
code('''
weather_tool = [{"type": "function", "function": {
    "name": "get_weather", "description": "Get the current weather for a city",
    "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}]
show("tool call", chat("What's the weather in Paris right now?", thinking=False, tools=weather_tool))
''')
code('''
show("Malayalam", chat("ഇന്ത്യയുടെ തലസ്ഥാനം ഏതാണ്? ഒരു വാക്യത്തിൽ ഉത്തരം നൽകുക.", thinking=False))
show("Hindi", chat("भारत की राजधानी क्या है? एक वाक्य में उत्तर दीजिए।", thinking=False))
''')
code('''
if MODEL == "27B":  # image input: the same invoice used in my tests
    url = "https://raw.githubusercontent.com/muhammedafsalpm/qwen-gguf-quantization/main/tools/test_images/invoice.png"
    show("image", chat("What is the invoice total and the tax amount?", thinking=False, image_url=url))
else:
    print("Image input needs the 27B model (set MODEL = '27B').")
''')

md("""
## 6. What I measured for all three models

The numbers below are loaded from the results files in the GitHub repository. Each quant was compared
with its own BF16 model on the wikitext-2 test split (150 chunks × 512 tokens): KL divergence shows how
far the quant's next-token probabilities drift from the original (lower is better), and "same top token"
is how often it picks the same next token.
""")
code('''
import pandas as pd
import matplotlib.pyplot as plt

BASE = "https://raw.githubusercontent.com/muhammedafsalpm/qwen-gguf-quantization/main/results"
SOURCES = {"Qwen3.8-27B": f"{BASE}/eval.json", "Qwen3-14B": f"{BASE}/Qwen3-14B/eval.json",
           "Qwen3-8B": f"{BASE}/Qwen3-8B/eval.json"}
rows = []
for name, url in SOURCES.items():
    ev = requests.get(url, timeout=30).json()
    for quant, q in ev["quants"].items():
        f = q.get("file") or q.get("functional", {}).get("file", {})
        rows.append({"model": name, "quant": quant, "size_gb": round(f.get("size", 0) / 1e9, 1),
                     "mean_kld": q["kld_mean"], "same_top_%": q["same_top"],
                     "tok_s (RTX 6000 Ada)": q.get("functional", {}).get("tokens_per_sec")})
df = pd.DataFrame(rows)
df.pivot(index="quant", columns="model", values="mean_kld").loc[
    ["Q8_0", "Q6_K", "Q5_K_M", "Q4_K_M", "IQ4_XS", "Q3_K_M", "IQ3_M"], list(SOURCES)].round(4)
''')
code('''
fig, ax = plt.subplots(figsize=(8, 5))
for name, g in df.groupby("model", sort=False):
    ax.plot(g["size_gb"], g["mean_kld"], "o-", label=name)
ax.set_yscale("log")
ax.set_xlabel("File size (GB)")
ax.set_ylabel("Mean KL divergence vs BF16 (lower is better)")
ax.set_title("Accuracy loss vs file size")
ax.grid(alpha=0.3)
ax.legend()
plt.show()
''')

md("""
**What I take from this**

- Larger models lose less. At Q4_K_M the 27B model drifts least (mean KLD 0.0121), then 14B (0.0188),
  then 8B (0.0262).
- Q8_0 is practically identical to the original for all three (98–99% same top token).
- For most people Q4_K_M is the right trade-off. For 8B, Q5_K_M or higher is worth it if quality matters.
- Below 4 bits (Q3_K_M, IQ3_M) the loss grows quickly, but the larger models still answered all my graded
  test questions correctly.

Full method, question tests and Malayalam/Hindi accuracy are on each model card.
""")
code('''
server.terminate()
print(open("/kaggle/working/server.log").read()[-600:])
''')

md("""
## Links

- Models: [Qwen3.8-27B-GGUF](https://huggingface.co/muhammed-afsal-p-m/Qwen3.8-27B-GGUF) ·
  [Qwen3-14B-GGUF](https://huggingface.co/muhammed-afsal-p-m/Qwen3-14B-GGUF) ·
  [Qwen3-8B-GGUF](https://huggingface.co/muhammed-afsal-p-m/Qwen3-8B-GGUF)
- Collection: [Qwen3 Quants](https://huggingface.co/collections/muhammed-afsal-p-m/qwen3-quants)
- Code and full results: [github.com/muhammedafsalpm/qwen-gguf-quantization](https://github.com/muhammedafsalpm/qwen-gguf-quantization)

If something doesn't work on your setup, leave a comment and I'll take a look.
""")

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                   "language_info": {"name": "python"}},
      "nbformat": 4, "nbformat_minor": 5}
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{len(cells)} cells -> {OUT}")


# ---------- second notebook: copy selected GGUF files from Hugging Face to Kaggle Models ----------
OUT2 = OUT.parent / "publish-kaggle-models.ipynb"
cells = []
md("""
# Publish the Qwen3 GGUF files as Kaggle Models

Copies selected files from my Hugging Face repos into Kaggle Models with `kagglehub`. Kaggle's network does
the transfer, so nothing is uploaded from a home connection.

**One-time setup:** Add-ons → Secrets → add `KAGGLE_USERNAME` and `KAGGLE_KEY` (from kaggle.com → Settings →
API → Create New Token). Internet must be on. Run one model at a time (the disk is limited).

After the upload, open each model page on Kaggle and paste the description from the drafts.
""")
code('''
!pip install -q -U kagglehub huggingface_hub
import os, shutil
from kaggle_secrets import UserSecretsClient
secrets = UserSecretsClient()
os.environ["KAGGLE_USERNAME"] = secrets.get_secret("KAGGLE_USERNAME")
os.environ["KAGGLE_KEY"] = secrets.get_secret("KAGGLE_KEY")
import kagglehub
from huggingface_hub import hf_hub_download
''')
code('''
OWNER = os.environ["KAGGLE_USERNAME"]
PLAN = {  # Kaggle model slug: (HF repo, files per variation)
    "qwen3-8b-gguf": ("muhammed-afsal-p-m/Qwen3-8B-GGUF",
                      {"q8_0": ["Qwen3-8B-Q8_0.gguf"], "q4_k_m": ["Qwen3-8B-Q4_K_M.gguf"],
                       "iq4_xs": ["Qwen3-8B-IQ4_XS.gguf"]}),
    "qwen3-14b-gguf": ("muhammed-afsal-p-m/Qwen3-14B-GGUF",
                       {"q8_0": ["Qwen3-14B-Q8_0.gguf"], "q4_k_m": ["Qwen3-14B-Q4_K_M.gguf"],
                        "iq3_m": ["Qwen3-14B-IQ3_M.gguf"]}),
    "qwen3.8-27b-gguf": ("muhammed-afsal-p-m/Qwen3.8-27B-GGUF",
                         {"q4_k_m": ["Qwen3.8-27B-Q4_K_M.gguf", "mmproj-Qwen3.8-27B-F16.gguf"],
                          "iq3_m": ["Qwen3.8-27B-IQ3_M.gguf", "mmproj-Qwen3.8-27B-F16.gguf"]}),
}
MODEL_SLUG = "qwen3-8b-gguf"   # run once per model: qwen3-8b-gguf, qwen3-14b-gguf, qwen3.8-27b-gguf
''')
code('''
repo, variations = PLAN[MODEL_SLUG]
for variation, files in variations.items():
    folder = f"/kaggle/tmp/{MODEL_SLUG}/{variation}"
    os.makedirs(folder, exist_ok=True)
    for f in files + ["SHA256SUMS.txt"]:
        hf_hub_download(repo, f, local_dir=folder)
    kagglehub.model_upload(f"{OWNER}/{MODEL_SLUG}/gguf/{variation}", folder, license_name="Apache 2.0",
                           version_notes=f"From https://huggingface.co/{repo}")
    shutil.rmtree(folder)  # free the disk before the next variation
    print("uploaded", variation)
print(f"https://www.kaggle.com/models/{OWNER}/{MODEL_SLUG}")
''')
md("""
If Kaggle rejects the `gguf` framework name, change `/gguf/` to `/other/` in the handle above and run again.
""")
nb2 = {"cells": cells, "metadata": nb["metadata"], "nbformat": 4, "nbformat_minor": 5}
OUT2.write_text(json.dumps(nb2, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{len(cells)} cells -> {OUT2}")
