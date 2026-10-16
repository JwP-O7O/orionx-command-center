#!/usr/bin/env python3
"""
ORIONX GOOGLE ADS B2B HIGH-CONVERSION CAMPAIGN GENERATOR
========================================================
Generates 100% valid Google Ads Editor import CSV files for:
1. NL-B2B-Accountancy-MKB-Delft-DenHaag (Factuurverwerking, Exact Online, Twinfield, AFAS, Notariaat)
2. NL-B2B-Zorgpraktijken-Delft-DenHaag (Tandarts, Fysio & ZBC Praktijkautomatisering)
3. NL-B2B-MKB-Kantoor-Automatisering (Werkbonnen, E-mail Triage, Dossieropbouw & 14-Dagen Pilot)

Strict Google Ads Character Limits (Enforced Programmatically):
- Headline: <= 30 chars
- Description: <= 90 chars
- Path 1 & Path 2: <= 15 chars
"""

import csv
from pathlib import Path

OUTPUT_FILE = Path("/root/hae_command_center/google_ads_import_campaigns.csv")


def validate_length(text: str, max_len: int, name: str) -> str:
    if len(text) > max_len:
        raise ValueError(f"Length violation for {name} ({len(text)} > {max_len}): '{text}'")
    return text


CAMPAIGNS = [
    {
        "name": "NL-B2B-Accountancy-MKB-Delft-DenHaag",
        "budget": 25.0,
        "type": "Search",
        "networks": "Google search",
        "languages": "nl",
        "ad_groups": [
            {
                "name": "AG-Factuur-Automatisering-Exact-AFAS",
                "cpc": 2.10,
                "keywords": [
                    ("factuurverwerking automatiseren", "Exact"),
                    ("factuurverwerking automatiseren", "Phrase"),
                    ("inkoopfacturen automatisch boeken", "Exact"),
                    ("exact online facturen automatiseren", "Phrase"),
                    ("afas factuurverwerking ai", "Phrase"),
                    ("twinfield ubl facturen verwerken", "Phrase"),
                    ("administratiekantoor automatisering", "Exact"),
                    ("boekhouding automatiseren mkb", "Phrase"),
                    ("ai administratie delft", "Phrase"),
                    ("ai administratie den haag", "Phrase"),
                ],
                "rsa": {
                    "headlines": [
                        "AI Factuurverwerking MKB",        # 24
                        "14-Dagen Pilot (€495)",           # 21
                        "100% No-Cure-No-Pay Garantie",    # 28
                        "Achteraf Betalen Op Factuur",     # 27
                        "Koppelt Met Exact & AFAS",        # 24
                        "Twinfield & UBL Integratie",      # 26
                        "Geen Handmatig Overtypen",        # 24
                        "Regio Delft & Den Haag",          # 22
                        "Binnen 14 Dagen Operationeel",    # 28
                        "AVG-Conform & EU Hosting",        # 24
                        "Menselijke Eindcontrole",         # 23
                        "Doorlopend Beheer €495/mnd",      # 26
                        "Maandelijks Opzegbaar",           # 21
                        "Test Live Op De Website",         # 23
                        "OrionX AI Automatisering",        # 24
                    ],
                    "descriptions": [
                        "Automatiseer inkoopfacturen en UBL-boekingsvoorstellen direct in Exact, Twinfield & AFAS.", # 89
                        "Start met de 14-Dagen AI Administratie Pilot (€495 eenmalig) op basis van no-cure-no-pay.", # 89
                        "Betaal pas achteraf op factuur na 14 dagen tevredenheid. Inclusief AVG-verwerkersakkoord.", # 89
                        "Voor accountants en MKB in Delft, Den Haag en Zuid-Holland. Test de workflow simulator.",   # 87
                    ],
                    "path1": "mkb-pilot",
                    "path2": "factuur-ai",
                    "final_url": "https://orionx.nl/#simulator",
                },
            },
            {
                "name": "AG-Notariaat-Makelaardij-Dossier-AI",
                "cpc": 2.25,
                "keywords": [
                    ("notariaat dossier automatisering", "Phrase"),
                    ("makelaardij administratie automatiseren", "Phrase"),
                    ("klant onboarding automatiseren kantoor", "Phrase"),
                    ("document verwerking automatiseren", "Exact"),
                    ("kantoorautomatisering ai den haag", "Phrase"),
                    ("kantoorautomatisering ai delft", "Phrase"),
                ],
                "rsa": {
                    "headlines": [
                        "AI Dossieropbouw Kantoren",       # 25
                        "Voor Notariaat & Makelaardij",    # 28
                        "14-Dagen Pilot (€495)",           # 21
                        "100% No-Cure-No-Pay",             # 19
                        "Start Op Factuur (€0 Vooraf)",    # 28
                        "Automatische Stukkencontrole",    # 28
                        "Regio Delft & Den Haag",          # 22
                        "AVG Verwerkersovereenkomst",      # 26
                        "Koppelt Met Microsoft 365",       # 25
                        "Geen Handmatig Knip-Plakwerk",    # 28
                        "Uw Team Houdt Eindcontrole",      # 26
                        "Binnen 14 Dagen Ingeleerd",       # 25
                        "Maandelijks Opzegbaar Beheer",    # 28
                        "Bekijk Live Workflow Demo",       # 25
                        "OrionX Zakelijke AI",             # 19
                    ],
                    "descriptions": [
                        "Automatiseer controle van klantstukken, koopovereenkomsten en dossieraanmaak op kantoor.", # 88
                        "Beproef de tijdwinst 14 dagen in uw eigen omgeving (€495 eenmalig, 100% no-cure-no-pay).",   # 88
                        "Uitsluitend dataverwerking binnen de EU inclusief standaard AVG-verwerkersovereenkomst.",    # 87
                        "Speciaal voor notarissen, makelaars en advieskantoren in regio Delft en Den Haag.",          # 81
                    ],
                    "path1": "kantoor",
                    "path2": "dossier-ai",
                    "final_url": "https://orionx.nl/#simulator",
                },
            },
        ],
        "negatives": [
            "gratis downloaden",
            "gratis software",
            "vacature",
            "vacatures",
            "stage",
            "opleiding",
            "cursus",
            "salaris",
            "werkstudent",
            "thuiswerk",
            "open sollicitatie",
            "excel template gratis",
            "zzp boekhouden gratis",
        ],
    },
    {
        "name": "NL-B2B-Zorgpraktijken-Delft-DenHaag",
        "budget": 20.0,
        "type": "Search",
        "networks": "Google search",
        "languages": "nl",
        "ad_groups": [
            {
                "name": "AG-Tandarts-Fysio-Zorgpraktijk-AI",
                "cpc": 2.15,
                "keywords": [
                    ("zorgadministratie automatiseren", "Exact"),
                    ("zorgadministratie automatiseren", "Phrase"),
                    ("tandartspraktijk administratie automatiseren", "Phrase"),
                    ("fysiotherapie praktijk automatisering", "Phrase"),
                    ("intake automatisering zorgpraktijk", "Phrase"),
                    ("verwijsbrieven automatisch verwerken", "Phrase"),
                    ("praktijkautomatisering den haag", "Phrase"),
                    ("praktijkautomatisering delft", "Phrase"),
                ],
                "rsa": {
                    "headlines": [
                        "AI Voor Zorg- & Tandpraktijk",    # 28
                        "14-Dagen Praktijk Pilot €495",    # 28
                        "100% No-Cure-No-Pay Garantie",    # 28
                        "Start Op Factuur Achteraf",       # 25
                        "Intakes & Verwijsbrieven AI",     # 27
                        "Minder Administratieve Druk",     # 27
                        "Voor Tandarts, Fysio & ZBC",      # 26
                        "Regio Delft & Den Haag",          # 22
                        "AVG-Conform & EU Servers",        # 24
                        "Behandelaar Houdt Controle",      # 26
                        "Geen Langdurig Jaarcontract",     # 27
                        "Doorlopend Beheer €495/mnd",      # 26
                        "Gratis 60s Besparingsscan",       # 25
                        "Binnen 14 Dagen Werkend",         # 23
                        "OrionX Praktijk AI",              # 18
                    ],
                    "descriptions": [
                        "Bespaar uren aan het overtypen van verwijsbrieven, intakeformulieren en patiëntvragen.",      # 86
                        "Start met de 14-Dagen AI Administratie Pilot (€495 eenmalig) op basis van no-cure-no-pay.",  # 89
                        "Geen vooruitbetaling nodig: betaal pas op factuur na 14 dagen tevredenheid in uw praktijk.", # 90
                        "Veilige dataverwerking binnen de EU inclusief standaard AVG-verwerkersovereenkomst (DPA).",  # 89
                    ],
                    "path1": "zorgpraktijk",
                    "path2": "14d-pilot",
                    "final_url": "https://orionx.nl/scan",
                },
            },
        ],
        "negatives": [
            "vacature",
            "vacatures",
            "stage",
            "opleiding",
            "cursus",
            "salaris",
            "afspraak maken tandarts",
            "spoedtandarts",
            "fysiotherapeut gezocht",
            "patiëntenportaal inloggen",
        ],
    },
    {
        "name": "NL-B2B-MKB-Kantoor-Automatisering",
        "budget": 20.0,
        "type": "Search",
        "networks": "Google search",
        "languages": "nl",
        "ad_groups": [
            {
                "name": "AG-MKB-Procesautomatisering-Pilot",
                "cpc": 1.95,
                "keywords": [
                    ("administratieve processen automatiseren", "Exact"),
                    ("administratieve processen automatiseren", "Phrase"),
                    ("ai procesautomatisering mkb", "Phrase"),
                    ("handmatig werk automatiseren kantoor", "Phrase"),
                    ("werkbonnen automatisch verwerken", "Phrase"),
                    ("offerte aanvragen automatiseren", "Phrase"),
                    ("bedrijfsprocessen automatiseren delft", "Phrase"),
                    ("bedrijfsprocessen automatiseren den haag", "Phrase"),
                ],
                "rsa": {
                    "headlines": [
                        "AI Administratie Voor MKB",       # 25
                        "14-Dagen Pilot Voor €495",        # 24
                        "100% No-Cure-No-Pay",             # 19
                        "Betaal Achteraf Op Factuur",      # 26
                        "Stop Handmatig Overtypen",        # 24
                        "Werkbonnen, Mail & Facturen",     # 27
                        "Regio Delft & Den Haag",          # 22
                        "Koppelt Met Uw Huidige ERP",      # 26
                        "Binnen 14 Dagen Live",            # 20
                        "Vast Tarief Zonder Verrassing",   # 29
                        "Beheer €495/mnd Opzegbaar",       # 25
                        "AVG & EU-Server Beveiliging",     # 27
                        "Bereken Uw ROI In 60 Sec",        # 24
                        "1-Klik Menselijk Akkoord",        # 24
                        "OrionX AI Technologies",          # 22
                    ],
                    "descriptions": [
                        "Automatiseer repetitief administratief werk in uw bestaande boekhoud- en kantoorsoftware.", # 89
                        "Test 14 dagen risicovrij in uw eigen bedrijf (€495 eenmalig, 100% niet-goed-geld-terug).",  # 88
                        "Start vandaag voor €0,- op factuur achteraf. Geen langdurige contracten of IT-trajecten.", # 88
                        "Bereken direct uw terugwinbare uren en jaarlijkse kostenbesparing op onze website.",       # 82
                    ],
                    "path1": "mkb-ai",
                    "path2": "14d-pilot",
                    "final_url": "https://orionx.nl/#pricing",
                },
            }
        ],
        "negatives": [
            "gratis",
            "vacature",
            "stageplaats",
            "afstudeerstage",
            "cursus",
            "opleiding",
            "thuiswerk",
        ],
    },
]


