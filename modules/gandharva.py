"""
Vedic Sutra 20: Gandharva Veda — Harmonic & DSP Analysis.
Real voices have micro-variations AI clones cannot replicate.
"""
import numpy as np
import librosa
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class GandharvaVoiceDetector:
    """Sutra 20: Gandharva Veda — Voice Deepfake Detector."""

    def __init__(self, ledger, sr=22050):
        self.ledger = ledger
        self.sr     = sr
        self.scaler = StandardScaler()
        self.model  = RandomForestClassifier(n_estimators=200,
                                              random_state=42)
        rng = np.random.RandomState(42)
        n   = 200

        def _samples(synthetic):
            j = rng.normal(0.01 if synthetic else 0.05, 0.005, n)
            m = rng.normal(0.20 if synthetic else 0.80, 0.08,  n)
            t = rng.normal(0.15 if synthetic else 0.60, 0.08,  n)
            c = rng.normal(1800 if synthetic else 2000, 80,    n)
            r = rng.normal(3500 if synthetic else 4000, 150,   n)
            z = rng.normal(0.04 if synthetic else 0.08, 0.008, n)
            return np.column_stack([j,m,t,c,r,z])

        X = np.vstack([_samples(False), _samples(True)])
        y = np.array([0]*n + [1]*n)
        self.scaler.fit(X)
        self.model.fit(self.scaler.transform(X), y)
        print("🔱 GANDHARVA ONLINE — Harmonic classifier trained")

    def _features(self, path):
        y, sr = librosa.load(path, sr=self.sr, mono=True)
        mfcc  = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        try:
            f0     = librosa.yin(y, fmin=50, fmax=500, sr=sr)
            jitter = float(np.std(f0[f0>0])) if np.any(f0>0) else 0.01
        except Exception:
            jitter = 0.01
        return np.array([[
            jitter,
            float(np.std(mfcc)),
            float(np.std(librosa.feature.tonnetz(y=y, sr=sr))),
            float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))),
            float(np.mean(librosa.feature.spectral_rolloff(y=y,  sr=sr))),
            float(np.mean(librosa.feature.zero_crossing_rate(y))),
        ]])

    def analyze(self, path, audio_id="unknown"):
        feats  = self._features(path)
        pred   = self.model.predict(self.scaler.transform(feats))[0]
        proba  = self.model.predict_proba(self.scaler.transform(feats))[0]
        label  = "SYNTHETIC" if pred==1 else "REAL"
        conf   = float(max(proba))
        sev    = ("TURIYA" if label=="SYNTHETIC" and conf>0.8 else
                  "RAJAS"  if label=="SYNTHETIC" else "TAMAS")
        result = {"audio_id":audio_id,"prediction":label,
                  "confidence":round(conf,4),"severity":sev}
        self.ledger.add_entry("Gandharva","Voice Analysis",sev,result)
        icon = "🔴" if label=="SYNTHETIC" else "🟢"
        print(f"""
════════════════════════════════════
🔱 GANDHARVA — VOICE ANALYSIS
════════════════════════════════════
File       : {audio_id}
Prediction : {icon} {label}
Confidence : {conf:.4f}
Severity   : {sev}
════════════════════════════════════""")
        return result
