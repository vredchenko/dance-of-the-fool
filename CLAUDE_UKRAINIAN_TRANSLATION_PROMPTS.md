# Optimized Claude Prompts for Ukrainian→English Translation

## Overview

This guide provides optimized prompts for using Claude (or other LLM APIs) to translate Ukrainian literature to English, specifically for literary/narrative works like your book "Танець недоумка" (Dance of the Fool).

## Why Use Claude for Ukrainian Translation?

### Advantages

✅ **Strong multilingual capabilities** - Claude has good Ukrainian language understanding
✅ **Literary quality** - Excellent at maintaining narrative style and tone
✅ **Context window** - Can handle large chunks (200K tokens in Claude 3.5 Sonnet)
✅ **No setup required** - API access, no GPU needed
✅ **Consistent quality** - Less variability than self-hosted models
✅ **Reliability** - No session timeouts or GPU quota issues

### Limitations

❌ **Not Ukrainian-specialized** - MamayLM is specifically trained on Ukrainian
❌ **Cost per token** - More expensive than self-hosting for large volumes
❌ **API dependency** - Requires internet, subject to rate limits
❌ **Less understanding of nuance** - May miss some Ukrainian cultural context

### When to Use Claude API vs MamayLM

**Use Claude API if:**
- Budget is $10-20 (vs $0 for free or $3 for RunPod)
- Want simplest workflow (no GPU setup)
- Need it done today/tomorrow
- Don't have technical background
- Value your time highly

**Use MamayLM if:**
- Want best possible Ukrainian understanding
- Have more time (1-2 weeks free, 1 day paid)
- Willing to set up GPU environment
- Want to learn about LLM deployment

## Cost Estimate for Your Book

### Your Project Specs
- **Book:** 468 pages
- **Chunks:** 39 chunks × 12 pages each
- **Average per chunk:** ~23,400 chars = ~3,840 words = ~5,120 tokens (Ukrainian)
- **Output per chunk:** ~4,000 words = ~5,300 tokens (English translation)

### Token Calculations

**Input tokens (Ukrainian text):**
```
39 chunks × 5,120 tokens/chunk = 199,680 tokens
Plus prompt overhead (~500 tokens each): 19,500 tokens
Total input: ~220,000 tokens
```

**Output tokens (English translation):**
```
39 chunks × 5,300 tokens/chunk = 206,700 tokens
```

### Pricing by Model

#### Claude 3.5 Sonnet (Recommended)

**Pricing:**
- Input: $3.00 per 1M tokens
- Output: $15.00 per 1M tokens

**Your cost:**
```
Input:  220,000 tokens × $3.00/1M  = $0.66
Output: 206,700 tokens × $15.00/1M = $3.10
────────────────────────────────────────
Total:                                $3.76
```

**With API overhead/retries (×1.3):** ~$5.00

#### Claude 3 Opus (Highest Quality)

**Pricing:**
- Input: $15.00 per 1M tokens
- Output: $75.00 per 1M tokens

**Your cost:**
```
Input:  220,000 tokens × $15.00/1M  = $3.30
Output: 206,700 tokens × $75.00/1M  = $15.50
────────────────────────────────────────
Total:                                 $18.80
```

**With overhead:** ~$24.00

#### Claude 3 Haiku (Budget Option)

**Pricing:**
- Input: $0.25 per 1M tokens
- Output: $1.25 per 1M tokens

**Your cost:**
```
Input:  220,000 tokens × $0.25/1M = $0.06
Output: 206,700 tokens × $1.25/1M = $0.26
────────────────────────────────────────
Total:                               $0.32
```

**With overhead:** ~$0.50

⚠️ **Warning:** Haiku may lose literary nuance - not recommended for literature

### Comparison Table

| Model | Total Cost | Quality | Speed | Recommendation |
|-------|-----------|---------|-------|----------------|
| **Claude 3.5 Sonnet** | **~$5** | ⭐⭐⭐⭐⭐ | Fast | ✅ **Best choice** |
| Claude 3 Opus | ~$24 | ⭐⭐⭐⭐⭐ | Slower | Overkill for this |
| Claude 3 Haiku | ~$0.50 | ⭐⭐⭐ | Very fast | Too basic |
| GPT-4 Turbo | ~$8-10 | ⭐⭐⭐⭐⭐ | Fast | Good alternative |
| GPT-4o | ~$4-6 | ⭐⭐⭐⭐ | Very fast | Good budget option |
| MamayLM (RunPod) | ~$3.50 | ⭐⭐⭐⭐⭐ | Medium | Best Ukrainian quality |
| MamayLM (Kaggle) | $0 | ⭐⭐⭐⭐ | Slow | Best free option |

