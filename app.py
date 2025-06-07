import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

# ---- Google Sheets Setup ----
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from Streamlit secrets
creds_dict = {
    "type": st.secrets["google_service_account"]["type"],
    "project_id": st.secrets["google_service_account"]["project_id"],
    "private_key_id": st.secrets["google_service_account"]["private_key_id"],
    "private_key": st.secrets["google_service_account"]["private_key"].replace('\\n', '\n'),
    "client_email": st.secrets["google_service_account"]["client_email"],
    "client_id": st.secrets["google_service_account"]["client_id"],
    "auth_uri": st.secrets["google_service_account"]["auth_uri"],
    "token_uri": st.secrets["google_service_account"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["google_service_account"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["google_service_account"]["client_x509_cert_url"],
}

# Authorize with Google Sheets
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open your Google Sheet by key
sheet = client.open_by_key("1VysccmFSZNpQSsqvZ6J0uaXnIh1SHE_Q60l3zDZwYyo").sheet1

# ---- Streamlit UI ----
st.set_page_config(page_title="Daily Work Tracker", layout="centered")
st.title("📆 Daily Work Log Entry")

selected_date = st.date_input("Select Date", datetime.today())
name = st.text_input("Your Name")
work_done = st.text_area("Work Done")

if st.button("Submit"):
    if not name.strip() or not work_done.strip():
        st.error("Please fill in all fields.")
    else:
        try:
            sheet.append_row([str(selected_date), name, work_done])
            st.success("✅ Your work log has been saved.")
        except Exception as e:
            st.error(f"Error saving to Google Sheet: {e}")
