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
