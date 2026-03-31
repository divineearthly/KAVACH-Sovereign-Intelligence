"""
Vedic Sutra 39: Indra's Net — All modules reflect each other.
SARATHI (the divine Charioteer) unifies all 6 modules.
"""
import json, os
from modules.akasha    import AkashaLedger
from modules.charaka   import CharakaAnomalyEngine
from modules.nyaya     import NyayaPhishingInterceptor
from modules.gandharva import GandharvaVoiceDetector
from modules.sushruta  import SushrutaIncidentResponse
from modules.dharma    import DharmaMonitor

BANNER = """
╔══════════════════════════════════════════════════╗
║   🔱  KAVACH — SOVEREIGN CYBER DEFENSE  🔱       ║
║      Divine Earthly Vedic Sutras Framework       ║
║   github.com/divineearthly/KAVACH               ║
╠══════════════════════════════════════════════════╣
║  AKASHA    ✅  Immutable Forensic Ledger         ║
║  CHARAKA   ✅  Behavioral Anomaly Engine         ║
║  NYAYA     ✅  Phishing Detector                 ║
║  GANDHARVA ✅  Voice Deepfake Analyzer           ║
║  SUSHRUTA  ✅  Autonomous Incident Response      ║
║  DHARMA    ✅  Shadow AI Monitor                 ║
╚══════════════════════════════════════════════════╝"""


class KAVACH:
    """SARATHI — KAVACH Unified Orchestrator."""

    def __init__(self):
        self.ledger    = AkashaLedger()
        self.charaka   = CharakaAnomalyEngine(self.ledger)
        self.nyaya     = NyayaPhishingInterceptor(self.ledger)
        self.gandharva = GandharvaVoiceDetector(self.ledger)
        self.sushruta  = SushrutaIncidentResponse(self.ledger)
        self.dharma    = DharmaMonitor(self.ledger)
        print(BANNER)

    def scan_behavior(self, behavior, user_id="anon"):
        r = self.charaka.analyze(behavior, user_id)
        self.sushruta.respond(r, "CHARAKA")
        return r

    def scan_text(self, text, msg_id="msg"):
        r = self.nyaya.analyze(text, msg_id)
        self.sushruta.respond(r, "NYAYA")
        return r

    def scan_audio(self, path, audio_id=None):
        r = self.gandharva.analyze(path, audio_id or path)
        self.sushruta.respond(r, "GANDHARVA")
        return r

    def scan_request(self, url, headers, payload, role="user"):
        r = self.dharma.analyze_request(url, headers, payload, role)
        self.sushruta.respond(r, "DHARMA")
        return r

    def demo(self):
        print("\n" + "="*52)
        print("🔱 KAVACH DEMO — Full System Test")
        print("="*52)

        self.scan_behavior({
            "user_id":"hacker_99","login_hour":3,"login_day":6,
            "country_code":1,"device_type":1,
            "data_accessed_mb":480,"failed_attempts":8,"new_ip":1
        }, "hacker_99")

        self.scan_text(
            "URGENT: Your SBI account is BLOCKED. Verify your OTP "
            "immediately or face legal action. Click: bit.ly/sbi-kyc",
            "phish_001"
        )

        wavs = [f for f in os.listdir(".") if f.endswith(".wav")]
        if wavs:
            self.scan_audio(wavs[0], wavs[0])

        self.scan_request(
            "https://freegpt.xyz/api/chat",
            {"User-Agent": "python-requests"},
            "My Aadhaar 1234 5678 9012, OTP is 834521",
            "employee"
        )

        print("\n" + "="*52)
        print("🔱 AKASHA LEDGER SUMMARY")
        print("="*52)
        print(json.dumps(self.ledger.summary(), indent=2))
        self.ledger.verify_chain()
        self.sushruta.forensic_report()
        self.ledger.export_evidence()
        print("\n✅ KAVACH DEMO COMPLETE — System is SOVEREIGN")


if __name__ == "__main__":
    kavach = KAVACH()
    kavach.demo()
