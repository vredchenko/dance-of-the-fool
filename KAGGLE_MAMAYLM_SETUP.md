# Running MamayLM on Kaggle (Free GPU)

## Overview

Kaggle provides free GPU access through their notebook environment - a better alternative to Google Colab for running MamayLM. This guide shows you how to set up and run MamayLM 9B (4-bit quantized) on Kaggle's free tier.

## Why Kaggle Over Colab?

| Feature | Kaggle Free | Colab Free |
|---------|-------------|------------|
| **GPU Quota** | 30 hours/week (visible) | ~15-20 hours (hidden) |
| **Session Limit** | 9 hours | 12 hours |
| **GPU Assignment** | P100 (16GB) guaranteed | Random (T4/K80/P100) |
| **Quota Visibility** | ✅ Clear counter | ❌ Mystery compute units |
| **Interruptions** | Less frequent | More frequent |
| **Idle Timeout** | 60 minutes | 90 minutes |

**Bottom line:** Kaggle is more predictable and transparent for free GPU access.

## Prerequisites

1. **Kaggle Account** (free)
   - Sign up at https://www.kaggle.com/
   - Verify your phone number (required for GPU access)

2. **Understanding the Limits**
   - 30 GPU hours per week (resets weekly)
   - 9-hour maximum per session
   - Must be actively used (60-minute idle timeout)

## Step-by-Step Setup

### Step 1: Create a New Notebook

1. Go to https://www.kaggle.com/code
2. Click **"New Notebook"**
3. Click the **three dots (⋮)** in the top-right
4. Select **"Notebook options"** or **"Accelerator"**
5. Choose **"GPU P100"** from the dropdown
6. Click **"Save"**

**Verify GPU:**
```python
# Run this in first cell to verify GPU
!nvidia-smi
```

You should see: `Tesla P100-PCIE-16GB`

### Step 2: Install Required Libraries

**Cell 1 - Installation (run once per session):**
```python
# Install required packages
!pip install -q transformers accelerate bitsandbytes huggingface_hub

# Verify installation
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
```

**Expected output:**
```
PyTorch version: 2.x.x
CUDA available: True
GPU: Tesla P100-PCIE-16GB
```

### Step 3: Load MamayLM Model

**Cell 2 - Load Model (takes ~5-10 minutes first time):**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

# Model configuration
model_name = "INSAIT-Institute/MamayLM-Gemma-2-9B-IT-v0.1"

# 4-bit quantization config (to fit in 16GB)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

print("Loading model... (this takes 5-10 minutes)")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
print("✓ Model loaded successfully!")
print(f"Model size in memory: ~{torch.cuda.memory_allocated() / 1024**3:.2f} GB")
```

**Expected memory usage:** ~4-5 GB VRAM (plenty of headroom on 16GB P100)

### Step 4: Create Translation Function

**Cell 3 - Translation Helper:**
```python
def translate_ukrainian_to_english(text, max_length=2048, temperature=0.1):
    """
    Translate Ukrainian text to English using MamayLM.

    Args:
        text: Ukrainian text to translate
        max_length: Maximum length of translation
        temperature: Sampling temperature (lower = more conservative)

    Returns:
        Translated English text
    """
    # Create prompt
    prompt = f"""Translate the following Ukrainian text to English. Maintain the narrative style, tone, and literary quality. Be faithful to the original meaning while producing natural English.

Ukrainian text:
{text}

English translation:"""

    # Prepare input
    messages = [{"role": "user", "content": prompt}]
    text_input = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    inputs = tokenizer(text_input, return_tensors="pt").to(model.device)

    # Generate translation
    print("Translating...")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_length,
            temperature=temperature,
            top_k=25,
            repetition_penalty=1.1,
            do_sample=True if temperature > 0 else False,
            pad_token_id=tokenizer.eos_token_id
        )

    # Decode and extract translation
    full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract just the translation (after "English translation:")
    if "English translation:" in full_output:
        translation = full_output.split("English translation:")[-1].strip()
    else:
        translation = full_output

    return translation

# Test the function
test_text = "Привіт! Як справи?"
result = translate_ukrainian_to_english(test_text)
print(f"\nTest translation:\n{result}")
```

### Step 5: Process Your Book Chunks

**Cell 4 - Upload and Process Chunks:**

#### Option A: Manual Upload (Simple)

1. Click **"+ Add data"** button (right sidebar)
2. Click **"Upload"** → **"New Dataset"**
3. Upload your JSON chunk files (e.g., `chunk_01.json`)
4. Click **"Create"**

```python
import json
import os

# Path to your uploaded chunk (Kaggle mounts datasets in /kaggle/input/)
chunk_path = "/kaggle/input/your-dataset-name/chunk_01.json"

