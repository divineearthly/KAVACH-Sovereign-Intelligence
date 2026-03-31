# Contributing to KAVACH

## Rules
Every new module MUST:
1. Be named after its Vedic Sutra
2. Include a docstring citing Sutra number and name
3. Write ALL events to the Akasha ledger
4. Print 🔱 at startup
5. Include test cases with real output

## Adding a Module
```python
class NewModule:
    """Vedic Sutra N: Name — Description."""
    def __init__(self, ledger: AkashaLedger):
        self.ledger = ledger
        print("🔱 MODULE ONLINE")
```
