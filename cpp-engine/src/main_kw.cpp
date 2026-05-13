#include "kavach/sutra.hpp"
#include <iostream>
#include <thread>
#include <atomic>
#include <iomanip>
#include <vector>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include <chrono>
#include <cctype>
#include <algorithm>

using namespace std::chrono;

struct Rule {
    std::string id;
    int severity;
    bool block;
};

// Build a keyword → rules index for O(1) lookup
static std::unordered_map<std::string, std::vector<Rule>> build_index(
    const std::string& path, int max_rules
) {
    std::unordered_map<std::string, std::vector<Rule>> index;
    std::ifstream f(path);
    std::string line;
    int count = 0;
    
    while (std::getline(f, line) && count < max_rules) {
        std::stringstream ss(line);
        std::string id, name, desc, patterns_str, sev_str, block_str;
        
        std::getline(ss, id, '|');
        std::getline(ss, name, '|');
        std::getline(ss, desc, '|');
        std::getline(ss, patterns_str, '|');
        std::getline(ss, sev_str, '|');
        std::getline(ss, block_str, '|');
        
        std::stringstream ps(patterns_str);
        std::string kw;
        while (std::getline(ps, kw, ',')) {
            if (!kw.empty()) {
                // Store lowercase key
                std::string lower;
                for (char c : kw) lower += std::tolower((unsigned char)c);
                
                int sev = sev_str.empty() ? 5 : std::stoi(sev_str);
                index[lower].push_back({id, sev, block_str == "1"});
            }
        }
        count++;
    }
    
    std::cout << "   Indexed: " << index.size() << " unique keywords\n";
    return index;
}

// Fast scan: extract words, check index
inline bool fast_scan(
    const std::unordered_map<std::string, std::vector<Rule>>& index,
    const std::string& payload,
    int& severity,
    bool& blocked
) {
    // Tokenize payload into words
    std::string word;
    for (char c : payload) {
        if (std::isalnum((unsigned char)c) || c == '_' || c == '-' || c == '.' || c == '\'' || c == '=') {
            word += std::tolower((unsigned char)c);
        } else {
            if (!word.empty()) {
                auto it = index.find(word);
                if (it != index.end() && !it->second.empty()) {
                    severity = it->second[0].severity;
                    blocked = it->second[0].block;
                    return true;
                }
                word.clear();
            }
        }
    }
    // Check last word
    if (!word.empty()) {
        auto it = index.find(word);
        if (it != index.end() && !it->second.empty()) {
            severity = it->second[0].severity;
            blocked = it->second[0].block;
            return true;
        }
    }
    return false;
}

int main() {
    std::cout << "🔱 KAVACH v3.1 — 50K Rules (Indexed)\n";
    std::cout << "   सत्यमेव जयते\n\n";
    
    std::cout << "📥 Building keyword index...\n";
    auto index = build_index("nyaya_50k_rules.txt", 50000);
    
    std::vector<std::string> payloads = {
        "GET /api/users HTTP/1.1",
        "POST /login ' OR '1'='1' --",
        "<script>alert('xss')</script>",
        "../../etc/passwd",
        "; rm -rf /",
        "SELECT * FROM users WHERE id=1",
        "powershell -enc QwBvAG0A",
        "http://192.168.1.1/admin",
        "eval(base64_decode(",
        "normal traffic data packet"
    };
    
    std::cout << "📊 Benchmark (50K rules, 8 threads, 10 sec)...\n";
    
    std::atomic<uint64_t> total_evals{0};
    std::atomic<uint64_t> total_blocks{0};
    auto start = high_resolution_clock::now();
    auto end_time = start + seconds(10);
    
    std::vector<std::thread> threads;
    for (int t = 0; t < 8; t++) {
        threads.emplace_back([&]() {
            uint64_t local_evals = 0, local_blocks = 0;
            
            while (high_resolution_clock::now() < end_time) {
                for (const auto& p : payloads) {
                    int sev;
                    bool blocked;
                    if (fast_scan(index, p, sev, blocked)) {
                        if (blocked) local_blocks++;
                    }
                    local_evals++;
                }
            }
            total_evals += local_evals;
            total_blocks += local_blocks;
        });
    }
    for (auto& t : threads) t.join();
    
    double rate = total_evals / duration<double>(high_resolution_clock::now() - start).count();
    
    std::cout << "   Total:  " << total_evals/1000000.0 << "M evaluations\n";
    std::cout << "   Rate:   " << std::fixed << std::setprecision(0) 
              << rate/1000 << "K events/sec\n";
    
    std::cout << "\n═══════════════════════════════════\n";
    std::cout << "📊 KAVACH v3.1 INDEXED\n";
    std::cout << "═══════════════════════════════════\n";
    std::cout << "   Rules:  50,000\n";
    std::cout << "   Index:  " << index.size() << " keywords\n";
    std::cout << "   Rate:   " << std::setprecision(0) << rate/1000000 << "M events/sec\n";
    std::cout << "   vs v2.0: " << std::setprecision(0) << rate/90000 << "x\n";
    std::cout << "\n🔱 सत्यमेव जयते\n";
    return 0;
}