# Load chunk
with open(chunk_path, 'r', encoding='utf-8') as f:
    chunk_data = json.load(f)

# Extract text
ukrainian_text = chunk_data['text']  # Adjust key based on your JSON structure

print(f"Loaded chunk: {len(ukrainian_text)} characters")
print(f"Translating pages {chunk_data.get('start_page', '?')}-{chunk_data.get('end_page', '?')}...")

# Translate
translation = translate_ukrainian_to_english(ukrainian_text)

# Save result
output_data = {
    "original": chunk_data,
    "translation": translation,
    "metadata": {
        "model": "INSAIT-Institute/MamayLM-Gemma-2-9B-IT-v0.1",
        "quantization": "4-bit",
        "temperature": 0.1
    }
}

# Save to output
with open('translation_chunk_01.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("✓ Translation complete!")
print("\nFirst 500 characters:")
print(translation[:500])
```

#### Option B: Batch Processing Multiple Chunks

```python
import json
import glob
from pathlib import Path

# If you uploaded multiple chunks as a dataset
chunks_dir = "/kaggle/input/ukrainian-book-chunks/"
output_dir = "/kaggle/working/"

# Get all chunk files
chunk_files = sorted(glob.glob(f"{chunks_dir}/chunk_*.json"))

print(f"Found {len(chunk_files)} chunks to process")

# Process each chunk
for i, chunk_path in enumerate(chunk_files, 1):
    chunk_name = Path(chunk_path).stem
    print(f"\n{'='*60}")
    print(f"Processing {chunk_name} ({i}/{len(chunk_files)})")
    print('='*60)

    # Load chunk
    with open(chunk_path, 'r', encoding='utf-8') as f:
        chunk_data = json.load(f)

    ukrainian_text = chunk_data.get('text', '')

    # Translate
    translation = translate_ukrainian_to_english(ukrainian_text)

    # Save result
    output_file = f"{output_dir}/translation_{chunk_name}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Translation: {chunk_name}\n\n")
        f.write(f"**Pages:** {chunk_data.get('start_page', '?')}-{chunk_data.get('end_page', '?')}\n\n")
        f.write(f"**Model:** MamayLM-Gemma-2-9B-IT-v0.1 (4-bit)\n\n")
        f.write("---\n\n")
        f.write(translation)

    print(f"✓ Saved: {output_file}")

    # Check GPU quota (if running many chunks)
    if i % 5 == 0:
        print(f"\n⚠ Reminder: Check your GPU quota (30h/week limit)")
        print(f"Estimated time used: ~{i * 10} minutes")

print(f"\n{'='*60}")
print(f"✓ All {len(chunk_files)} chunks processed!")
print(f"Results saved to: {output_dir}")
```

### Step 6: Download Results

**After translation is complete:**

1. Files saved to `/kaggle/working/` are in the right sidebar
2. Click the **folder icon** → **"working"**
3. Select files → **"Download"**
4. Or download all as ZIP

**Download programmatically:**
```python
# Create a ZIP of all translations
!zip -r translations.zip /kaggle/working/translation_*.md

# Download link will appear in output files
print("✓ Download translations.zip from the Output tab")
```

## Workflow for Your 39 Chunks

### Strategy: Split Across Multiple Sessions

**Week 1 (30 GPU hours available):**
- Session 1 (9 hours): Process chunks 1-20 (~15 hours estimated)
  - Actually use ~7-8 hours before timeout
  - Download results

**Week 2 (30 GPU hours available):**
- Session 1 (9 hours): Process chunks 21-39 (~15 hours estimated)
  - Download results

**Total cost:** $0 (free)
**Total calendar time:** 1-2 weeks (due to quota)

### Optimizing Session Time

**Tips to maximize each session:**

1. **Upload all chunks at once** as a dataset (don't re-upload each session)
2. **Process in order** - easier to track progress
3. **Save incrementally** - download every 5 chunks in case of interruption
4. **Monitor memory** - if issues arise, restart kernel and resume
5. **Keep tab active** - prevents idle timeout (or click occasionally)

## Monitoring GPU Quota

**Check remaining quota:**
1. Click your profile (top-right)
2. Go to **"Settings"** → **"Account"**
3. Look for **"GPU Quota"**

**Or in notebook:**
```python
# This won't show quota directly, but you can estimate
import time
start_time = time.time()

# ... do your work ...