## Optimized Translation Prompts

### Basic Translation Prompt

**For straightforward translation:**

```xml
<task>Translate the following Ukrainian text to English</task>

<context>
This is a chunk from the Ukrainian science fiction novel "Танець недоумка"
(Dance of the Fool) by Ілларіон Павлюк. The book is a literary work with
philosophical and social commentary elements.
</context>

<guidelines>
- Maintain the original narrative voice and tone
- Preserve literary devices (metaphors, imagery, wordplay where possible)
- Use natural, fluent English while staying faithful to the original meaning
- Keep paragraph structure intact
- Do not add explanatory notes or commentary in the translation itself
- Translate dialogue naturally, capturing character voices
</guidelines>

<ukrainian_text>
{INSERT YOUR UKRAINIAN TEXT HERE}
</ukrainian_text>

Provide only the English translation, without additional commentary.
```

### Advanced Literary Translation Prompt

**For higher quality with more context:**

```xml
<task>Literary Translation: Ukrainian to English</task>

<context>
This is pages {X-Y} from "Танець недоумка" (Dance of the Fool), a 1970
Ukrainian science fiction novel by Ілларіон Павлюк. The novel explores
themes of social conformity, individual freedom, and the nature of
intelligence through a satirical lens.

The title "Танець недоумка" is challenging to translate directly.
"Недоумок" means "fool" or "simpleton" but carries connotations
of someone who doesn't fit societal norms due to different thinking
rather than lack of intelligence. Consider "Dance of the Fool" or
"Dance of the Misfit" based on context.
</context>

<translation_philosophy>
This is a literary translation, not a technical one. Prioritize:
1. Narrative flow and readability in English
2. Preservation of tone (satirical, philosophical, or dramatic as appropriate)
3. Character voice consistency
4. Literary quality over word-for-word accuracy
5. Natural English idioms over direct Ukrainian idiom translation

Where Ukrainian cultural references or wordplay cannot be directly
translated, choose English equivalents that preserve the intent and
emotional impact.
</translation_philosophy>

<style_notes>
- The original has a sardonic, observational tone
- Dialogue is often formal/Soviet-era bureaucratic speech patterns
- Descriptions can be poetic and philosophical
- Maintain any intentional ambiguity or wordplay
</style_notes>

<ukrainian_text>
{INSERT YOUR UKRAINIAN TEXT HERE}
</ukrainian_text>

<output_format>
Provide only the English translation without commentary, maintaining
original paragraph breaks and formatting.
</output_format>
```

### Prompt with Translation Memory

**For maintaining consistency across chunks:**

```xml
<task>Translate Ukrainian text to English (Chunk {N} of 39)</task>

<previous_context>
This chunk follows the previous translation where:
- Main character: {Character name/description}
- Setting: {Current location/situation}
- Key terms established:
  * "{Ukrainian term}" → "{English translation}"
  * "{Ukrainian term}" → "{English translation}"
</previous_context>

<consistency_guidelines>
Maintain terminology consistency with previous chunks:
- Character names: {List established translations}
- Place names: {List established translations}
- Technical/invented terms: {List established translations}
- Recurring phrases: {List established translations}
</consistency_guidelines>

<ukrainian_text>
{INSERT YOUR UKRAINIAN TEXT HERE}
</ukrainian_text>

Translate maintaining consistency with established terminology and style.
```

### Prompt for Difficult Passages

**When you encounter challenging sections:**

```xml
<task>Translate challenging Ukrainian passage with analysis</task>

<text>
{INSERT PROBLEMATIC UKRAINIAN TEXT}
</text>

<challenges>
This passage contains:
- [Wordplay/puns]
- [Cultural references specific to Soviet Ukraine]
- [Ambiguous pronouns]
- [Poetic/metaphorical language]
</challenges>

<request>
1. Provide your best English translation
2. In a separate section labeled "Translation Notes," explain:
   - Any difficult choices you made
   - Alternative interpretations considered
   - Cultural context that may not be obvious to English readers
   - Wordplay or nuances that couldn't be fully preserved
</request>

<output_format>
# Translation

{Your English translation}

# Translation Notes

{Your explanations and context}
</output_format>
```

## Workflow for Your 39 Chunks

### Option A: One-by-One (Simple)

**Process:**
1. Load chunk_01.json
2. Copy Ukrainian text
3. Send to Claude with Basic Prompt
4. Save translation as markdown
5. Repeat for chunk_02, chunk_03, etc.

