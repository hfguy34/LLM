import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ---- Google Sheets Setup ----
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from Streamlit secrets
service_account_info = st.secrets["google_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

# Use your specific Google Sheet by ID (from the link)
sheet = client.open_by_key("1VysccmFSZNpQSsqvZ6J0uaXnIh1SHE_Q60l3zDZwYyo").sheet1  # Defaults to first sheet

# ---- Streamlit UI ----
st.set_page_config(page_title="Daily Work Tracker", layout="centered")
st.title("📆 Daily Work Log Entry")

# Date picker
selected_date = st.date_input("Select Date", datetime.today())

# User inputs
name = st.text_input("Your Name")
work_done = st.text_area("Work Done")

# Submit button
if st.button("Submit"):
    if not name or not work_done:
        st.error("Please fill in all fields.")
    else:
        try:
            sheet.append_row([str(selected_date), name, work_done])
            st.success("✅ Your work log has been saved.")
        except Exception as e:
            st.error(f"Error saving to Google Sheet: {e}")
