import imaplib
import smtplib
import email
import re

from email.header import decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

# =====================================
# IMPORT PERSONAL DETAILS
# =====================================

from my_details import (
    GMAIL_USER,
    GMAIL_PASS,
    full_name,
    location,
    email as email_addr,
    phone,
    linkedin,
    Disclaimer
)


# =====================================
# PROCESSED EMAIL TRACKING
# =====================================

PROCESSED_FILE = "processed_rejections.txt"


def already_processed(message_id):

    try:
        with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
            return message_id.strip() in {
                line.strip()
                for line in f.readlines()
            }

    except FileNotFoundError:
        return False


def mark_processed(message_id):

    with open(PROCESSED_FILE, "a", encoding="utf-8") as f:
        f.write(message_id.strip() + "\n")

# =====================================
# NON JOB RELATED KEYWORDS (for Skipping mail)
# =====================================

def is_non_job_email(text):

    text = text.lower()

    exclusions = [

        "invoice",
        "payment",
        "order",
        "shipment",
        "delivery",
        "bank",
        "otp",
        "password",
        "newsletter",
        "subscription",
        "receipt",
        "ticket",
        "support request",
        "marketing"
    ]

    return any(
        word in text
        for word in exclusions
    )


# =====================================
# JOB RELATED KEYWORDS
# =====================================

JOB_KEYWORDS = [

    # English
    "application",
    "job",
    "position",
    "vacancy",
    "candidate",
    "recruitment",
    "recruiter",
    "hiring",
    "career",
    "interview",

    # Dutch
    "sollicitatie",
    "vacature",

    # German
    "bewerbung",
    "stelle",

    # French
    "candidature",
    "poste",

    # Italian
    "candidatura",
    "posizione",

    # Spanish
    "solicitud",
    "puesto"
]


# =====================================
# REJECTION KEYWORDS
# =====================================

REJECTION_PATTERNS = [

    # English
    "unfortunately",
    "regret to inform",
    "not moving forward",
    "not move forward",
    "not moving forward with your application",
    "not selected",
    "application was unsuccessful",
    "position has been filled",
    "other candidates",
    "after careful consideration",
    "we have decided to proceed",
    "we have decided not to proceed",
    "we have decided not to move forward",
    "not successful",
    "we regret to inform you",
    "more closely matches",
    "better match",
    "stronger match",
    "language barrier",
    "due to the language barrier",
    "will not be progressing",
    "unable to progress",
    "not advancing",
    "not advance to the next stage",
    "next stage",
    "decline your application",
    "not be taking your application further",

    # Dutch
    "helaas",
    "afwijzing",
    "niet geselecteerd",
    "niet gekozen",
    "wij gaan verder met andere kandidaten",
    "terugkoppeling sollicitatie",
    "taalbarrière",
    "taalbarriere",

    # German
    "absage",
    "leider",
    "nicht berücksichtigt",
    "andere kandidaten",

    # French
    "malheureusement",
    "refus",
    "nous ne donnerons pas suite",

    # Italian
    "purtroppo",
    "non selezionato",
    "non proseguiremo",

    # Spanish
    "lamentamos",
    "no seleccionado",

    # Portuguese
    "infelizmente",
    "não selecionado"
]


# =====================================
# REJECTION DETECTION
# =====================================

def is_rejection_email(text):

    text = text.lower()

    if is_non_job_email(text):
        return False

    job_match = any(
        keyword in text
        for keyword in JOB_KEYWORDS
    )

    rejection_match = any(
        pattern in text
        for pattern in REJECTION_PATTERNS
    )

    return job_match and rejection_match


# =====================================
# JOB KEYWORDS DETECTION
# =====================================


JOB_KEYWORDS.extend([
    "talent acquisition",
    "hiring manager",
    "job opening",
    "employment",
    "candidate home",
    "career opportunity",
    "your application",
    "applied",
    "recruitment process"
])


# =====================================
# LANGUAGE REJECTION DETECTION
# =====================================

def is_language_rejection(text):

    language_keywords = [

        # English
        "language",
        "native speaker",
        "fluency",
        "language requirement",

        # Languages
        "dutch",
        "german",
        "french",
        "italian",
        "spanish",
        "portuguese",

        # Dutch
        "nederlands",
        "vloeiend nederlands",

        # German
        "deutsch",
        "deutschkenntnisse",

        # French
        "français",
        "francais",

        # Italian
        "italiano",

        # Spanish
        "español",
        "espanol"
    ]

    text = text.lower()

    return any(
        keyword.lower() in text
        for keyword in language_keywords
    )

# =====================================
# EMAIL EXTRACTION
# =====================================

def extract_email_addresses(text):

    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return list(set(emails))


# =====================================
# RECIPIENT FILTERS
# =====================================

def valid_recipient(email_address):

    blocked = [
        "noreply",
        "no-reply",
        "donotreply",
        "do-not-reply",
        "notifications",
        "notification",
        "mailer-daemon",
        "automated",
        "auto-reply"
    ]

    email_address = email_address.lower()

    return not any(
        word in email_address
        for word in blocked
    )


def recruiter_address(email_address):

    email_address = email_address.lower()

    recruiter_keywords = [
        "recruit",
        "talent",
        "career",
        "jobs",
        "hr",
        "hiring"
    ]

    return any(
        keyword in email_address
        for keyword in recruiter_keywords
    )


# =====================================
# COMPANY EXTRACTION
# =====================================

