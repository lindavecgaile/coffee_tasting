import streamlit as st
import pandas as pd

# Function to load existing data or create a new DataFrame
def load_data():
    try:
        return pd.read_csv("coffee_tasting_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Session Number", "Date of Tasting", "Coffee Name", "Roast Level", "Brew Method", "Acidity", "Sweetness", "Body", "Flavor Notes", "Overall Rating", "Tasting Notes"])

# Title and header for the Streamlit app
st.title("Coffee Tasting Club")
st.header("Enter Coffee Tasting Data")

# Input fields for coffee tasting data
session_number = st.text_input("Session Number")
tasting_date = st.date_input("Date of Tasting")
coffee_name = st.text_input("Coffee Name")
roast_level = st.selectbox("Roast Level", ["Light", "Light-Medium", "Medium", "Medium-Dark", "Dark"])
brew_method = st.selectbox("Brew Method", ["V60", "AeroPress", "Espresso", "French Press", "Chemex", "Cold Brew", "Moka Pot", "Pour Over", "Siphon", "Turkish Coffee"])
acidity = st.slider("Acidity (1 = Low, 10 = High)", 1, 10, 5)
sweetness = st.slider("Sweetness (1 = Low, 10 = High)", 1, 10, 5)
body = st.slider("Body (1 = Light, 10 = Heavy)", 1, 10, 5)
flavor_notes = st.text_input("Flavor Notes")
overall_rating = st.slider("Overall Rating (1 to 10)", 1, 10)
tasting_notes = st.text_area("Tasting Notes")

# Submit button to save the data
if st.button("Submit"):
    # Load the existing data
    data = load_data()

    # Create a new entry as a dictionary
    new_entry = {
        "Session Number": session_number,
        "Date of Tasting": tasting_date,
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

    # Use pd.concat() to add the new entry to the existing data
    data = pd.concat([data, pd.DataFrame([new_entry])], ignore_index=True)

    # Save the updated data to CSV
    data.to_csv("coffee_tasting_data.csv", index=False)
    st.success("Data saved successfully!")

# Display the existing data in a table format
st.header("Previous Tasting Sessions")
data = load_data()
st.dataframe(data)