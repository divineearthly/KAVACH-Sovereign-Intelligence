import sys
sys.path.insert(0, '.')
from modules.nyaya import NyayaPhishingInterceptor
from modules.akasha import AkashaLedger

REAL_PHISHING_SAMPLES = [
    "Your SBI account will be blocked. Update KYC: http://sbi-kyc-update.tk",
    "Congratulations! You won 50000 Amazon gift card. Claim: http://amzn-gift.xyz",
    "Dear customer, your HDFC card charged 45000. Dispute: call 9876543210",
    "UPI reward: Get 500 cashback instantly. Click: http://upi-reward.ml",
    "Your electricity bill pending. Power cut tonight. Pay: http://ebill-pay.cc",
    "PM Kisan Yojana: Your installment approved. Submit Aadhaar: http://pmkisan.info",
]

BENIGN_SAMPLES = [
    "Meeting at 3pm tomorrow. Please confirm.",
    "Happy birthday! Have a great day ahead.",
    "Your order 12345 has been shipped. Track: amazon.in",
    "Reminder: doctor appointment on Friday at 10am.",
    "Mom: dinner is ready, come home",
    "Your OTP for login is 456789. Do not share.",
]

ledger = AkashaLedger()
nyaya = NyayaPhishingInterceptor(ledger)

print("=" * 50)
print("KAVACH Real Threat Test")
print("=" * 50)

print("\nPhishing Detection (verdict=PHISHING or SUSPICIOUS = detected):")
correct = 0
for sample in REAL_PHISHING_SAMPLES:
    result = nyaya.analyze(sample)
    verdict = result.get("verdict", "LEGITIMATE")
    score = result.get("score", 0)
    detected = verdict in ("PHISHING", "SUSPICIOUS")
    status = "OK" if detected else "MISS"
    print(f"  [{status}] score={score:.2f} {verdict} | {sample[:50]}...")
    if detected:
        correct += 1
print(f"\nDetection Rate: {correct}/{len(REAL_PHISHING_SAMPLES)} ({correct/len(REAL_PHISHING_SAMPLES)*100:.0f}%)")

print("\nFalse Positive Test:")
fp = 0
for sample in BENIGN_SAMPLES:
    result = nyaya.analyze(sample)
    verdict = result.get("verdict", "LEGITIMATE")
    detected = verdict in ("PHISHING", "SUSPICIOUS")
    status = "FP" if detected else "OK"
    if not detected:
        print(f"  [{status}] {verdict} | {sample[:50]}...")
    else:
        print(f"  [{status}] score={result.get('score',0):.2f} {verdict} | {sample[:50]}...")
    if detected:
        fp += 1
print(f"\nFalse Positives: {fp}/{len(BENIGN_SAMPLES)}")
