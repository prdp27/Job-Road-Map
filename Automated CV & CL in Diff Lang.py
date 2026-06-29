# ===============================
# Personal Details (fill your info)
# ===============================

# =====================================
# Begin from here
# =====================================
import pdfkit
import markdown2
from datetime import datetime
from deep_translator import GoogleTranslator
import re


# =====================================
# IMPORT PERSONAL DETAILS
# =====================================

from my_details import (
    GMAIL_USER,
    GMAIL_PASS,
    full_name,
    location,
    email,
    phone,
    linkedin
)


# ===============================
# Input Section
# ===============================
print("\nEnter job application details (leave blank if unknown):\n")

def capitalize_input(text):
    """Capitalize the first letter of each word."""
    return text.strip().title()


star = input("Star                    : ").strip().lower()

hiring_manager = ""
company_name    = input("Company Name            : ")

if star == "y":
    AB = input("Blank                   : ")

job_title       = input("Job Title               : ")

AB              = input("Blank                   : ")
company_address = input("Company Address         : ")

region = company_address
# ===============================
# Handle hiring manager variations
# ===============================
if hiring_manager == "":
    hiring_manager1 = ""          # Before company name
    hiring_manager2 = "Sir/Madam" # Greeting
else:
    hiring_manager1 = hiring_manager
    hiring_manager2 = hiring_manager

# ===============================
# Check if job is for India
# ===============================
is_india = (region == "")

# ===============================
# Auto-generate current date
# ===============================
date_today = datetime.today().strftime("%B %d, %Y")  # e.g., June 05, 2026

# ===============================
# Personal Details (fill your info)
# ===============================
full_name = full_name
location = location
email = email
phone = phone
linkedin = linkedin

# ===============================
# Education, Certifications, Languages, Skills, Experience
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
    },
    {
        "title": "Executive Systems EDP",
        "company": "Anuradha Enterprises Pvt. Ltd.",
        "location": "New Delhi",
        "duration": "Mar 2018 – Mar 2022",
        "responsibilities": [
            "Managed accounting systems and email workflows for efficient billing.",
            "Created invoices, purchase orders, pricing reports.",
            "Provided IT support and system troubleshooting."
        ]
    }
]

# ===============================
# Configure PDFKit
# ===============================
path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

# ===============================
# CV Markdown Generator
# ===============================
def generate_cv_markdown():
    md = f"# {full_name}\n"
    md += f"{location}\nEmail: {email} | Phone: {phone} | LinkedIn: {linkedin}\n\n"

    md += "## PROFESSIONAL SUMMARY\n"
    md += "Experienced professional with 20+ years in administration, logistics, and system management. Currently transitioning into Data Analytics using Python, Power BI, SQL, and Excel.\n\n"

    md += "## CORE SKILLS\n"
    for skill in skills_list:
        md += f"- {skill}\n"

    md += "\n## PROFESSIONAL EXPERIENCE\n"
    for exp in experience_list:
        md += f"### {exp['title']} | {exp['company']}, {exp['location']} | {exp['duration']}\n"
        for resp in exp['responsibilities']:
            md += f"- {resp}\n"
        md += "\n"

    md += "## EDUCATION\n"
    for edu in education_list:
        md += f"- {edu['degree']} - {edu['institution']}, {edu['year']}\n"

    md += "\n## CERTIFICATIONS\n"
    for cert in certifications_list:
        md += f"- {cert}\n"

    md += "\n## LANGUAGES\n"
    for lang in languages_list:
        md += f"- {lang}\n"

    return md

# ===============================
# Cover Letter Markdown Generator
# ===============================

