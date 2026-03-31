"""
Vedic Sutra 19: Sushruta Samhita — Surgical Precision Response.
Mandukya 4 states (Sutra 25) map to 4 response levels.
Astras (Sutra 48) are dormant routines that activate on triggers.
"""
import uuid
from datetime import datetime


class SushrutaIncidentResponse:
    """Sutra 19: Sushruta Samhita — Autonomous Incident Response."""

    def __init__(self, ledger):
        self.ledger    = ledger
        self.incidents = []
        print("🔱 SUSHRUTA ONLINE — Surgical Response Ready")

    def _state(self, score):
        if score < 0.30: return "JAGRAT"
        if score < 0.60: return "SVAPNA"
        if score < 0.85: return "SUSHUPTI"
        return "TURIYA"

    def _astras(self, result, score):
        fired = []
        if score >= 0.85:
            fired.append("Brahmastra→FULL_LOCKDOWN")
        elif score >= 0.60:
            fired.append("Narayanastra→ISOLATE_SESSION")
        if result.get("rasa") == "Bhayanaka":
            fired.append("Agneyastra→BLOCK_URLS")
        if result.get("prediction") == "SYNTHETIC":
            fired.append("Varunastra→TERMINATE_CALL")
        return fired

    def _actions(self, state):
        return {
            "JAGRAT":   ["LOG_ONLY"],
            "SVAPNA":   ["ALERT_USER","INCREASE_MONITORING"],
            "SUSHUPTI": ["BLOCK_ACTION","QUARANTINE","PRESERVE_EVIDENCE"],
            "TURIYA":   ["FULL_LOCKDOWN","HUMAN_ESCALATION",
                         "PRESERVE_EVIDENCE","GENERATE_REPORT"],
        }[state]

    def respond(self, detection, source):
        score = float(detection.get("score") or
                      detection.get("threat_score") or
                      detection.get("confidence") or 0.0)
        state   = self._state(score)
        astras  = self._astras(detection, score)
        actions = self._actions(state)
        inc = {"incident_id": str(uuid.uuid4())[:8],
               "timestamp":   datetime.utcnow().isoformat(),
               "source":      source, "score": round(score,4),
               "state":       state,  "astras": astras,
               "actions":     actions,"escalate": state=="TURIYA"}
        self.incidents.append(inc)
        self.ledger.add_entry("Sushruta","Incident Response",state,inc)
        icon = "🚨" if state=="TURIYA" else "⚠️" if state in ("SUSHUPTI","SVAPNA") else "✅"
        print(f"""
════════════════════════════════════
🔱 SUSHRUTA — INCIDENT RESPONSE
════════════════════════════════════
ID      : {inc["incident_id"]}
Source  : {source}
Score   : {score:.4f}
State   : {icon} {state}
Astras  : {astras or "None"}
Actions : {actions}
Escalate: {"🚨 YES" if inc["escalate"] else "No"}
════════════════════════════════════"""
)
        return inc

    def forensic_report(self, path="kavach_forensic_report.txt"):
        lines = ["="*50, "🔱 KAVACH FORENSIC REPORT",
                 f"Generated: {datetime.utcnow().isoformat()}",
                 f"Total Incidents: {len(self.incidents)}", "="*50]
        for i in self.incidents:
            lines += [f"\nIncident : {i['incident_id']}",
                      f"Time     : {i['timestamp']}",
                      f"Source   : {i['source']}",
                      f"Score    : {i['score']}",
                      f"State    : {i['state']}",
                      f"Astras   : {i['astras']}",
                      f"Actions  : {i['actions']}", "-"*40]
        report = "\n".join(lines)
        with open(path,"w") as f:
            f.write(report)
        print(f"📋 Report → {path}")
        return report
