# KAVACH Benchmarks — Methodology & Honest Numbers

## Test Environment
- **Hardware:** ARM64 (8 cores), 4GB RAM, Ubuntu 24.04
- **Compiler:** GCC 13.2, `-O3 -march=native -flto`
- **Test:** 8 threads, 10-second duration, 15 payload types

## What We Measure
The benchmark measures **in-memory keyword lookup throughput** — how fast KAVACH's hash-indexed engine can scan payloads against a rule index. This is the core detection loop, isolated for benchmarking.

## What We DON'T Measure (Yet)
- Packet capture overhead (libpcap/DPDK)
- Network I/O latency
- Disk I/O for logging
- Real traffic with diverse payload sizes
- Production context switching

## Honest Comparison

| System | Measurement Type | Throughput |
|--------|-----------------|:----------:|
| KAVACH v3.2 | In-memory keyword lookup | 9.2M/sec |
| KAVACH v3.2 | Python API (estimated) | 90K/sec |
| Snort 3 | On-wire packet inspection | 1-5M/sec |
| Suricata | On-wire packet inspection | 5-10M/sec |

**KAVACH's 9.2M/sec is NOT directly comparable to Snort's on-wire numbers.** It demonstrates that KAVACH's detection core will not be the bottleneck when packet capture is added. With DPDK integration (roadmap), we project 5-8M/sec on-wire throughput.

## Rule Count Honesty
- **150,000 total keyword-rule pairs** (50K rules × ~3 keywords each)
- **Unique keywords in index:** ~65 (generated rules use overlapping vocabulary)
- **Curated threat intel keywords:** 10 (from public feeds)
- **This is a stress test of the engine, not a claim of 150K unique threat signatures**

## What Matters
The key finding: KAVACH's hash-indexed architecture shows **no performance degradation** when scaling from 10 to 50,000 rules. This proves the O(1) lookup design works for production-scale rule sets.

## Nyaya Phishing Detection — Real-World Test

**Test Date:** May 2026  
**Samples:** 6 real Indian phishing SMS + 6 benign messages  
**Methodology:** NyayaPhishingInterceptor.analyze() on raw text

| Metric | Score |
|--------|:-----:|
| Detection Rate | 3/6 (50%) |
| False Positives | 0/6 (0%) |
| Precision | 100% |
| Recall | 50% |

### Known Gaps (Documented)
- P4 (sensitive data) fires alone on Aadhaar/PAN without enough weight to reach PHISHING threshold (>0.5)
- Suspicious TLDs (.tk, .ml, .xyz) not detected
- Urgency patterns without authority match score too low

### Next: Nyaya v1.1 with P5 (URL reputation) and adjusted scoring weights

## Updated: 29-Sample Test (May 2026)

| Metric | Score |
|--------|:-----:|
| Samples | 19 scam + 10 benign |
| Detection Rate | 3/19 (15.8%) |
| False Positives | 0/10 (0%) |
| Precision | 100% |

### Root Cause
The 4 Rasa patterns (Bhayanaka, Shringara, Vira, Adbhuta) cover only ~20 emotional keywords. Most Indian scam SMS use urgency without fear, reward without romance — patterns that don't match the current Rasa dictionary.

### Next Step
Expand Rasa patterns with India-specific scam language collected from public sources.

## XAI Framework: Explainable Detection Lineage

Every KAVACH detection is traceable through three stages:

### 1. Pratyaksha (Observation) — E
The set of evidence tokens extracted from raw data:
- Suspicious TLDs (`.tk`, `.ml`, `.xyz`)
- Authority keywords ("SBI", "APDCL", "PM Kisan")
- Urgency patterns ("blocked", "within 24 hours")
- Hinglish transliterations ("band ho jayega")

### 2. Anumana (Inference) — A
The vector of individual module scores:
```

A = [score_nyaya, score_charaka, score_gandharva, score_dharma]

```
Each module independently scores the evidence. No module trusts another.

### 3. Sabda (Consensus) — S
The Sushruta consensus engine evaluates:
```

if score_gandharva = 1.0 → TURIYA (immediate)
elif count(A_i ≥ 0.85) ≥ 2 → TURIYA (multi-module consensus)
elif max(A) ≥ 0.60 → SUSHUPTI
elif max(A) ≥ 0.30 → SVAPNA
else → JAGRAT

```

### Traceability Guarantee
Every TURIYA escalation has a documented lineage:
- **Which evidence tokens triggered?** (Pratyaksha log)
- **Which modules scored high?** (Anumana vector)
- **Was it single-module certainty or multi-module consensus?** (Sabda decision)

This ensures KAVACH is **deterministic, auditable, and defensible** — 
unlike black-box ML systems that cannot explain their decisions.