def generate_cover_letter_markdown():
    md = f"""# Cover Letter – {full_name}

{full_name}  
{location}  
Email: {email} | Phone: {phone}  

{date_today}  

{hiring_manager1}  
{company_name}  
{company_address}  

**Subject:** Application for {job_title}  

Dear {hiring_manager2},  

I am writing to express my interest in the {job_title} position at {company_name}.

With over twenty years of professional experience across system management, office administration, and application support—now strongly aligned with data science and analytics. I am eager to contribute to a modern, data-driven environment.

I bring a strong foundation in Data Analytics and software programming, along with 8 years in office administration and 3 years in logistics. In previous roles, I worked extensively as a System Manager and application support professional, responsible for the maintenance, troubleshooting, and enhancement of legacy business applications developed in Visual FoxPro. This experience developed a deep understanding of structured data, database-driven systems, and the importance of data integrity, reliability, and process continuity - core principles that directly align with data engineering and analytics.

Since January 2026, I have been actively working in Data Analytics using Python, Pandas, NumPy, and Power BI to transform data into actionable business insights. Alongside my professional experience, I am pursuing a Master’s in Data Science, developing practical skills in data wrangling, machine learning, big data processing with PySpark and Databricks, and data visualization using Power BI and Matplotlib. I also work with Azure Data Factory, SQL Server, and web scraping, enabling me to integrate and analyse data across modern business platforms.

I bring a strong foundation in Data Analytics and software programming, supported by experience in office administration and logistics. As a System Manager and application support professional, I maintained and enhanced business applications developed in Visual FoxPro, gaining valuable expertise in structured data, database systems, data integrity, and process optimization—skills that align closely with data engineering and analytics.

I would welcome the opportunity to discuss how my experience and skills can support your team.

In my current role as {experience_list[0]['title']} at {experience_list[0]['company']}, I have:
"""

    for resp in experience_list[0]['responsibilities']:
        md += f"- {resp}\n"

    md += "\n\nMy expertise in reporting and analytics enables me to bridge business and technical requirements effectively."

    if not is_india:
        md += f"\n\nI am particularly interested in opportunities where English-speaking roles are available."
        md += "\n\nI am also open to opportunities that offer Sponsored Work Permit Visa support and Relocation Assistance, and I am prepared to relocate for the right position."

    md += f"""

Thank you for your time and consideration.

Kind regards,

{full_name}
    """

    return md

# ===============================
# Translation Helper (Preserve Capitalization)
# ===============================
def preserve_capitals(english_text, translated_text):
    """Preserve capitalization of English proper nouns/acronyms in translated text."""
    caps = re.findall(r'\b[A-Z][a-zA-Z0-9&]+\b', english_text)
    for word in caps:
        translated_text = re.sub(r'\b' + re.escape(word.lower()) + r'\b', word, translated_text, flags=re.IGNORECASE)
    return translated_text

def translate_text(text, lang="en"):
    """Translate text and preserve capitalization."""
    if lang == "en":
        return text
    try:
        translated = GoogleTranslator(source='auto', target=lang).translate(text)
        translated = preserve_capitals(text, translated)
        return translated
    except Exception as e:
        print(f"Translation error ({lang}): {e}")
        return text

# ===============================
# Markdown to PDF
# ===============================
def md_to_pdf(md_content, file_name, lang="en"):
    md_content = translate_text(md_content, lang)
    html_body = markdown2.markdown(md_content)
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.5; }}
            h1, h2, h3 {{ color: #222; }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    pdfkit.from_string(html, file_name, configuration=config)
    print(f"✅ PDF generated: {file_name} ({lang})")

# ===============================
# Generate PDFs in Multiple Languages
# ===============================
cv_md = generate_cv_markdown()
cover_md = generate_cover_letter_markdown()

languages = {
    "English": "en",
    "German": "de",
    "Italian": "it",
    "French": "fr",
    "Dutch": "nl",
}

for language_name, lang_code in languages.items():
    # md_to_pdf(cv_md, f"CV_{language_name}.pdf", lang=lang_code)
    md_to_pdf(cover_md, f"Cover_Letter_{language_name}.pdf", lang=lang_code)

print("\n🎉 All PDFs generated successfully!")