**Time estimate:** ~5 minutes per chunk = ~3.5 hours total
**Cost:** ~$5 (Claude 3.5 Sonnet)
**Pros:** Simple, can review each as you go
**Cons:** Repetitive, manual work

### Option B: Automated via API (Recommended)

**Setup script (Python):**

```python
import anthropic
import json
import time
from pathlib import Path

# Initialize client
client = anthropic.Anthropic(api_key="your-api-key-here")

# Configuration
CHUNKS_DIR = "book/originals/chunks/"
OUTPUT_DIR = "book/translations/v1_claude/"
MODEL = "claude-3-5-sonnet-20241022"

def translate_chunk(chunk_num, ukrainian_text):
    """Translate a chunk using Claude API"""

    prompt = f"""<task>Translate the following Ukrainian text to English</task>

<context>
This is chunk {chunk_num} of 39 from the Ukrainian science fiction novel
"Танець недоумка" (Dance of the Fool) by Ілларіон Павлюк.
</context>

<guidelines>
- Maintain narrative voice and literary quality
- Preserve paragraph structure
- Use natural, fluent English
- Stay faithful to original meaning
</guidelines>

<ukrainian_text>
{ukrainian_text}
</ukrainian_text>

Provide only the English translation."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text

# Process all chunks
for chunk_num in range(1, 40):
    chunk_file = Path(CHUNKS_DIR) / f"chunk_{chunk_num:02d}.json"

    print(f"Processing chunk {chunk_num}/39...")

    # Load chunk
    with open(chunk_file, 'r', encoding='utf-8') as f:
        chunk_data = json.load(f)

    ukrainian_text = chunk_data['text']

    # Translate
    translation = translate_chunk(chunk_num, ukrainian_text)

    # Save
    output_file = Path(OUTPUT_DIR) / f"translation_chunk_{chunk_num:02d}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Translation: Chunk {chunk_num}\n\n")
        f.write(f"**Pages:** {chunk_data['start_page']}-{chunk_data['end_page']}\n\n")
        f.write(f"**Model:** Claude 3.5 Sonnet\n\n")
        f.write("---\n\n")
        f.write(translation)

    print(f"✓ Saved: {output_file}")

    # Rate limiting (be nice to the API)
    time.sleep(2)

print("✓ All chunks translated!")
```

**Time:** ~30 minutes total (mostly API calls)
**Cost:** ~$5
**Pros:** Automated, consistent, fast
**Cons:** Need API key, basic Python knowledge

### Option C: Batch with Review

**Process:**
1. Auto-translate all 39 chunks (Option B)
2. Review each translation
3. Manually refine difficult passages
4. Create uncertainty notes for ambiguous sections

**Time:** ~2-3 hours total
**Cost:** ~$5-6 (some retries)
**Pros:** Best quality, consistent, efficient
**Cons:** Requires more attention

## Quality Optimization Techniques

### Technique 1: Provide Character Glossary

**Add to prompt:**

```xml
<characters>
- Protagonist: {Name and brief description}
- Supporting: {Name and brief description}
- {etc.}
</characters>

Maintain consistent characterization and voice for each.
```

### Technique 2: Include Previous Paragraph

**For better context continuity:**

```xml
<previous_paragraph>
{Last paragraph from previous chunk's translation}
</previous_paragraph>

<current_text>
{Current chunk to translate}
</current_text>

Ensure smooth narrative flow from previous paragraph.
```

### Technique 3: Two-Pass Translation

**First pass - literal:**
```xml
<task>Provide a literal, word-for-word translation of this Ukrainian text</task>
```

**Second pass - literary:**
```xml
<task>
Take this literal translation and refine it into natural, literary English
while preserving the original meaning and tone.
</task>

<literal_translation>
{Output from first pass}
</literal_translation>
```

**Cost:** 2x tokens, but higher quality
**Use for:** Challenging sections only

### Technique 4: Uncertainty Tracking

**Modified prompt:**

```xml
After the translation, include a brief section labeled "Translator Notes"
if there are any:
- Ambiguous phrases requiring interpretation
- Cultural references that may need footnotes
- Wordplay that couldn't be fully preserved
- Alternative translation choices considered

Keep notes minimal and only for significant decisions.
```

## API Setup Instructions

### Using Claude API (Anthropic)

**1. Get API Key:**
- Go to https://console.anthropic.com/
- Sign up / log in
- Navigate to "API Keys"
- Create new key
- Copy and save securely

**2. Install SDK:**
```bash
pip install anthropic
```

