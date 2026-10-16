#!/usr/bin/env python3
"""
OrionX Local B2B Outreach Dispatcher (Delft & Den Haag)
=======================================================
Sends hyper-personalized, 100% Dutch Telecommunicatiewet & AVG compliant
invitations to verified professional practices and SMEs in Delft & Den Haag.

Strict Standards:
- Feitelijk, nuchter en uiterst zakelijk (geen speculaties, geen overdreven claims).
- Geen directe betaallinks in koude outreach.
- Verplichte heldere afmeldmogelijkheid.
- Aanbod voor risicovrije 14-dagen proefopstelling op factuur achteraf (€0 vooraf, no-cure-no-pay).
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

# Auto-load .env if not loaded
def load_env_if_needed():
    candidates = [
        BASE_DIR / ".env",
        BASE_DIR.parent / ".env",
        Path("/root/empire/.env"),
        Path("/root/.env")
    ]
    for env_path in candidates:
        if env_path.exists():
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            k, v = line.split('=', 1)
                            k = k.strip()
                            v = v.strip().strip('"').strip("'")
                            if k not in os.environ:
                                os.environ[k] = v
            except Exception:
                pass

load_env_if_needed()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.transip.email")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
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

def format_salutation(contact_raw: str, company: str) -> str:
    contact = contact_raw.strip() if contact_raw else ""
    c_lower = contact.lower()
    
    if not contact or c_lower in ["onbekend", "directie", "management"]:
        return f"Geachte directie van {company},"
    if "vennoten" in c_lower:
        return f"Geachte vennoten van {company},"
    if "vestigingsleiding" in c_lower or "vestigingsmanager" in c_lower:
        return f"Geachte vestigingsleiding van {company},"
    if "kantoordirecteur" in c_lower or "kantoordirectie" in c_lower:
        return f"Geachte kantoordirectie van {company},"
    if "regiomanager" in c_lower:
        return f"Geachte regiomanager van {company},"
    if c_lower.startswith("dhr."):
        name_part = contact[4:].strip()
        return f"Geachte heer {name_part},"
    if c_lower.startswith("mevr."):
        name_part = contact[5:].strip()
        return f"Geachte mevrouw {name_part},"
    if c_lower.startswith("dr.") or c_lower.startswith("drs."):
        return f"Geachte {contact},"
    
    # Split first and last name if regular name
    parts = contact.split()
    if len(parts) >= 2:
        last_name = " ".join(parts[1:])
        return f"Geachte heer/mevrouw {last_name},"
    
    return f"Geachte {contact},"

def build_email_content(lead: dict) -> tuple:
    company = lead.get("company", "uw organisatie").strip()
    contact_raw = lead.get("contact_name") or lead.get("contact") or ""
    salutation = format_salutation(contact_raw, company)
    sector = lead.get("sector", "Zakelijke Dienstverlening").strip()
    city = lead.get("city", "de regio Delft / Den Haag").strip()
    hook = lead.get("hook") or lead.get("pain_point") or "het handmatig verwerken van administratieve documentstromen"

    # Healthcare template
    if any(k in sector.lower() for k in ["tandarts", "fysio", "huisarts", "zorg", "kliniek", "arts", "medisch"]):
        subject = f"Administratieve procesondersteuning voor {company} — OrionX {city}"
        body = f"""{salutation}

Binnen particuliere praktijken en zelfstandige behandelcentra in {city} zien wij dat zorgmedewerkers en praktijkmanagers aanzienlijk worden belast door repeterende administratieve handelingen. Hierbij valt te denken aan het handmatig verwerken van intakeformulieren, het structureren van documentstromen of de telefonische bereikbaarheid tijdens spreekuren.

Vanuit OrionX (gevestigd in de regio Delft en Den Haag) ontwikkelen wij gerichte software-koppelingen en private AI-assistenten. Deze systemen lezen inkomende gegevens automatisch uit en plaatsen deze gestructureerd in uw bestaande praktijksoftware. Alle dataverwerking geschiedt uitsluitend binnen de Europese Unie conform de AVG en de NEN 7510 normering.

Omdat de effectiviteit van automatisering in de praktijk bewezen moet worden, werken wij met een risicovrije 14-dagen pilot:
• Wij richten één specifiek administratief proces binnen uw praktijk volledig werkend in.
• Er zijn geen kosten vooraf (€ 0,-).
• Facturatie geschiedt uitsluitend achteraf op factuur (14 dagen betaaltermijn) indien uw team daadwerkelijk tevreden is met het resultaat.

Wilt u vooraf een indicatie van de potentiële tijdsbesparing binnen uw praktijkgrootte?
📊 U kunt een vrijblijvende berekening maken via onze scan: https://scan.orionx.nl

Schikt het u om komende week 15 minuten telefonisch van gedachten te wisselen over de mogelijkheden voor {company}?

Met vriendelijke groet,

J.W. Pabst
OrionX — AI Procesautomatisering Delft & Den Haag
Telefoon: 015 - 202 4589
E-mail: jwp@orionx.nl | Website: https://orionx.nl