def build_csv_rows():
    rows = []

    headers = [
        "Campaign", "Campaign Daily Budget", "Campaign Type", "Networks", "Languages",
        "Ad Group", "Max CPC", "Keyword", "Criterion Type",
        "Headline 1", "Headline 2", "Headline 3", "Headline 4", "Headline 5",
        "Headline 6", "Headline 7", "Headline 8", "Headline 9", "Headline 10",
        "Headline 11", "Headline 12", "Headline 13", "Headline 14", "Headline 15",
        "Description 1", "Description 2", "Description 3", "Description 4",
        "Path 1", "Path 2", "Final URL",
    ]

    for camp in CAMPAIGNS:
        c_name = camp["name"]
        c_budget = camp["budget"]
        c_type = camp["type"]
        c_net = camp["networks"]
        c_lang = camp["languages"]

        rows.append({
            "Campaign": c_name,
            "Campaign Daily Budget": str(c_budget),
            "Campaign Type": c_type,
            "Networks": c_net,
            "Languages": c_lang,
        })

        for neg in camp.get("negatives", []):
            rows.append({
                "Campaign": c_name,
                "Keyword": neg,
                "Criterion Type": "Campaign Negative",
            })

        for ag in camp["ad_groups"]:
            ag_name = ag["name"]
            cpc = str(ag["cpc"])

            for kw, match_type in ag["keywords"]:
                rows.append({
                    "Campaign": c_name,
                    "Ad Group": ag_name,
                    "Max CPC": cpc,
                    "Keyword": kw,
                    "Criterion Type": match_type,
                })

            rsa = ag["rsa"]
            rsa_row = {
                "Campaign": c_name,
                "Ad Group": ag_name,
                "Final URL": rsa["final_url"],
                "Path 1": validate_length(rsa["path1"], 15, "Path 1"),
                "Path 2": validate_length(rsa["path2"], 15, "Path 2"),
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
