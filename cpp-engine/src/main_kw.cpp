#include "kavach/aho_corasick.hpp"
#include "kavach/sutra.hpp"
#include <iostream>
#include <thread>
#include <atomic>
#include <iomanip>
#include <vector>
#include <fstream>
#include <sstream>
#include <chrono>
#include <cctype>
#include <algorithm>

using namespace kavach;
using namespace std::chrono;

struct Rule {
    std::string id;
    int severity;
    bool block;
};

// Build hybrid index from rules file
static std::unordered_map<std::string, std::vector<Rule>> build_index(const std::string& path) {
    std::unordered_map<std::string, std::vector<Rule>> index;
    std::ifstream f(path);
    std::string line;
    
    while (std::getline(f, line)) {
        std::stringstream ss(line);
        std::string id, name, desc, patterns, sev_str, block_str;
        std::getline(ss, id, '|'); std::getline(ss, name, '|');
        std::getline(ss, desc, '|'); std::getline(ss, patterns, '|');
        std::getline(ss, sev_str, '|'); std::getline(ss, block_str, '|');
        
        std::stringstream ps(patterns);
        std::string kw;
        while (std::getline(ps, kw, ',')) {
            if (!kw.empty()) {
                int sev = sev_str.empty() ? 5 : std::stoi(sev_str);
                index[kw].push_back({id, sev, block_str == "1"});
            }
        }
    }
    return index;
}

// Build Aho-Corasick with all Pramana keywords
static AhoCorasick build_pramana_automaton() {
    AhoCorasick ac;
    
    std::vector<std::string> keywords = {
        // P1: Action/Verification triggers
        "verify", "update", "confirm", "click", "pay", "send", "submit",
        "urgent", "immediately", "now", "today", "tonight",
        // P2: Rasa - Fear/Urgency
        "blocked", "suspended", "locked", "unauthorized", "security",
        "alert", "warning", "failed", "invalid", "expired", "limit",
        // P2: Rasa - Attraction
        "won", "cashback", "reward", "prize", "gift", "free", "bonus",
        "congratulations", "selected", "lucky",
        // P3: Indian Authorities
        "sbi", "hdfc", "icici", "axis", "pnb", "bob", "canara",
        "phonepe", "gpay", "google pay", "paytm", "amazon pay",
        "pm kisan", "ayushman", "epfo", "income tax", "gst",
        "aadhaar", "uidai", "pan card", "passport", "digilocker",
        "apdcl", "cesc", "bescom", "tangedco", "msedcl", "tneb",
        "jio", "airtel", "vi", "bsnl",
        "india post", "fedex", "dhl", "delhivery", "blue dart",
        "rbi", "sebi", "irda", "trai", "cibil",
        // P4: Sensitive Data
        "aadhaar", "pan", "kyc", "password", "otp", "cvv",
        "credit card", "debit card", "upi pin", "account number",
        "date of birth", "mother maiden",
        // P5: Suspicious TLDs
        ".tk", ".ml", ".xyz", ".cc", ".info", ".top", ".click", ".live",
        // P6: Temporal Urgency
        "within 24 hours", "before 12", "by tonight", "immediately",
        "closing soon", "last chance", "limited time",
        // P7: Call-to-Action
        "call now", "contact immediately", "dispute call",
        "toll free", "helpline", "customer care",
        // Hinglish
        "kijiye", "kripa karke", "turant", "foran", "jaldi",
        "band ho jayega", "block kar diya", "verify karein",
        "update karein", "call karein", "sampark karein",
        "abhi", "aaj hi", "kal subah", "chalu", "band",
    };
    
    for (size_t i = 0; i < keywords.size(); i++) {
        ac.add_pattern(keywords[i], i);
    }
    ac.build_failure_links();
    return ac;
}

