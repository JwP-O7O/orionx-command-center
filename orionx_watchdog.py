#!/usr/bin/env python3
"""
OrionX Self-Healing Uptime Watchdog
==================================
Monitors all core services, automatically restarts them if crashed,
and sends real-time recovery notifications via Telegram.
"""

import time
import subprocess
import urllib.request
import json
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("OrionXWatchdog")

TELEGRAM_BOT_TOKEN = "8608971534:AAH_XDzmmp229-OhR3JVsGXy_LErAxEpvxM"
TELEGRAM_CHAT_ID = "6133249549"

SERVICES = [
    {"name": "nginx", "type": "systemd", "check": "systemctl is-active nginx"},
    {"name": "openclaw-portal.service", "type": "http", "url": "http://127.0.0.1:8899/health"},
    {"name": "agency-swarm.service", "type": "http", "url": "http://127.0.0.1:8000/api/agents"},
    {"name": "orionx-alpha-sentinel.service", "type": "systemd", "check": "systemctl is-active orionx-alpha-sentinel.service"},
    {"name": "orionx-promoter.service", "type": "systemd", "check": "systemctl is-active orionx-promoter.service"}
]

def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        logger.error(f"Telegram error: {e}")

def check_and_heal():
    for s in SERVICES:
        name = s["name"]
        healthy = False

        if s["type"] == "systemd":
            res = subprocess.run(s["check"], shell=True, capture_output=True, text=True)
            if res.stdout.strip() == "active":
                healthy = True
        elif s["type"] == "http":
            try:
                req = urllib.request.Request(s["url"], headers={"User-Agent": "Watchdog/1.0"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    if resp.status == 200:
                        healthy = True
            except Exception:
                healthy = False

        if not healthy:
            logger.warning(f"🚨 [SERVICE UNHEALTHY] {name} is down! Restarting...")
            subprocess.run(f"systemctl restart {name}", shell=True)
            time.sleep(2)
            # Verify recovery
            verify = subprocess.run(f"systemctl is-active {name}", shell=True, capture_output=True, text=True)
            if verify.stdout.strip() == "active":
                logger.info(f"✓ {name} successfully self-healed!")
                send_telegram(f"🛡️ <b>[ORIONX SELF-HEALING NOTIFICATIE]</b>\n\nDienst <code>{name}</code> was onbereikbaar en is zojuist <b>automatisch herstart en hersteld</b> door de Watchdog.")
            else:
                logger.error(f"❌ Kon {name} niet herstellen!")
                send_telegram(f"🚨 <b>[ORIONX ALARM]</b>\n\nDienst <code>{name}</code> kon niet worden hersteld. Handmatige inspectie vereist!")

def main():
    logger.info("🛡️ OrionX Self-Healing Watchdog gestart.")
    while True:
        try:
            check_and_heal()
        except Exception as e:
            logger.error(f"Watchdog loop error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()
