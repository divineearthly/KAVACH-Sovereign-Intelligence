# KAVACH Privacy & Data Protection

## DPDPA Compliance (Digital Personal Data Protection Act 2023)

KAVACH is designed for **zero-cloud, on-device** operation.

### Data That NEVER Leaves Your Device
- SMS messages, emails, and packet payloads
- Aadhaar numbers, PAN cards, phone numbers
- Bank account details, UPI IDs
- Voice samples (Gandharva module)

### How Detection Works
1. All text processing happens in **volatile memory (RAM)**
2. Sensitive identifiers are matched via regex patterns — never stored
3. Detection results are returned immediately
4. No data is transmitted to any external server
5. No analytics, no telemetry, no cloud sync

### Akasha Ledger (Forensic Logging)
The immutable SHA-256 ledger records only:
- Module name (e.g., "nyaya")
- Event type (e.g., "phishing_detected")
- Severity score
- Timestamp

**Sensitive data is REDACTED before logging.** Aadhaar numbers, PAN cards, 
and phone numbers are replaced with `[REDACTED]` markers.

### Third-Party Dependencies
- No cloud APIs
- No external threat intelligence services that receive your data
- All detection patterns are locally stored
- Threat feed updates are pulled (not pushed) — your data never leaves

### Your Rights Under DPDPA
- Right to access: All data is on your device
- Right to erasure: Delete `akasha_ledger.json`
- Right to portability: MIT license — take the code anywhere
- Right to know: Every detection decision is explainable via Nyaya Pramana logic

### Privacy Guarantee
**KAVACH processes your most sensitive data without ever seeing it. 
The engine runs on your device. The patterns match in your RAM. 
Nothing leaves. Nothing is stored. Nothing is shared.**

This is sovereign AI — security that protects you without surveilling you.