---
Afmelden: Heeft dit onderwerp geen prioriteit voor uw praktijk? Reageer gerust met 'geen interesse' op dit bericht, dan verwijderen wij uw adres direct uit ons bestand.
"""
    else:
        # SME, Accounting & Professional Services template
        subject = f"Document- en factuurverwerking automatiseren bij {company} — OrionX {city}"
        body = f"""{salutation}

Voor administratiekantoren en zakelijke dienstverleners in {city} brengt de periodieke documentaanlevering van cliënten vaak een aanzienlijke administratieve werklast met zich mee. Het handmatig controleren, overtypen en verifiëren van inkomende facturen, declaraties en bonnen kost maandelijks veel tijd die niet declarabel is.

Vanuit OrionX (gevestigd in de regio Delft en Den Haag) leveren wij praktische AI-koppelingen die dit proces digitaliseren: inkomende documenten (per e-mail of upload) worden automatisch uitgelezen, inhoudelijk geverifieerd en direct als kant-en-klaar boekingsvoorstel klaargezet in uw administratiepakket (zoals Exact Online, Twinfield of Afas).

Wij hanteren een transparante werkwijze via een 14-dagen pilot:
• Wij richten de koppeling werkend in voor één specifiek document- of factuurproces binnen uw kantoor.
• Er zijn vooraf geen kosten verschuldigd (€ 0,-).
• Betaling geschiedt pas na 14 dagen op factuur (14 dagen termijn) op basis van no-cure-no-pay: ervaart uw team geen duidelijke tijdswinst, dan betaalt u niets.

Wilt u vooraf een indicatie van de administratieve tijdwinst binnen uw organisatie?
📊 U kunt een indicatieve berekening bekijken via: https://scan.orionx.nl

Zullen we komende week 15 minuten vrijblijvend bellen of op kantoor van gedachten wisselen om te beoordelen of dit voor {company} van meerwaarde is?

Met vriendelijke groet,

J.W. Pabst
OrionX — AI Procesautomatisering Delft & Den Haag
Telefoon: 015 - 202 4589
E-mail: jwp@orionx.nl | Website: https://orionx.nl

---
Afmelden: Stelt u geen prijs op dit bericht? Reageer met 'geen interesse' en uw gegevens worden per direct verwijderd uit ons contactbestand.
"""

    return subject, body

def dispatch_batch(batch_size: int = 10, dry_run: bool = True):
    load_env_if_needed()
    smtp_pass = os.getenv("SMTP_PASS", "")
    smtp_user = os.getenv("SMTP_USER", "jwp@orionx.nl")
    
    tracker = load_tracker()
    leads = []
    
    if MKB_LEADS_FILE.exists():
        with open(MKB_LEADS_FILE, 'r', encoding='utf-8') as f:
            leads.extend(json.load(f))
            
    if ZORG_LEADS_FILE.exists():
        with open(ZORG_LEADS_FILE, 'r', encoding='utf-8') as f:
            leads.extend(json.load(f))

    logger.info(f"Totaal beschikbare leads in database: {len(leads)}")
    
    dispatched_count = 0
    for lead in leads:
        email = lead.get("email", "").strip()
        company = lead.get("company", "Bedrijf").strip()
        
        if not email or "@" not in email:
            continue
            
        if email in tracker:
            continue
            
        subject, body = build_email_content(lead)
        
        if dry_run:
            logger.info(f"[DRY-RUN {dispatched_count+1}/{batch_size}] Naar: {company} <{email}>")
            logger.info(f"             Onderwerp: {subject}")
            dispatched_count += 1
            if dispatched_count >= batch_size:
                break
        else:
            if not smtp_pass:
                logger.error("Geen SMTP_PASS gevonden. Controleer /root/empire/.env.")
                return
                
            try:
                msg = MIMEMultipart("alternative")
                msg["From"] = f'"J.W. Pabst | OrionX" <{smtp_user}>'
                msg["To"] = email
                msg["Reply-To"] = smtp_user
                msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain", "utf-8"))
                
                server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
                server.quit()
                
                tracker[email] = {
                    "company": company,
                    "dispatched_at": datetime.now(timezone.utc).isoformat(),
                    "subject": subject,
                    "status": "sent"
                }
                save_tracker(tracker)
                logger.info(f"✓ [{dispatched_count+1}/{batch_size}] E-mail succesvol verzonden naar: {company} <{email}>")
                dispatched_count += 1
                time.sleep(3.5) # Netjes pauzeren tussen verzendingen
                
                if dispatched_count >= batch_size:
                    break
            except Exception as e:
                logger.error(f"Fout bij verzenden naar {email}: {e}")

    logger.info(f"Verzending afgerond. Totaal verzonden: {dispatched_count} (dry_run={dry_run})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OrionX Local B2B Outreach Dispatcher")
    parser.add_argument("--batch", type=int, default=10, help="Aantal e-mails om te verwerken")
    parser.add_argument("--send", action="store_true", help="Daadwerkelijk verzenden via TransIP SMTP")
    args = parser.parse_args()
    
    dispatch_batch(batch_size=args.batch, dry_run=not args.send)
