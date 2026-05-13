"""
Gandharva Vishing Module — Sutra 20: Voice/Call Scam Detection
Detects phone-based scams without audio processing.
Uses text patterns from call transcripts/SMS to identify vishing attempts.
"""

import re

class GandharvaVishingDetector:
    """Detects vishing (voice phishing) patterns in text/transcripts."""
    
    def __init__(self):
        # Indian phone number patterns
        self.phone_patterns = [
            r"\+91[-\s]?\d{10}",           # +91XXXXXXXXXX
            r"\b[6-9]\d{9}\b",             # 10-digit Indian mobile
            r"\b0[6-9]\d{9}\b",            # 0XXXXXXXXXX
            r"\b\d{3}[-\s]\d{3}[-\s]\d{4}\b", # XXX-XXX-XXXX
            r"toll[-\s]?free[-\s]?\d+",    # Toll-free numbers
            r"helpline[-\s]?\d+",          # Helpline numbers
            r"call\s+(us\s+)?(at\s+)?\d+", # Call us at XXXXX
        ]
        
        # Vishing action verbs
        self.call_actions = [
            r"call\s+(now|immediately|urgently|today|back)",
            r"phone\s+(us|now|immediately)",
            r"dial\s+\d+",
            r"ring\s+(us|back|now)",
            r"contact\s+(immediately|urgently|now)",
            r"speak\s+to\s+(our\s+)?(officer|executive|manager|agent)",
            r"verify\s+(over|by|via)\s+(phone|call)",
            r"dispute\s+(this|call|now)",
            r"report\s+(this|immediately|now)",
        ]
        
        # Vishing threat patterns (what scammers say)
        self.threat_patterns = [
            r"account\s+(blocked|suspended|frozen|locked|deactivated)",
            r"card\s+(blocked|suspended|hotlisted)",
            r"legal\s+(action|notice|proceedings)",
            r"police\s+(complaint|case|action)",
            r"court\s+(order|summons|notice)",
            r"investigation\s+(pending|started|launched)",
            r"criminal\s+(case|charges|proceedings)",
            r"arrest\s+warrant",
            r"CBI|ED|Income\s+Tax.*(raid|notice|investigation)",
            r"RBI.*(guideline|circular|notice|restriction)",
        ]
        
        # Fake authority impersonation
        self.authority_claims = [
            r"(calling|speaking)\s+(from|on\s+behalf\s+of)\s+(SBI|HDFC|ICICI|RBI|bank)",
            r"(officer|official)\s+(from|of)\s+(bank|RBI|SEBI|IRDA|TRAI)",
            r"(government|govt)\s+(officer|official|department)",
            r"(cyber\s+crime|police)\s+(department|cell|officer)",
            r"(customer|support)\s+(officer|executive)\s+(calling|here)",
        ]
        
        # Urgency triggers specific to calls
        self.call_urgency = [
            r"(don't|do\s+not)\s+(cut|disconnect|hang)",
            r"stay\s+on\s+(the\s+)?(line|call|phone)",
            r"(last|final)\s+(warning|notice|call)",
            r"(within|in)\s+\d+\s+(minute|hour|second)",
            r"(immediately|urgently|right\s+now|instantly)",
            r"before\s+(we|your|the)\s+(block|suspend|close)",
            r"confirm\s+(your|the)\s+(identity|details|KYC)",
            r"share\s+(your|the)\s+(OTP|PIN|password|CVV)",
        ]
        
        # Hinglish vishing patterns
        self.hinglish_vishing = [
            r"phone\s+(karo|karein|kijiye)",
            r"call\s+(karo|karein|kijiye)",
            r"number\s+(do|bhejo|bhejein)",
            r"baat\s+(karo|karein|suno)",
            r"(aapka|apka)\s+(number|phone|mobile)",
            r"(humare|hamare)\s+(officer|agent|executive)",
            r"(aapko|apko)\s+(call|phone)\s+(karega|karenge)",
            r"line\s+(mat\s+)?(kato|kaato|cut)",
        ]
    
    def analyze(self, text: str) -> dict:
        """
        Analyze text/transcript for vishing indicators.
        Returns risk score and matched patterns.
        """
        t = text.lower()
        
        # Count matches per category
        phone_matches = sum(1 for p in self.phone_patterns if re.search(p, t, re.I))
        action_matches = sum(1 for p in self.call_actions if re.search(p, t, re.I))
        threat_matches = sum(1 for p in self.threat_patterns if re.search(p, t, re.I))
        authority_matches = sum(1 for p in self.authority_claims if re.search(p, t, re.I))
        urgency_matches = sum(1 for p in self.call_urgency if re.search(p, t, re.I))
        hinglish_matches = sum(1 for p in self.hinglish_vishing if re.search(p, t, re.I))
        
        # Weighted scoring
        score = (
            min(phone_matches * 0.10, 0.20) +
            min(action_matches * 0.15, 0.25) +
            min(threat_matches * 0.20, 0.30) +
            min(authority_matches * 0.15, 0.20) +
            min(urgency_matches * 0.15, 0.20) +
            min(hinglish_matches * 0.10, 0.15)
        )
        
        # Boost: phone number + threat = high risk
        if phone_matches > 0 and (threat_matches > 0 or authority_matches > 0):
            score = min(score + 0.25, 1.0)
        
        # Boost: phone + urgency + authority = almost certainly vishing
        if phone_matches > 0 and urgency_matches > 0 and authority_matches > 0:
            score = min(score + 0.15, 1.0)
        
        verdict = "VISHING" if score > 0.5 else "SUSPICIOUS" if score > 0.3 else "LEGITIMATE"
        
        return {
            "module": "gandharva_vishing",
            "score": round(score, 4),
            "verdict": verdict,
            "phone_detected": phone_matches > 0,
            "threat_count": threat_matches,
            "authority_claim": authority_matches > 0,
            "hinglish_patterns": hinglish_matches > 0,
            "risk_level": "HIGH" if score > 0.6 else "MEDIUM" if score > 0.3 else "LOW"
        }


