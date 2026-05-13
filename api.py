"""KAVACH API — FastAPI endpoint for external integration."""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import time

from modules.charaka import CharakaAnomalyEngine
from modules.nyaya import NyayaPhishingInterceptor
from modules.gandharva import GandharvaVoiceDetector
from modules.akasha import AkashaLedger

app = FastAPI(
    title="🔱 KAVACH API",
    description="Sovereign Vedic Cyber Defense Intelligence",
    version="3.2.0"
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

charaka = CharakaAnomalyEngine()
nyaya = NyayaPhishingInterceptor()
gandharva = GandharvaVoiceDetector()
akasha = AkashaLedger()

class NetworkEvent(BaseModel):
    source_ip: str = Field("0.0.0.0", description="Source IP address")
    dest_ip: Optional[str] = Field(None, description="Destination IP")
    port: Optional[int] = Field(None, description="Port number")
    payload: Optional[str] = Field(None, description="Request payload")
    event_type: Optional[str] = Field("unknown", description="Event type")

class ScanRequest(BaseModel):
    events: List[NetworkEvent]

@app.get("/")
def root():
    return {
        "name": "KAVACH API",
        "version": "3.2.0",
        "status": "ACTIVE",
        "modules": ["charaka", "nyaya", "gandharva", "akasha", "sushruta", "dharma"],
        "sutra": "सत्यमेव जयते"
    }

@app.post("/scan/network")
def scan_network(request: ScanRequest):
    """Scan network events for threats."""
    results = []
    for event in request.events:
        event_dict = event.model_dump()
        
        # Charaka anomaly analysis
        charaka_result = charaka.analyze(event_dict)
        
        # Nyaya phishing analysis
        nyaya_result = nyaya.analyze(str(event_dict))
        
        # Record in Akasha
        akasha.add_entry("api", "network_scan", 
                        charaka_result.get("severity", 5),
                        str(event_dict))
        
        results.append({
            "charaka": charaka_result,
            "nyaya": nyaya_result,
            "severity": charaka_result.get("severity", 0)
        })
    
    return {"results": results, "count": len(results)}

@app.post("/scan/audio")
async def scan_audio(file: UploadFile = File(...)):
    """Analyze audio file for voice deepfakes."""
    audio_data = await file.read()
    result = gandharva.analyze(audio_data)
    akasha.add_entry("api", "audio_scan", result.get("severity", 5), file.filename)
    return result

@app.get("/status")
def system_status():
    """Get complete KAVACH system status."""
    return {
        "charaka_samples": charaka.n_samples if hasattr(charaka, 'n_samples') else "trained",
        "nyaya_patterns": len(nyaya.rasa_patterns) if hasattr(nyaya, 'rasa_patterns') else "loaded",
        "akasha_chain_height": len(akasha.chain)
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
