#!/bin/bash
# Hourly threat feed fetcher — cron job
while true; do
    echo "[$(date)] Fetching threat intel..."
    
    # AlienVault OTX (real-time pulses)
    curl -s -H "X-OTX-API-KEY: YOUR_FREE_KEY" \
        "https://otx.alienvault.com/api/v1/pulses/subscribed?limit=500" | \
        python3 -c "
import json,sys
data=json.load(sys.stdin)
for pulse in data.get('results',[]):
    for ind in pulse.get('indicators',[]):
        print(ind.get('indicator',''))
" 2>/dev/null | sort -u > rules/threat_intel_keywords.txt
    
    # MalwareBazaar (last 24h)
    curl -s https://mb-api.abuse.ch/api/v1/ -d "query=get_recent&selector=time" | \
        python3 -c "
import json,sys
data=json.load(sys.stdin)
for m in data.get('data',[]):
    print(m.get('sha256_hash',''))
    print(m.get('file_name',''))
" 2>/dev/null | sort -u >> rules/threat_intel_keywords.txt
    
    # Deduplicate
    sort -u rules/threat_intel_keywords.txt -o rules/threat_intel_keywords.txt
    
    count=$(wc -l < rules/threat_intel_keywords.txt)
    echo "  ✅ $count active threat indicators"
    
    # Rebuild engine
    cd /root/KAVACH-full/cpp-engine/build
    make -j$(nproc) 2>/dev/null
    
    # Sleep 1 hour
    sleep 3600
done
