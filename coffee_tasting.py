import streamlit as st
import pandas as pd
import plotly.express as px

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

    # Bar Chart: Show average ratings for each coffee
    st.header("Average Ratings for Each Coffee")

    # Group by Coffee Name and calculate the mean of ratings for each coffee
    rating_summary = data.groupby("Coffee Name")["Overall Rating"].mean().reset_index()

    # Sort the summary by highest average rating
    rating_summary = rating_summary.sort_values("Overall Rating", ascending=False)

    # Plot the bar chart using Plotly
    fig = px.bar(
        rating_summary,
        x="Coffee Name",
        y="Overall Rating",
        color="Overall Rating",
        color_continuous_scale='Blues',
        labels={"Coffee Name": "Coffee", "Overall Rating": "Average Rating"},
        title="Average Ratings of Coffees"
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)
else:
    st.warning("No tasting sessions available yet. Please add some entries.")
