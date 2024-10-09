import streamlit as st
import pandas as pd

# Function to load data from a CSV file
def load_data():
    try:
        return pd.read_csv("coffee_tasting_data.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=[
            "Session Number", "Date of Tasting", "Coffee Name", "Roast Level", "Brew Method", 
            "Acidity", "Sweetness", "Body", "Flavor Notes", "Overall Rating", "Tasting Notes"
        ])

# Function to save data back to CSV
def save_data(data):
    data.to_csv("coffee_tasting_data.csv", index=False)

# Load existing data
data = load_data()

# Streamlit app title and description
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

# Submit button to add a new entry
if st.button("Submit"):
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
    
    # Append new entry to the dataframe
    data = pd.concat([data, pd.DataFrame([new_entry])], ignore_index=True)
    save_data(data)  # Save updated data
    st.success("New tasting session added successfully!")

# Display existing data in a table
st.header("Previous Tasting Sessions")
if not data.empty:
    st.dataframe(data)

    # Add selection box for editing and deleting entries
    selected_index = st.number_input("Select a row to edit or delete", min_value=0, max_value=len(data)-1, step=1)
    
    # Show the selected entry details
    st.write("### Selected Entry:")
    st.write(data.iloc[selected_index])

    # Edit the selected entry
    if st.button("Edit Selected Entry"):
        with st.form("Edit Entry"):
            edited_session_number = st.text_input("Edit Session Number", value=data.iloc[selected_index]["Session Number"])
            edited_tasting_date = st.date_input("Edit Date of Tasting", value=pd.to_datetime(data.iloc[selected_index]["Date of Tasting"]))
            edited_coffee_name = st.text_input("Edit Coffee Name", value=data.iloc[selected_index]["Coffee Name"])
            edited_roast_level = st.selectbox("Edit Roast Level", ["Light", "Light-Medium", "Medium", "Medium-Dark", "Dark"], index=["Light", "Light-Medium", "Medium", "Medium-Dark", "Dark"].index(data.iloc[selected_index]["Roast Level"]))
            edited_brew_method = st.selectbox("Edit Brew Method", ["V60", "AeroPress", "Espresso", "French Press", "Chemex", "Cold Brew", "Moka Pot", "Pour Over", "Siphon", "Turkish Coffee"], index=["V60", "AeroPress", "Espresso", "French Press", "Chemex", "Cold Brew", "Moka Pot", "Pour Over", "Siphon", "Turkish Coffee"].index(data.iloc[selected_index]["Brew Method"]))
            edited_acidity = st.slider("Edit Acidity (1 = Low, 10 = High)", 1, 10, value=int(data.iloc[selected_index]["Acidity"]))
            edited_sweetness = st.slider("Edit Sweetness (1 = Low, 10 = High)", 1, 10, value=int(data.iloc[selected_index]["Sweetness"]))
            edited_body = st.slider("Edit Body (1 = Light, 10 = Heavy)", 1, 10, value=int(data.iloc[selected_index]["Body"]))
            edited_flavor_notes = st.text_input("Edit Flavor Notes", value=data.iloc[selected_index]["Flavor Notes"])
            edited_overall_rating = st.slider("Edit Overall Rating (1 to 10)", 1, 10, value=int(data.iloc[selected_index]["Overall Rating"]))
            edited_tasting_notes = st.text_area("Edit Tasting Notes", value=data.iloc[selected_index]["Tasting Notes"])

            # Submit button to update the edited entry
            if st.form_submit_button("Update Entry"):
                # Update the selected row with new values
                data.at[selected_index, "Session Number"] = edited_session_number
                data.at[selected_index, "Date of Tasting"] = edited_tasting_date
                data.at[selected_index, "Coffee Name"] = edited_coffee_name
                data.at[selected_index, "Roast Level"] = edited_roast_level
                data.at[selected_index, "Brew Method"] = edited_brew_method
                data.at[selected_index, "Acidity"] = edited_acidity
                data.at[selected_index, "Sweetness"] = edited_sweetness
                data.at[selected_index, "Body"] = edited_body
                data.at[selected_index, "Flavor Notes"] = edited_flavor_notes
                data.at[selected_index, "Overall Rating"] = edited_overall_rating
                data.at[selected_index, "Tasting Notes"] = edited_tasting_notes

                # Save the updated data
                save_data(data)
                st.success("Entry updated successfully!")

    # Delete button to remove a row
    if st.button("Delete Selected Entry"):
        data = data.drop(selected_index).reset_index(drop=True)
        save_data(data)  # Save after deleting
        st.success("Entry deleted successfully!")
else:
    st.warning("No tasting sessions available yet. Please add some entries.")