**3. Test connection:**
```python
import anthropic

client = anthropic.Anthropic(api_key="your-key-here")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Translate to English: Привіт, як справи?"}]
)

print(response.content[0].text)
```

### Using OpenAI API (GPT-4 Alternative)

**1. Get API Key:**
- Go to https://platform.openai.com/
- Sign up / log in
- API keys section
- Create new key

**2. Install SDK:**
```bash
pip install openai
```

**3. Usage:**
```python
from openai import OpenAI

client = OpenAI(api_key="your-key-here")

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[{
        "role": "user",
        "content": "Translate this Ukrainian text to English: {text}"
    }]
)

print(response.choices[0].message.content)
```

## Cost Management

### Tip 1: Start with Small Test

**Before processing all 39 chunks:**
```python
# Test with chunk 1 only
test_chunk = load_chunk(1)
translation = translate(test_chunk)

# Review quality
# Estimate tokens
# Calculate cost
# Decide if approach is good
```

**Investment:** $0.13 (one chunk)
**Saves:** Wasting $5 on poor approach

### Tip 2: Use Haiku for Draft, Sonnet for Refinement

**Two-stage approach:**
```python
# Stage 1: Haiku draft (cheap)
draft = translate_with_haiku(text)  # ~$0.01 per chunk

# Stage 2: Sonnet refinement (selective)
if needs_refinement(draft):
    final = refine_with_sonnet(draft)  # ~$0.13 per chunk
else:
    final = draft
```

**Savings:** ~40-60% on straightforward passages

### Tip 3: Batch with Caching (Advanced)

**Claude has prompt caching:**
```python
# Reusable system prompt cached (not charged repeatedly)
system = "You are an expert Ukrainian→English literary translator..."

# Only charged once, reused for 39 chunks
# Savings: ~$0.50-1.00 total
```

### Tip 4: Monitor Token Usage

```python
import anthropic

response = client.messages.create(...)

print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
print(f"Cost: ${calculate_cost(response.usage)}")

# Adjust strategy if costs higher than expected
```

## Comparison: API vs Self-Hosted

### Full Cost-Benefit Analysis

| Factor | Claude API | MamayLM RunPod | MamayLM Kaggle |
|--------|-----------|----------------|----------------|
| **Total Cost** | $5 | $3.50 | $0 |
| **Setup Time** | 10 min | 1 hour | 1 hour |
| **Processing Time** | 30 min | 5 hours | 1-2 weeks |
| **Your Time Investment** | 1 hour | 2 hours | 5-10 hours |
| **Technical Skill** | Low | Medium | Medium |
| **Quality (Ukrainian)** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Reliability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Convenience** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

### When Each Makes Sense

**Choose Claude API ($5) if:**
- ✅ Your time is worth $20+/hour (saves 3-5 hours)
- ✅ You want it done today
- ✅ You prefer simple Python scripts
- ✅ You're okay with "very good" vs "best" Ukrainian quality

**Choose MamayLM RunPod ($3.50) if:**
- ✅ You want absolute best Ukrainian understanding
- ✅ You can dedicate 5-7 hours tomorrow
- ✅ You're comfortable with GPU setup
- ✅ You want to learn about LLM deployment

**Choose MamayLM Kaggle ($0) if:**
- ✅ Budget is zero (student/hobby project)
- ✅ You have 1-2 weeks timeline
- ✅ You can babysit sessions
- ✅ You view it as learning experience

## Sample Complete Workflow (Claude API)

### End-to-End Script

