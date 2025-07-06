import streamlit as st
import requests, socket, os
import pandas as pd
from bs4 import BeautifulSoup
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import base64

# === PAGE CONFIG ===
st.set_page_config(page_title="LeadGen Pro", page_icon="leadgen_logo.png", layout="wide")

# === LOGO ===
def load_logo():
    with open("leadgen_logo.png", "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"<img src='data:image/png;base64,{encoded}' width='130' style='margin-bottom:-20px;'/>"

st.markdown(f"<div style='text-align: center;'>{load_logo()}</div>", unsafe_allow_html=True)

# === CSS ===
st.markdown("""
    <style>
    body            { background:#0d0d0d; }
    .stApp          { background:#0d0d0d; color:#ffffff; }

    .stTextInput > div > input {
        background-color: #2c2c2c !important;
        color: white !important;
        border: 1px solid #5e5e5e;
        border-radius: 8px;
    }

    .stTextInput input:disabled {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 500;
        border: 1px solid #888;
        border-radius: 8px;
    }

    .stTextInput label {
        font-size: 36px !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        letter-spacing: 0.8px !important;
        margin-bottom: 10px !important;
    }

    .stButton button {
        color: white;
        background-color: #8e44ad;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-size: 16px;
    }

    .stButton button:hover {
        background-color: #9b59b6;
        transition: 0.3s;
    }

    .stDownloadButton button {
        background-color: #34495e;
        color: white;
        border-radius: 8px;
        font-weight: 500;
        padding: 10px 20px;
        font-size: 15px;
    }

    .centered-title    { text-align:center; color:#b48ef2; font-size:36px; margin-bottom:-10px; }
    
    /* Subtitle customized */
    .centered-subtitle {
        text-align: center;
        color: #d3d3ff;
        font-size: 20px;
        font-weight: 500;
        letter-spacing: 0.5px;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    .main > div {
        padding-top: 0rem !important;
    }

    .block-container {
        padding-top: 3rem !important;
        margin-top: -10px !important;
    }

    img {
        margin-top: -40px;
    }
    </style>
""", unsafe_allow_html=True)

# === ABSTRACT API KEY ===
API_KEY = "aac864f47288445b9bb7d1623f5d5391"

# === FUNCTIONS ===
def get_verified_email(email: str) -> str:
    try:
        url = f"https://emailvalidation.abstractapi.com/v1/?api_key={API_KEY}&email={email}"
        res = requests.get(url, timeout=4).json()
        return f"{email} {'✅' if res.get('deliverability') == 'DELIVERABLE' else '❌'}"
    except:
        return f"{email} ❌"

def generate_pdf(data: dict, filename="lead_info.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, y, "Lead Info Report")
    c.setFont("Helvetica", 12)
    y -= 40
    for key, value in data.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 25
    c.save()

# === HEADER ===
st.markdown("<h1 class='centered-title'>🔍 Lead Generation Tool</h1>", unsafe_allow_html=True)
st.markdown("<p class='centered-subtitle'>Enter a domain to extract useful company lead information.</p>", unsafe_allow_html=True)

# === MAIN LAYOUT ===
sp_l, col_in, gap, col_out, sp_r = st.columns([1, 3.5, 0.5, 3.5, 1])

# === INPUT COLUMN ===
with col_in:
       st.markdown("""
    <p style='
        font-size: 24px;
        color: white;
        font-weight: bold;
        margin-bottom: -5px;
        line-height: 1;
    '>Domain:</p>
    """, unsafe_allow_html=True)

       domain = st.text_input("", placeholder="e.g., openai.com")
       if st.button("**Get Lead Info**"):
        st.session_state.domain = domain

# === OUTPUT COLUMN ===
if 'domain' in st.session_state and st.session_state.domain.strip():
    domain = st.session_state.domain.strip()

    try:
        ip = socket.gethostbyname(domain)
        try:
            html = requests.get(f"https://{domain}", timeout=4, headers={'User-Agent': 'Mozilla/5.0'}).text
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string.strip() if soup.title else "N/A"
        except:
            title = "N/A"

        email = f"info@{domain}"
        verified = get_verified_email(email)
        linkedin = f"https://www.linkedin.com/company/{domain.split('.')[0]}"

        data = {
            "Domain": domain,
            "IP Address": ip,
            "Website Title": title,
            "Verified Email": verified,
            "LinkedIn": linkedin
        }

        with col_out:
            st.markdown("<p style='color:#3498db; font-size:20px; font-weight:700;'> Data fetched successfully!</p>", unsafe_allow_html=True)
            st.text_input("**Domain:**", value=domain, disabled=True)
            st.text_input("**IP Address:**", value=ip, disabled=True)
            st.markdown(f"**Website Title:** {title}")
            st.markdown(f"**Email:** {email} {'✅' if '✅' in verified else '❌'}")
            st.markdown(f"**LinkedIn:** [Visit LinkedIn]({linkedin})")

            df = pd.DataFrame([data])
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download CSV", csv, file_name="lead_info.csv", mime="text/csv")

            generate_pdf(data)
            with open("lead_info.pdf", "rb") as f:
                st.download_button("⬇️ Download PDF", data=f, file_name="lead_info.pdf", mime="application/pdf")
            
            if os.path.exists("lead_info.pdf"):
                os.remove("lead_info.pdf")

    except Exception as e:
        with col_out:
            st.error(f"❌ Error: {e}")
