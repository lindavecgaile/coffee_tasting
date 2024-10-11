import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import plotly.express as px
import qrcode
from PIL import Image

# Define the required OAuth scopes for Google Sheets and Drive
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Load Google Sheets credentials from Streamlit Secrets with the necessary scopes
credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)

# Authorize the gspread client using the credentials
client = gspread.authorize(credentials)

# Use the Spreadsheet ID to access the Google Sheet
sheet = client.open_by_key("1VEzDuBcyEGGtYT2m0P7uwiZRfTWl84Cb2b7eQkCMOlo").sheet1

# Load data from the Google Sheet into a Pandas DataFrame
def load_data():
    sheet_data = sheet.get_all_records()
    return pd.DataFrame(sheet_data)

# Save the DataFrame back to the Google Sheet
def save_data(df):
    df = df.astype(str)  # Convert all data types to strings to avoid JSON issues
    sheet.clear()
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

# Load existing data from Google Sheets
data = load_data()

# Preprocess 'Bean Origin Countries' to ensure no NaN or unexpected types
data["Bean Origin Countries"] = data["Bean Origin Countries"].fillna("").astype(str)

# Streamlit app title and description
st.title("Coffee Snob Club")

# URL of the deployed Streamlit app (replace this with your actual app link)
# app_url = "https://your-app-link.streamlit.app"  # Replace with your actual app URL
app_url = "https://coffeetasting.streamlit.app"  # Replace with your actual app URL

# Generate and display the QR code for easy sharing
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data(app_url)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white")
qr_img.save("streamlit_qr_code.png")
st.image("streamlit_qr_code.png", caption="Scan this QR code to share the Coffee Snob Club app!", use_column_width=True)

# Now add the section title below the QR code
st.header("Enter Coffee Tasting Data")

# Define country options for the dropdown menu
countries = ["Brazil", "Colombia", "Ethiopia", "Guatemala", "Kenya", "Costa Rica", "Peru", "India", "Honduras", "Indonesia"]

# Wrap all input fields inside a single form with a visible Submit button
with st.form(key="tasting_form", clear_on_submit=True):
    session_number = st.text_input("Session Number")
    tasting_date = st.date_input("Date of Tasting")
    taster_name = st.text_input("Taster Name")
    coffee_name = st.text_input("Coffee Name")
    roast_level = st.selectbox("Roast Level", ["Light", "Light-Medium", "Medium", "Medium-Dark", "Dark"])
    brew_method = st.selectbox("Brew Method", ["V60", "AeroPress", "Espresso", "French Press", "Chemex", "Cold Brew", "Moka Pot", "Pour Over", "Siphon", "Turkish Coffee"])
    shop_name = st.text_input("Shop Name (Where Coffee Was Bought)")
    address = st.text_input("Address (Where Coffee Was Bought)")
    roasted_at = st.text_input("Roasted At (Roasting Location)")  # New input for roasting location
    bean_origins = st.multiselect("Bean Origin Countries", countries)  # Multi-select field for coffee bean origins
    acidity = st.slider("Acidity (1 = Low, 10 = High)", 1, 10, 5)
    sweetness = st.slider("Sweetness (1 = Low, 10 = High)", 1, 10, 5)
    body = st.slider("Body (1 = Light, 10 = Heavy)", 1, 10, 5)
    flavor_notes = st.text_input("Flavor Notes")
    overall_rating = st.slider("Overall Rating (1 to 10)", 1, 10)
    tasting_notes = st.text_area("Tasting Notes")
    submit_button = st.form_submit_button(label="Submit")  # Submit button for the form

# Handle the submission
if submit_button:
    new_entry = {
        "Session Number": session_number,
        "Date of Tasting": str(tasting_date),  # Convert date to string to prevent JSON issues
        "Taster": taster_name,
        "Coffee Name": coffee_name,
        "Roast Level": roast_level,
        "Brew Method": brew_method,
        "Shop Name": shop_name,
        "Address": address,
        "Roasted At": roasted_at,
        "Bean Origin Countries": ", ".join(bean_origins),  # Save selected countries as a comma-separated string
        "Acidity": acidity,
        "Sweetness": sweetness,
        "Body": body,
        "Flavor Notes": flavor_notes,
        "Overall Rating": overall_rating,
        "Tasting Notes": tasting_notes,
    }
    data = pd.concat([data, pd.DataFrame([new_entry])], ignore_index=True)
    save_data(data)
    st.success(f"New tasting session added successfully by {taster_name}!")

