"""
Vedic Sutra 3: Nyaya Sutras — 5-Step Pramana Inference Engine.
Vedic Sutra 13: Natya Shastra — Rasa (emotional manipulation) detection.
"""
import re


class NyayaPhishingInterceptor:
    """Sutra 3: Nyaya Sutras — Phishing Detection via Pramana."""

    RASAS = {
        "Bhayanaka": [r"block",r"suspend",r"legal.action",r"arrest",
                      r"unauthori[zs]ed",r"kyc.{0,10}expir",r"case.filed"],
        "Shringara":  [r"\bwon\b",r"prize",r"reward",r"cashback",
                       r"lottery",r"gift",r"lucky"],
        "Vira":       [r"immediately",r"within.{0,5}24",r"act.now",
                       r"expir",r"urgent",r"deadline"],
        "Adbhuta":    [r"congratulation",r"selected",r"exclusively",r"chosen"],
    }
    AUTHORITIES = ["sbi","hdfc","icici","paytm","phonepe","google",
                   "amazon","flipkart","irctc","uidai","income.tax",
                   "rbi","lic","npci","microsoft","apple","paypal"]
    SENSITIVE   = [r"\botp\b",r"password",r"\bpin\b",r"\bcvv\b",
                   r"card.number",r"account.number",r"aadhaar",r"pan.card",
                   r"click.{0,10}link",r"download",r"install"]

    def __init__(self, ledger):
        self.ledger   = ledger
        self._rr = {r:[re.compile(p,re.I) for p in ps]
                    for r,ps in self.RASAS.items()}
        self._ar = [re.compile(a,re.I) for a in self.AUTHORITIES]
        self._sr = [re.compile(p,re.I) for p in self.SENSITIVE]
        print("🔱 NYAYA ONLINE — 5-Step Pramana Ready")

    def analyze(self, text, msg_id="unknown"):
        t = text.lower()
        rasa,hits = "None",[]
        for r,pats in self._rr.items():
            h = [p.pattern for p in pats if p.search(t)]
            if h: rasa,hits = r,h; break

        auth = next((p.search(t).group() for p in self._ar
                     if p.search(t)), "")
        sens = [p.pattern for p in self._sr if p.search(t)]

        p1 = bool(re.search(r"verify|update|confirm|click|call|pay|send",t,re.I))
        p2 = rasa != "None"
        p3 = bool(auth)
        p4 = bool(sens)
        score = round(min(0.10*p1+0.25*p2+0.20*p3+0.30*p4+0.15*(p1&p2&p3&p4),1.0),4)

        verdict = "PHISHING" if score>0.5 else "SUSPICIOUS" if score>0.3 else "LEGITIMATE"
        sev     = {"PHISHING":"TURIYA","SUSPICIOUS":"RAJAS","LEGITIMATE":"TAMAS"}[verdict]
        result  = {"msg_id":msg_id,"score":score,"verdict":verdict,
                   "rasa":rasa,"authority":auth,"sensitive":sens}
        self.ledger.add_entry("Nyaya","Phishing Analysis",sev,result)
        icon = "🔴" if verdict=="PHISHING" else "🟡" if verdict=="SUSPICIOUS" else "🟢"
        print(f"""
════════════════════════════════════
🔱 NYAYA — PHISHING ANALYSIS
════════════════════════════════════
ID      : {msg_id}
Score   : {score:.4f}  {icon} {verdict}
Rasa    : {rasa}
Auth    : {auth or "None"}
Sens    : {sens}
Pramana : P1={p1} P2={p2} P3={p3} P4={p4}
════════════════════════════════════""")
        return result
