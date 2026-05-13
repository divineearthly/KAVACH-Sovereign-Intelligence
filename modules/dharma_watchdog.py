"""Dharma Watchdog — Hot-reload policies without restarting KAVACH."""

import time
import os
import threading

class DharmaWatchdog:
    """Watches dharma_policies.yaml for changes and reloads automatically."""
    
    def __init__(self, parser, policy_path='modules/dharma_policies.yaml', check_interval=5):
        self.parser = parser
        self.policy_path = policy_path
        self.check_interval = check_interval
        self.last_mtime = os.path.getmtime(policy_path)
        self.running = False
        self.thread = None
        self.reload_count = 0
    
    def start(self):
        """Start background watcher thread."""
        self.running = True
        self.thread = threading.Thread(target=self._watch, daemon=True)
        self.thread.start()
        print(f"🔱 DHARMA WATCHDOG: Monitoring {self.policy_path} for changes")
    
    def stop(self):
        """Stop the watcher."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def _watch(self):
        """Background loop: check for file changes and reload."""
        while self.running:
            try:
                current_mtime = os.path.getmtime(self.policy_path)
                if current_mtime != self.last_mtime:
                    self.last_mtime = current_mtime
                    self._reload()
            except FileNotFoundError:
                pass  # Policy file not yet created
            except Exception as e:
                print(f"⚠️ DHARMA WATCHDOG ERROR: {e}")
            
            time.sleep(self.check_interval)
    
    def _reload(self):
        """Hot-reload policies without dropping detection."""
        import yaml
        try:
            with open(self.policy_path, 'r') as f:
                new_policies = yaml.safe_load(f)
            
            # Atomic swap — no gap in coverage
            self.parser.policies = new_policies
            self.reload_count += 1
            
            yama_count = len(new_policies.get('yamas', []))
            niyama_count = len(new_policies.get('niyamas', []))
            
            print(f"🔱 DHARMA RELOAD #{self.reload_count}: "
                  f"{yama_count} Yamas, {niyama_count} Niyamas loaded")
            
        except Exception as e:
            print(f"⚠️ DHARMA RELOAD FAILED — keeping current policies: {e}")
    
    def status(self):
        """Return watchdog status."""
        return {
            "running": self.running,
            "policy_file": self.policy_path,
            "reload_count": self.reload_count,
            "last_check": time.time()
        }