elapsed_hours = (time.time() - start_time) / 3600
print(f"Session running for: {elapsed_hours:.2f} hours")
print(f"Estimated quota remaining: {30 - elapsed_hours:.2f} hours this week")
```

## Troubleshooting

### Problem: "Out of Memory" Error

**Solution 1 - Process smaller chunks:**
```python
# Split large chunks into smaller pieces
def chunk_text(text, max_chars=10000):
    """Split text into smaller chunks"""
    chunks = []
    current = ""

    for paragraph in text.split('\n\n'):
        if len(current) + len(paragraph) > max_chars:
            chunks.append(current)
            current = paragraph
        else:
            current += "\n\n" + paragraph

    chunks.append(current)
    return chunks

# Use it:
if len(ukrainian_text) > 15000:
    parts = chunk_text(ukrainian_text, max_chars=12000)
    translations = [translate_ukrainian_to_english(part) for part in parts]
    translation = "\n\n".join(translations)
else:
    translation = translate_ukrainian_to_english(ukrainian_text)
```

**Solution 2 - Clear cache:**
```python
import torch
torch.cuda.empty_cache()
import gc
gc.collect()
```

### Problem: Session Timeout (9 hours)

**Solution - Resume from last chunk:**
```python
# Keep track of processed chunks
processed_chunks = []

# Before each chunk
chunk_name = Path(chunk_path).stem
if chunk_name in processed_chunks:
    print(f"Skipping {chunk_name} (already done)")
    continue

# After successful translation
processed_chunks.append(chunk_name)

# Save progress
with open('progress.txt', 'w') as f:
    f.write('\n'.join(processed_chunks))
```

### Problem: Idle Timeout (60 minutes)

**Solution - Keep alive script:**
```python
# Run this in a separate cell to prevent idle timeout
from IPython.display import Javascript
import time

def keep_alive():
    display(Javascript('''
        function KeepClicking(){
            console.log("Keeping session alive...");
            document.querySelector("colab-toolbar-button#connect").click();
        }
        setInterval(KeepClicking, 60000); // Click every 60 seconds
    '''))

keep_alive()
```

Or simply: **Click notebook occasionally** (every 30-40 minutes)

### Problem: Download Speed Slow

**Solution - Use Google Drive integration:**
```python
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Save directly to Drive
output_path = '/content/drive/MyDrive/mamaylm_translations/'
os.makedirs(output_path, exist_ok=True)

# Save translations there instead of /kaggle/working/
```

## Cost Analysis

**Free Kaggle approach:**
- **GPU cost:** $0 (free 30 hours/week)
- **Storage cost:** $0 (temporary)
- **Time investment:** 2-4 hours of setup + monitoring
- **Calendar time:** 1-2 weeks (quota constraints)
- **Effort:** Medium (need to babysit sessions)

**Total: $0 but requires time and patience**

## Comparison: Kaggle vs Alternatives

| Approach | Cost | Time | Quality | Effort |
|----------|------|------|---------|--------|
| **Kaggle Free** | $0 | 1-2 weeks | Good (4-bit) | Medium |
| **Colab Free** | $0 | 2-3 weeks | Good (4-bit) | High |
| **RunPod** | ~$5-10 | 1 day | Excellent (full) | Low |
| **API (Claude)** | ~$5-15 | 1 day | Excellent | Very Low |
| **Colab Pro** | $10/mo | 3-5 days | Good (4-bit) | Medium |

## Sample Notebook Template

**Complete working notebook structure:**

```
Cell 1: Setup
- !pip install libraries
- Verify GPU

Cell 2: Load Model
- Import transformers
- Load MamayLM with 4-bit quantization

Cell 3: Helper Functions
- translate_ukrainian_to_english()
- chunk_text() for large texts

Cell 4: Upload Data
- Mount dataset
- List chunk files

Cell 5: Process Chunks
- Loop through chunks
- Translate each
- Save results

Cell 6: Download
- Zip results
- Provide download link
```

## Next Steps

1. **Sign up for Kaggle** (if not already)
2. **Create first notebook** following steps above
3. **Test with 1-2 chunks** to verify quality
4. **Process remaining chunks** across sessions
5. **Download and integrate** results

## Tips for Success

1. **Start with one chunk** - verify quality before batch processing
2. **Upload all chunks as one dataset** - save time across sessions
3. **Track progress** - keep a list of completed chunks
4. **Download frequently** - don't lose work to session timeouts
5. **Monitor quota** - don't waste GPU time on debugging
6. **Use version control** - commit translations as you go

## When Kaggle Isn't the Right Choice

**Consider alternatives if:**
- You need all 39 chunks done in one day → Use RunPod
- You don't want to monitor sessions → Use APIs
- You need highest quality (full precision) → Rent GPU
- You have budget ($10-50) → Colab Pro or cloud GPU

---

**Created:** 2025-11-16
**For project:** spastics-dance Ukrainian book translation
**Model:** MamayLM-Gemma-2-9B-IT-v0.1 (4-bit quantization)
