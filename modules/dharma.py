"""
Vedic Sutra 30: Dharma Shastras — Access Control & Governance.
Vedic Sutra 55: Pancha Kosha — 5 Detection Layers.
"""
import re, math


class DharmaMonitor:
    """Sutra 30: Dharma Shastras — Shadow AI Monitor (5 Koshas)."""

    DHARMIC  = ["api.anthropic.com","api.openai.com",
                "generativelanguage.googleapis.com",
                "api.cohere.com","huggingface.co","api.mistral.ai"]
    ADHARMIC = ["freegpt","jailbreak","ungated","leaked-gpt",
                "shadow-ai","nocensor","bypass-ai"]
    PII = {
        "aadhaar":     r"\b[2-9]\d{3}\s?\d{4}\s?\d{4}\b",
        "pan_card":    r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "phone_india": r"\b[6-9]\d{9}\b",
        "credit_card": r"\b(?:\d[ -]?){15,16}\b",
        "email":       r"\b[\w.+-]+@[\w-]+\.[a-z]{2,}\b",
        "otp":         r"\b\d{4,8}\b",
    }

    def __init__(self, ledger):
        self.ledger  = ledger
        self._pii    = {k: re.compile(v,re.I) for k,v in self.PII.items()}
        print("🔱 DHARMA ONLINE — 5 Kosha Layers Active")

    def _entropy(self, t):
        if not t: return 0.0
        freq = {}
        for c in t: freq[c] = freq.get(c,0)+1
        n = len(t)
        return -sum((v/n)*math.log2(v/n) for v in freq.values())

    def analyze_request(self, url, headers, payload, role="user"):
        domain = re.sub(r"https?://","",url).split("/")[0].lower()
        # L1 Annamaya — domain
        if   any(d in domain for d in self.DHARMIC):  l1 = "DHARMIC"
        elif any(d in domain for d in self.ADHARMIC): l1 = "ADHARMIC"
        else:                                          l1 = "UNKNOWN"
        # L2 Pranamaya — headers
        flags = []
        if not headers.get("Authorization"): flags.append("no_auth")
        if not headers.get("User-Agent"):    flags.append("no_ua")
        l2 = "SUSPICIOUS" if flags else "CLEAN"
        # L3 Manomaya — payload scan
        pii_found = [k for k,r in self._pii.items() if r.search(payload)]
        # L4 Vijnanamaya — classify
        fin = {"credit_card","otp"}
        idn = {"aadhaar","pan_card","phone_india","email"}
        if any(p in fin for p in pii_found) and any(p in idn for p in pii_found):
            l4 = "CRITICAL"
        elif pii_found: l4 = "HIGH"
        else:           l4 = "LOW"
        # L5 Anandamaya — entropy
        ent = self._entropy(payload)
        l5  = "HIGH_ENTROPY" if ent > 4.5 else "NORMAL"

        if l1=="ADHARMIC" or l4=="CRITICAL": verdict,sev = "ADHARMIC","TURIYA"
        elif l1=="UNKNOWN" or l4=="HIGH":    verdict,sev = "SUSPICIOUS","RAJAS"
        else:                                verdict,sev = "DHARMIC","TAMAS"

        result = {"url":url,"verdict":verdict,"domain_status":l1,
                  "header_flags":flags,"pii_found":pii_found,
                  "classification":l4,"entropy":round(ent,4)}
        self.ledger.add_entry("Dharma","Request Analysis",sev,result)
        icon = "🔴" if verdict=="ADHARMIC" else "🟡" if verdict=="SUSPICIOUS" else "🟢"
        print(f"""
════════════════════════════════════
🔱 DHARMA — REQUEST ANALYSIS
════════════════════════════════════
URL      : {url[:45]}
Verdict  : {icon} {verdict}
L1 Domain: {l1}
L2 Headers:{l2} {flags}
L3 PII   : {pii_found or "None"}
L4 Class : {l4}
L5 Entropy:{round(ent,4)} {l5}
════════════════════════════════════""")
        return result
