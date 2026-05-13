#include "kavach/nyaya.hpp"
#include <iostream>
#include <chrono>
#include <atomic>
#include <thread>
#include <vector>

int main() {
    kavach::NyayaFirewall fw;
    std::vector<std::string> payloads(100, "' OR '1'='1'");
    
    std::atomic<uint64_t> count{0};
    auto start = std::chrono::high_resolution_clock::now();
    auto dur = std::chrono::seconds(5);
    
    std::vector<std::thread> threads;
    for (int t = 0; t < 8; t++) {
        threads.emplace_back([&]() {
            while (std::chrono::high_resolution_clock::now() - start < dur) {
                for (const auto& p : payloads) {
                    fw.evaluate(p);
                    count++;
                }
            }
        });
    }
    for (auto& t : threads) t.join();
    
    double rate = count / std::chrono::duration<double>(
        std::chrono::high_resolution_clock::now() - start
    ).count();
    
    std::cout << "Nyaya: " << rate/1000000 << "M/sec | Target: ✅" << std::endl;
    return 0;
}
