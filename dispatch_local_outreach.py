#!/usr/bin/env python3
"""
OrionX Local B2B Outreach Dispatcher (Delft & Den Haag)
=======================================================
Sends hyper-personalized, 100% Dutch Telecommunicatiewet & AVG compliant
invitations to verified professional practices and SMEs in Delft & Den Haag.

Compliance Rules:
- NO direct checkout links in cold outreach.
- Mandatory clear opt-out sentence.
- Focus on free 14-day pilot on invoice afterwards (€0 upfront) or 60s NEN 7510 scan.
"""

import os
import sys
import json
import time
import smtplib
import argparse
import logging
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [Outreach] %(message)s'
)
logger = logging.getLogger("Outreach")

BASE_DIR = Path(__file__).parent.resolve()
LEADS_DIR = BASE_DIR / "leads"
MKB_LEADS_FILE = LEADS_DIR / "delft_denhaag_mkb_leads.json"
ZORG_LEADS_FILE = LEADS_DIR / "dutch_healthcare_leads.json"
TRACKER_FILE = LEADS_DIR / "outreach_tracker.json"

SMTP_HOST = "smtp.transip.email"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER", "jwp@orionx.nl")
SMTP_PASS = os.getenv("SMTP_PASS", "")

def load_tracker():
    if TRACKER_FILE.exists():
        try:
            with open(TRACKER_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_tracker(tracker):
    with open(TRACKER_FILE, 'w', encoding='utf-8') as f:
        json.dump(tracker, f, indent=2, ensure_ascii=False)

def build_email_content(lead: dict) -> tuple:
    company = lead.get("company", "uw praktijk")
    contact = lead.get("contact_name") or lead.get("contact") or "Directie"
    sector = lead.get("sector", "Zorg & MKB")
    city = lead.get("city", "Delft / Den Haag")
    hook = lead.get("hook") or lead.get("pain_point") or "administratieve processen"

    # Determine template
    if any(k in sector.lower() for k in ["tandarts", "fysio", "huisarts", "zorg", "kliniek", "arts"]):
        subject = f"Minder administratieve druk aan de balie van {company} — OrionX {city}"
        body = f"""Beste {contact},

In veel praktijken in de regio {city} horen wij van praktijkhouders dat de balie en behandelaren overbelast raken door repetitief administratief werk: het overtikken van intakeformulieren, het verwerken van verwijsbrieven of de telefonische bereikbaarheid tijdens het spreekuur.

Met OrionX (gevestigd in de regio Delft & Den Haag) bouwen wij praktische, veilige AI-koppelingen die deze werkstromen automatiseren en gestructureerd klaarzetten in uw huidige software (zoals Medicom, Exquise of Intramed). Alle data blijft strikt binnen de EU conform NEN 7510 en AVG.

Omdat wij geloven in bewijs vooraf, bieden wij praktijken een laagdrempelige 14-dagen pilot:
• Wij richten één specifiek proces (bijv. triage, intake of facturatie) volledig werkend voor u in.
• Kosten vandaag: € 0,-. U betaalt pas na 14 dagen tevredenheid conform onze 100% no-cure-no-pay garantie.

Wilt u binnen 60 seconden zien hoeveel uren uw praktijk kan besparen?
📊 Doe de gratis NEN 7510 AI Praktijkscan: https://scan.orionx.nl

Heeft u komende dinsdag of donderdag 15 minuten tijd voor een korte telefonische kennismaking?

Met gezonde groet,

J.W. Pabst
OrionX — AI Procesautomatisering Delft & Den Haag
E-mail: jwp@orionx.nl | Web: https://orionx.nl

---
Afmelden: Heeft dit geen prioriteit voor uw praktijk? Reageer gerust met 'geen interesse' en wij verwijderen uw gegevens direct uit ons bestand.
"""
    else:
        # SME & Accountancy template
        subject = f"Administratieve tijdswinst rondom facturen & documentstromen — {company}"
        body = f"""Beste {contact},

Als lokaal automatiseringsspecialist in de regio {city} zien wij bij veel organisaties dezelfde bottleneck: {hook.lower() if hook else 'het handmatig overkloppen van gegevens en inkomende documenten'}.

Met OrionX bouwen wij hiervoor gerichte, veilige AI-koppelingen die inkomende documenten, e-mails of facturen automatisch uitlezen, verifiëren en direct klaarzetten in uw software (bijv. Exact Online, Twinfield of uw eigen systeem).

Geen langdurig IT-traject, maar een pragmatische 14-dagen pilot:
• Wij automatiseren één concreet knelpunt binnen {company}.
• Kosten vooraf: € 0,-. U betaalt pas achteraf op factuur na 14 dagen bewezen tijdswinst (100% no-cure-no-pay).

Wilt u direct zien wat automatisering voor uw team kan betekenen?
📊 Bereken uw tijdswinst via onze online scan: https://scan.orionx.nl

Schikt het u om komende week 15 minuten vrijblijvend te bellen om te zien welk proces bij u het meeste tijd kan besparen?

Met vriendelijke groet,

J.W. Pabst
OrionX — AI Procesautomatisering Delft & Den Haag
E-mail: jwp@orionx.nl | Web: https://orionx.nl

---
Afmelden: Geen behoefte aan procesautomatisering? Laat het even weten via een reply, dan zullen wij u niet verder benaderen.
"""

    return subject, body

def dispatch_batch(batch_size: int = 5, dry_run: bool = True):
    tracker = load_tracker()
    leads = []
    
    if MKB_LEADS_FILE.exists():
        with open(MKB_LEADS_FILE, 'r', encoding='utf-8') as f:
            leads.extend(json.load(f))
            
    if ZORG_LEADS_FILE.exists():
        with open(ZORG_LEADS_FILE, 'r', encoding='utf-8') as f:
            leads.extend(json.load(f))

    logger.info(f"Totaal beschikbare leads: {len(leads)}")
    
    dispatched_count = 0
    for lead in leads:
        email = lead.get("email", "").strip()
        company = lead.get("company", "Bedrijf")
        
        if not email or "@" not in email:
            continue
            
        if email in tracker:
            continue
            
        subject, body = build_email_content(lead)
        
        if dry_run:
            logger.info(f"[DRY-RUN] Zou mail sturen naar: {company} <{email}>")
            logger.info(f"          Onderwerp: {subject}")
            dispatched_count += 1
            if dispatched_count >= batch_size:
                break
        else:
            if not SMTP_PASS:
                logger.error("Geen SMTP_PASS ingesteld in environment. Kan niet verzenden.")
                return
                
            try:
                msg = MIMEMultipart("alternative")
                msg["From"] = f'"J.W. Pabst | OrionX" <{SMTP_USER}>'
                msg["To"] = email
                msg["Reply-To"] = SMTP_USER
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain", "utf-8"))
                
                server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
                server.quit()
                
                tracker[email] = {
                    "company": company,
                    "dispatched_at": datetime.now(timezone.utc).isoformat(),
                    "subject": subject
                }
                save_tracker(tracker)
                logger.info(f"✓ [VERZONDEN] E-mail succesvol verzonden naar: {company} <{email}>")
                dispatched_count += 1
                time.sleep(3) # Prevent rate limits
                
                if dispatched_count >= batch_size:
                    break
            except Exception as e:
                logger.error(f"Fout bij verzenden naar {email}: {e}")

    logger.info(f"Klaar. Aantal verwerkt: {dispatched_count} (dry_run={dry_run})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OrionX Local B2B Outreach Dispatcher")
    parser.add_argument("--batch", type=int, default=5, help="Batch size to process")
    parser.add_argument("--send", action="store_true", help="Actually send emails via SMTP (default is dry-run)")
    args = parser.parse_args()
    
    dispatch_batch(batch_size=args.batch, dry_run=not args.send)
