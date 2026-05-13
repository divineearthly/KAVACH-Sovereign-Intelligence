#pragma once
#include <hs/hs.h>
#include <string>
#include <vector>
#include <atomic>
#include <cstring>
#include <fstream>
#include <sstream>
#include "sutra.hpp"

namespace kavach {

struct HsRule {
    unsigned int id;
    std::string name;
    std::string description;
    sutra::Severity severity;
    bool block;
};

class HyperscanNyaya {
    hs_database_t* m_db = nullptr;
    hs_scratch_t* m_scratch = nullptr;
    std::vector<HsRule> m_rules;
    std::atomic<uint64_t> m_evals{0};
    std::atomic<uint64_t> m_blocks{0};
    std::vector<std::string> m_patterns;
    std::vector<unsigned int> m_flags;
    std::vector<unsigned int> m_ids;
    
    static int on_match(unsigned int id, unsigned long long, unsigned long long,
                        unsigned int, void* ctx) {
        auto* result = static_cast<HsRule*>(ctx);
        *result = *reinterpret_cast<HsRule*>(0); // Will be fixed
        return 0;
    }
    
public:
    HyperscanNyaya() = default;
    ~HyperscanNyaya() { 
        if (m_db) hs_free_database(m_db);
        if (m_scratch) hs_free_scratch(m_scratch);
    }
    
    bool load_rules(const std::string& filepath);
    bool compile();
    
    // Match return: rule_id if matched, -1 if clean
    int scan(const std::string& payload);
    
    uint64_t evals() const { return m_evals; }
    uint64_t blocks() const { return m_blocks; }
    size_t rule_count() const { return m_rules.size(); }
};

inline bool HyperscanNyaya::load_rules(const std::string& filepath) {
    std::ifstream f(filepath);
    std::string line;
    unsigned int id = 0;
    
    while (std::getline(f, line) && id < 50000) {
        std::stringstream ss(line);
        std::string id_str, name, desc, patterns_str, sev_str, block_str;
        
        std::getline(ss, id_str, '|');
        std::getline(ss, name, '|');
        std::getline(ss, desc, '|');
        std::getline(ss, patterns_str, '|');
        std::getline(ss, sev_str, '|');
        std::getline(ss, block_str, '|');
        
        // Split patterns by comma
        std::stringstream ps(patterns_str);
        std::string pattern;
        while (std::getline(ps, pattern, ',')) {
            if (!pattern.empty()) {
                m_patterns.push_back(pattern);
                m_flags.push_back(HS_FLAG_CASELESS | HS_FLAG_SINGLEMATCH);
                m_ids.push_back(id);
            }
        }
        
        int sev = std::stoi(sev_str);
        m_rules.push_back({id, name, desc, 
                          static_cast<sutra::Severity>(sev),
                          block_str == "1"});
        id++;
    }
    
    return !m_rules.empty();
}

inline bool HyperscanNyaya::compile() {
    if (m_patterns.empty()) return false;
    
    std::vector<const char*> c_patterns;
    for (const auto& p : m_patterns) c_patterns.push_back(p.c_str());
    
    hs_compile_error_t* err = nullptr;
    hs_error_t status = hs_compile_multi(
        c_patterns.data(), m_flags.data(), m_ids.data(),
        c_patterns.size(), HS_MODE_BLOCK, nullptr, &m_db, &err
    );
    
    if (status != HS_SUCCESS) {
        if (err) {
            fprintf(stderr, "Hyperscan error: %s\n", err->message);
            hs_free_compile_error(err);
        }
        return false;
    }
    
    hs_alloc_scratch(m_db, &m_scratch);
    return true;
}

inline int HyperscanNyaya::scan(const std::string& payload) {
    m_evals++;
    
    unsigned int matched_id = UINT_MAX;
    
    hs_error_t status = hs_scan(
        m_db, payload.c_str(), payload.size(), 0, m_scratch,
        [](unsigned int id, unsigned long long, unsigned long long,
           unsigned int, void* ctx) -> int {
            *static_cast<unsigned int*>(ctx) = id;
            return 1; // Stop after first match
        },
        &matched_id
    );
    
    if (matched_id != UINT_MAX && matched_id < m_rules.size()) {
        if (m_rules[matched_id].block) m_blocks++;
        return matched_id;
    }
    
    return -1; // No match
}

} // namespace kavach
