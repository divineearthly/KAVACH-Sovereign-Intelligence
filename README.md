# 🔱 KAVACH: Sovereign Cyber Defense Intelligence

<div align="center">

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/divineearthly/KAVACH-Sovereign-Intelligence/blob/main/KAVACH_Complete.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![C++ Engine](https://img.shields.io/badge/C++-2.2M%20events%2Fsec-green.svg)](cpp-engine/)
[![Detection](https://img.shields.io/badge/Detection-73.7%25-blue.svg)](BENCHMARKS.md)
[![False Positives](https://img.shields.io/badge/False%20Positives-0%25-brightgreen.svg)](BENCHMARKS.md)
[![Privacy](https://img.shields.io/badge/Privacy-DPDPA%20Compliant-purple.svg)](PRIVACY.md)

**2.2M events/sec on ARM64 · 73.7% detection · 0% false positives · Zero-cloud · On-device**

</div>

---

## ⚡ Why KAVACH?

| Question | Answer |
|----------|--------|
| **What is it?** | Sovereign cyber defense mapping 64 Vedic Sutras to modern AI |
| **How fast?** | 2.2M events/sec on ARM64 (Android/Termux) |
| **How accurate?** | 73.7% phishing detection with 0% false positives |
| **Where does data go?** | Nowhere. All detection is on-device. Zero cloud. |
| **What makes it unique?** | Explainable Nyaya logic instead of black-box ML |
| **Who is it for?** | India's 1.4 billion. Runs on ₹8,000 phones. |

---

## 🛡️ The Vedic AI Architecture

| Module | Vedic Sutra | Real Function |
|--------|-------------|---------------|
| **CHARAKA** | Sutra 14 | Anomaly detection via Vata/Pitta/Kapha dosha classification |
| **NYAYA** | Sutra 3 | Phishing detection via 7-Pramana logical inference |
| **GANDHARVA** | Sutra 20 | Voice deepfake detection via harmonic fingerprinting |
| **AKASHA** | Sutra 45 | SHA-256 immutable forensic ledger |
| **SUSHRUTA** | Sutra 19 | Autonomous incident response (4 Mandukya states) |
| **DHARMA** | Sutra 30 | Shadow AI monitoring (5-layer Pancha Kosha analysis) |
| **SARATHI** | Sutra 39 | Unified orchestrator |

### The Nyaya Pramana Scoring System

KAVACH doesn't use black-box ML. Every detection decision is explainable 
through 7 Pramanas (proofs):

| Pramana | Type | Weight | What It Detects |
|---------|------|:------:|-----------------|
| P₁ | Action/Urgency | 0.10 | "verify", "update", "click", "pay" |
| P₂ | Emotional Rasa | 0.25 | Fear, urgency, attraction, greed |
| P₃ | Authority Claim | 0.20 | "SBI", "HDFC", "PM Kisan", "APDCL" |
| P₄ | Sensitive Data | 0.30 | Aadhaar, PAN, KYC, OTP, passwords |
| P₅ | Suspicious URL | 0.15 | .tk, .ml, .xyz, .cc domains |
| P₆ | Temporal Urgency | 0.05 | "within 24 hours", "by tonight" |
| P₇ | Call-to-Action | 0.10 | Phone numbers + "call/dispute" |

---

## ⚡ Performance

| Metric | Value | Environment |
|--------|:-----:|-------------|
| **Detection Rate** | 73.7% | 19 Indian scam SMS samples |
| **False Positives** | 0% | 10 benign SMS samples |
| **C++ Throughput** | 2.2M events/sec | ARM64, 8 threads, Aho-Corasick |
| **Python Throughput** | 90K/sec | Single-threaded reference |
| **Patterns** | 124 | P1-P7 + Hinglish transliteration |
| **Rule Index** | 150K | Hash-indexed keyword engine |

📖 Full methodology: [BENCHMARKS.md](BENCHMARKS.md)

---

## 🔒 Privacy by Design

KAVACH is **DPDPA-compliant** by architecture:

- ✅ All detection on-device — zero cloud
- ✅ Sensitive data (Aadhaar/PAN/OTP) processed in volatile RAM only
- ✅ Redacted in forensic logs
- ✅ No analytics, no telemetry, no external APIs
- ✅ MIT licensed — audit everything

📖 Full privacy policy: [PRIVACY.md](PRIVACY.md)

---

## 🚀 Quick Start

### One-Click: Google Colab
Click the **Open in Colab** badge at top. No installation.

### Termux (Android)
```bash
pkg install python git
git clone https://github.com/divineearthly/KAVACH-Sovereign-Intelligence.git
cd KAVACH-Sovereign-Intelligence
pip install -r requirements.txt
python kavach_main.py
```

C++ Engine (2.2M events/sec)

```bash
cd cpp-engine && mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release && make -j$(nproc)
./kavach
```

---

🏗️ Architecture

```
KAVACH/
├── modules/              # Python defense modules
│   ├── charaka.py        # Anomaly detection
│   ├── nyaya.py          # Logic firewall (7-Pramana)
│   ├── gandharva.py      # Voice analysis
│   ├── akasha.py         # Immutable ledger
│   ├── sushruta.py       # Incident response
│   └── dharma.py         # Shadow AI monitor
├── cpp-engine/           # C++ high-performance engine
│   ├── include/kavach/   # Aho-Corasick, Sutra constants
│   ├── src/              # Detection pipeline
│   └── rules/            # 150K threat signatures
├── tests/                # Real-world phishing tests
├── api.py                # FastAPI REST integration
└── kavach_main.py        # SARATHI orchestrator
```

---

🌐 Live Ecosystem

Service Description
⚖️ Nyaya Lens API Vedic logical reasoning engine
🌾 Krishi-Veda Vedic agricultural AI
🤖 @NyayaLensBot Telegram bot
🧮 Vedic Math CNN Sutra-based CNN

---

🎯 Roadmap

Phase Milestone Status
1 Python modules (6/6) ✅
2 C++ Aho-Corasick pipeline ✅
3 124 Pramana patterns + Hinglish ✅
4 MITRE ATT&CK mapping 📋
5 OpenSSF Best Practices badge 📋
6 IndiaAI Mission application 📋

---

📜 License

MIT © 2026 divineearthly

🕉️ सत्यमेव जयते — Truth Alone Triumphs 🔱

Built solo in Silchar, Assam · Android/Termux · Zero budget · Sovereign AI
