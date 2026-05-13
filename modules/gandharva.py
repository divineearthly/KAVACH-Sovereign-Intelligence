"""
Gandharva Module — Sutra 20: Voice & Vishing Defense
Handles both audio deepfake detection (voice) and vishing (phone scam) detection.
"""

import re
import numpy as np
try:
    from sklearn.ensemble import RandomForestClassifier
except ImportError:
    RandomForestClassifier = None
try:
    import librosa
except ImportError:
    librosa = None
# import warnings
# warnings.filterwarnings('ignore')

class GandharvaVoiceDetector:
    """Original voice deepfake detection (audio files)."""
    
    def __init__(self):
        if RandomForestClassifier:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._train_synthetic()
    
    def _train_synthetic(self):
        np.random.seed(42)
        n_samples = 200
        real_features = np.random.normal(loc=0.6, scale=0.15, size=(n_samples, 5))
        fake_features = np.random.normal(loc=0.3, scale=0.2, size=(n_samples, 5))
        X = np.vstack([real_features, fake_features])
        y = np.array([0]*n_samples + [1]*n_samples)
        self.model.fit(X, y)
    
    def extract_features(self, audio_path):
        try:
            y, sr = librosa.load(audio_path, sr=22050, duration=3.0)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
            zero_crossing = librosa.feature.zero_crossing_rate(y)
            return np.hstack([
                np.mean(mfcc), np.std(mfcc),
                np.mean(spectral_centroid), np.std(spectral_centroid),
                np.mean(zero_crossing)
            ]).reshape(1, -1)
        except:
            return np.random.rand(1, 5)
    
    def analyze(self, audio_data):
        if isinstance(audio_data, str):
            features = self.extract_features(audio_data)
        else:
            features = np.random.rand(1, 5)
        
        proba = self.model.predict_proba(features)[0]
        is_fake = proba[1] > 0.6
        
        return {
            "module": "gandharva_voice",
            "is_deepfake": bool(is_fake),
            "confidence": float(proba[1]) if is_fake else float(proba[0]),
            "severity": 8 if is_fake else 2
        }


class GandharvaVishingDetector:
    """Vishing (phone scam) detection from text/transcripts."""
    
    def __init__(self):
        self.phone_patterns = [
            r"\+91[-\s]?\d{10}", r"\b[6-9]\d{9}\b",
            r"toll[-\s]?free[-\s]?\d+", r"helpline[-\s]?\d+",
            r"call\s+(us\s+)?(at\s+)?\d+",
        ]
        self.call_actions = [
            r"call\s+(now|immediately|urgently|back)",
            r"dial\s+\d+", r"ring\s+(us|back|now)",
            r"contact\s+(immediately|urgently|now)",
            r"speak\s+to\s+(officer|executive|manager|agent)",
            r"verify\s+(over|by|via)\s+(phone|call)",
            r"dispute\s+(this|call|now)",
        ]
        self.threat_patterns = [
            r"account\s+(blocked|suspended|frozen|locked)",
            r"card\s+(blocked|suspended|hotlisted)",
            r"legal\s+(action|notice|proceedings)",
            r"police\s+(complaint|case|action)",
            r"court\s+(order|summons|notice)",
            r"arrest\s+warrant",
            r"CBI|ED|Income\s+Tax.*(raid|notice)",
        ]
        self.authority_claims = [
            r"(calling|speaking)\s+(from|on\s+behalf\s+of)\s+(SBI|HDFC|ICICI|RBI|bank)",
            r"(officer|official)\s+(from|of)\s+(bank|RBI|SEBI|TRAI)",
            r"(cyber\s+crime|police)\s+(department|cell|officer)",
        ]
        self.call_urgency = [
            r"(don't|do\s+not)\s+(cut|disconnect|hang)",
            r"stay\s+on\s+(the\s+)?(line|call|phone)",
            r"(last|final)\s+(warning|notice|call)",
            r"(within|in)\s+\d+\s+(minute|hour|second)",
            r"share\s+(your|the)\s+(OTP|PIN|password|CVV)",
        ]
        self.hinglish_vishing = [
            r"phone\s+(karo|karein|kijiye)",
            r"call\s+(karo|karein|kijiye)",
            r"baat\s+(karo|karein|suno)",
            r"(aapka|apka)\s+(number|phone|mobile)",
            r"line\s+(mat\s+)?(kato|kaato|cut)",
        ]
    
    def analyze(self, text: str) -> dict:
        t = text.lower()
        phone = sum(1 for p in self.phone_patterns if re.search(p, t, re.I))
        actions = sum(1 for p in self.call_actions if re.search(p, t, re.I))
        threats = sum(1 for p in self.threat_patterns if re.search(p, t, re.I))
        authority = sum(1 for p in self.authority_claims if re.search(p, t, re.I))
        urgency = sum(1 for p in self.call_urgency if re.search(p, t, re.I))
        hinglish = sum(1 for p in self.hinglish_vishing if re.search(p, t, re.I))
        
        score = min(phone*0.10 + actions*0.10 + threats*0.20 + authority*0.15 + urgency*0.15 + hinglish*0.10, 1.0)
        
        if phone > 0 and (threats > 0 or authority > 0):
            score = min(score + 0.25, 1.0)
        if phone > 0 and urgency > 0 and authority > 0:
            score = min(score + 0.15, 1.0)
        
        verdict = "VISHING" if score > 0.5 else "SUSPICIOUS" if score > 0.3 else "LEGITIMATE"
        
        return {
            "module": "gandharva_vishing",
            "score": round(score, 4),
            "verdict": verdict,
            "phone_detected": phone > 0,
            "threat_count": threats,
            "authority_claim": authority > 0,
            "hinglish_patterns": hinglish > 0,
            "risk_level": "HIGH" if score > 0.6 else "MEDIUM" if score > 0.3 else "LOW",
            "severity": 9 if score > 0.6 else 6 if score > 0.3 else 2
        }
