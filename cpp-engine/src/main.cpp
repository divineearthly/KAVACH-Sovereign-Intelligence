#include "kavach/hs_nyaya.hpp"
#include "kavach/akasha.hpp"
#include "kavach/sutra.hpp"
#include <iostream>
#include <thread>
#include <atomic>
#include <iomanip>
#include <vector>
#include <chrono>

using namespace kavach;
using namespace std::chrono;

int main() {
    std::cout << "🔱 KAVACH v3.1 — 50K Rules + Hyperscan\n";
    std::cout << "   " << sutra::MANTRA << "\n\n";
    
    // Load 50K rules
    HyperscanNyaya nyaya;
    std::cout << "📥 Loading 50,000 rules...\n";
    if (!nyaya.load_rules("rules/nyaya_50k_rules.txt")) {
        std::cerr << "Failed to load rules\n";
        return 1;
    }
    std::cout << "   Loaded: " << nyaya.rule_count() << " rules\n";
    
    std::cout << "🔧 Compiling Hyperscan database...\n";
    if (!nyaya.compile()) {
        std::cerr << "Failed to compile Hyperscan DB\n";
        return 1;
    }
    std::cout << "   Database compiled successfully\n\n";
    
    // Test payloads
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
    
    // ==========================================
    // BENCHMARK: 50K rules, 8 threads, 10 sec
    // ==========================================
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
                    int match = nyaya.scan(p);
                    local_evals++;
                    if (match >= 0) local_blocks++;
                }
            }
            total_evals += local_evals;
            total_blocks += local_blocks;
        });
    }
    for (auto& t : threads) t.join();
    
    double rate = total_evals / duration<double>(high_resolution_clock::now() - start).count();
    
    std::cout << "   Total:  " << total_evals/1000000.0 << "M evaluations\n";
    std::cout << "   Rate:   " << std::fixed << std::setprecision(1) 
              << rate/1000000 << "M events/sec\n";
    std::cout << "   Blocks: " << total_blocks << " (" 
              << std::setprecision(1) << (double)total_blocks/total_evals*100 << "%)\n";
    
    // ==========================================
    // SUMMARY
    // ==========================================
    std::cout << "\n═══════════════════════════════════\n";
    std::cout << "📊 KAVACH v3.1 RESULTS\n";
    std::cout << "═══════════════════════════════════\n";
    std::cout << "   Rules:  " << nyaya.rule_count() << "\n";
    std::cout << "   Rate:   " << std::setprecision(1) << rate/1000000 << "M events/sec\n";
    std::cout << "   vs v2.0: " << std::setprecision(0) << rate/90000 << "x faster\n";
    std::cout << "\n🔱 सत्यमेव जयते\n";
    
    return 0;
}
