#include "kavach/nyaya.hpp"
#include <cctype>
#include <algorithm>
#include <chrono>

namespace kavach {

static bool icontains(std::string_view haystack, std::string_view needle) {
    if (needle.empty()) return true;
    if (needle.size() > haystack.size()) return false;
    
    auto it = std::search(haystack.begin(), haystack.end(),
                          needle.begin(), needle.end(),
                          [](char a, char b) {
                              return std::tolower(static_cast<unsigned char>(a)) 
                                  == std::tolower(static_cast<unsigned char>(b));
                          });
    return it != haystack.end();
}

NyayaFirewall::NyayaFirewall() {
    m_rules.push_back({"SQLI-001", "SQL Injection", "SQL keywords",
              {"union select", "drop table", "' or '1'='1", "1=1", "insert into"},
              sutra::Severity::PRALAYA, true});
    
    m_rules.push_back({"XSS-001", "Cross-Site Scripting", "Script injection",
              {"<script>", "javascript:", "onerror=", "onload=", "alert("},
              sutra::Severity::MAHA, true});
    
    m_rules.push_back({"CMDI-001", "Command Injection", "Shell commands",
              {"; ls", "; cat", "; rm", "wget ", "curl ", "`", "$(", "| nc"},
              sutra::Severity::PRALAYA, true});
    
    m_rules.push_back({"PATH-001", "Path Traversal", "Directory traversal",
              {"../", "/etc/passwd", "/etc/shadow", "boot.ini"},
              sutra::Severity::MAHA, true});
    
    m_rules.push_back({"PS-001", "PowerShell", "PS execution",
              {"powershell", "-enc", "invoke-expression", "downloadstring", "iex "},
              sutra::Severity::TIVRA, true});
    
    m_rules.push_back({"SSRF-001", "SSRF", "Internal request",
              {"http://127.", "http://10.", "http://192.168.", "http://172."},
              sutra::Severity::TIVRA, true});
    
    m_rules.push_back({"WSH-001", "Webshell", "Webshell detected",
              {"eval(", "system(", "shell_exec(", "passthru(", "base64_decode"},
              sutra::Severity::PRALAYA, true});
    
    m_rules.push_back({"C2-001", "C2 Beacon", "C2 traffic",
              {"/beacon", "/c2/poll", "callback?id=", "auth_token="},
              sutra::Severity::MAHA, true});
    
    m_rules.push_back({"EXFIL-001", "Data Exfil", "Sensitive data",
              {"password=", "credit_card=", "ssn=", "api_key=", "token="},
              sutra::Severity::TIVRA, true});
    
    m_rules.push_back({"DOS-001", "DoS Pattern", "Denial of service",
              {"syn flood", "ping flood", "slowloris", "ddos"},
              sutra::Severity::MAHA, true});
}

void NyayaFirewall::add_rule(NyayaRule rule) {
    m_rules.push_back(std::move(rule));
}

std::optional<NyayaVerdict> NyayaFirewall::evaluate(std::string_view payload) noexcept {
    m_total_evaluations++;
    
    for (const auto& rule : m_rules) {
        for (const auto& kw : rule.keywords) {
            if (icontains(payload, kw)) {
                if (rule.block) m_total_blocks++;
                
                NyayaVerdict v;
                v.rule_id = rule.id;
                v.pratijna = rule.pratijna;
                v.hetu = rule.hetu;
                v.severity = rule.severity;
                v.blocked = rule.block;
                v.timestamp_ns = static_cast<uint64_t>(
                    std::chrono::duration_cast<std::chrono::nanoseconds>(
                        std::chrono::high_resolution_clock::now().time_since_epoch()
                    ).count()
                );
                return v;
            }
        }
    }
    return std::nullopt;
}

double NyayaFirewall::block_rate() const {
    auto total = m_total_evaluations.load();
    return total > 0 ? (double)m_total_blocks / total * 100.0 : 0.0;
}

} // namespace kavach