```python
#!/usr/bin/env python3
"""
Complete translation workflow using Claude API
For "Танець недоумка" Ukrainian book translation
"""

import anthropic
import json
import time
from pathlib import Path
from datetime import datetime

# Configuration
API_KEY = "your-api-key-here"  # Get from console.anthropic.com
CHUNKS_DIR = Path("book/originals/chunks")
OUTPUT_DIR = Path("book/translations/v1_claude")
MODEL = "claude-3-5-sonnet-20241022"

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Initialize client
client = anthropic.Anthropic(api_key=API_KEY)

def load_chunk(chunk_num):
    """Load a chunk JSON file"""
    chunk_file = CHUNKS_DIR / f"chunk_{chunk_num:02d}.json"
    with open(chunk_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def translate_chunk(chunk_num, chunk_data):
    """Translate a chunk using Claude"""

    ukrainian_text = chunk_data['text']

    prompt = f"""<task>Translate Ukrainian text to English</task>

<context>
Chunk {chunk_num}/39 from "Танець недоумка" (Dance of the Fool) by Ілларіон Павлюк,
a 1970 Ukrainian science fiction novel exploring themes of conformity and individuality.
Pages {chunk_data.get('start_page', '?')}-{chunk_data.get('end_page', '?')}.
</context>

<guidelines>
- Maintain literary quality and narrative voice
- Preserve paragraph structure
- Use natural, fluent English
- Stay faithful to original meaning
</guidelines>

<ukrainian_text>
{ukrainian_text}
</ukrainian_text>

Provide only the English translation."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}]
    )

    translation = response.content[0].text

    # Track usage
    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "cost": (response.usage.input_tokens * 3 + response.usage.output_tokens * 15) / 1_000_000
    }

    return translation, usage

def save_translation(chunk_num, chunk_data, translation, usage):
    """Save translation as markdown"""

    output_file = OUTPUT_DIR / f"translation_chunk_{chunk_num:02d}.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Translation: Chunk {chunk_num}\n\n")
        f.write(f"**Pages:** {chunk_data.get('start_page', '?')}-{chunk_data.get('end_page', '?')}\n")
        f.write(f"**Model:** {MODEL}\n")
        f.write(f"**Translated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Tokens:** {usage['input_tokens']} in, {usage['output_tokens']} out\n")
        f.write(f"**Cost:** ${usage['cost']:.4f}\n\n")
        f.write("---\n\n")
        f.write(translation)

    return output_file

# Main execution
def main():
    print("="*60)
    print("Ukrainian → English Translation")
    print("Book: Танець недоумка (Dance of the Fool)")
    print("="*60)

    total_cost = 0
    total_input_tokens = 0
    total_output_tokens = 0

    for chunk_num in range(1, 40):
        print(f"\n[{chunk_num}/39] Processing chunk {chunk_num}...")

        # Load
        chunk_data = load_chunk(chunk_num)
        print(f"  Loaded: {len(chunk_data['text'])} characters")

        # Translate
        translation, usage = translate_chunk(chunk_num, chunk_data)
        print(f"  Translated: {len(translation)} characters")
        print(f"  Cost: ${usage['cost']:.4f}")

        # Save
        output_file = save_translation(chunk_num, chunk_data, translation, usage)
        print(f"  Saved: {output_file}")

        # Track totals
        total_cost += usage['cost']
        total_input_tokens += usage['input_tokens']
        total_output_tokens += usage['output_tokens']

        # Rate limiting
        time.sleep(1)

    # Final summary
    print("\n" + "="*60)
    print("TRANSLATION COMPLETE")
    print("="*60)
    print(f"Chunks processed: 39")
    print(f"Total input tokens: {total_input_tokens:,}")
    print(f"Total output tokens: {total_output_tokens:,}")
    print(f"Total cost: ${total_cost:.2f}")
    print(f"Output directory: {OUTPUT_DIR}")
    print("="*60)

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
# Install dependencies
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Run
python translate_book.py
```

## Summary: Best Approach for Your Book

### My Recommendation: Claude API

**Why:**
1. **Cost-effective:** $5 total (vs $24 for Opus, $0 for free but slow)
2. **Fast:** Done in < 1 hour
3. **Simple:** No GPU setup, no session management
4. **Reliable:** No timeouts, no interruptions
5. **Good quality:** Not specialized like MamayLM, but very capable

**When to reconsider:**
- If you want absolute best Ukrainian quality → MamayLM RunPod ($3.50)
- If you have $0 budget → MamayLM Kaggle (free)
- If you want to learn GPU/LLM deployment → Any self-hosted option

### Quick Start (Next 15 Minutes)

1. **Sign up:** https://console.anthropic.com/
2. **Add $10 credit** (you'll use ~$5)
3. **Copy API key**
4. **Test one chunk** with basic prompt
5. **Review quality**
6. **Decide:** If good, use automation script. If not, try MamayLM.

### Total Investment Summary

```
Time:      1 hour (setup + monitoring)
Cost:      $5
Quality:   ⭐⭐⭐⭐/5 (very good, not specialized)
Effort:    Low
Timeline:  Done today

vs MamayLM RunPod:
Time:      2 hours
Cost:      $3.50
Quality:   ⭐⭐⭐⭐⭐/5 (best Ukrainian quality)
Effort:    Medium
Timeline:  Done tomorrow
```

**Both are good options.** Choose based on your priorities: simplicity (Claude) vs quality (MamayLM).

---

**Created:** 2025-11-16
**For project:** spastics-dance Ukrainian book translation
**Recommended approach:** Claude 3.5 Sonnet API at ~$5 total cost
