#pragma once
#include <cstdint>
#include <string_view>

namespace kavach::sutra {
    // Nyaya Sutras
    constexpr uint16_t NYAYA_INFERENCE = 65;
    constexpr uint16_t CHARAKA_DIAGNOSIS = 12;
    constexpr uint16_t GANDHARVA_SONAR = 33;
    constexpr uint16_t AKASHA_LEDGER = 1;
    
    // Dosha classifications
    enum class Dosha : uint8_t { VATA=0, PITTA=1, KAPHA=2, TRIDOSHA=3 };
    
    // Threat severities (1-10, Vedic scale)
    enum class Severity : uint8_t {
        SUKSHMA=1,   // Subtle
        LAGHU=3,     // Light
        MADHYA=5,    // Medium
        TIVRA=7,     // Intense
        MAHA=9,      // Great
        PRALAYA=10   // Catastrophic
    };
    
    constexpr std::string_view MANTRA = "सत्यमेव जयते";
}
