# LeadGen-Pro : Lead Generation Tool

**LeadGen Pro** is a fast, elegant, and AI-ready lead generation tool that extracts high-value company information from any domain. Built in under 5 hours for the [Caprae Capital AI-Readiness Challenge](https://www.saasquatchleads.com), it demonstrates how practical AI and thoughtful UX can turn raw web data into strategic insight.

---

## Features

Enter any company domain
Extract:
- IP Address  
- Website Title  
- Auto-Generated Company Email  
- LinkedIn URL (company-level)  
- Email Verification via [Abstract API](https://www.abstractapi.com/email-verification-api)  
Download Lead Data as:
- CSV  
- PDF  

Smart, clean UI (Dark mode)  
Fully deployable via Streamlit Cloud or locally  

---

## Tech Stack

- Python 3.9+
- Streamlit
- BeautifulSoup (HTML parsing)
- Requests
- Abstract Email Verification API
- ReportLab (PDF generation)
- Pandas
- PIL (Logo embedding)

---

## Business Rationale

This tool is designed to be integrated into post-acquisition sales workflows. It supports:
- Fast prospecting
- Pre-CRM lead intelligence
- Automated email enrichment & validation
- Export-ready formats for sales teams

Aligned with Caprae Capital's mission to support SaaS businesses with real, usable AI tools.

---

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/yourusername/leadgen-pro.git
cd leadgen-pro

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the app
streamlit run app.py

## Environment Variables
Set your Abstract API key for email verification:

Inside app.py, update this line:
API_KEY = "your_abstract_api_key"
You can get a free key from https://www.abstractapi.com

---

## Author
Built by Nagendra U S


