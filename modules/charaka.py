"""
Vedic Sutra 14: Charaka Samhita — Anomaly Detection.
Three Doshas = three anomaly classes.
Three Gunas  = three threat states (Sutra 51).
"""
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


class CharakaAnomalyEngine:
    """Sutra 14: Charaka Samhita — Behavioral Anomaly Engine."""

    FEATURES = ["login_hour","login_day","country_code",
                "device_type","data_accessed_mb","failed_attempts","new_ip"]

    def __init__(self, ledger):
        self.ledger = ledger
        self.scaler = StandardScaler()
        self.model  = IsolationForest(contamination=0.1,
                                      n_estimators=100, random_state=42)
        rng = np.random.RandomState(42)
        n = 300
        X = np.column_stack([
            np.clip(rng.normal(10,2,n), 7, 20),
            rng.randint(0, 5, n),
            np.zeros(n),
            np.zeros(n),
            np.clip(rng.normal(50,15,n), 0, 200),
            np.clip(rng.poisson(0.3,n), 0, 3),
            rng.binomial(1, 0.05, n),
        ])
        self.scaler.fit(X)
        self.model.fit(self.scaler.transform(X))
        print("🔱 CHARAKA ONLINE — Baseline trained on 300 samples")

    def analyze(self, behavior, user_id="unknown"):
        x = np.array([[behavior.get(f,0) for f in self.FEATURES]])
        raw   = self.model.decision_function(self.scaler.transform(x))[0]
        score = float(np.clip(1-(raw+0.5), 0, 1))

        if score < 0.35:   guna = "TAMAS";   sev = "TAMAS"
        elif score < 0.70: guna = "RAJAS";   sev = "RAJAS"
        else:              guna = "SATTVA";  sev = "TURIYA"

        if behavior.get("login_hour",12)<6 or behavior.get("country_code",0)==1:
            dosha = "Vata"
        elif behavior.get("data_accessed_mb",0)>150 or behavior.get("failed_attempts",0)>3:
            dosha = "Pitta"
        elif behavior.get("new_ip",0)==1 and behavior.get("device_type",0)==1:
            dosha = "Kapha"
        else:
            dosha = "Balanced"

        result = {"user_id":user_id,"score":round(score,4),
                  "guna":guna,"dosha":dosha}
        self.ledger.add_entry("Charaka","Behavioral Analysis",sev,result)
        icon = "🔴" if score>=0.70 else "🟡" if score>=0.35 else "🟢"
        print(f"""
════════════════════════════════════
🔱 CHARAKA — BEHAVIORAL ANALYSIS
════════════════════════════════════
User  : {user_id}
Score : {score:.4f}
Guna  : {guna}  {icon}
Dosha : {dosha}
════════════════════════════════════""")
        return result
