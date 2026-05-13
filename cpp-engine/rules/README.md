# KAVACH Threat Rules

## Rule Sources
- **50,000 generated rules** — Auto-generated for stress-testing the hash index engine. These are random keyword-severity combinations designed for benchmarking throughput, not production detection accuracy.
- **Real threat intelligence** — Curated from AlienVault OTX, Emerging Threats, MalwareBazaar.

## Important Note
The generated rules (nyaya_50k_rules.txt) are **benchmarking tools**, not curated threat signatures. They demonstrate that KAVACH's hash-indexed engine can handle 50K+ rules at 9M+ events/sec without performance degradation. Production deployment should use curated rules from `threat_intel_keywords.txt` or custom rule sets.

## Rule Format
```

ID|Name|Description|keyword1,keyword2,keyword3|Severity(1-10)|Block(0/1)

```
