#!/usr/bin/env python3
"""
OrionX Autonomous Promotion & Customer Acquisition Engine
=========================================================
24/7 Autonomous marketing supervisor that drives customer acquisition:
1. Automated B2B Outreach Pipeline (Dutch Clinics, Healthcare & SMEs)
2. Real-time Multi-Platform Content Syndication (Twitter/X, Reddit, LinkedIn)
3. Telegram VIP Broadcast & Alpha Alerts via @AgentO7Obot
4. Public Syndication Feed & RSS Generation (for Buffer, Zapier, IFTTT)
5. Lead Magnet Conversion & Notification Dispatch
"""

import os
import sys
import json
import time
import urllib.request
import logging
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

# Setup logging
LOG_FORMAT = '%(asctime)s [%(levelname)s] [OrionXPromoter] %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("OrionXPromoter")

TELEGRAM_BOT_TOKEN = "8608971534:AAH_XDzmmp229-OhR3JVsGXy_LErAxEpvxM"
TELEGRAM_CHAT_ID = "6133249549"

# TransIP Live Authenticated SMTP Configuration
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.transip.email")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "jwp@orionx.nl")
SMTP_PASS = os.environ.get("SMTP_PASS", "TheHagueO7O-")

BASE_DIR = Path(__file__).resolve().parent
# Resolve Hetzner vs local layout
HAE_DIR = BASE_DIR / "hae_command_center" if (BASE_DIR / "hae_command_center").exists() else Path("/root/empire/hae_command_center")
if not HAE_DIR.exists():
    HAE_DIR = Path("/root/hae_command_center")

LOGS_DIR = HAE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
PROMOTER_LOG = LOGS_DIR / "promoter.log"
FEED_FILE = HAE_DIR / "promotions_feed.json"
RSS_FILE = HAE_DIR / "promotions_rss.xml"
LEADS_FILE = HAE_DIR / "leads" / "dutch_healthcare_leads.json"
DISPATCH_LOG = LOGS_DIR / "outreach_dispatches.log"

