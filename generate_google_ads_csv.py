#!/usr/bin/env python3
"""
ORIONX GOOGLE ADS CAMPAIGN GENERATOR
====================================
Generates 100% valid Google Ads Editor import CSV files for:
1. NL-SEARCH-B2B-Zorgklinieken (High-ticket Healthcare Process Automation)
2. NL-SEARCH-B2B-MKB-Factuur-AI (Mid-ticket SME Invoice & ERP Automation)
3. GLOBAL-SEARCH-Crypto-Solana-TradingBot (Scalable Digital Product - OpenClaw €47)

Strict Google Ads Character Limits:
- Headline: <= 30 chars
- Description: <= 90 chars
- Path 1 & Path 2: <= 15 chars
"""

import csv
import sys
from pathlib import Path

OUTPUT_FILE = Path("/root/hae_command_center/google_ads_import_campaigns.csv")

def validate_length(text: str, max_len: int, name: str):
    if len(text) > max_len:
        raise ValueError(f"Length violation for {name} ({len(text)} > {max_len}): '{text}'")
    return text

# --- DEFINITIONS ---

CAMPAIGNS = [
    {
        "name": "NL-SEARCH-B2B-Zorgklinieken",
        "budget": 25.0,
        "type": "Search",
        "networks": "Google search",
        "languages": "nl",
        "ad_groups": [
            {
                "name": "AG-EPD-Automatisering",
                "cpc": 2.20,
                "keywords": [
                    ("epd automatisering", "Exact"),
                    ("epd automatisering", "Phrase"),
                    ("zorgadministratie automatiseren", "Exact"),
                    ("zorgadministratie software ai", "Phrase"),
                    ("dossier automatisering kliniek", "Exact"),
                    ("intake automatisering zorg", "Phrase"),
                    ("verwijsbrieven verwerken ai", "Exact"),
                    ("declaratieverwerking kliniek", "Phrase")
                ],
                "rsa": {
                    "headlines": [
                        "AI EPD Automatisering Zorg",       # 27 chars
                        "Bespaar 20 Uur Per Week",          # 23 chars
                        "NEN 7510 & AVG Compliant",         # 24 chars
                        "Voor Klinieken & Praktijken",      # 28 chars
                        "Koppelt Met Nedap & Cliniseer",    # 29 chars
                        "Van 18 Min Naar 30 Seconden",      # 27 chars
                        "Bereken Uw Besparing Gratis",      # 27 chars
                        "96% Minder Administratie",         # 24 chars
                        "Terugverdientijd < 2,5 Maand",     # 28 chars
                        "OrionX AI Zorgtechnologie",        # 26 chars
                        "Directe EPD Integratie",           # 22 chars
                        "Geen Handmatig Typewerk Meer",     # 28 chars
                        "Gegarandeerde Databeveiliging",    # 29 chars
                        "Gratis 60-Sec Besparingsscan",     # 29 chars
                        "Kies Voor Autonome Zorg AI"        # 26 chars
                    ],
                    "descriptions": [
                        "Bespaar tot 25 uur per behandelaar per week. Automatiseer EPD intakes & verwijzingen.", # 86 chars
                        "100% NEN 7510 & AVG-proof zorg AI. Direct koppelbaar aan Cliniseer, Nedap & Exquise.", # 86 chars
                        "Bereken exact hoeveel duizenden euro's uw kliniek bespaart in onze gratis 60s scan.",   # 85 chars
                        "Implementatie zonder downtime binnen 14 dagen. Vraag uw strategisch voorstel aan."      # 83 chars
                    ],
                    "path1": "zorg",
                    "path2": "epd-ai",
                    "final_url": "https://orionx.nl/scan"
                }
            },
            {
                "name": "AG-Kliniek-Tandarts-Software",
                "cpc": 1.85,
                "keywords": [
                    ("tandartspraktijk automatisering", "Exact"),
                    ("software tandartspraktijk ai", "Phrase"),
                    ("zbc kliniek administratie", "Exact"),
                    ("zbc administratie software", "Phrase"),
                    ("mondzorg software koppeling", "Exact"),
                    ("vektis declaratie automatisering", "Phrase")
                ],
                "rsa": {
                    "headlines": [
                        "AI Software voor Klinieken",       # 26 chars
                        "Tandarts & ZBC Automatisering",    # 29 chars
                        "Vektis Declaraties Foutloos",      # 27 chars
                        "Bespaar Uren Aan Typewerk",        # 25 chars
                        "NEN 7510 Veilig & AVG Proof",      # 27 chars
                        "Exquise & Nedap Koppeling",        # 24 chars
                        "Gratis Besparingsscan 60s",        # 25 chars
                        "Kliniek Rendement Verhogen",       # 26 chars
                        "Patiëntintake Automatiseren",      # 27 chars
                        "OrionX Slimme Zorg AI",            # 22 chars
                        "Minder Werkdruk Praktijk",         # 24 chars
                        "Directe Lokale Integratie",        # 25 chars
                        "Veilige Zorg Cloud NL",            # 22 chars
                        "Erkend AI Zorgpartner",            # 22 chars
                        "Start Met Besparen Vandaag"        # 26 chars
                    ],
                    "descriptions": [
                        "Verlaag de administratieve werkdruk in uw tandarts- of ZBC-kliniek direct met OrionX AI.", # 89 chars
                        "Koppel uw agenda, informed consent formulieren en EPD direct met slimme AI agents.",      # 83 chars
                        "96% snellere intake en foutloze declaratiecontrole conform NEN 7510 richtlijnen.",        # 81 chars
                        "Doe de gratis scan en ontdek binnen 60 seconden uw jaarlijkse personeelsbesparing."       # 84 chars
                    ],
                    "path1": "klinieken",
                    "path2": "besparing",
                    "final_url": "https://orionx.nl/scan"
                }
            }
        ],
        "negatives": [
            "gratis downloaden",
            "vacature",
            "vacatures",
            "stage",
            "opleiding",
            "cursus",
            "salaris",
            "werkstudent",
            "thuiswerk",
            "open sollicitatie"
        ]
    },
    {
        "name": "NL-SEARCH-B2B-MKB-Factuur-AI",
        "budget": 20.0,
        "type": "Search",
        "networks": "Google search",
        "languages": "nl",
        "ad_groups": [
            {
                "name": "AG-Factuur-OCR-ExactOnline",
                "cpc": 1.75,
                "keywords": [
                    ("facturen automatisch boeken", "Exact"),
                    ("factuur ocr ai exact online", "Phrase"),
                    ("factuurverwerking automatiseren", "Exact"),
                    ("afas facturen automatisch boeken", "Phrase"),
                    ("twinfield ai factuur koppeling", "Exact"),
                    ("ubl facturen automatisch verwerken", "Phrase")
                ],
                "rsa": {
                    "headlines": [
                        "AI Factuurverwerking Exact",       # 26 chars
                        "Boek Facturen 100% Autonoom",      # 27 chars
                        "AFAS & Exact Online AI",           # 22 chars
                        "Geen Handmatig Overtypen",         # 24 chars
                        "99,4% OCR Herkenningsgraad",       # 26 chars
                        "Bespaar 80% Boekhoudtijd",         # 24 chars
                        "Binnen 24 Uur Live In MKB",        # 25 chars
                        "Twinfield & Exact Koppeling",      # 27 chars
                        "Automatische UBL Conversie",       # 26 chars
                        "OrionX MKB Automatisering",        # 25 chars
                        "Directe Factuurscan AI",           # 23 chars
                        "Minder Boekhoudkosten",            # 22 chars
                        "Gratis Besparingsscan",            # 22 chars
                        "Stop Handmatige Invoer",           # 22 chars
                        "Vraag Uw Demo Aan",                # 18 chars
                    ],
                    "descriptions": [
                        "Geen handmatig overtypen meer. Onze AI matcht en boekt direct in Exact & AFAS.",             # 79 chars
                        "Bespaar maandelijks tientallen uren op uw debiteuren- en crediteurenadministratie.",         # 83 chars
                        "99,4% herkenningsgraad van factuurregels en directe controle op KvK- en IBAN-nummers.",       # 86 chars
                        "Koppel naadloos met uw bestaande boekhoudsoftware. Bereken uw ROI in 60 seconden."            # 82 chars
                    ],
                    "path1": "mkb",
                    "path2": "factuur-ai",
                    "final_url": "https://orionx.nl/scan"
                }
            }
        ],
        "negatives": [
            "gratis template",
            "excel voorbeeld",
            "stageplaats",
            "afstudeerstage",
            "cursus boekhouden",
            "vacature administrateur"
        ]
    },
    {
        "name": "GLOBAL-SEARCH-Crypto-Solana-TradingBot",
        "budget": 20.0,
        "type": "Search",
        "networks": "Google search",
        "languages": "en",
        "ad_groups": [
            {
                "name": "AG-Pumpfun-Sniper-Bot",
                "cpc": 0.85,
                "keywords": [
                    ("pump fun sniper bot", "Exact"),
                    ("pump fun sniper bot", "Phrase"),
                    ("solana memecoin trading bot", "Exact"),
                    ("solana trading bot python", "Phrase"),
                    ("jito bundle sniper solana", "Exact"),
                    ("automated pump fun trading", "Phrase"),
                    ("openclaw solana bot", "Exact"),
                    ("solana token launch sniper", "Phrase")
                ],
                "rsa": {
                    "headlines": [
                        "Solana Pump.fun Sniper Bot",       # 26 chars
                        "Sub-100ms MEV Jito Bundles",       # 26 chars
                        "OpenClaw Solana Trading Kit",      # 27 chars
                        "Full Python Source Code €47",      # 27 chars
                        "Zero Monthly Subscription",        # 25 chars
                        "Automated Dev-Wallet Tracking",    # 29 chars
                        "Anti-Rug & Liquidity Checks",      # 27 chars
                        "Instant PDF & Code Delivery",      # 27 chars
                        "Stop Losing To Sandwiches",        # 25 chars
                        "Run On Your Own VPS 24/7",         # 24 chars
                        "Direct RPC & Websocket Flow",      # 27 chars
                        "Official OrionX OpenClaw",         # 24 chars
                        "Download Trading Kit Now",         # 24 chars
                        "Only €47 Lifetime Access",         # 24 chars
                        "Frontrun New Token Launches"       # 27 chars
                    ],
                    "descriptions": [
                        "Dominate pump.fun with sub-100ms execution. Jito bundles, anti-rug logic & full code.",   # 86 chars
                        "One-time payment of €47. No recurring fees or profit cuts. Host completely on your VPS.", # 89 chars
                        "Comprehensive step-by-step master guide & ready-to-deploy Python scripts included.",      # 83 chars
                        "Instant digital delivery with secure Stripe checkout. Start sniping within minutes."      # 84 chars
                    ],
                    "path1": "solana",
                    "path2": "sniper-bot",
                    "final_url": "https://trade.orionx.nl/openclaw"
                }
            }
        ],
        "negatives": [
            "free download",
            "github leak",
            "cracked",
            "nulled",
            "scam report",
            "telegram group free"
        ]
    }
]

