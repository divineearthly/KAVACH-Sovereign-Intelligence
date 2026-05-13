#pragma once
#include <string>
#include <vector>
#include <optional>
#include <atomic>
#include <chrono>
#include "sutra.hpp"

namespace kavach {

struct NyayaRule {
    std::string id;
    std::string pratijna;
    std::string hetu;
    std::vector<std::string> keywords;
    sutra::Severity severity;
    bool block;
};

struct NyayaVerdict {
    std::string rule_id;
    std::string pratijna;
    std::string hetu;
    sutra::Severity severity;
    bool blocked;
    uint64_t timestamp_ns;
};

class NyayaFirewall {
    std::vector<NyayaRule> m_rules;
    std::atomic<uint64_t> m_total_evaluations{0};
    std::atomic<uint64_t> m_total_blocks{0};
    
public:
    NyayaFirewall();
    void add_rule(NyayaRule rule);
    std::optional<NyayaVerdict> evaluate(std::string_view payload) noexcept;
    
    uint64_t total_evaluations() const { return m_total_evaluations; }
    uint64_t total_blocks() const { return m_total_blocks; }
    double block_rate() const;
    size_t rule_count() const { return m_rules.size(); }
};

} // namespace kavach
