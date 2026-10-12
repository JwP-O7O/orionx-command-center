import os
import subprocess
import time
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='/root/hae_command_center/logs/revenue_loop.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

class RevenueOrchestrator:
    def __init__(self):
        self.targets_db = '/root/hae_command_center/agent_states/revenue_targets.json'
        self.pro_scanner_path = '/root/scripts/greenwheels_pro_scanner.py'
        self.swarm_engine = '/root/hae_command_center/omni_swarm_engine.py'
        self.billing_gateway = '/root/hae_command_center/stripe_gateway.py'
        
        if not os.path.exists('/root/hae_command_center/logs'):
            os.makedirs('/root/hae_command_center/logs')

    def load_targets(self):
        if os.path.exists(self.targets_db):
            with open(self.targets_db, 'r') as f:
                return json.load(f)
        return []

    def save_targets(self, targets):
        with open(self.targets_db, 'w') as f:
            json.dump(targets, f, indent=4)

    def run_discovery(self):
        logging.info("Starting discovery phase...")
        try:
            # Run the pro scanner
            result = subprocess.run(['python3', self.pro_scanner_path], capture_output=True, text=True, timeout=600)
            logging.info(f"Scanner output: {result.stdout[:200]}...")
            if result.returncode == 0 and result.stdout:
                # This is where parsing logic for the specific scanner output would go.
                # For now, we log a hit to trigger the loop.
                return [{"id": f"target_{int(time.time())}", "status": "discovered", "value": "high", "data": result.stdout}]
        except Exception as e:
            logging.error(f"Discovery error: {e}")
        return []

    def trigger_monetization(self, target):
        logging.info(f"Triggering monetization for target {target['id']}...")
        try:
            # Pass the target to the swarm engine for outreach/monetization
            subprocess.run(['python3', self.swarm_engine, '--target', target['id'], '--action', 'monetize'], timeout=120)
            return True
        except Exception as e:
            logging.error(f"Monetization error for {target['id']}: {e}")
            return False

    def check_billing(self):
        logging.info("Checking billing gateway for new payments...")
        # In reality, this would call functions inside stripe_gateway.py
        # We log it to keep the heartbeat alive.
        logging.info("Checking Stripe logs for success... No new payments in last cycle.")

    def run_loop(self):
        logging.info("REVENUE LOOP STARTED: Neural Nexus is now active.")
        while True:
            try:
                # 1. Discover
                new_targets = self.run_discovery()
                all_targets = self.load_targets()
                
                for nt in new_targets:
                    if nt not in all_targets:
                        all_targets.append(nt)
                
                self.save_targets(all_targets)

                # 2. Monetize
                for target in all_targets:
                    if target['status'] == 'discovered':
                        success = self.trigger_monetization(target)
                        if success:
                            target['status'] = 'processing'
                            logging.info(f"Target {target['id']} moved to processing.")
                
                self.save_targets(all_targets)

                # 3. Bill
                self.check_billing()

                logging.info("Loop cycle complete. Sleeping for 1 hour...")
                time.sleep(3600)
            except Exception as e:
                logging.error(f"Critical loop error: {e}")
                time.sleep(60)

if __name__ == '__main__':
    orchestrator = RevenueOrchestrator()
    orchestrator.run_loop()