def send_telegram(text: str, disable_preview: bool = False) -> bool:
    """Dispatches a formatted notification to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": disable_preview
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return True
    except Exception as e:
        logger.error(f"Telegram dispatch error: {e}")
def check_domain_has_mx(email: str) -> bool:
    """Verifies that the target email's domain has active MX records before sending to prevent bounces."""
    try:
        domain = email.split("@")[1].strip()
        url = f"https://dns.google/resolve?name={domain}&type=MX"
        req = urllib.request.Request(url, headers={"User-Agent": "OrionX-MXChecker"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return bool(data.get("Answer"))
    except Exception as e:
        logger.warning(f"MX lookup error for {email}: {e}")
        return False

def send_b2b_email(to_email: str, contact: str, company: str, pain_point: str, pitch_angle: str) -> bool:
    """Sends a professional, factual B2B outreach email via authenticated TransIP SMTP."""
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = f'"J.W. Pabst | OrionX AI Technologies" <{SMTP_USER}>'
        msg["To"] = to_email
        msg["Reply-To"] = SMTP_USER
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="orionx.nl")
        msg["Subject"] = f"Administratieve procesautomatisering & NEN 7510 voor {company}"

        text_content = f"""Geachte {contact},

Binnen zelfstandige behandelcentra en gespecialiseerde praktijken zien wij dat administratieve lasten rondom patiëntintakes, documentverwerking en dossierbeheer wekelijks tientallen uren opeisen van het team.

Voor {company} hebben wij een gerichte analyse uitgevoerd naar praktische procesautomatisering:
- Focuspunt: {pain_point}
- Oplossing: {pitch_angle}

Onze systemen draaien op beveiligde, Europese ISO 27001-gecertificeerde infrastructuur conform de NEN 7510 en AVG kwaliteitsnormen. Patiëntgegevens verlaten de EU niet en worden strikt conform medische geheimhouding verwerkt.

Wilt u inzicht in de concrete tijds- en kostenbesparing voor uw praktijk? U kunt via onze beveiligde omgeving direct een vrijblijvende calculatie maken:
https://scan.orionx.nl

Mocht u liever een korte toelichting van 15 minuten wensen, dan beantwoorden wij deze e-mail graag om een geschikt moment af te stemmen.

Met vriendelijke groet,

J.W. Pabst
OrionX AI Technologies
E-mail: jwp@orionx.nl | Web: https://orionx.nl
Gevestigd te Den Haag

Dit bericht is gericht aan de directie of praktijkleiding van {company}. Wilt u geen verdere communicatie ontvangen? Beantwoord deze e-mail gerust met 'afmelden'.
"""

        html_content = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; max-width: 620px; margin: 0 auto; padding: 24px; background-color: #ffffff;">
  
  <div style="border-bottom: 2px solid #0284c7; padding-bottom: 14px; margin-bottom: 24px;">
    <h2 style="margin: 0; color: #0f172a; font-size: 20px; letter-spacing: -0.5px;">OrionX AI Technologies</h2>
    <p style="margin: 4px 0 0 0; color: #64748b; font-size: 13px;">Praktijk- &amp; Procesautomatisering | NEN 7510 &amp; AVG Compliant</p>
  </div>

  <p style="font-size: 15px; margin-bottom: 16px;">Geachte {contact},</p>

  <p style="font-size: 14px; color: #334155; margin-bottom: 14px;">
    Binnen zelfstandige behandelcentra en gespecialiseerde praktijken zien wij dat administratieve lasten rondom patiëntintakes, documentverwerking en dossierbeheer wekelijks tientallen kostbare uren van het team opeisen.
  </p>

  <p style="font-size: 14px; color: #334155; margin-bottom: 14px;">
    Voor <strong>{company}</strong> hebben wij een gerichte analyse uitgevoerd naar praktische procesautomatisering:
  </p>

  <div style="background-color: #f8fafc; border-left: 4px solid #0284c7; padding: 14px 18px; margin: 18px 0; border-radius: 4px;">
    <p style="margin: 0 0 6px 0; font-weight: 600; color: #0f172a; font-size: 14px;">Focuspunt: {pain_point}</p>
    <p style="margin: 0; color: #475569; font-size: 13px; line-height: 1.5;">{pitch_angle}</p>
  </div>

  <p style="font-size: 14px; color: #334155; margin-bottom: 14px;">
    Onze systemen draaien op beveiligde, Europese ISO 27001-gecertificeerde infrastructuur conform de <strong>NEN 7510</strong> en <strong>AVG</strong> kwaliteitsnormen. Patiëntgegevens verlaten de EU niet en worden strikt conform medische geheimhouding verwerkt.
  </p>

  <p style="font-size: 14px; color: #334155; margin-bottom: 20px;">
    Wilt u inzicht in de concrete tijds- en kostenbesparing voor uw praktijk? U kunt via onze beveiligde omgeving direct een vrijblijvende calculatie maken:
  </p>

  <div style="text-align: left; margin: 24px 0;">
    <a href="https://scan.orionx.nl" style="background-color: #0284c7; color: #ffffff; padding: 12px 22px; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 14px; display: inline-block;">
      Bereken Praktijkbesparing &rarr;
    </a>
  </div>

  <p style="font-size: 14px; color: #334155; margin-bottom: 24px;">
    Mocht u liever een korte toelichting van 15 minuten wensen, dan beantwoorden wij deze e-mail graag om een geschikt moment af te stemmen.
  </p>

  <div style="border-top: 1px solid #e2e8f0; padding-top: 18px; margin-top: 28px;">
    <p style="margin: 0; font-weight: 600; color: #0f172a; font-size: 14px;">J.W. Pabst</p>
    <p style="margin: 2px 0; color: #64748b; font-size: 13px;">OrionX AI Technologies</p>
    <p style="margin: 2px 0; color: #64748b; font-size: 13px;">E-mail: <a href="mailto:jwp@orionx.nl" style="color: #0284c7; text-decoration: none;">jwp@orionx.nl</a> | Web: <a href="https://orionx.nl" style="color: #0284c7; text-decoration: none;">orionx.nl</a></p>
  </div>

  <p style="margin-top: 24px; font-size: 11px; color: #94a3b8; line-height: 1.4;">
    Dit bericht is uitsluitend gericht aan de directie of praktijkleiding van {company}. Wilt u geen verdere communicatie ontvangen? Beantwoord deze e-mail gerust met het woord 'afmelden', waarna uw gegevens direct worden verwijderd.
  </p>
</body>
</html>"""

        msg.attach(MIMEText(text_content, "plain", "utf-8"))
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.starttls(context=context)
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [to_email], msg.as_string())

        logger.info(f"✓ E-mail SUCCESVOL verzonden via TransIP naar {company} ({to_email})")
        return True
    except Exception as e:
        logger.error(f"Fout bij verzenden naar {to_email}: {e}")
        return False

class OrionXPromotionEngine:
    def __init__(self):
        self.leads_file = LEADS_FILE
        self.dispatch_log = DISPATCH_LOG
        self.feed_file = FEED_FILE
        self.rss_file = RSS_FILE

    def generate_syndication_assets(self) -> Dict[str, Any]:
        """Generates comprehensive social syndication feeds and writes to disk."""
        now_iso = datetime.now(timezone.utc).isoformat()
        now_rfc = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

        feed_data = {
            "status": "online",
            "last_updated": now_iso,
            "engine": "OrionX Autonomous Promotion Engine v2.0",
            "active_promos": [
                {
                    "code": "ORIONLAUNCH",
                    "label": "Officiële Lanceringsactie 2026",
                    "discount": "Levenslange Toegang + Updates",
                    "product": "OpenClaw Solana AI Trading Kit",
                    "price_eur": 47.0,
                    "checkout_url": "https://trade.orionx.nl/checkout"
                },
                {
                    "code": "VIPSWARM",
                    "label": "VIP Quant Alpha Club",
                    "discount": "Yellowstone gRPC Sub-80ms Breakout Radar",
                    "product": "OrionX VIP Solana Signals & Terminal",
                    "price_eur": 97.0,
                    "checkout_url": "https://trade.orionx.nl/checkout/vip"
                },
                {
                    "code": "AIFTE",
                    "label": "Dedicated AI-FTE Retainer",
                    "discount": "96% Minder Administratie, NEN 7510 & AVG",
                    "product": "OrionX AI-FTE Staff-as-a-Service",
                    "price_eur": 1450.0,
                    "checkout_url": "https://agency.orionx.nl/checkout/retainer"
                }
            ],
            "campaigns": {
                "twitter": [
                    {
                        "id": "TW-01",
                        "title": "Autonomous 3-Agent Solana MEV Swarm Blueprint",
                        "tweets": [
                            "1/6 🧵 Ik heb een autonoom AI trading agent netwerk gebouwd voor Solana memecoins op Pump.fun. 0 slaaptekort, strikte 2% risicobeheersing, 24/7 execution 👇",
                            "2/6 Handmatig snipen is kansloos tegen MEV bots. Onze AI zwerm draait op cloud VPS met Yellowstone gRPC (<80ms response).",
                            "3/6 De Swarm Triad:\n• SCOUT: Filtert bonding curves & dev wallet %.\n• SNIPER: Jito MEV bundles tegen frontrunning.\n• PUMPTRADER: Trailing stop-loss & take-profit via Kelly Criterion.",
                            "4/6 Emotieloze heuristieken: -30% hard stop-loss, scaling take-profit bij 1.5x en 2x via wiskundig risicomodel.",
                            "5/6 Bekijk de complete live telemetrie van de actieve agents in onze showroom:\n👉 https://trade.orionx.nl",
                            "6/6 De complete gids, productiescripts, SOUL.md templates en Telegram alerts staan nu live in de OpenClaw Kit (€47 eenmalig):\n👉 https://trade.orionx.nl/openclaw"
                        ]
                    },
                    {
                        "id": "TW-02",
                        "title": "Why 98% of Pump.fun Traders Lose Money (And How AI Solves It)",
                        "tweets": [
                            "1/4 🧵 98% van memecoin traders verliezen geld door 3 redenen: MEV frontrunning, slapeloosheid en emotioneel 'diamond handing' tot $0.",
                            "2/4 Algoritmische snipers concurreren met sub-100ms RPCs en private Jito validator bundles. Handmatig klikken is letterlijk liquidity doneren aan bots.",
                            "3/4 Ons antwoord: Een autonome 3-agent zwerm die 24/7 draait op een VPS, risico beperkt tot 2% per trade, en winst mathematisch afroomt.",
                            "4/4 Blueprint + code snippets + productieve SOUL.md templates:\n👉 https://trade.orionx.nl/openclaw"
                        ]
                    }
                ],
                "reddit": [
                    {
                        "id": "RD-01",
                        "subreddits": ["r/solana", "r/CryptoCurrency", "r/SolanaMemeCoins"],
                        "title": "How we built an automated pump.fun sniper workflow that avoids 99% of honeypots (Architecture Breakdown)",
                        "url": "https://trade.orionx.nl/openclaw",
                        "body_preview": "Full architecture breakdown: Yellowstone gRPC Websockets, bytecode static inspection, dynamic sell-simulation before real entry, and Jito bundle tips."
                    },
                    {
                        "id": "RD-02",
                        "subreddits": ["r/Automate", "r/SideProject", "r/Entrepreneur"],
                        "title": "Scaling an Autonomous Multi-Agent B2B & Trading Infrastructure on Hetzner Cloud (NEN 7510 & DeFi)",
                        "url": "https://trade.orionx.nl",
                        "body_preview": "Case study of running high-uptime autonomous agent nodes: Uptime watchdogs, Stripe instant webhook verification, and Telegram dispatcher."
                    }
                ],
                "linkedin": [
                    {
                        "id": "LI-01",
                        "target": "Nederlandse Zorgklinieken, Tandartspraktijken & ZBCs",
                        "title": "Elimineer administratieve bottlenecks in zorg en MKB met autonome AI-FTE agents",
                        "cta_url": "https://scan.orionx.nl",
                        "body": "Zorgpersoneel besteedt wekelijks 20+ uur aan administratie en EPD-invoer. OrionX levert Dedicated AI-FTEs (€1.450/mnd) conform NEN 7510 en AVG, waardoor de intake-verwerkingstijd daalt van 18 min naar <1 minuut."
                    }
                ],
                "telegram": [
                    {
                        "id": "TG-01",
                        "headline": "🚀 ORIONX PROMOTION ENGINE ACTIEF",
                        "body": "De autonome promotie en acquisitie engine draait 24/7 op Hetzner!\n\n• OpenClaw Solana AI Trading Kit: https://trade.orionx.nl/openclaw\n• Live Agent Swarm Showroom: https://trade.orionx.nl\n• VIP Quant Signals (€97/mnd): https://trade.orionx.nl/checkout/vip\n• Gratis AI Besparingsscan: https://scan.orionx.nl\n• B2B AI-FTE Retainer (€1.450/mnd): https://agency.orionx.nl/checkout/retainer"
                    }
                ]
            }
        }

        # Write JSON Feed
        with open(self.feed_file, "w", encoding="utf-8") as f:
            json.dump(feed_data, f, indent=2, ensure_ascii=False)

        # Write RSS Feed
        rss_xml = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>OrionX Promotion &amp; Customer Acquisition Stream</title>
  <link>https://orionx.nl</link>
  <description>Automated syndication drops for OrionX AI Technologies and OpenClaw Solana Swarm</description>
  <lastBuildDate>{now_rfc}</lastBuildDate>
  <item>
    <title>Autonomous 3-Agent Solana Memecoin Swarm Live</title>
    <link>https://trade.orionx.nl/openclaw</link>
    <description>Launch of OpenClaw Solana AI Trading Kit with 24/7 MEV protection and live showroom.</description>
    <pubDate>{now_rfc}</pubDate>
  </item>
  <item>
    <title>VIP Solana Alpha Signals &amp; Neural Swarm Terminal</title>
    <link>https://trade.orionx.nl/checkout/vip</link>
    <description>Sub-80ms Yellowstone gRPC signals and on-chain breakout radar via Telegram for €97/month.</description>
    <pubDate>{now_rfc}</pubDate>
  </item>
  <item>
    <title>Dedicated AI-FTE Staff-as-a-Service voor Zorg &amp; MKB</title>
    <link>https://scan.orionx.nl</link>
    <description>Ontdek binnen 60 seconden hoeveel administratieve uren uw kliniek of praktijk bespaart conform NEN 7510.</description>
    <pubDate>{now_rfc}</pubDate>
  </item>
</channel>
</rss>"""
        self.rss_file.write_text(rss_xml, encoding="utf-8")

        logger.info(f"✓ Syndication feeds opgeslagen: {self.feed_file} en {self.rss_file}")
        return feed_data

    def dispatch_b2b_outreach_batch(self, batch_size: int = 5, dry_run: bool = False) -> List[Dict[str, Any]]:
        """Processes and dispatches next batch of B2B healthcare & SME outreach."""
        if not self.leads_file.exists():
            logger.warning(f"Leads bestand niet gevonden: {self.leads_file}")
            return []

        with open(self.leads_file, "r", encoding="utf-8") as f:
            leads = json.load(f)

        pending_leads = [l for l in leads if l.get("status") in ["ready_for_outreach", "inbound_registered"]]
        if not pending_leads:
            logger.info("Geen openstaande leads gereed voor outreach.")
            return []

        to_dispatch = pending_leads[:batch_size]
        logger.info(f"🚀 Verwerken van {len(to_dispatch)} B2B leads (dry_run={dry_run})...")

        dispatched = []
        for lead in to_dispatch:
            company = lead.get("company", "Zorginstelling")
            contact = lead.get("contact", "Directie")
            email = lead.get("email", "info@bedrijf.nl").strip()
            pain_point = lead.get("pain_point", "handmatige administratieve overlast")
            pitch_angle = lead.get("pitch_angle", "NEN 7510 AI procesautomatisering")
            checkout_url = lead.get("checkout_url", "https://agency.orionx.nl/checkout/retainer")

            # 1. Zero Bounce Protection: Verify Domain MX
            has_mx = check_domain_has_mx(email)
            if not has_mx and not dry_run:
                logger.warning(f"  ⚠️ [OVERGESLAGEN: GEEN MX] {company} ({email}) heeft geen actief mailserver record. Bounce voorkomen!")
                lead["status"] = "skipped_no_mx"
                lead["skip_reason"] = "Domein heeft geen geldig MX record"
                continue

            # 2. Dispatch real email or simulation
            email_sent = False
            if not dry_run:
                email_sent = send_b2b_email(
                    to_email=email,
                    contact=contact,
                    company=company,
                    pain_point=pain_point,
                    pitch_angle=pitch_angle
                )
                time.sleep(5)  # Professional pacing between sends

            record = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "company": company,
                "contact": contact,
                "email": email,
                "subject": f"Administratieve procesautomatisering & NEN 7510 voor {company}",
                "status": "DISPATCHED_LIVE_SMTP" if email_sent else ("SIMULATED" if dry_run else "SEND_FAILED"),
                "checkout_url": checkout_url
            }

            if not dry_run and email_sent:
                lead["status"] = "dispatched"
                lead["dispatched_at"] = record["timestamp"]
                lead["delivery_method"] = "transip_smtp_tls"
                lead["last_autonomous_check"] = record["timestamp"]
                # Append to dispatch log
                with open(self.dispatch_log, "a", encoding="utf-8") as lf:
                    lf.write(json.dumps(record, ensure_ascii=False) + "\n")
                dispatched.append(record)
            elif dry_run:
                dispatched.append(record)

            logger.info(f"  ✉️ {'[SIMULATIE] ' if dry_run else ('[LIVE SMTP VERZONDEN] ' if email_sent else '[MISLUKT] ')}Outreach -> {company} ({contact} <{email}>)")

        if not dry_run:
            with open(self.leads_file, "w", encoding="utf-8") as f:
                json.dump(leads, f, indent=2, ensure_ascii=False)

            # Send Telegram update if any were dispatched
            if dispatched:
                tg_text = (
                    f"📨 <b>[B2B OUTREACH LIVE VERZONDEN VIA TRANSIP]</b>\n\n"
                    f"Er zijn <b>{len(dispatched)} officiële voorstellen</b> succesvol per e-mail bezorgd:\n"
                )
                for d in dispatched:
                    tg_text += f"• <b>{d['company']}</b> ({d['email']})\n"
                tg_text += f"\n📊 Bekijk status in het dashboard: https://orionx.nl/dashboard"
                send_telegram(tg_text)

        return dispatched

    def broadcast_launch_telegram(self):
        """Dispatches official marketing launch announcement to Telegram."""
        text = (
            "🚀 <b>ORIONX TRADING EMPIRE PROMOTIE ENGINE IS LIVE!</b>\n\n"
            "De 24/7 autonome acquisitie & promotie engine is officieel ingeschakeld op de Hetzner server.\n\n"
            "<b>Actieve Componenten:</b>\n"
            "• <b>OpenClaw Sales Portal:</b> https://orionx.nl/openclaw\n"
            "• <b>Live Trading Swarm Showroom:</b> https://orionx.nl/trade\n"
            "• <b>Stripe Checkout (€47,-):</b> https://orionx.nl/checkout\n"
            "• <b>Gratis Besparingsscan:</b> https://orionx.nl/scan\n"
            "• <b>Syndication API Feed:</b> https://orionx.nl/api/promotions/feed\n"
            "• <b>Social RSS Feed:</b> https://orionx.nl/api/promotions/rss.xml\n\n"
            "🔥 <b>Actieve Launchcode:</b> <code>ORIONLAUNCH</code>\n"
            "<i>Alle leads, checkouts en alerts worden nu 24/7 autonoom verwerkt en gerapporteerd.</i>"
        )
        send_telegram(text)
        logger.info("✓ Launch broadcast verzonden naar Telegram!")

    def run_cycle(self):
        """Runs a single autonomous promotion cycle."""
        logger.info("--- Start Promotie Cyclus ---")
        self.generate_syndication_assets()
        # Dispatch small batch of pending leads if any
        self.dispatch_b2b_outreach_batch(batch_size=5, dry_run=False)
        logger.info("--- Promotie Cyclus Afgerond ---")

    def run_daemon(self, interval_seconds: int = 1800):
        """Runs the promoter daemon indefinitely with interval check."""
        logger.info(f"🛡️ OrionX Promotion Daemon gestart (interval: {interval_seconds}s).")
        # First cycle immediate
        self.broadcast_launch_telegram()
        self.run_cycle()

        while True:
            try:
                time.sleep(interval_seconds)
                self.run_cycle()
            except Exception as e:
                logger.error(f"Fout in promoter cyclus: {e}")
                time.sleep(60)

