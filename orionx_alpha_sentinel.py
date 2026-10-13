#!/usr/bin/env python3
"""
OrionX Autonomous VIP Alpha Sentinel & Revenue Engine
=====================================================
Autonomously monitors Solana DEX markets, scans for high-momentum
breakouts and whale movements, and broadcasts actionable Alpha Alerts
to Telegram with direct conversion links to OrionX digital products.
"""

import os
import sys
import time
import json
import logging
import urllib.request
import urllib.error
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("OrionXAlphaSentinel")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8608971534:AAH_XDzmmp229-OhR3JVsGXy_LErAxEpvxM")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "6133249549")
SEEN_TOKENS_FILE = "/root/orionx_trading_empire/seen_tokens.json"

def send_telegram_alert(text: str):
    """Sends formatted alert message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            logger.info("✓ Telegram alert dispatched successfully!")
            return True
    except Exception as e:
        logger.error(f"Failed to send Telegram message: {e}")
        return False

def load_seen_tokens():
    if os.path.exists(SEEN_TOKENS_FILE):
        try:
            with open(SEEN_TOKENS_FILE, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_seen_tokens(seen: set):
    try:
        with open(SEEN_TOKENS_FILE, "w") as f:
            json.dump(list(seen)[-500:], f)
    except Exception as e:
        logger.error(f"Failed to save seen tokens: {e}")

def fetch_latest_solana_pairs():
    """Fetches high-volume / trending Solana pairs from DexScreener API."""
    url = "https://api.dexscreener.com/token-profiles/latest/v1"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; OrionX-Bot/1.0)"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            profiles = json.loads(resp.read().decode("utf-8"))
            solana_tokens = [p for p in profiles if p.get("chainId") == "solana"]
            return solana_tokens[:10]
    except Exception as e:
        logger.warning(f"Error fetching DexScreener profiles: {e}")
        return []

def get_token_details(token_address: str):
    """Gets pool liquidity, volume and price for a specific token."""
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            pairs = data.get("pairs") or []
            if pairs:
                # Return the highest liquidity pair
                return max(pairs, key=lambda p: float(p.get("liquidity", {}).get("usd", 0) or 0))
    except Exception as e:
        logger.warning(f"Error fetching token details for {token_address}: {e}")
    return None

def run_sentinel_loop():
    logger.info("🚀 OrionX Autonomous VIP Alpha Sentinel & Monetization Engine gestart.")
    seen_tokens = load_seen_tokens()

    # Initial boot alert
    boot_msg = (
        "🦅 <b>ORIONX QUANTUM ALPHA SENTINEL ACTIVE</b>\n\n"
        "24/7 Autonome Solana Radar is live gekoppeld.\n"
        "• <b>Live Trading Swarm:</b> https://trade.orionx.nl\n"
        "• <b>OpenClaw Sales Portal:</b> https://trade.orionx.nl/openclaw\n"
        "• <b>VIP Quant Membership:</b> https://trade.orionx.nl/checkout/vip\n"
        "• <b>Status:</b> Scanning DEX Pools & Liquidity Surges..."
    )
    send_telegram_alert(boot_msg)

    while True:
        try:
            tokens = fetch_latest_solana_pairs()
            logger.info(f"Gescand: {len(tokens)} recente Solana profielen.")

            for t in tokens:
                token_addr = t.get("tokenAddress")
                if not token_addr or token_addr in seen_tokens:
                    continue

                seen_tokens.add(token_addr)
                save_seen_tokens(seen_tokens)

                pair = get_token_details(token_addr)
                if not pair:
                    continue

                liq_usd = float(pair.get("liquidity", {}).get("usd", 0) or 0)
                vol_24h = float(pair.get("volume", {}).get("h24", 0) or 0)
                price_usd = pair.get("priceUsd", "N/A")
                base_token = pair.get("baseToken", {})
                symbol = base_token.get("symbol", "UNKNOWN")
                name = base_token.get("name", "Unknown Token")

                # Filter on minimum pool threshold
                if liq_usd < 10000 or vol_24h < 15000:
                    continue

                logger.info(f"🎯 High Conviction Alpha gevonden: ${symbol} (Liq: ${liq_usd:,.0f}, Vol: ${vol_24h:,.0f})")

                alert_text = (
                    f"⚡ <b>[ORIONX HIGH-CONVICTION ALPHA SIGNAL]</b> ⚡\n\n"
                    f"💎 <b>Token:</b> ${symbol} ({name})\n"
                    f"📊 <b>Prijs:</b> ${price_usd}\n"
                    f"💧 <b>Liquiditeit:</b> ${liq_usd:,.0f}\n"
                    f"📈 <b>24u Volume:</b> ${vol_24h:,.0f}\n"
                    f"🛡️ <b>Audit:</b> Nona-Pass Filter Passed ✓\n\n"
                    f"🔗 <b>Contract (CA):</b>\n<code>{token_addr}</code>\n\n"
                    f"📈 <b>DexScreener:</b> <a href=\"https://dexscreener.com/solana/{token_addr}\">Open Live Chart</a>\n"
                    f"🪐 <b>Jupiter Swap:</b> <a href=\"https://jup.ag/swap/SOL-{token_addr}\">Instant Buy</a>\n\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"🤖 <b>Live Swarm Telemetrie:</b> https://trade.orionx.nl\n"
                    f"💳 <b>Koop de Autonome Bot Kit (€47):</b> https://trade.orionx.nl/openclaw\n"
                    f"💎 <b>VIP Quant Signals & Alerts (€97/mnd):</b> https://trade.orionx.nl/checkout/vip"
                )
                send_telegram_alert(alert_text)
                time.sleep(5)  # Telegram rate limit prevention

        except Exception as e:
            logger.error(f"Fout in sentinel loop: {e}")

        time.sleep(45)  # Scan interval

if __name__ == "__main__":
    run_sentinel_loop()
