#pragma once
#include <vector>
#include <string>
#include <queue>
#include <unordered_map>
#include <memory>

namespace kavach {

// Aho-Corasick automaton for O(n+m) multi-pattern matching
class AhoCorasick {
    struct Node {
        std::unordered_map<char, std::unique_ptr<Node>> children;
        Node* fail = nullptr;
        std::vector<int> output; // Pattern IDs that end here
    };
    
    std::unique_ptr<Node> root;
    std::vector<std::string> patterns;
    
public:
    AhoCorasick() : root(std::make_unique<Node>()) {}
    
    void add_pattern(const std::string& pattern, int id) {
        Node* node = root.get();
        for (char c : pattern) {
            c = std::tolower(static_cast<unsigned char>(c));
            if (!node->children[c]) {
                node->children[c] = std::make_unique<Node>();
            }
            node = node->children[c].get();
        }
        node->output.push_back(id);
        patterns.push_back(pattern);
    }
    
    void build_failure_links() {
        std::queue<Node*> q;
        
        // Initialize root's children
        for (auto& [c, child] : root->children) {
            child->fail = root.get();
            q.push(child.get());
        }
        
        // BFS to build failure links
        while (!q.empty()) {
            Node* current = q.front();
            q.pop();
            
            for (auto& [c, child] : current->children) {
                Node* fail = current->fail;
                while (fail && !fail->children.count(c)) {
                    fail = fail->fail;
                }
                child->fail = fail ? fail->children[c].get() : root.get();
                
                // Merge outputs from failure node
                for (int id : child->fail->output) {
                    child->output.push_back(id);
                }
                
                q.push(child.get());
            }
        }
    }
    
    // Scan text and return all matched pattern IDs
    std::vector<int> scan(const std::string& text) const {
        std::vector<int> matches;
        Node* node = root.get();
        
        for (char ch : text) {
            char c = std::tolower(static_cast<unsigned char>(ch));
            
            while (node && !node->children.count(c)) {
                node = node->fail;
            }
            
            if (!node) {
                node = root.get();
                continue;
            }
            
            node = node->children[c].get();
            
            for (int id : node->output) {
                matches.push_back(id);
            }
        }
        
        return matches;
    }
    
    size_t pattern_count() const { return patterns.size(); }
};

} // namespace kavach
