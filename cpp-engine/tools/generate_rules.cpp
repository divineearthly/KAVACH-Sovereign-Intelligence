#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <random>
#include <sstream>

int main() {
    std::ofstream out("rules/nyaya_50k_rules.txt");
    
    std::vector<std::string> categories = {
        "SQLI", "XSS", "CMDI", "PATH", "SSRF", "LFI", "RFI", "XXE",
        "CSRF", "IDOR", "JWT", "OAUTH", "CORS", "DESERIAL", "UPLOAD",
        "SCANNER", "BOTNET", "RANSOMWARE", "SPYWARE", "TROJAN",
        "WORM", "ROOTKIT", "BACKDOOR", "KEYLOGGER", "MINER",
        "PHISHING", "DEFACEMENT", "DOS", "DDOS",
        "BRUTEFORCE", "CREDENTIAL", "SESSION", "COOKIE", "HEADER"
    };
    
    std::vector<std::string> keywords = {
        "union", "select", "drop", "script", "alert", "eval", "system",
        "exec", "passwd", "shadow", "etc", "bin", "boot", "cmd", "powershell",
        "wget", "curl", "nc", "netcat", "bash", "sh", "python", "perl",
        "php", "asp", "jsp", "admin", "root", "config", "backup", "dump",
        "token", "api", "key", "secret", "password", "credential", "auth",
        "session", "cookie", "csrf", "jwt", "oauth", "saml", "ldap",
        "mysql", "postgres", "mongo", "redis", "elastic", "kibana",
        "docker", "kubernetes", "jenkins", "gitlab", "github", "bitbucket"
    };
    
    std::mt19937 rng(42);
    std::uniform_int_distribution<int> cat_dist(0, categories.size()-1);
    std::uniform_int_distribution<int> kw_dist(0, keywords.size()-1);
    std::uniform_int_distribution<int> sev_dist(1, 10);
    std::uniform_int_distribution<int> block_dist(0, 1);
    std::uniform_int_distribution<int> num_kw(1, 5);
    
    for (int i = 0; i < 50000; i++) {
        std::string cat = categories[cat_dist(rng)];
        int nkw = num_kw(rng);
        
        out << cat << "-" << i << "|"
            << cat << " Threat " << i << "|"
            << "Detected " << cat << " pattern|";
        
        for (int k = 0; k < nkw; k++) {
            if (k > 0) out << ",";
            out << keywords[kw_dist(rng)];
        }
        
        out << "|" << sev_dist(rng) << "|" << block_dist(rng) << "\n";
    }
    
    out.close();
    std::cout << "Generated 50,000 rules in rules/nyaya_50k_rules.txt\n";
    return 0;
}
