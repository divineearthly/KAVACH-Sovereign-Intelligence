#pragma once
#include "sutra.hpp"
#include <vector>
#include <deque>
#include <cmath>
#include <algorithm>
#include <numeric>

namespace kavach {

struct TrafficSample {
    double packets_per_sec;
    double bytes_per_sec;
    uint32_t unique_ips;
    uint64_t timestamp;
};

class CharakaML {
    double m_mean_pps = 0.0, m_std_pps = 0.0;
    double m_mean_bps = 0.0, m_std_bps = 0.0;
    double m_mean_ips = 0.0, m_std_ips = 0.0;
    double m_threshold = 2.5;  // Z-score threshold
    bool m_trained = false;
    
public:
    void train(const std::vector<TrafficSample>& normal_traffic);
    
    struct AnomalyResult {
        bool is_anomalous;
        sutra::Dosha dosha;
        double z_score;
        std::string reason;
    };
    
    AnomalyResult detect(const TrafficSample& sample) const noexcept;
    bool is_trained() const { return m_trained; }
};

inline void CharakaML::train(const std::vector<TrafficSample>& data) {
    if (data.size() < 50) return;
    
    std::vector<double> pps, bps, ips;
    for (const auto& s : data) {
        pps.push_back(s.packets_per_sec);
        bps.push_back(s.bytes_per_sec);
        ips.push_back(s.unique_ips);
    }
    
    auto calc_stats = [](const std::vector<double>& v, double& mean, double& std) {
        mean = std::accumulate(v.begin(), v.end(), 0.0) / v.size();
        double sq_sum = 0.0;
        for (double x : v) sq_sum += (x - mean) * (x - mean);
        std = std::sqrt(sq_sum / v.size());
    };
    
    calc_stats(pps, m_mean_pps, m_std_pps);
    calc_stats(bps, m_mean_bps, m_std_bps);
    calc_stats(ips, m_mean_ips, m_std_ips);
    m_trained = true;
}

inline CharakaML::AnomalyResult CharakaML::detect(const TrafficSample& s) const noexcept {
    if (!m_trained) return {false, sutra::Dosha::TRIDOSHA, 0.0, "Untrained"};
    
    double max_z = 0.0;
    std::string reason;
    sutra::Dosha dosha = sutra::Dosha::TRIDOSHA;
    
    auto check = [&](double val, double mean, double std, const char* name, sutra::Dosha d) {
        if (std > 0) {
            double z = std::abs(val - mean) / std;
            if (z > m_threshold && z > max_z) {
                max_z = z;
                reason = name;
                dosha = d;
            }
        }
    };
    
    check(s.packets_per_sec, m_mean_pps, m_std_pps, "Packet rate anomaly", sutra::Dosha::VATA);
    check(s.bytes_per_sec, m_mean_bps, m_std_bps, "Data exfiltration", sutra::Dosha::PITTA);
    check(s.unique_ips, m_mean_ips, m_std_ips, "Lateral movement", sutra::Dosha::KAPHA);
    
    return {max_z > 0, dosha, max_z, reason};
}

} // namespace kavach
