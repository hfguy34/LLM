import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Define scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load creds from secrets
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_service_account"], scope)
client = gspread.authorize(creds)

# Connect to your sheet
sheet = client.open_by_key("1VysccmFSZNpQSsqvZ6J0uaXnIh1SHE_Q60l3zDZwYyo").sheet1

# Streamlit UI
st.set_page_config(page_title="Daily Work Tracker")
st.title("📆 Daily Work Log Entry")

selected_date = st.date_input("Select Date", datetime.today())
name = st.text_input("Your Name")
work_done = st.text_area("Work Done")

if st.button("Submit"):
    if not name or not work_done:
        st.error("Please fill in all fields.")
    else:
        sheet.append_row([str(selected_date), name, work_done])
        st.success("✅ Your work log has been saved.")
