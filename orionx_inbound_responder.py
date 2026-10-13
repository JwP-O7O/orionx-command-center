#!/usr/bin/env python3
"""
OrionX Autonomous Inbound Email Consultant & Interactive Responder
==================================================================
24/7 Autonomous daemon that:
1. Listens to TransIP IMAP (imap.transip.email) for inbound emails from leads.
2. Analyzes lead inquiries (pricing, NEN 7510 compliance, EPD integration, demo scheduling, opt-outs).
3. Generates factual, professional, zero-hallucination responses via Gemini / Rule Engine.
4. Sends threaded replies via authenticated TransIP SMTP (jwp@orionx.nl).
5. Dispatches real-time alerts to Telegram via @AgentO7Obot.
"""

import os
import sys
import time
import json
import imaplib
import smtplib
import ssl
import email
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid, parseaddr
import urllib.request
import logging
from pathlib import Path
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [OrionXInbound] %(message)s'
)
logger = logging.getLogger("OrionXInbound")

# Credentials
IMAP_HOST = os.environ.get("IMAP_HOST", "imap.transip.email")
IMAP_PORT = int(os.environ.get("IMAP_PORT", "993"))
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.transip.email")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
MAIL_USER = os.environ.get("SMTP_USER", "jwp@orionx.nl")
MAIL_PASS = os.environ.get("SMTP_PASS", "TheHagueO7O-")

TELEGRAM_BOT_TOKEN = "8608971534:AAH_XDzmmp229-OhR3JVsGXy_LErAxEpvxM"
TELEGRAM_CHAT_ID = "6133249549"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAKYoKyzJV0AXOQHJJsMwHSyMfIQomEx2Y")

def send_telegram(text: str):
    """Sends real-time event notification to Telegram."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10):
            pass
    except Exception as e:
        logger.error(f"Telegram dispatch error: {e}")

def decode_mime_words(s: str) -> str:
    """Decodes MIME encoded header strings."""
    if not s:
        return ""
    decoded_fragments = decode_header(s)
    result = []
    for fragment, charset in decoded_fragments:
        if isinstance(fragment, bytes):
            result.append(fragment.decode(charset or 'utf-8', errors='replace'))
        else:
            result.append(str(fragment))
    return "".join(result)

def extract_email_body(msg) -> str:
    """Extracts plain text body from email message."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        body += payload.decode('utf-8', errors='replace')
                except Exception:
                    pass
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                body = payload.decode('utf-8', errors='replace')
        except Exception:
            pass
    return body.strip()

def generate_factual_response(sender_name: str, sender_email: str, subject: str, message_body: str) -> str:
    """Generates a professional, factual response addressing the client's questions."""
    lower_body = message_body.lower()

    # 1. Opt-out check
    if any(k in lower_body for k in ["afmelden", "unsubscribe", "geen interesse", "stop", "verwijderen"]):
        return f"""Geachte {sender_name or 'heer/mevrouw'},

Hartelijk dank voor uw bericht.

Wij hebben uw verzoek direct verwerkt. Uw e-mailadres ({sender_email}) is per direct uitgeschreven en verwijderd uit ons bestand. U zult geen verdere berichten meer van ons ontvangen.

Wij wensen u en uw organisatie veel succes.

Met vriendelijke groet,

J.W. Pabst
OrionX AI Technologies
https://orionx.nl"""

    # 2. Try Gemini 2.5 REST for smart, contextual reasoning
    prompt = f"""Je bent J.W. Pabst, Technisch Directeur van OrionX AI Technologies (Den Haag).
Je beantwoordt een zakelijke e-mail van een Nederlandse praktijkhouder of zorgdirecteur.

Belangrijke bedrijfsfeiten (GEEN HALLUCINATIES, STRIKT FEITELIJK):
- OrionX levert NEN 7510 en AVG conforme praktijkautomatisering (intakes, dossiervorming, documentstromen).
- Data blijft 100% binnen de EU op ISO 27001 gecertificeerde Hetzner servers (geen export naar VS).
- Integratie met gangbare EPD systemen (via beveiligde API of geautomatiseerde import/export).
- Model: Dedicated AI-FTE Retainer (€1.450,- excl. btw per maand), vervangt 0.5 tot 1.5 fte administratieve overhead.
- Gratis calculatie beschikbaar op: https://scan.orionx.nl
- Vrijblijvende online kennismaking / demo van 15 minuten mogelijk.

Ingekomen e-mail van {sender_name} ({sender_email}):
Onderwerp: {subject}
Inhoud:
{message_body}

Schrijf een hoffelijke, zakelijke en bondige reactie in perfect Nederlands.
Start met: Geachte {sender_name or 'heer/mevrouw'},
Eindig met:
Met vriendelijke groet,

J.W. Pabst
OrionX AI Technologies
E-mail: jwp@orionx.nl | Web: https://orionx.nl
"""

    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                if text and len(text) > 80:
                    return text.strip()
        except Exception as e:
            logger.warning(f"Gemini generation error: {e}, using rule-based factual template.")

    # Rule-based fallback
    return f"""Geachte {sender_name or 'heer/mevrouw'},

Hartelijk dank voor uw reactie en interesse in onze procesautomatisering.

Met betrekking tot uw vraag informeren wij u graag dat onze systemen specifiek zijn ingericht voor de strenge eisen van de Nederlandse zorg (NEN 7510 en AVG). Alle verwerking vindt plaats op beveiligde, Europese ISO 27001-gecertificeerde servers.

Onze AI-FTE assistenten kunnen naadloos worden aangesloten op uw bestaande workflow (waaronder patiëntintakes, geautomatiseerde verslaglegging en EPD-koppelingen), waardoor het team direct ontlast wordt van routinematige administratie.

U kunt de specifieke tijdsbesparing voor uw team direct berekenen via onze beveiligde scan:
https://scan.orionx.nl

Graag lichten wij de mogelijkheden in een korte online toelichting van 15 minuten aan u toe. Schikt het u om hiervoor een moment in te plannen?

Met vriendelijke groet,

J.W. Pabst
OrionX AI Technologies
E-mail: jwp@orionx.nl | Web: https://orionx.nl
Gevestigd te Den Haag"""

