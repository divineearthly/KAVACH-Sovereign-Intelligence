"""Akasha Module — Sutra 45: Immutable Blockchain Forensic Ledger"""
import json, hashlib
from datetime import datetime
from collections import Counter

class AkashaLedger:
    def __init__(self, ledger_path="akasha_ledger.json"):
        self.ledger_path = ledger_path
        self.chain = []
        self._load()

    def _load(self):
        try:
            with open(self.ledger_path) as f:
                self.chain = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.chain = [{
                "block_id": 0,
                "timestamp": datetime.utcnow().isoformat(),
                "module_name": "genesis",
                "event_type": "genesis",
                "severity": 0,
                "event_details": "Akasha Genesis Block",
                "data_hash": "0" * 64,
                "previous_hash": "0" * 64,
                "current_hash": self._hash({"block_id": 0})
            }]
            self._save()

    def _hash(self, data):
        return hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()

    def _save(self):
        with open(self.ledger_path, 'w') as f:
            json.dump(self.chain, f, indent=2, default=str)

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
        return b["current_hash"]

    def record(self, event_type: str, data: dict, module: str) -> str:
        """Alias for add_entry — for API compatibility."""
        return self.add_entry(module, event_type, data.get("severity", 5), str(data))

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i]["previous_hash"] != self.chain[i-1]["current_hash"]:
                return False
        return True

    def stats(self):
        return {
            "total_blocks": len(self.chain),
            "by_module": dict(Counter(b["module_name"] for b in self.chain)),
            "by_severity": dict(Counter(b["severity"] for b in self.chain)),
            "integrity": "INTACT" if self.verify_chain() else "COMPROMISED"
        }