def company_from_sender(sender):

    try:

        domain = sender.split("@")[1]
        company = domain.split(".")[0]

        blocked = [
            "linkedin",
            "indeed",
            "greenhouse",
            "lever",
            "workday",
            "smartrecruiters",
            "ashby",
            "teamtailor",
            "personio"
        ]

        if company.lower() in blocked:
            return ""

        return company.title()

    except:
        return ""


def extract_company_name(text, sender=""):

    patterns = [

        r"position at\s+([A-Za-z0-9&.,\- ]+?)(?:\.|\n|,)",

        r"role at\s+([A-Za-z0-9&.,\- ]+?)(?:\.|\n|,)",

        r"opportunity at\s+([A-Za-z0-9&.,\- ]+?)(?:\.|\n|,)",

        r"at\s+([A-Za-z0-9&.,\- ]+?)(?:\.|\n|,)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            company = match.group(1).strip()

            company = re.sub(
                r"\s+",
                " ",
                company
            )

            if len(company) < 60:
                return company

    sender_company = company_from_sender(sender)

    if sender_company:
        return sender_company

    return "your organization"


# =====================================
# REPLY GENERATOR
# =====================================

def generate_reply(company_name, language_issue=False):

    reply = f"""
Dear Hiring Team,

Thank you for informing me about the outcome of my application.

While I am naturally disappointed, I sincerely appreciate the time and effort invested in reviewing my profile and considering my application.
"""
    if language_issue:

        reply += """

I understand that certain role requirements may have been a stronger match for other candidates. I remain very interested in future opportunities within your organization and would be grateful if my profile could be kept in mind for positions where my skills and experience may be a strong fit, particularly roles in which English is the primary working language. I would welcome the opportunity to be considered should such openings become available in the future.
"""
    reply += f"""

Although I was not selected for this opportunity with {company_name}, I remain interested in future positions that may align with my experience and skills.

If possible, I would be grateful for any feedback regarding my application, qualifications, or interview performance. Any insights would help me improve and prepare more effectively for future opportunities.

Thank you once again for your consideration.

Kind regards,

{full_name}
Phone: {phone}
Email: {email_addr}
LinkedIn: {linkedin}

Disclaimer: {Disclaimer}
"""

    return reply


# =====================================
# SEND EMAIL
# =====================================

def send_reply_email(
    recipients,
    original_subject,
    reply_body
):

    msg = MIMEMultipart()

    msg["From"] = GMAIL_USER
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = f"Re: {original_subject}"

    msg.attach(
        MIMEText(reply_body, "plain")
    )

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            GMAIL_USER,
            GMAIL_PASS
        )

        server.sendmail(
            GMAIL_USER,
            recipients,
            msg.as_string()
        )


# =====================================
# MAIN PROCESS
# =====================================

def process_rejection_emails():

    mail = imaplib.IMAP4_SSL(
        "imap.gmail.com"
    )

    mail.login(
        GMAIL_USER,
        GMAIL_PASS
    )

    mail.select("inbox")

    status, messages = mail.search(
        None,
        "UNSEEN"
    )

    email_ids = messages[0].split()

    if not email_ids:

        print("No unread emails found.")
        return

    for email_id in email_ids:

        res, msg_data = mail.fetch(
            email_id,
            "(RFC822)"
        )

        for response in msg_data:

            if not isinstance(response, tuple):
                continue

            msg = email.message_from_bytes(
                response[1]
            )

            message_id = msg.get(
                "Message-ID",
                ""
            ).strip()

            if already_processed(message_id):
                continue

            subject = decode_header(
                msg["Subject"]
            )[0][0]

            if isinstance(subject, bytes):
                subject = subject.decode(
                    errors="ignore"
                )

            sender = email.utils.parseaddr(
                msg.get("From")
            )[1]

            body = ""
            html_body = ""

            if msg.is_multipart():

                for part in msg.walk():

                    content_type = (
                        part.get_content_type()
                    )

                    if content_type == "text/plain":

                        try:
                            body += part.get_payload(
                                decode=True
                            ).decode(
                                errors="ignore"
                            )
                        except:
                            pass

                    elif content_type == "text/html":

                        try:
                            html_body += part.get_payload(
                                decode=True
                            ).decode(
                                errors="ignore"
                            )
                        except:
                            pass

            else:

                body = msg.get_payload(
                    decode=True
                ).decode(
                    errors="ignore"
                )

            if html_body:

                soup = BeautifulSoup(
                    html_body,
                    "html.parser"
                )

                text = soup.get_text(
                    " ",
                    strip=True
                )

            else:
                text = body

            combined_text = f"{subject} {text}"

            is_rejection = is_rejection_email(combined_text)

            if not is_rejection:
                # Restore unread status
                mail.store(
                    email_id,
                    "-FLAGS",
                    "\\Seen"
                )

                continue

            print(f"\nRejection Found: {subject}")

            company_name = extract_company_name(
                text,
                sender
            )

            language_issue = is_language_rejection(text)

            recipients = []

            if valid_recipient(sender):
                recipients.append(sender)

            for addr in extract_email_addresses(text):

                if valid_recipient(addr):
                    recipients.append(addr)

            recipients = list(set(recipients))

            if not recipients:
                continue

            reply_body = generate_reply(
                company_name,
                language_issue
            )

            send_reply_email(
                recipients,
                subject,
                reply_body
            )

            mark_processed(message_id)

            print(
                f"Reply sent to: {', '.join(recipients)}"
            )

            mail.store(
                email_id,
                "+FLAGS",
                "\\Seen"
            )

    mail.logout()




# =====================================
# RUN
# =====================================

if __name__ == "__main__":

    process_rejection_emails()

    print(
        "\nCompleted rejection mail processing."
    )