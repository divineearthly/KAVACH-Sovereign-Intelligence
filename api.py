"""KAVACH API — FastAPI endpoint for external integration."""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import time

from modules.charaka import CharakaDiagnosticEngine
from modules.nyaya_engine import NyayaRuleEngine
from modules.gandharva import GandharvaSonarDefense
from modules.akasha import AkashaLedger

app = FastAPI(
    title="🔱 KAVACH API",
    description="Sovereign Vedic Cyber Defense Intelligence",
    version="2.0.0"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Initialize engines
charaka = CharakaDiagnosticEngine()
nyaya = NyayaRuleEngine()
gandharva = GandharvaSonarDefense()
akasha = AkashaLedger()

# Models
class NetworkEvent(BaseModel):
    source_ip: str = Field(..., description="Source IP address")
    dest_ip: Optional[str] = Field(None, description="Destination IP")
    port: Optional[int] = Field(None, description="Port number")
    payload: Optional[str] = Field(None, description="Request payload")
    event_type: Optional[str] = Field("unknown", description="Event type")
    bytes_sent: Optional[int] = Field(0, description="Bytes transmitted")

class ScanRequest(BaseModel):
    events: List[NetworkEvent]
    context: Optional[dict] = Field({}, description="Additional context")

class ThreatResponse(BaseModel):
    verdict: str
    diagnosis: dict
    rule_matched: Optional[str]
    severity: int
    action: str
    timestamp: float

# Routes
@app.get("/")
def root():
    return {
        "name": "KAVACH API",
        "version": "2.0.0",
        "status": "ACTIVE",
        "modules": ["charaka", "nyaya", "gandharva", "akasha"],
        "sutra": "सत्यमेव जयते"
    }

@app.post("/scan/network", response_model=ThreatResponse)
def scan_network(request: ScanRequest):
    """Scan network events for threats."""
    results = []
    
    for event in request.events:
        event_dict = event.model_dump()
        
        # Charaka diagnosis
        diagnosis = charaka.diagnose([event_dict])
        
        # Nyaya firewall
        payload = event_dict.get("payload", "")
        rule_match = nyaya.evaluate(payload, request.context)
        
        verdict = "BLOCK" if (rule_match and rule_match["verdict"] in ("BLOCK", "RATE_LIMIT")) else "ALLOW"
        
        results.append({
            "verdict": verdict,
            "diagnosis": diagnosis,
            "rule_matched": rule_match["rule_id"] if rule_match else None,
            "severity": diagnosis.get("severity", 0),
            "action": "BLOCKED" if verdict == "BLOCK" else "ALLOWED",
            "timestamp": time.time()
        })
    
    # Record in Akasha
    akasha.record("api_scan", {"events_count": len(request.events), "results": len(results)}, "api")
    
    return results[0] if results else {"verdict": "ALLOW", "severity": 0}

@app.post("/scan/audio")
async def scan_audio(file: UploadFile = File(...)):
    """Analyze audio file for sonic threats."""
    audio_data = await file.read()
    result = gandharva.analyze(audio_data, file.filename)
    akasha.record("audio_scan", result, "api")
    return result

@app.get("/status")
def system_status():
    """Get complete KAVACH system status."""
    return {
        "nyaya": nyaya.stats(),
        "akasha": akasha.get_stats(),
        "charaka_diagnoses": len(charaka.diagnosis_history),
        "gandharva_signatures": len(gandharva.sonic_threat_db)
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
