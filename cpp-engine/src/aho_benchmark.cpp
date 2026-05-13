#include "kavach/aho_corasick.hpp"
#include <iostream>
#include <chrono>
#include <vector>
#include <string>

using namespace kavach;
using namespace std::chrono;

int main() {
    AhoCorasick ac;
    
    // Load all 7 Pramana keyword sets
    std::vector<std::string> keywords = {
        // P1: Verification/Urgency
        "verify", "update", "confirm", "click", "call", "pay", "send",
        "urgent", "immediately", "now", "today", "tonight",
        // P2 Rasa: Fear
        "blocked", "suspended", "locked", "unauthorized", "security",
        "alert", "warning", "failed", "invalid", "expired",
        // P3 Authority (Indian banks)
        "sbi", "hdfc", "icici", "axis", "pnb", "phonepe", "gpay",
        "paytm", "aadhaar", "pm kisan", "apdcl", "cesc",
        // P4 Sensitive
        "aadhaar", "pan card", "kyc", "password", "otp", "cvv",
        "credit card", "debit card", "upi pin",
        // P5 Suspicious TLD
        ".tk", ".ml", ".xyz", ".cc", ".info", ".top",
        // P6 Temporal urgency
        "within 24 hours", "before 12", "by tonight", "immediately",
        // P7 Vishing
        "call now", "contact immediately", "dispute call",
        // Hinglish
        "kijiye", "kripa karke", "turant", "band ho jayega",
    };
    
    for (size_t i = 0; i < keywords.size(); i++) {
        ac.add_pattern(keywords[i], i);
    }
    
    ac.build_failure_links();
    
    std::cout << "🔱 KAVACH Aho-Corasick Benchmark\n";
    std::cout << "   Patterns: " << ac.pattern_count() << "\n";
    std::cout << "   Automaton built\n\n";
    
    // Test payloads
    std::vector<std::string> payloads = {
        "Your SBI account will be blocked. Update KYC immediately",
        "Congratulations you won 50000 rupees click here",
        "Meeting at 3pm tomorrow please confirm",
        "Your HDFC card charged 45000 dispute call 9876543210",
        "Normal traffic data packet routing information",
    };
    
    std::cout << "📊 Scanning payloads:\n";
    for (const auto& p : payloads) {
        auto matches = ac.scan(p);
        std::cout << "   Matches: " << matches.size() 
                  << " | " << p.substr(0, 50) << "...\n";
    }
    
    // Speed benchmark
    std::cout << "\n📊 Speed Benchmark (1M scans)...\n";
    auto start = high_resolution_clock::now();
    
    int total_matches = 0;
    for (int i = 0; i < 1000000; i++) {
        for (const auto& p : payloads) {
            total_matches += ac.scan(p).size();
        }
    }
    
    auto elapsed = duration<double>(high_resolution_clock::now() - start).count();
    double scans_per_sec = 5000000.0 / elapsed; // 1M * 5 payloads
    
    std::cout << "   Total scans: 5,000,000\n";
    std::cout << "   Time: " << elapsed << "s\n";
    std::cout << "   Rate: " << scans_per_sec/1000000 << "M scans/sec\n";
    std::cout << "   Matches found: " << total_matches << "\n";
    
    return 0;
}
