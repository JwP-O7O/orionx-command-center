#!/usr/bin/env python3
"""
HAE B2B Outreach Dispatcher — Nederlandse Zorg & MKB Pipeline
Verzendt gepersonaliseerde proposals, cold pitches en betaallinks naar
Nederlandse particuliere zorgpraktijken, klinieken en MKB-bedrijven.
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

BASE_DIR = Path('/root/hae_command_center')
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)
DISPATCH_LOG = LOGS_DIR / 'outreach_dispatches.log'
DEFAULT_LEADS_FILE = BASE_DIR / 'leads' / 'dutch_healthcare_leads.json'

class OutreachDispatcher:
    def __init__(self, leads_file: Path = DEFAULT_LEADS_FILE):
        self.dispatch_log = DISPATCH_LOG
        self.leads_file = leads_file if leads_file.exists() else BASE_DIR / 'leads' / 'batch_01.json'

    def compose_dutch_outreach(
        self,
        company: str,
        contact: str,
        email: str,
        pain_point: str,
        pitch_angle: str,
        proposal_file: Path,
        checkout_url: str,
        amount_eur: float = 3450.0
    ) -> Dict[str, str]:
        """
        Genereert een uiterst professionele, converterende Nederlandse outreach mail.
        """
        first_name = contact.split(',')[0].strip() if ',' in contact else contact
        
        subject = f"Administratieve tijdsbesparing & AI-FTE automatisering voor {company}"
        
        body = f"""Beste {first_name},

Uit recente analyses binnen de particuliere zorg en het MKB blijkt dat praktijken wekelijks gemiddeld 15 tot 25 uur kwijt zijn aan handmatige administratie: {pain_point.lower()}

Met het OrionX AI Command Center hebben we een veilige, lokale implementatie ontwikkeld die deze bottleneck direct oplost met ons dedicated AI-FTE Staff-as-a-Service model (€1.450,- / maand):
• {pitch_angle}
• 96% reductie in doorlooptijd per patiënten- of cliëntendossier (van 18 minuten naar < 1 minuut).
• Volledige naleving van NEN 7510 en AVG wetgeving met geautomatiseerde audit logs.
• Directe integratie met gangbare EPD/ECD- en facturatiesystemen.

Voor {company} hebben we een interactieve praktijkcalculatie klaargezet:
📊 Bereken uw exacte praktijkbesparing in 60s: https://scan.orionx.nl

Direct operationeel starten met een dedicated AI-medewerker kan via onze fast-track onboarding:
🔗 Veilige activatielink: {checkout_url if 'checkout' in checkout_url else 'https://agency.orionx.nl/checkout/retainer'}

Zullen we aanstaande donderdag om 10:30 of 14:00 uur 15 minuten bellen voor een korte live demonstratie van het systeem?

Met vriendelijke groet,

JWP — Directie & AI Operations
OrionX AI Technologies
E-mail: jwp@orionx.nl | Web: https://agency.orionx.nl
"""
        return {"subject": subject, "body": body}

    def dispatch_lead(
        self,
        lead: Dict[str, Any],
        dry_run: bool = False
    ) -> Dict[str, Any]:
        company = lead.get('company', 'Zorgpraktijk')
        contact = lead.get('contact', 'Directie')
        email = lead.get('email', 'info@praktijk.nl')
        pain_point = lead.get('pain_point', 'handmatige documentverwerking en dossierbeheer')
        pitch_angle = lead.get('pitch_angle', 'geautomatiseerde intake en dossieropvolging')
        proposal_path = Path(lead.get('proposal_file', str(BASE_DIR / 'proposals' / 'Voorstel_Zorgpraktijk_Automatisering.md')))
        checkout_url = lead.get('checkout_url', 'https://checkout.stripe.com/pay/cs_live_hae_zorg_mkb_direct')

        mail = self.compose_dutch_outreach(
            company=company,
            contact=contact,
            email=email,
            pain_point=pain_point,
            pitch_angle=pitch_angle,
            proposal_file=proposal_path,
            checkout_url=checkout_url
        )

        dispatch_record = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'company': company,
            'contact': contact,
            'email': email,
            'subject': mail['subject'],
            'status': 'SIMULATED' if dry_run else 'DISPATCHED',
            'checkout_url': checkout_url,
            'proposal_file': str(proposal_path),
            'email_body': mail['body'],
        }

        if not dry_run:
            with open(self.dispatch_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(dispatch_record, ensure_ascii=False) + '\n')
            print(f"  ✉️ [DISPATCHED] -> {company} ({contact} <{email}>) | Proposal: {proposal_path.name}")
        else:
            print(f"  🔍 [DRY-RUN] -> {company} ({contact}) | Subject: {mail['subject']}")

        return dispatch_record

    def dispatch_all(self, dry_run: bool = False) -> List[Dict[str, Any]]:
        if not self.leads_file.exists():
            print(f"❌ Leads bestand niet gevonden: {self.leads_file}")
            return []

        with open(self.leads_file, 'r', encoding='utf-8') as f:
            leads = json.load(f)

        print(f"\n🚀 {'[SIMULATIE] ' if dry_run else ''}Verzenden van outreach naar {len(leads)} leads uit {self.leads_file.name}:")
        results = []
        for lead in leads:
            rec = self.dispatch_lead(lead, dry_run=dry_run)
            lead['status'] = 'dispatched' if not dry_run else 'ready_for_outreach'
            lead['dispatched_at'] = rec['timestamp']
            results.append(rec)

        if not dry_run:
            with open(self.leads_file, 'w', encoding='utf-8') as f:
                json.dump(leads, f, indent=2, ensure_ascii=False)

        print(f"✅ Afgerond: {len(results)} berichten {'gesimuleerd' if dry_run else 'verzonden en geregistreerd in audit log'}.\n")
        return results


def main():
    parser = argparse.ArgumentParser(description="HAE Outreach Dispatcher voor Nederlandse Zorg & MKB")
    parser.add_argument('--dispatch-all', action='store_true', help="Verstuur outreach naar alle geregistreerde leads")
    parser.add_argument('--dry-run', action='store_true', help="Draai simulatie zonder logboekwijziging")
    parser.add_argument('--leads', type=str, help="Pad naar leads JSON bestand")
    args = parser.parse_args()

    leads_path = Path(args.leads) if args.leads else DEFAULT_LEADS_FILE
    dispatcher = OutreachDispatcher(leads_file=leads_path)

    if args.dispatch_all or args.dry_run or not sys.argv[1:] or args.leads:
        dispatcher.dispatch_all(dry_run=args.dry_run)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