# Display existing data in a table
st.header("Previous Tasting Sessions")
if not data.empty:
    st.dataframe(data)

    # Add selection box for editing and deleting entries
    selected_index = st.number_input("Select a row to edit or delete", min_value=0, max_value=len(data)-1, step=1)
    st.write("### Selected Entry:")
    st.write(data.iloc[selected_index])

    # Handle editing of an existing entry
    with st.form(key="edit_entry_form"):
        edited_session_number = st.text_input("Edit Session Number", value=str(data.iloc[selected_index].get("Session Number", "")))
        edited_tasting_date = st.date_input("Edit Date of Tasting", value=pd.to_datetime(data.iloc[selected_index].get("Date of Tasting", pd.Timestamp.now())))
        edited_taster_name = st.text_input("Edit Taster Name", value=data.iloc[selected_index].get("Taster", ""))
        edited_coffee_name = st.text_input("Edit Coffee Name", value=data.iloc[selected_index].get("Coffee Name", ""))
        edited_roast_level = st.selectbox("Edit Roast Level", ["Light", "Light-Medium", "Medium", "Medium-Dark", "Dark"], index=["Light", "Light-Medium", "Medium", "Medium-Dark", "Dark"].index(data.iloc[selected_index].get("Roast Level", "Medium")))
        edited_brew_method = st.selectbox("Edit Brew Method", ["V60", "AeroPress", "Espresso", "French Press", "Chemex", "Cold Brew", "Moka Pot", "Pour Over", "Siphon", "Turkish Coffee"], index=["V60", "AeroPress", "Espresso", "French Press", "Chemex", "Cold Brew", "Moka Pot", "Pour Over", "Siphon", "Turkish Coffee"].index(data.iloc[selected_index].get("Brew Method", "V60")))
        edited_shop_name = st.text_input("Edit Shop Name", value=data.iloc[selected_index].get("Shop Name", ""))
        edited_address = st.text_input("Edit Address", value=data.iloc[selected_index].get("Address", ""))
        edited_roasted_at = st.text_input("Edit Roasted At", value=data.iloc[selected_index].get("Roasted At", ""))
        
        # Corrected to handle missing or malformed data
        default_origins = data.iloc[selected_index].get("Bean Origin Countries", "")
        if not isinstance(default_origins, str):
            default_origins = ""
        edited_origins = st.multiselect("Edit Bean Origin Countries", countries, default=default_origins.split(", ") if default_origins else [])
        
        edited_acidity = st.slider("Edit Acidity (1 = Low, 10 = High)", 1, 10, value=int(data.iloc[selected_index].get("Acidity", 5)))
        edited_sweetness = st.slider("Edit Sweetness (1 = Low, 10 = High)", 1, 10, value=int(data.iloc[selected_index].get("Sweetness", 5)))
        edited_body = st.slider("Edit Body (1 = Light, 10 = Heavy)", 1, 10, value=int(data.iloc[selected_index].get("Body", 5)))
        edited_flavor_notes = st.text_input("Edit Flavor Notes", value=data.iloc[selected_index].get("Flavor Notes", ""))
        edited_overall_rating = st.slider("Edit Overall Rating (1 to 10)", 1, 10, value=int(data.iloc[selected_index].get("Overall Rating", 5)))
        edited_tasting_notes = st.text_area("Edit Tasting Notes", value=data.iloc[selected_index].get("Tasting Notes", ""))

        # Submit button for editing the entry
        update_button = st.form_submit_button("Update Entry")
        if update_button:
            data.at[selected_index, "Session Number"] = edited_session_number
            data.at[selected_index, "Date of Tasting"] = str(edited_tasting_date)  # Convert date to string
            data.at[selected_index, "Taster"] = edited_taster_name
            data.at[selected_index, "Coffee Name"] = edited_coffee_name
            data.at[selected_index, "Roast Level"] = edited_roast_level
            data.at[selected_index, "Brew Method"] = edited_brew_method
            data.at[selected_index, "Shop Name"] = edited_shop_name
            data.at[selected_index, "Address"] = edited_address
            data.at[selected_index, "Roasted At"] = edited_roasted_at
            data.at[selected_index, "Bean Origin Countries"] = ", ".join(edited_origins)  # Save selected countries as a comma-separated string
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
