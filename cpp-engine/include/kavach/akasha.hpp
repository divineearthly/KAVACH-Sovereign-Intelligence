#pragma once
#include <string>
#include <vector>
#include <shared_mutex>
#include <openssl/sha.h>
#include <chrono>

namespace kavach {

struct AkashaEvent {
    uint64_t id;
    uint64_t timestamp_ns;
    std::string event_type;
    std::string module;
    std::string data;
    std::string previous_hash;
    std::string hash;
};

class AkashaLedger {
    std::vector<AkashaEvent> m_chain;
    mutable std::shared_mutex m_mutex;
    bool m_batch_mode = false;
    
    std::string hash_event(const AkashaEvent& e) const;
    
public:
    AkashaLedger(bool batch = false) : m_batch_mode(batch) {}
    
    std::string record(std::string event_type, std::string data, std::string module);
    bool verify_integrity() const;
    size_t size() const { 
        std::shared_lock lock(m_mutex);
        return m_chain.size(); 
    }
};

inline std::string AkashaLedger::hash_event(const AkashaEvent& e) const {
    std::string content = std::to_string(e.id) + std::to_string(e.timestamp_ns) 
                        + e.event_type + e.module + e.data + e.previous_hash;
    
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256(reinterpret_cast<const unsigned char*>(content.c_str()), content.size(), hash);
    
    std::string result;
    result.reserve(SHA256_DIGEST_LENGTH * 2);
    for (int i = 0; i < SHA256_DIGEST_LENGTH; i++) {
        char buf[3];
        snprintf(buf, sizeof(buf), "%02x", hash[i]);
        result += buf;
    }
    return result;
}

inline std::string AkashaLedger::record(std::string event_type, std::string data, std::string module) {
    std::unique_lock lock(m_mutex);
    
    AkashaEvent e;
    e.id = m_chain.size() + 1;
    e.timestamp_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(
        std::chrono::high_resolution_clock::now().time_since_epoch()
    ).count();
    e.event_type = std::move(event_type);
    e.module = std::move(module);
    e.data = std::move(data);
    e.previous_hash = m_chain.empty() ? std::string(64, '0') : m_chain.back().hash;
    e.hash = hash_event(e);
    
    std::string h = e.hash;
    m_chain.push_back(std::move(e));
    return h;
}

inline bool AkashaLedger::verify_integrity() const {
    std::shared_lock lock(m_mutex);
    for (size_t i = 1; i < m_chain.size(); i++) {
        if (m_chain[i].previous_hash != m_chain[i-1].hash) return false;
        if (hash_event(m_chain[i]) != m_chain[i].hash) return false;
    }
    return true;
}

} // namespace kavach
