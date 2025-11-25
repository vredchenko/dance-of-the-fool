# RunPod Cost Calculator for MamayLM

## Overview

RunPod is a cloud GPU rental platform that's ideal for running MamayLM at full precision. This guide provides cost estimates specifically for translating your 468-page Ukrainian book (39 chunks).

## What is RunPod?

**RunPod** (https://www.runpod.io/) is a cloud computing platform that rents GPU instances by the hour. Think "Airbnb for GPUs."

**Key advantages:**
- Pay only for GPU time used (per-second billing)
- Wide range of GPU options
- No monthly subscription required
- Persistent storage available
- SSH and Jupyter notebook access

## GPU Options & Pricing

### Current RunPod GPU Pricing (as of 2025)

| GPU Model | VRAM | Price/hour | Best For |
|-----------|------|------------|----------|
| **RTX 4090** | 24GB | $0.39-0.49 | ⭐ Best value for MamayLM 12B |
| **RTX 3090** | 24GB | $0.29-0.39 | Good budget option |
| **RTX A5000** | 24GB | $0.49-0.59 | Professional, reliable |
| **RTX 4080** | 16GB | $0.34-0.44 | Can run 9B, not 12B |
| **A100 40GB** | 40GB | $0.99-1.29 | Overkill for this task |
| **A100 80GB** | 80GB | $1.49-1.99 | Not needed |

**Recommendation for MamayLM:** RTX 4090 (24GB) at ~$0.39-0.49/hour

### Why RTX 4090 is Optimal

- **24GB VRAM:** Runs MamayLM 12B at full BF16 precision comfortably
- **Speed:** ~50-80 tokens/sec (3-4x faster than T4 on Kaggle)
- **Cost-effective:** Cheapest 24GB option
- **Availability:** Usually good availability

## Cost Breakdown for Your Book Translation

### Project Specifications

- **Book:** 468 pages
- **Chunks:** 39 total (12 pages each)
- **Chunk size:** ~23,400 characters (~3,840 words) per chunk
- **Model:** MamayLM-Gemma-3-12B-IT-v1.0 (recommended)

### Time Estimates

**Per chunk processing time:**
```
Model loading:         ~2-3 minutes (one-time per session)
Chunk translation:     ~5-8 minutes per chunk
Saving/processing:     ~1 minute per chunk
Total per chunk:       ~6-9 minutes average
```

**Total project time:**
```
Setup (one-time):      ~10 minutes
39 chunks × 7 min:     ~273 minutes (4.5 hours)
Buffer/overhead:       ~30 minutes
Total GPU time:        ~5 hours
```

### Cost Calculations

#### Scenario 1: RTX 4090 (Recommended)

**GPU:** RTX 4090 (24GB VRAM)
**Hourly rate:** $0.44 (average)
**Estimated time:** 5 hours

```
GPU cost:          5 hours × $0.44/hour = $2.20
Storage (10GB):    ~$0.10/month prorated  = $0.01
Network egress:    ~1GB download          = $0.02
Total:             $2.23
```

**With safety buffer (in case of issues):**
```
Conservative estimate: 7 hours × $0.44 = $3.08
Realistic total:       $3.00-3.50
```

#### Scenario 2: RTX 3090 (Budget Option)

**GPU:** RTX 3090 (24GB VRAM)
**Hourly rate:** $0.34 (average)
**Estimated time:** 6 hours (slightly slower)

```
GPU cost:          6 hours × $0.34/hour = $2.04
Storage:           $0.01
Network:           $0.02
Total:             $2.07
```

**Conservative estimate:** $2.50-3.00

#### Scenario 3: RTX A5000 (Premium/Reliable)

**GPU:** RTX A5000 (24GB VRAM)
**Hourly rate:** $0.54 (average)
**Estimated time:** 5 hours

```
GPU cost:          5 hours × $0.54/hour = $2.70
Storage:           $0.01
Network:           $0.02
Total:             $2.73
```

**Conservative estimate:** $3.50-4.00

## Detailed Cost Comparison

### Your 468-Page Book (All Approaches)

| Approach | Total Cost | Time to Complete | Quality | Effort |
|----------|-----------|------------------|---------|--------|
| **RunPod RTX 4090** | **$3.00-3.50** | **~5-7 hours** | ⭐⭐⭐⭐⭐ Full precision | ⭐⭐⭐⭐ Low |
| **RunPod RTX 3090** | **$2.50-3.00** | **~6-8 hours** | ⭐⭐⭐⭐⭐ Full precision | ⭐⭐⭐⭐ Low |
| Kaggle Free | $0 | 1-2 weeks | ⭐⭐⭐⭐ 4-bit quant | ⭐⭐⭐ Medium |
| Colab Free | $0 | 2-3 weeks | ⭐⭐⭐⭐ 4-bit quant | ⭐⭐ High |
| Claude API | $5-15 | 4-6 hours | ⭐⭐⭐⭐⭐ GPT quality | ⭐⭐⭐⭐⭐ Very Low |
| GPT-4 API | $8-20 | 3-5 hours | ⭐⭐⭐⭐⭐ GPT quality | ⭐⭐⭐⭐⭐ Very Low |
| Colab Pro | $10/month | 3-5 days | ⭐⭐⭐⭐ 4-bit quant | ⭐⭐⭐ Medium |

**Value Analysis:**
- **Best ROI:** RunPod RTX 4090 ($3.50 for 5 hours, full quality)
- **Absolute cheapest:** Kaggle/Colab free (but slow and frustrating)
- **Easiest:** Claude/GPT API (but more expensive, less Ukrainian-optimized)

## Hidden Costs & Considerations

### What's Included

✅ **Included in hourly rate:**
- GPU usage
- CPU cores (typically 8-16)
- RAM (typically 32-64GB)
- Basic bandwidth

### What Costs Extra

❌ **Additional charges:**
- **Storage:** ~$0.10/GB/month (you need ~10GB)
  - Prorated by hour: ~$0.01 for a day
- **Egress bandwidth:** ~$0.02/GB over 1GB/hour
  - You'll download ~1-2GB: ~$0.02-0.04
- **Persistent storage:** If you want to keep environment between sessions
  - ~$0.20/GB/month

**For your use case:** Additional costs are negligible (~$0.05 total)

### Cost Traps to Avoid

1. **Forgetting to terminate instance** 💸
   - Solution: Set auto-stop timer
   - Cost if left running 24h: $0.44 × 24 = $10.56

2. **Choosing oversized GPU**
   - A100 80GB costs 4x more than RTX 4090
   - No benefit for MamayLM 12B

3. **Persistent storage you don't need**
   - Just download results at end
   - Don't pay for storage

4. **Multiple failed attempts**
   - Test with 1 chunk first
   - Debug before processing all 39

## Setup Cost Estimate

**One-time setup (before processing chunks):**

```
Account creation:          Free
Initial deposit:           $10 minimum (credits, not a fee)
Template/image setup:      ~5 minutes (included in GPU time)
Testing (1-2 chunks):      ~0.5 hours × $0.44 = $0.22

Total one-time cost:       ~$0.25 (testing)
Minimum deposit required:  $10 (but you keep unused credits)
```

## Total Project Budget

### Conservative Budget (Recommended)

```
GPU rental (RTX 4090):     7 hours × $0.44 = $3.08
Storage (1 day):           $0.01
Network egress:            $0.04
Testing/debugging:         $0.50
Buffer for issues:         $0.40
────────────────────────────────────────
TOTAL:                     $4.03

Round up to:               $5.00 (safe estimate)
```

### Minimum Deposit

```
RunPod minimum:            $10
Expected usage:            ~$3-4
Remaining credits:         ~$6-7 (kept for future use)
```

**Effective cost:** $3-4 (you keep remaining balance)

### Optimistic Budget (If Everything Goes Smoothly)

```
GPU rental (RTX 4090):     5 hours × $0.44 = $2.20
Storage/network:           $0.05
No issues/retries:         $0.00
────────────────────────────────────────
TOTAL:                     $2.25
```

## Cost Per Chunk Breakdown

**Individual chunk economics:**

```
Per chunk (RTX 4090):
Translation time:          ~7 minutes = 0.117 hours
Cost per chunk:            0.117 × $0.44 = $0.051

Cost per page:             $0.051 ÷ 12 pages = $0.0043/page
Cost per word:             $0.051 ÷ 3,840 words = $0.000013/word

For 468 pages total:
Total cost:                468 × $0.0043 = $2.01
Plus overhead (~40%):      $2.01 × 1.4 = $2.81
```

**Reality check:** Expect $3-4 total (overhead, model loading, etc.)

## Comparison: RunPod vs Other Cloud Providers

| Provider | GPU | Price/hour | Your Project Cost |
|----------|-----|------------|-------------------|
| **RunPod** (RTX 4090) | 24GB | $0.44 | **$3.00-3.50** |
| **Vast.ai** (RTX 4090) | 24GB | $0.35-0.55 | $2.50-4.00 |
| Lambda Labs (A100) | 40GB | $1.10 | $6.00-8.00 |
| Google Colab Pro+ | V100 | $50/mo | $50 (monthly) |
| AWS g4dn.xlarge (T4) | 16GB | $0.526 | Can't run 12B |
| Azure NC6s v3 (V100) | 16GB | $3.06 | $15-20 (overkill) |

**RunPod wins on price/performance for this task.**

## When to Choose RunPod

✅ **RunPod is best if:**
- You want full precision (best quality)
- You want it done in one session (5-7 hours)
- You can budget $3-5
- You're comfortable with basic terminal/Python
- You want faster inference than free options

❌ **Skip RunPod if:**
- You have $0 budget (use Kaggle free)
- You prefer API simplicity (use Claude/GPT)
- You don't want to manage GPU instance
- You only need to test 1-2 chunks

## ROI Analysis: Is $3.50 Worth It?

**What you get for $3.50:**

| Item | Value |
|------|-------|
| GPU time saved vs free | ~20-30 hours of waiting |
| Your time saved | ~3-5 hours of session management |
| Quality improvement | Full BF16 vs 4-bit quantization |
| Reliability | One session vs 3-5 sessions |
| Completion speed | 1 day vs 1-2 weeks |

**Your hourly rate calculation:**
- If your time is worth $10/hour: $3.50 saves you 3-5 hours = $30-50 value
- If your time is worth $20/hour: $60-100 value
- **ROI: 8-28x return on investment**

**Bottom line:** If your time has any value, $3.50 is a bargain.

## Step-by-Step Setup Guide

### Prerequisites

1. **RunPod Account**
   - Sign up at https://www.runpod.io/
   - Email verification required

2. **Minimum Deposit: $10**
   - Credit card or crypto
   - Unused credits remain in account

3. **Your Book Chunks**
   - Have all 39 JSON files ready to upload

### Setup Process (Included in Budget)

```
1. Create account:             Free, 2 minutes
2. Add $10 credit:             2 minutes
3. Deploy GPU pod:             1 minute
4. Upload chunks:              5 minutes
5. Install libraries:          3 minutes
6. Load MamayLM:               5 minutes
7. Test one chunk:             7 minutes
   ─────────────────────────────────────
   Total setup:                ~25 minutes ($0.18)

8. Process 39 chunks:          ~4.5 hours ($1.98)
9. Download results:           5 minutes ($0.04)
10. Terminate instance:        1 minute
   ─────────────────────────────────────
   Total project:              ~5.1 hours ($2.24)
```

**With buffer for issues:** ~7 hours = $3.08

## Advanced Cost Optimization

### Tip 1: Use Spot Instances (30-50% cheaper)

**Spot pricing:**
- RTX 4090 spot: ~$0.25-0.35/hour (vs $0.44 regular)
- **Risk:** Can be interrupted if someone bids higher
- **Mitigation:** Save progress frequently

**For your project:**
- Spot price: 5 hours × $0.30 = $1.50 (vs $2.20)
- **Savings:** ~$0.70 (32% cheaper)
- **Risk:** Low for 5-hour job (interruptions rare)

### Tip 2: Process During Off-Peak Hours

**Peak hours (expensive/busy):** 9 AM - 6 PM US Eastern
**Off-peak (cheaper/available):** 10 PM - 8 AM US Eastern

- Better availability
- Sometimes 10-15% cheaper
- Faster to deploy

### Tip 3: Batch Everything in One Session

**Don't do:**
- Session 1: Test (1 hour) = $0.44
- Session 2: Process 20 chunks (3 hours) = $1.32
- Session 3: Process 19 chunks (3 hours) = $1.32
- **Total:** $3.08 + overhead from restarts

**Do:**
- Session 1: Test + all 39 chunks (5 hours) = $2.20
- **Savings:** ~$0.88 + time saved on setup

### Tip 4: Use Pre-built Templates

RunPod has community templates with PyTorch/transformers pre-installed:
- Saves 5-10 minutes setup
- Saves ~$0.07 in GPU time
- Less room for error

## Budget Scenarios

### Scenario A: Everything Works Perfectly

```
RTX 4090 spot instance:    4.5 hours × $0.30 = $1.35
Storage/network:           $0.03
Total:                     $1.38
```

**Probability:** 40% (if you follow guide carefully)

### Scenario B: Normal Execution (Expected)

```
RTX 4090 regular instance: 5.5 hours × $0.44 = $2.42
Storage/network:           $0.05
One retry (1 chunk):       $0.10
Total:                     $2.57
```

**Probability:** 50% (most likely outcome)

### Scenario C: Learning Curve / Issues

```
RTX 4090 regular instance: 7 hours × $0.44 = $3.08
Storage/network:           $0.05
Multiple retries:          $0.50
Debugging time:            $0.40
Total:                     $4.03
```

**Probability:** 10% (if first time using RunPod)

## Final Recommendation

**For your 468-page Ukrainian book translation:**

### Best Choice: RunPod RTX 4090

**Budget:** $5 deposit ($3-4 expected usage)
**Time:** 5-7 hours GPU time, done in 1 day
**Quality:** Full BF16 precision (best possible)
**Effort:** Low (set up and let it run)

### When to Choose Alternatives:

- **$0 budget:** Kaggle free (but plan for 1-2 weeks)
- **Want easiest:** Claude API ($10-15, no setup)
- **Testing only:** Colab free (1-2 chunks to evaluate)

### Expected Total Cost Summary

```
Minimum deposit:           $10.00
Expected usage:            $3.00-4.00
Remaining credits:         $6.00-7.00 (kept)

Effective cost:            $3.00-4.00
Cost per page:             $0.0064-0.0085
Cost per word:             ~$0.000020

Time to completion:        1 day
Your time investment:      ~1 hour (setup + monitoring)
```

**Bottom line:** For $3-4 and 1 hour of your time, you get professional-quality Ukrainian→English translation using the best specialized model available.

---

**Created:** 2025-11-16
**For project:** spastics-dance Ukrainian book translation
**Platform:** RunPod.io GPU rental
**Recommended GPU:** RTX 4090 (24GB) at $0.44/hour