# Test
if __name__ == "__main__":
    detector = GandharvaVishingDetector()
    
    test_samples = [
        # Vishing call transcript
        "Hello, I am calling from SBI customer care. Your account has been blocked due to KYC pending. Please share your OTP immediately. Call us at 9876543210. Don't disconnect this call.",
        
        # Fake police threat
        "This is Cyber Crime Department Mumbai. A criminal case has been registered against you. An arrest warrant is pending. Call 9830012345 immediately to resolve this.",
        
        # Bank impersonation
        "Speaking from HDFC Bank verification department. Your card has been hotlisted due to suspicious transaction. Stay on the line. Do not hang up. Confirm your CVV now.",
        
        # Hinglish vishing
        "Hello ji, main SBI se bol raha hoon. Aapka account block ho jayega. Abhi call karo 9876543210 pe. Apka number verify karna hai.",
        
        # Legitimate call
        "Hi, this is Rahul from your team. The meeting is rescheduled to 3pm. Please confirm your availability.",
        
        # Legitimate bank call
        "Hello, this is HDFC Bank calling about your recent credit card application. We need to verify your employment details. Please call our official number 1800-202-6161.",
    ]
    
    print("=" * 60)
    print("🔊 GANDHARVA VISHING MODULE — Test")
    print("=" * 60)
    
    for sample in test_samples:
        result = detector.analyze(sample)
        emoji = "🔴" if result["verdict"] == "VISHING" else "🟡" if result["verdict"] == "SUSPICIOUS" else "🟢"
        print(f"\n{emoji} {result['verdict']} (score: {result['score']:.2f})")
        print(f"   Phone: {result['phone_detected']} | Threats: {result['threat_count']} | Authority: {result['authority_claim']}")
        print(f"   Text: {sample[:80]}...")
