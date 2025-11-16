# MamayLM: Ukrainian Large Language Model - Research Report

## Executive Summary

**MamayLM** is a state-of-the-art Ukrainian language model developed by INSAIT (Institute for Computer Science, Artificial Intelligence and Technology) in Bulgaria and ETH Zurich in Switzerland. It's the best-performing efficient Ukrainian LLM available, optimized for both Ukrainian and English languages.

### Quick System Check

Before diving into the details, you can check if your system meets the requirements to run MamayLM locally:

```bash
./tools/check-mamaylm-requirements.sh
```

This script will analyze your GPU, CUDA, RAM, storage, and Python environment to determine if your hardware is adequate for running MamayLM.

---

## 1. What Makes MamayLM Special?

### Key Differentiators

**Outstanding Performance:**
- **Outperforms models up to 10x larger** across various benchmarks
- Achieves the highest score on ZNO (National Ukrainian high school exams) amongst similarly-sized models
- Surpasses much larger models including Gemma2 27B, Llama 3.1 70B, and Qwen 2.5 72B on Ukrainian tasks
- Beats proprietary models like GPT-4 mini on Ukrainian-specific topics

**Ukrainian Language Expertise:**
- Trained on 75B tokens combining Ukrainian and English data
- Superior understanding of Ukrainian dialects, legal and educational terminology, historical references, and societal context
- Instruction fine-tuned on Ukrainian datasets
- Handles Cyrillic script and Ukrainian linguistic nuances better than general-purpose models

**Efficiency:**
- 9B parameters (v0.1) and 4B/12B (v1.0) - much smaller than competitors
- Can run on a single GPU
- Faster adaptation, lower operational costs, simpler deployment
- Memory-efficient for local deployment

**Multimodal Capabilities (v1.0):**
- First open Ukrainian LLM with vision capabilities
- Can process both text and images
- Larger context windows for handling long documents

### When to Choose MamayLM Over Other LLMs

**Choose MamayLM when you need:**

1. **Ukrainian language processing** - significantly better than general-purpose models (GPT-4, Claude, etc.) for Ukrainian content
2. **Data privacy** - can run entirely locally without sending data to third-party APIs
3. **Cost efficiency** - smaller model = lower inference costs, no API fees
4. **Government/institutional use** - designed specifically for Ukrainian government integration
5. **Offline operation** - self-hosted, no internet dependency
6. **Bilingual tasks** - excellent at both Ukrainian and English
7. **Educational applications** - understands Ukrainian educational context (ZNO exams, etc.)
8. **Resource constraints** - runs on consumer hardware unlike 70B+ models

**Stick with other LLMs when:**
- You need broader multilingual support (beyond Ukrainian/English)
- You require the absolute cutting-edge capabilities of frontier models (GPT-4, Claude Sonnet 4)
- You don't have GPU resources and prefer cloud API simplicity
- Your use case is primarily English with no Ukrainian content

---

## 2. How to Use MamayLM - Availability & Licensing

### Is it Free?

**Yes, completely free to download and use** from Hugging Face. Downloaded over 10,000 times within months of release.

### Is it Open?

**Partially open** with important caveats:

**What's Open:**
- Model weights freely available on Hugging Face
- Implementation code is open source
- No API costs or usage fees
- Can be modified and fine-tuned

**What's Restricted:**
- Licensed under **Gemma Terms of Use** (NOT Apache 2.0 or MIT)
- Gemma Terms of Use have commercial restrictions
- Must comply with Google's Gemma license conditions
- Not fully "open source" in the OSI definition