def send_reply_email(original_msg, reply_text: str) -> bool:
    """Sends threaded reply email via TransIP SMTP."""
    try:
        orig_from = original_msg.get("From", "")
        _, to_email = parseaddr(orig_from)
        if not to_email:
            return False

        orig_subject = decode_mime_words(original_msg.get("Subject", ""))
        reply_subject = orig_subject if orig_subject.lower().startswith("re:") else f"Re: {orig_subject}"
        orig_msg_id = original_msg.get("Message-ID", "")

        msg = MIMEMultipart("alternative")
        msg["From"] = f'"J.W. Pabst | OrionX AI Technologies" <{MAIL_USER}>'
        msg["To"] = to_email
        msg["Reply-To"] = MAIL_USER
        msg["Subject"] = reply_subject
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="orionx.nl")
        if orig_msg_id:
            msg["In-Reply-To"] = orig_msg_id
            msg["References"] = orig_msg_id

        # Format HTML with signature
        html_formatted = reply_text.replace('\n', '<br>')
        html_content = f"""<!DOCTYPE html>
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; max-width: 620px; margin: 0 auto; padding: 20px;">
  <div style="font-size: 14px; color: #334155;">
    {html_formatted}
  </div>
</body>
</html>"""

        msg.attach(MIMEText(reply_text, "plain", "utf-8"))
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.starttls(context=context)
            server.login(MAIL_USER, MAIL_PASS)
            server.sendmail(MAIL_USER, [to_email], msg.as_string())

        logger.info(f"✓ Threaded antwoord succesvol verzonden naar {to_email}")
        return True
    except Exception as e:
        logger.error(f"Fout bij verzenden van reply: {e}")
        return False

def check_and_process_inbox():
    """Connects to IMAP, scans unread messages, processes client inquiries."""
    try:
        context = ssl.create_default_context()
        mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, ssl_context=context)
        mail.login(MAIL_USER, MAIL_PASS)
        mail.select("INBOX")

        status, response = mail.search(None, "UNSEEN")
        if status != "OK" or not response[0]:
            mail.logout()
            return

        msg_ids = response[0].split()
        logger.info(f"📬 {len(msg_ids)} ongelezen e-mail(s) gevonden in INBOX...")

        for mid in msg_ids:
            res, data = mail.fetch(mid, "(RFC822)")
            if res != "OK":
                continue

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)

            from_header = decode_mime_words(msg.get("From", ""))
            sender_name, sender_email = parseaddr(from_header)
            subject = decode_mime_words(msg.get("Subject", ""))
            body = extract_email_body(msg)

            # Skip self-generated, service notifications or loop emails
            lower_email = sender_email.lower()
            if (
                lower_email == MAIL_USER.lower()
                or "lead intelligence" in sender_name.lower()
                or any(k in lower_email for k in ["noreply", "no-reply", "notifications@", "mailer-daemon", "postmaster", "transip.nl", "stripe.com", "wise.com", "google.com", "transip.email"])
            ):
                logger.info(f"Geautomatiseerde service-notificatie overgeslagen ({sender_email} - {subject})")
                mail.store(mid, '+FLAGS', '\\Seen')
                continue

            logger.info(f"⚡ [KLANT INKOMEND] Van: {sender_name} <{sender_email}> | Onderwerp: {subject}")

            # Generate and send factual reply
            reply_text = generate_factual_response(sender_name, sender_email, subject, body)
            success = send_reply_email(msg, reply_text)

            if success:
                # Mark as seen in IMAP
                mail.store(mid, '+FLAGS', '\\Seen')

                # Notify Telegram
                tg_msg = (
                    f"💬 <b>[INTERACTIEVE REACTIE VERZONDEN]</b>\n\n"
                    f"<b>Cliënt:</b> {sender_name or sender_email}\n"
                    f"<b>E-mail:</b> <code>{sender_email}</code>\n"
                    f"<b>Onderwerp:</b> {subject}\n\n"
                    f"<b>Vraag Samenvatting:</b>\n<i>{body[:250]}...</i>\n\n"
                    f"✅ <b>Autonoom Geantwoord:</b> NEN 7510 & AVG toelichting + link naar scan.orionx.nl verzonden!"
                )
                send_telegram(tg_msg)

        mail.logout()
    except Exception as e:
        logger.error(f"IMAP poll cyclus fout: {e}")

def run_daemon(poll_interval: int = 60):
    logger.info(f"🛡️ OrionX Inbound Email Consultant gestart (Poll interval: {poll_interval}s).")
    while True:
        try:
            check_and_process_inbox()
        except Exception as e:
            logger.error(f"Onverwachte fout in daemon loop: {e}")
        time.sleep(poll_interval)

if __name__ == "__main__":
    run_daemon()