def main():
    parser = argparse.ArgumentParser(description="OrionX Autonomous Promotion & Customer Acquisition Engine")
    parser.add_argument("--daemon", action="store_true", help="Start als 24/7 achtergrond daemon")
    parser.add_argument("--cycle-now", action="store_true", help="Draai 1 volledige promotie cyclus")
    parser.add_argument("--dispatch-all", action="store_true", help="Verstuur outreach naar alle resterende leads")
    parser.add_argument("--broadcast", action="store_true", help="Verstuur launch broadcast naar Telegram")
    parser.add_argument("--dry-run", action="store_true", help="Draai in simulatiemodus")
    parser.add_argument("--interval", type=int, default=1800, help="Daemon interval in seconden (standaard 1800s)")

    args = parser.parse_args()
    engine = OrionXPromotionEngine()

    if args.broadcast:
        engine.broadcast_launch_telegram()
    elif args.dispatch_all:
        engine.dispatch_b2b_outreach_batch(batch_size=100, dry_run=args.dry_run)
    elif args.cycle_now:
        engine.run_cycle()
    elif args.daemon:
        engine.run_daemon(interval_seconds=args.interval)
    else:
        # Default: generate feeds and print summary
        feed = engine.generate_syndication_assets()
        print("=" * 60)
        print("🚀 ORIONX PROMOTION ENGINE STATUS")
        print("=" * 60)
        print(f"Feed JSON: {FEED_FILE}")
        print(f"RSS XML:   {RSS_FILE}")
        print(f"Twitter Campagnes: {len(feed['campaigns']['twitter'])}")
        print(f"Reddit Posts:      {len(feed['campaigns']['reddit'])}")
        print(f"LinkedIn Posts:    {len(feed['campaigns']['linkedin'])}")
        print("\nGebruik --daemon voor 24/7 achtergronduitvoering.")

if __name__ == "__main__":
    main()
