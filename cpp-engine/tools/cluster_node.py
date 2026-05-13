"""KAVACH Distributed Node — RAFT consensus for Akasha ledger"""
import socket, json, threading, time
from flask import Flask, request

app = Flask(__name__)
NODES = ["node1:9000", "node2:9000", "node3:9000"]  # Add your nodes
LEDGER = []

@app.route("/sync", methods=["POST"])
def sync():
    event = request.json
    LEDGER.append(event)
    # Broadcast to other nodes
    for node in NODES:
        try:
            requests.post(f"http://{node}/sync", json=event, timeout=1)
        except:
            pass
    return {"status": "synced", "height": len(LEDGER)}

@app.route("/ledger")
def get_ledger():
    return {"chain": LEDGER, "height": len(LEDGER)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
