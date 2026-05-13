"""Collect and test against public Indian scam SMS data"""
import sys
sys.path.insert(0, '.')
from modules.nyaya import NyayaPhishingInterceptor
from modules.akasha import AkashaLedger

# Expanded dataset from public sources
REAL_SCAMS = [
    # Bank scams
    "SBI Alert: Your account will be debited Rs.49,500. If not done, call 9830529249",
    "Dear Customer, Your HDFC Bank NetBanking has been blocked. Update KYC: http://hdfc-kyc.tk",
    "ICICI Bank: Your card has been used for Rs.25,000 at Amazon. Report: 1800-XXX-XXXX",
    "Axis Bank Urgent: Your account will be suspended. Verify PAN: http://axis-verify.ml",
    # UPI scams
    "You received Rs.5,000 from UPI. Accept: http://upi-cashback.xyz",
    "PhonePe: Congratulations! You won Rs.10,000 cashback. Claim within 1 hour",
    "Google Pay: Your payment of Rs.2,499 is on hold. Verify: http://gpay-verify.cc",
    # Government scheme scams
    "PM Kisan Yojana: Your 10th installment of Rs.6,000 approved. Submit Aadhaar: http://pmkisan.info",
    "Ayushman Bharat: Your health card is ready. Complete KYC: http://ayushman-gov.top",
    # Job scams
    "Amazon hiring: Work from home, earn Rs.5,000/day. Register: http://amazon-jobs.ml",
    "Government job alert: Railway recruitment 2026. Apply: http://rrb-recruitment.xyz",
    # Loan scams
    "Pre-approved personal loan Rs.10L at 5%. Apply: http://loan-sbi.tk",
    "Instant loan without documents. Disbursed in 1 hour. Call: 9876543210",
    # Electricity bill scams
    "APDCL Alert: Your electricity will be disconnected tonight. Pay now: http://apdcl-bill.cc",
    "CESC: Bill payment pending Rs.850. Power cut in 2 hours. Pay: http://cesc-pay.ml",
    # Delivery scams
    "India Post: Your parcel is held at customs. Pay Rs.50 clearance: http://indiapost-fee.top",
    "FedEx: Delivery attempted. Reschedule: http://fedex-india.info",
    # OTP scams
    "Your OTP is 783492. Share this to complete KYC verification",
    "WhatsApp verification code: 849201. Do not share with anyone",
]

BENIGN_SAMPLES = [
    "Your order OD123456 has been shipped via Delhivery",
    "Reminder: Your appointment with Dr. Sharma is tomorrow at 11am",
    "Happy Diwali! Wishing you and your family a prosperous year",
    "Your Amazon order has been delivered. Rate your experience",
    "Meeting rescheduled to 4pm. Please confirm your availability",
    "Mom: Pick up vegetables on your way home",
    "Your flight AI-405 to Delhi is on time. Gate 12",
    "EMI of Rs.12,500 deducted from your account as per standing instructions",
    "Your LPG cylinder booking confirmed. Delivery expected tomorrow",
    "School notice: Parent-teacher meeting on Saturday, 10am",
]

ledger = AkashaLedger()
nyaya = NyayaPhishingInterceptor(ledger)

print("=" * 60)
print("KAVACH — Large-Scale Phishing Detection Test")
print(f"Scam samples: {len(REAL_SCAMS)} | Benign: {len(BENIGN_SAMPLES)}")
print("=" * 60)

print("\n🔴 PHISHING DETECTION:")
detected, missed = 0, 0
for sample in REAL_SCAMS:
    result = nyaya.analyze(sample)
    verdict = result.get("verdict", "LEGITIMATE")
    if verdict in ("PHISHING", "SUSPICIOUS"):
        detected += 1
    else:
        missed += 1

print(f"  Detected: {detected}/{len(REAL_SCAMS)} ({detected/len(REAL_SCAMS)*100:.1f}%)")
print(f"  Missed:   {missed}/{len(REAL_SCAMS)}")

print("\n🟢 FALSE POSITIVE TEST:")
fp, ok = 0, 0
for sample in BENIGN_SAMPLES:
    result = nyaya.analyze(sample)
    verdict = result.get("verdict", "LEGITIMATE")
    if verdict in ("PHISHING", "SUSPICIOUS"):
        fp += 1
    else:
        ok += 1

print(f"  False Positives: {fp}/{len(BENIGN_SAMPLES)}")
print(f"  Correctly Passed: {ok}/{len(BENIGN_SAMPLES)}")

print("\n" + "=" * 60)
print(f"📊 SUMMARY: {detected+ok}/{len(REAL_SCAMS)+len(BENIGN_SAMPLES)} correct")
print(f"   Detection Rate: {detected/len(REAL_SCAMS)*100:.1f}%")
print(f"   False Positive Rate: {fp/len(BENIGN_SAMPLES)*100:.1f}%")
