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

# Use the new Spreadsheet ID to access the Google Sheet
sheet = client.open_by_key("1VEzDuBcyEGGtYT2m0P7uwiZRfTWl84Cb2b7eQkCMOlo").sheet1

# Load data from the Google Sheet into a Pandas DataFrame
def load_data():
    sheet_data = sheet.get_all_records()
    return pd.DataFrame(sheet_data)

# Save the DataFrame back to the Google Sheet
def save_data(df):
    # Convert the Date of Tasting column to strings
    if "Date of Tasting" in df.columns:
        df["Date of Tasting"] = df["Date of Tasting"].astype(str)
    
    # Clear the existing data in the sheet and update with the new data
    sheet.clear()  
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

# Display existing data in a table
st.header("Previous Tasting Sessions")
if not data.empty:
    st.dataframe(data)

    # Add selection box for editing and deleting entries
    selected_index = st.number_input("Select a row to edit or delete", min_value=0, max_value=len(data)-1, step=1)
    
    # Show the selected entry details
    st.write("### Selected Entry:")
    st.write(data.iloc[selected_index])

    # Handle editing of an existing entry
    with st.form(key="edit_entry_form"):
        # Fill in the default values for editing form
        edited_session_number = st.text_input("Edit Session Number", value=str(data.iloc[selected_index].get("Session Number", "")))
        edited_tasting_date = st.date_input("Edit Date of Tasting", value=pd.to_datetime(data.iloc[selected_index].get("Date of Tasting", pd.Timestamp.now())))
        edited_taster_name = st.text_input("Edit Taster Name", value=data.iloc[selected_index].get("Taster", ""))
        edited_coffee_name = st.text_input("Edit Coffee Name", value=data.iloc[selected_index].get("Coffee Name", ""))
        edited_roast_level = st.selectbox("Edit Roast Level", ["Light", "Light-Medium", "Medium", "Medium-Dark", "Dark"], index=["Light", "Light-Medium", "Medium", "Medium-Dark", "Dark"].index(data.iloc[selected_index].get("Roast Level", "Medium")))
        edited_brew_method = st.selectbox("Edit Brew Method", ["V60", "AeroPress", "Espresso", "French Press", "Chemex", "Cold Brew", "Moka Pot", "Pour Over", "Siphon", "Turkish Coffee"], index=["V60", "AeroPress", "Espresso", "French Press", "Chemex", "Cold Brew", "Moka Pot", "Pour Over", "Siphon", "Turkish Coffee"].index(data.iloc[selected_index].get("Brew Method", "V60")))
        edited_acidity = st.slider("Edit Acidity (1 = Low, 10 = High)", 1, 10, value=int(data.iloc[selected_index].get("Acidity", 5)))
        edited_sweetness = st.slider("Edit Sweetness (1 = Low, 10 = High)", 1, 10, value=int(data.iloc[selected_index].get("Sweetness", 5)))
        edited_body = st.slider("Edit Body (1 = Light, 10 = Heavy)", 1, 10, value=int(data.iloc[selected_index].get("Body", 5)))
        edited_flavor_notes = st.text_input("Edit Flavor Notes", value=data.iloc[selected_index].get("Flavor Notes", ""))
        edited_overall_rating = st.slider("Edit Overall Rating (1 to 10)", 1, 10, value=int(data.iloc[selected_index].get("Overall Rating", 5)))
        edited_tasting_notes = st.text_area("Edit Tasting Notes", value=data.iloc[selected_index].get("Tasting Notes", ""))

        # Submit button for editing the entry
        update_button = st.form_submit_button("Update Entry")
        if update_button:
            # Update the selected row with new values
            data.at[selected_index, "Session Number"] = edited_session_number
            data.at[selected_index, "Date of Tasting"] = edited_tasting_date
            data.at[selected_index, "Taster"] = edited_taster_name
            data.at[selected_index, "Coffee Name"] = edited_coffee_name
            data.at[selected_index, "Roast Level"] = edited_roast_level
            data.at[selected_index, "Brew Method"] = edited_brew_method
            data.at[selected_index, "Acidity"] = edited_acidity
            data.at[selected_index, "Sweetness"] = edited_sweetness
            data.at[selected_index, "Body"] = edited_body
            data.at[selected_index, "Flavor Notes"] = edited_flavor_notes
            data.at[selected_index, "Overall Rating"] = edited_overall_rating
            data.at[selected_index, "Tasting Notes"] = edited_tasting_notes

            # Save the updated data back to Google Sheets
            save_data(data)
            st.success(f"Entry updated successfully for {edited_taster_name}!")

# Bar Chart: Show average ratings for each coffee grouped by taster
if not data.empty:
    st.header("Average Ratings per Coffee by Taster")
    fig = px.bar(
        data,
        x="Coffee Name",
        y="Overall Rating",
        color="Taster",
        barmode="group",
        labels={"Coffee Name": "Coffee", "Overall Rating": "Average Rating"},
        title="Average Ratings of Coffees by Each Taster"
    )
    st.plotly_chart(fig)