// Fast scan using Aho-Corasick + hash index
inline int fast_scan_ac(
    const AhoCorasick& ac,
    const std::unordered_map<std::string, std::vector<Rule>>& index,
    const std::string& payload
) {
    // Get all keyword matches in one pass
    auto matches = ac.scan(payload);
    
    // Check if any matched keyword is in our rule index
    // This is O(matches) instead of O(all_keywords)
    for (int match_id : matches) {
        // We need the actual keyword text — use the match count as signal
        // Simplified: if Aho-Corasick found anything, run hash lookup on payload tokens
        break; // Just need to know if ANYTHING matched
    }
    
    if (matches.empty()) return -1;
    
    // Tokenize and check index for matched keywords
    std::string word;
    for (char c : payload) {
        if (std::isalnum((unsigned char)c) || c == '_' || c == '-' || c == '.' || c == '\'' || c == '=' || c == '/') {
            word += std::tolower((unsigned char)c);
        } else {
            if (!word.empty()) {
                auto it = index.find(word);
                if (it != index.end() && !it->second.empty()) {
                    return it->second[0].severity;
                }
                word.clear();
            }
        }
    }
    if (!word.empty()) {
        auto it = index.find(word);
        if (it != index.end() && !it->second.empty()) {
            return it->second[0].severity;
        }
    }
    
    return matches.empty() ? -1 : 3; // Low-severity flag if AC matched but index didn't
}

int main() {
    std::cout << "🔱 KAVACH v3.3 — Aho-Corasick Pipeline\n";
    std::cout << "   सत्यमेव जयते\n\n";
    
    // Build automaton
    std::cout << "📥 Building Aho-Corasick automaton...\n";
    auto ac = build_pramana_automaton();
    std::cout << "   Patterns: " << ac.pattern_count() << " loaded\n";
    
    // Build hash index
    std::cout << "📥 Building rule index...\n";
    auto index = build_index("nyaya_50k_rules.txt");
    std::cout << "   Index: " << index.size() << " keywords\n\n";
    
    std::vector<std::string> payloads = {
        "Your SBI account will be blocked. Update KYC immediately",
        "Congratulations you won 50000 rupees click here",
        "Meeting at 3pm tomorrow please confirm",
        "Your HDFC card charged 45000 dispute call 9876543210",
        "Normal traffic data packet routing information",
        "PM Kisan Yojana: Submit Aadhaar at http://pmkisan.tk",
        "APDCL Alert: Power cut tonight. Pay at http://apdcl-bill.cc",
        "Your Amazon order shipped. Track: amazon.in",
        "Urgent: Band ho jayega aapka account. Kripa karke verify karein",
        "Congratulations! Aap jeet gaye hain 10000 rupaye. Abhi claim karein",
    };
    
    std::cout << "📊 Pipeline Benchmark (8 threads, 10 sec)...\n";
    
    std::atomic<uint64_t> total_evals{0};
    std::atomic<uint64_t> total_hits{0};
    auto start = high_resolution_clock::now();
    auto end_time = start + seconds(10);
    
    std::vector<std::thread> threads;
    for (int t = 0; t < 8; t++) {
        threads.emplace_back([&]() {
            uint64_t local_evals = 0, local_hits = 0;
            while (high_resolution_clock::now() < end_time) {
                for (const auto& p : payloads) {
                    int sev = fast_scan_ac(ac, index, p);
                    local_evals++;
                    if (sev >= 5) local_hits++;
                }
            }
            total_evals += local_evals;
            total_hits += local_hits;
        });
    }
    for (auto& t : threads) t.join();
    
    double rate = total_evals / duration<double>(high_resolution_clock::now() - start).count();
    
    std::cout << "   Total:  " << total_evals/1000000.0 << "M evaluations\n";
    std::cout << "   Rate:   " << std::fixed << std::setprecision(1) 
              << rate/1000000 << "M events/sec\n";
    std::cout << "   Alerts: " << total_hits << "\n\n";
    
    // Detail scan
    std::cout << "📊 Detail Scan:\n";
    for (const auto& p : payloads) {
        auto matches = ac.scan(p);
        int sev = fast_scan_ac(ac, index, p);
        std::cout << "   [" << (sev >= 5 ? "🔴" : sev >= 3 ? "🟡" : "🟢") << "] "
                  << "matches=" << matches.size() << " sev=" << sev 
                  << " | " << p.substr(0, 60) << "\n";
    }
    
    std::cout << "\n═══════════════════════════════════\n";
    std::cout << "📊 KAVACH v3.3 — Aho-Corasick Pipeline\n";
    std::cout << "═══════════════════════════════════\n";
    std::cout << "   Patterns: " << ac.pattern_count() << "\n";
    std::cout << "   Index:    " << index.size() << " keywords\n";
    std::cout << "   Rate:     " << std::setprecision(1) << rate/1000000 << "M events/sec\n";
    std::cout << "\n🔱 सत्यमेव जयते\n";
    
    return 0;
}