**Key Licensing Points:**
- Free to use for research, education, and most commercial applications
- Some deployment restrictions apply (review Gemma Terms at https://ai.google.dev/gemma/terms)
- Models derived from MamayLM must also follow Gemma Terms
- Full license text: https://github.com/google-deepmind/gemma/blob/main/LICENSE

### Available Versions

**v0.1 (April 2025):**
- Model ID: `INSAIT-Institute/MamayLM-Gemma-2-9B-IT-v0.1`
- 9 billion parameters
- Text-only
- Built on Gemma 2 9B

**v1.0 (September 2025) - Recommended:**
- Model ID: `INSAIT-Institute/MamayLM-Gemma-3-12B-IT-v1.0`
- 4B and 12B parameter variants
- **Multimodal** (text + vision)
- Larger context windows
- Built on Gemma 3
- Better performance overall

### Quick Start Usage

**Installation:**
```bash
# Install required libraries
pip install transformers torch accelerate

# Optional: For faster inference
pip install vllm
```

**Basic Python Example:**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer
model_name = "INSAIT-Institute/MamayLM-Gemma-3-12B-IT-v1.0"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Prepare chat message
messages = [
    {"role": "user", "content": "Розкажи про історію України"}
]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
inputs = tokenizer(text, return_tensors="pt").to(model.device)

# Generate response
outputs = model.generate(
    **inputs,
    max_new_tokens=2048,
    temperature=0.1,
    top_k=25,
    repetition_penalty=1.1
)
response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

**Download Model Locally:**
```bash
# Using Hugging Face CLI
pip install huggingface-hub
huggingface-cli download INSAIT-Institute/MamayLM-Gemma-3-12B-IT-v1.0
```

**Chat Format:**
Uses Gemma chat template with special tokens:
```
<start_of_turn>user
Your question here<end_of_turn>
<start_of_turn>model
Model response<end_of_turn>
```

---

## 3. Self-Hosting: Hardware Requirements & Prerequisites

### Can You Self-Host?

**Yes, absolutely!** MamayLM is specifically designed for self-hosting and local deployment.

### Hardware Requirements

#### GPU Requirements (Critical)

**For 12B Model (v1.0) - Full Precision:**
- **Minimum:** 24GB VRAM (e.g., RTX 3090, RTX 4090, A5000)
- **Recommended:** 32GB+ VRAM (e.g., RTX A6000, A100 40GB)
- **Memory calculation:** ~12B params × 2 bytes (BF16) = ~24GB base + overhead

**For 9B Model (v0.1) - Full Precision:**
- **Minimum:** 20GB VRAM (e.g., RTX 3090 24GB)
- **Recommended:** 24GB VRAM
- **Memory needed:** ~18.6GB for model + context buffer

**For Quantized Models (4-bit/8-bit):**
- **12GB VRAM:** Works with 4-bit quantization (RTX 3060 12GB, RTX 4070)
- **16GB VRAM:** Works with 8-bit quantization (RTX 4080)
- **8GB VRAM:** Challenging even with quantization; expect slowness

**For 4B Model (v1.0):**
- **Minimum:** 8GB VRAM with quantization
- **Recommended:** 12GB+ VRAM for comfortable use

#### CPU/RAM Requirements

**RAM:**
- **Minimum:** Match your VRAM (e.g., 24GB RAM for 24GB GPU)
- **Recommended:** 1.5-2x your VRAM (e.g., 48GB RAM for 24GB GPU)
- **Why:** Model offloading, system stability, preprocessing

**CPU:**
- Modern multi-core CPU (8+ cores recommended)
- AMD Ryzen 5/7 or Intel Core i5/i7 or better
- CPU speed matters less than GPU for inference

**Storage:**
- **30-50GB free space** for model files
- **SSD recommended** for faster loading
- Models are cached locally in `~/.cache/huggingface/`

### Software Prerequisites

**Operating System:**
- Linux (Ubuntu 20.04+, Debian, etc.) - **Best support**
- Windows 10/11 with WSL2 - Good
- macOS - Limited (no NVIDIA CUDA, but can use CPU/MPS)

**Required Software:**

1. **Python 3.8+** (3.10 or 3.11 recommended)
   ```bash
   python3 --version
   ```

2. **CUDA Toolkit** (for NVIDIA GPUs)
   ```bash
   # Check CUDA version
   nvidia-smi

   # Install CUDA 11.8 or 12.1+ recommended
   # Download from: https://developer.nvidia.com/cuda-downloads
   ```

3. **PyTorch with CUDA support**
   ```bash
   # For CUDA 12.1
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

   # Verify GPU access
   python -c "import torch; print(torch.cuda.is_available())"
   ```

4. **Transformers & Dependencies**
   ```bash
   pip install transformers>=4.40.0 accelerate>=0.25.0
   ```

5. **Optional Performance Boosters**
   ```bash
   # Flash Attention 2 (faster inference)
   pip install flash-attn --no-build-isolation

   # vLLM (production serving)
   pip install vllm

   # bitsandbytes (quantization)
   pip install bitsandbytes
   ```

### Deployment Options

#### Option 1: Direct Python Script (Simplest)
```python
# As shown in Usage section above
# Good for: Development, testing, small-scale use
```

#### Option 2: vLLM Server (Production)
```bash
# Install vLLM
pip install vllm

# Start server
python -m vllm.entrypoints.openai.api_server \
    --model INSAIT-Institute/MamayLM-Gemma-3-12B-IT-v1.0 \
    --host 0.0.0.0 \
    --port 8000

# Query with OpenAI-compatible API
curl http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "INSAIT-Institute/MamayLM-Gemma-3-12B-IT-v1.0",
        "prompt": "Привіт! Як справи?",
        "max_tokens": 100
    }'
```

#### Option 3: Ollama (User-Friendly)
```bash
# Note: Check if MamayLM is available in Ollama registry
# As of research date, may need custom import

# If available:
ollama pull mamaylm

# Run
ollama run mamaylm "Розкажи про Київ"
```

#### Option 4: Text Generation WebUI (GUI)
```bash
# Clone oobabooga's text-generation-webui
git clone https://github.com/oobabooga/text-generation-webui
cd text-generation-webui

# Install
./start_linux.sh  # or start_windows.bat

# Download MamayLM through the UI or place in models/
# Access at http://localhost:7860
```

#### Option 5: LM Studio (Desktop App)
- Download LM Studio: https://lmstudio.ai/
- Search for MamayLM GGUF versions
- One-click download and run
- Great for non-technical users

### Quantization for Lower VRAM

**GGUF Quantized Versions:**
Available for download - look for GGUF format models on Hugging Face.

**Common Quantization Levels:**
- **Q2_K:** ~3GB VRAM (lowest quality, significant degradation)
- **Q4_K_M:** ~5-6GB VRAM (good quality/size balance) ⭐ **Recommended**
- **Q5_K_M:** ~7-8GB VRAM (better quality)
- **Q8_0:** ~10GB VRAM (minimal quality loss)

**Creating Custom Quantization:**
```bash
# Install llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

# Convert and quantize
python convert.py /path/to/mamaylm --outtype f16
./quantize ./mamaylm-f16.gguf ./mamaylm-q4_k_m.gguf Q4_K_M
```

### Performance Expectations

**Inference Speed (Approximate):**
- **RTX 4090 (24GB):** ~50-80 tokens/sec (12B model, BF16)
- **RTX 3090 (24GB):** ~30-50 tokens/sec (12B model, BF16)
- **RTX 4070 (12GB):** ~20-35 tokens/sec (4-bit quantized)
- **CPU only:** 1-5 tokens/sec (painfully slow, not recommended)

### Troubleshooting Common Issues

**Out of Memory Errors:**
```python
# Use 8-bit quantization
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    bnb_8bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)
```

**Slow Loading:**
- Use SSD, not HDD
- Download model first with `huggingface-cli download`
- Use `torch_dtype=torch.bfloat16` instead of float32

**CUDA Not Available:**
```bash
# Verify GPU drivers
nvidia-smi

# Reinstall PyTorch with CUDA
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

---

## 4. Additional Context

### Development Team
- **INSAIT** (Institute for Computer Science, Artificial Intelligence and Technology) - Bulgaria
- **ETH Zurich** - Switzerland
- **Affiliation:** Sofia University St. Kliment Ohridski, Bulgaria

### Related Projects
- **National Ukrainian LLM:** Separate project by Ukraine's Ministry of Digital Transformation and Kyivstar (due December 2025)
- **LiBERTa:** BERT Large model for Ukrainian (predecessor work)

### Community & Support
- **Hugging Face:** Primary distribution platform
- **GitHub:** Check INSAIT organization for related code
- **Downloads:** 10,000+ within months of release

### Future Developments
Watch for:
- Larger context windows
- Additional language support
- Fine-tuned specialized versions (legal, medical, etc.)
- Integration with Ukrainian government platforms (Diia, etc.)

---

## Conclusion

**MamayLM is an excellent choice if you:**
- Work with Ukrainian language content
- Need data privacy and local deployment
- Have at least a 24GB NVIDIA GPU (or 12GB with quantization)
- Want state-of-the-art Ukrainian language understanding
- Require cost-efficient inference

**Consider alternatives if:**
- You need dozens of languages
- You lack GPU resources
- You prefer managed API services
- Your use case is primarily non-Ukrainian

**Bottom Line:** MamayLM represents a significant advancement in Ukrainian NLP, offering near-frontier performance specifically for Ukrainian language tasks while remaining accessible for self-hosting. It's genuinely free (though not fully open-source), runs on consumer hardware, and significantly outperforms general-purpose models for Ukrainian content.

---

## Resources

### Official Links
- **Hugging Face (v0.1):** https://huggingface.co/INSAIT-Institute/MamayLM-Gemma-2-9B-IT-v0.1
- **Hugging Face (v1.0):** https://huggingface.co/INSAIT-Institute/MamayLM-Gemma-3-12B-IT-v1.0
- **Official Announcement:** https://huggingface.co/blog/INSAIT-Institute/mamaylm
- **INSAIT Website:** https://insait.ai/
- **Gemma License:** https://ai.google.dev/gemma/terms

### Related Research
- Ukrainian NLP Resources: https://github.com/osyvokon/awesome-ukrainian-nlp
- Tokenization Efficiency Study: https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1538165/full
- LiBERTa Paper: https://aclanthology.org/2024.unlp-1.14/

---

**Report compiled:** 2025-11-16
**Sources:** Hugging Face, INSAIT official blog, dev.ua, academic papers, web research
**Model versions researched:** v0.1 (9B) and v1.0 (4B/12B)
**Researcher:** Claude (Anthropic)
