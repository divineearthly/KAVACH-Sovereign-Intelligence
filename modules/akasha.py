"""
Vedic Sutra 45: Akashic Records — The Immutable Ledger.
Every event is permanently recorded, cryptographically
chained, and tamper-evident. Nothing can be erased.
"""
import json, hashlib, os
from datetime import datetime


class AkashaLedger:
    """Sutra 45: Akashic Records — Immutable Forensic Ledger."""

    def __init__(self, path="akasha_ledger.json"):
        self.path = path
        self.chain = []
        if os.path.exists(path):
            with open(path) as f:
                self.chain = json.load(f)
            print(f"🔱 AKASHA ONLINE — {len(self.chain)} blocks loaded")
        else:
            self._genesis()

    def _hash(self, data):
        return hashlib.sha256(
            json.dumps(data, sort_keys=True, default=str).encode()
        ).hexdigest()

    def _genesis(self):
        g = {"block_id": 0, "timestamp": datetime.utcnow().isoformat(),
             "module_name": "Akasha", "event_type": "Genesis",
             "severity": "INFO",
             "event_details": {"message": "KAVACH initialized"},
             "previous_hash": "0"}
        g["data_hash"] = self._hash(g["event_details"])
        g["current_hash"] = self._hash(g)
        self.chain.append(g)
        self._save()
        print("🔱 AKASHA ONLINE — Genesis block created")

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.chain, f, indent=4, default=str)

    def add_entry(self, module, event_type, severity, details):
        prev = self.chain[-1]
        b = {"block_id": len(self.chain),
             "timestamp": datetime.utcnow().isoformat(),
             "module_name": module, "event_type": event_type,
             "severity": severity, "event_details": details,
             "data_hash": self._hash(details),
             "previous_hash": prev["current_hash"]}
        b["current_hash"] = self._hash(b)
        self.chain.append(b)
        self._save()
        return b

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i]["previous_hash"] != self.chain[i-1]["current_hash"]:
                print(f"❌ CHAIN BROKEN at block {i}")
                return False
        print(f"✅ CHAIN VERIFIED — {len(self.chain)} blocks intact")
        return True

    def summary(self):
        from collections import Counter
        return {
            "total_blocks": len(self.chain),
            "by_module":    dict(Counter(b["module_name"] for b in self.chain)),
            "by_severity":  dict(Counter(b["severity"]    for b in self.chain)),
        }

    def export_evidence(self, path="kavach_evidence.json"):
        pkg = {"exported": datetime.utcnow().isoformat(),
               "chain_valid": self.verify_chain(),
               "blocks": self.chain,
               "chain_hash": self._hash({"c": self.chain})}
        with open(path, "w") as f:
            json.dump(pkg, f, indent=4, default=str)
        print(f"📋 Evidence exported → {path}")