# Quick fix description 1 of MKB campaign to strictly <= 90 chars:
CAMPAIGNS[1]["ad_groups"][0]["rsa"]["descriptions"][0] = "Geen handmatig overtypen meer. Onze AI matcht en boekt direct in Exact & AFAS." # 79 chars

def build_csv_rows():
    rows = []
    
    # We will format for Google Ads Editor standard import
    # Headers
    headers = [
        "Campaign", "Campaign Daily Budget", "Campaign Type", "Networks", "Languages",
        "Ad Group", "Max CPC", "Keyword", "Criterion Type",
        "Headline 1", "Headline 2", "Headline 3", "Headline 4", "Headline 5",
        "Headline 6", "Headline 7", "Headline 8", "Headline 9", "Headline 10",
        "Headline 11", "Headline 12", "Headline 13", "Headline 14", "Headline 15",
        "Description 1", "Description 2", "Description 3", "Description 4",
        "Path 1", "Path 2", "Final URL"
    ]

    for camp in CAMPAIGNS:
        c_name = camp["name"]
        c_budget = camp["budget"]
        c_type = camp["type"]
        c_net = camp["networks"]
        c_lang = camp["languages"]

        # Campaign Settings Row
        rows.append({
            "Campaign": c_name,
            "Campaign Daily Budget": str(c_budget),
            "Campaign Type": c_type,
            "Networks": c_net,
            "Languages": c_lang
        })

        # Campaign Negative Keywords
        for neg in camp.get("negatives", []):
            rows.append({
                "Campaign": c_name,
                "Keyword": neg,
                "Criterion Type": "Campaign Negative"
            })

        for ag in camp["ad_groups"]:
            ag_name = ag["name"]
            cpc = str(ag["cpc"])

            # Ad Group Keywords
            for kw, match_type in ag["keywords"]:
                rows.append({
                    "Campaign": c_name,
                    "Ad Group": ag_name,
                    "Max CPC": cpc,
                    "Keyword": kw,
                    "Criterion Type": match_type
                })

            # Responsive Search Ad (RSA)
            rsa = ag["rsa"]
            rsa_row = {
                "Campaign": c_name,
                "Ad Group": ag_name,
                "Final URL": rsa["final_url"],
                "Path 1": validate_length(rsa["path1"], 15, "Path 1"),
                "Path 2": validate_length(rsa["path2"], 15, "Path 2")
            }

            for idx, h in enumerate(rsa["headlines"], start=1):
                rsa_row[f"Headline {idx}"] = validate_length(h, 30, f"Headline {idx}")

            for idx, d in enumerate(rsa["descriptions"], start=1):
                rsa_row[f"Description {idx}"] = validate_length(d, 90, f"Description {idx}")

            rows.append(rsa_row)

    return headers, rows

def main():
    headers, rows = build_csv_rows()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"✅ Generated {OUTPUT_FILE} with {len(rows)} entries successfully!")

if __name__ == "__main__":
    main()
