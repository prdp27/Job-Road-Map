
# =====================================
# Main Automated Job Application Script
# =====================================

import pdfkit
import markdown2
from datetime import datetime
from deep_translator import GoogleTranslator
import re
import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup

# =====================================
# IMPORT PERSONAL DETAILS
# =====================================

from D:\prdp\Data Analytics\my_details import (
    GMAIL_USER,
    GMAIL_PASS,
    full_name,
    location,
    email,
    phone,
    linkedin
)

email_addr = email

# ===============================
# Input placeholders
# ===============================
job_title = ""
hiring_manager = ""
company_name = ""
company_address = ""
region = ""

hiring_manager1 = ""
hiring_manager2 = "Sir/Madam"

# ===============================
# READ EMAIL (HTML VERSION)
# ===============================
def read_latest_email():
    global job_title, hiring_manager, company_name, company_address, region

    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_PASS)
        mail.select("inbox")

        status, messages = mail.search(None, 'UNSEEN')
        messages = messages[0].split()

        if not messages:
            print("❌ No new emails.")
            return False

        latest = messages[-1]
        res, msg = mail.fetch(latest, "(RFC822)")

        for response in msg:
            if isinstance(response, tuple):
                msg_email = email.message_from_bytes(response[1])

                # ================= SUBJECT =================
                subject = decode_header(msg_email["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode(errors="ignore")

                # ================= BODY =================
                body = ""
                html_body = ""

                if msg_email.is_multipart():
                    for part in msg_email.walk():
                        ctype = part.get_content_type()
                        cdisp = str(part.get("Content-Disposition"))

                        if ctype == "text/plain" and "attachment" not in cdisp:
                            body = part.get_payload(decode=True).decode(errors="ignore")

                        if ctype == "text/html":
                            html_body = part.get_payload(decode=True).decode(errors="ignore")
                else:
                    body = msg_email.get_payload(decode=True).decode(errors="ignore")

                # ================= HTML PARSING =================
                text = ""
                if html_body:
                    soup = BeautifulSoup(html_body, "html.parser")
                    text = soup.get_text(" ", strip=True)
                else:
                    text = body

                # ================= EXTRACTION =================
                job_title_match = re.search(
                    r"(Data Analyst|Power BI Developer|Business Analyst|Software Engineer|Analyst)",
                    text, re.I
                )
                company_match = re.search(
                    r"(?:at|@)\s([A-Z][A-Za-z0-9 &.,]+)",
                    text
                )
                region_match = re.search(
                    r"(India|Germany|France|Italy|Netherlands|Remote)",
                    text, re.I
                )

                # ================= ASSIGN VALUES =================
                job_title = job_title_match.group(1).title() if job_title_match else ""
                company_name = company_match.group(1).title() if company_match else ""
                region = region_match.group(1).title() if region_match else ""

                # ================= MARK AS READ =================
                mail.store(latest, '+FLAGS', '\\Seen')

                print("\n📧 Email extracted:")
                print(f"Job: {job_title}")
                print(f"Company: {company_name}")

        return True

    except Exception as e:
        print(f"❌ Error reading email: {e}")
        return False

# ===============================
# HANDLE MANAGER
# ===============================
def handle_manager():
    global hiring_manager1, hiring_manager2
    if hiring_manager == "":
        hiring_manager1 = ""
        hiring_manager2 = "Sir/Madam"
    else:
        hiring_manager1 = hiring_manager
        hiring_manager2 = hiring_manager

# ===============================
# INDIA CHECK
# ===============================
def check_india():
    return (region == "" or region.lower() == "india")

# ===============================
# DATE
# ===============================
date_today = datetime.today().strftime("%B %d, %Y")

# ===============================
# CV DATA
# ===============================
education_list = [
    {"degree": "Master in Data Science with Power BI", "institution": "Consol Flare", "year": "Ongoing"},
    {"degree": "Higher Secondary (12th)", "institution": "NIOS India", "year": "2006"},
    {"degree": "Secondary School (10th)", "institution": "NIOS India", "year": "2004"}
]

certifications_list = [
    "Visual FoxPro (2008)",
    "Data Science with Power BI (Ongoing)"
]

languages_list = ["English (B2)", "Hindi (Native)"]

skills_list = [
    "Python (Pandas, NumPy)",
    "SQL",
    "Excel Advanced Reporting",
    "Power BI",
    "Financial & KPI Dashboards"
]

experience_list = [
    {
        "title": "Manager Systems EDP",
        "company": "Anuradha Enterprises Pvt. Ltd.",
        "location": "New Delhi",
        "duration": "Apr 2022 – Present",
        "responsibilities": [
            "Developed and automated financial, sales, and inventory reports using Python, Pandas, Power BI, Excel.",
            "Built dashboards for KPI tracking and business insights.",
            "Enhanced procurement and financial workflows through automation."
        ]
    }
]

# ===============================
# PDF CONFIG
# ===============================
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# ===============================
# CV GENERATOR
# ===============================
def generate_cv_markdown():
    md = f"# {full_name}\n{location}\nEmail: {email_addr} | Phone: {phone} | LinkedIn: {linkedin}\n\n"
    md += "## PROFESSIONAL SUMMARY\nExperienced professional with 20+ years in administration, logistics, and system management.\n\n"
    md += "## CORE SKILLS\n" + "\n".join(f"- {s}" for s in skills_list) + "\n\n"
    md += "## PROFESSIONAL EXPERIENCE\n"
    for exp in experience_list:
        md += f"### {exp['title']} | {exp['company']} | {exp['duration']}\n"
        md += "\n".join(f"- {r}" for r in exp['responsibilities']) + "\n\n"
    md += "## EDUCATION\n" + "\n".join(f"- {e['degree']} - {e['institution']}, {e['year']}" for e in education_list) + "\n\n"
    return md

# ===============================
# COVER LETTER
# ===============================
def generate_cover_letter_markdown():
    handle_manager()
    is_india_flag = check_india()

    md = f"""# Cover Letter – {full_name}

{full_name}  
{location}  
Email: {email_addr} | Phone: {phone}  

{date_today}  

{hiring_manager1}  
{company_name}  
{company_address}  

**Subject:** Application for {job_title}  

Dear {hiring_manager2},  

I am writing to express my interest in the {job_title} position at {company_name}.  

With experience in data analytics, Python, Power BI, and SQL, I bring strong technical and business understanding.  

In my current role as {experience_list[0]['title']} at {experience_list[0]['company']}, I have:
"""

    md += "\n".join(f"- {r}" for r in experience_list[0]['responsibilities'])

    md += "\n\nMy expertise in reporting and analytics enables me to bridge business and technical requirements effectively."

    if not is_india_flag:
        md += f" I am particularly interested in opportunities in {region}."

    md += f"\n\nThank you for your time.\n\nKind regards,\n{full_name}"
    return md

# ===============================
# TRANSLATION SAFE
# ===============================
def translate_text(text, lang="en"):
    if lang == "en":
        return text
    try:
        return GoogleTranslator(source="auto", target=lang).translate(text)
    except:
        return text

# ===============================
# PDF GENERATOR
# ===============================
def md_to_pdf(md_content, file_name, lang="en"):
    md_content = translate_text(md_content, lang)
    html = markdown2.markdown(md_content)

    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>{html}</body>
    </html>
    """

    pdfkit.from_string(html, file_name, configuration=config)
    print(f"✅ Generated: {file_name}")

# ===============================
# RUN SYSTEM
# ===============================
if read_latest_email():
    cv_md = generate_cv_markdown()
    cover_md = generate_cover_letter_markdown()

    languages = {
        "English": "en",
        "German": "de",
        "Italian": "it",
        "French": "fr",
        "Dutch": "nl"
    }

    for name, code in languages.items():
        md_to_pdf(cv_md, f"CV_{name}.pdf", code)
        md_to_pdf(cover_md, f"Cover_{name}.pdf", code)

    print("\n🎉 ALL PDFs GENERATED SUCCESSFULLY at", datetime.now().strftime("%d-%b-%Y %I:%M %p"))
else:
    print("\n❌ No emails processed")