import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import plotly.express as px

# Define the required OAuth scopes for Google Sheets and Drive
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Load Google Sheets credentials from Streamlit Secrets with the necessary scopes
credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)

# Authorize the gspread client using the credentials
client = gspread.authorize(credentials)

# Open the Google Sheet and select the first sheet by name
sheet = client.open("Coffee_Tasting_Data").sheet1

# Load data from the Google Sheet into a Pandas DataFrame
def load_data():
    sheet_data = sheet.get_all_records()
    return pd.DataFrame(sheet_data)

# Save the DataFrame back to the Google Sheet
def save_data(df):
    sheet.clear()  # Clear the existing data in the sheet
    sheet.update([df.columns.values.tolist()] + df.values.tolist())  # Update with new data

# Load existing data from Google Sheets
data = load_data()

# Streamlit app title and description
st.title("Coffee Snob Club")  # Updated title
st.header("Enter Coffee Tasting Data")

# Correctly wrap all input fields inside a single form with a visible Submit button
with st.form(key="tasting_form", clear_on_submit=True):
    # Input fields for coffee tasting data inside the form
    session_number = st.text_input("Session Number")         # e.g., "Session 1"
    tasting_date = st.date_input("Date of Tasting")          # e.g., Date Picker
    taster_name = st.text_input("Taster Name")               # e.g., "John Doe"
    coffee_name = st.text_input("Coffee Name")               # e.g., "Ethiopian Yirgacheffe"
    roast_level = st.selectbox("Roast Level", ["Light", "Light-Medium", "Medium", "Medium-Dark", "Dark"])
    brew_method = st.selectbox("Brew Method", ["V60", "AeroPress", "Espresso", "French Press", "Chemex", "Cold Brew", "Moka Pot", "Pour Over", "Siphon", "Turkish Coffee"])
    acidity = st.slider("Acidity (1 = Low, 10 = High)", 1, 10, 5)
    sweetness = st.slider("Sweetness (1 = Low, 10 = High)", 1, 10, 5)
    body = st.slider("Body (1 = Light, 10 = Heavy)", 1, 10, 5)
    flavor_notes = st.text_input("Flavor Notes")             # e.g., "Citrus, Berry"
    overall_rating = st.slider("Overall Rating (1 to 10)", 1, 10)
    tasting_notes = st.text_area("Tasting Notes")            # Detailed comments or observations

    # Visible submit button for the form
    submit_button = st.form_submit_button(label="Submit")    # Use st.form_submit_button inside the form

# Handle the submission
if submit_button:
    # Create a new entry from the form inputs
    new_entry = {
        "Session Number": session_number,
        "Date of Tasting": tasting_date,
        "Taster": taster_name,
        "Coffee Name": coffee_name,
        "Roast Level": roast_level,
        "Brew Method": brew_method,
        "Acidity": acidity,
        "Sweetness": sweetness,
        "Body": body,
        "Flavor Notes": flavor_notes,
        "Overall Rating": overall_rating,
        "Tasting Notes": tasting_notes,
    }

    # Append the new entry to the existing data
    data = pd.concat([data, pd.DataFrame([new_entry])], ignore_index=True)
    save_data(data)  # Save the updated data back to Google Sheets
    st.success(f"New tasting session added successfully by {taster_name}!")
