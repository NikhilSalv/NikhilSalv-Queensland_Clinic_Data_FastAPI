import streamlit as st
import requests

# FastAPI base URL
base_url = "http://127.0.0.1:8080"

# Streamlit app
st.title("Queensland Clinic Scraper")

# Button to start data extraction and save to CSV
if st.button("Extract Data and Download CSV"):
    with st.spinner('Extracting data...'):
        # Call the FastAPI endpoint to scrape data and download the CSV
        response = requests.get(f"{base_url}/save_to_csv")
    
    if response.status_code == 200:

        file_name = "queensland_clinics_detailed.csv"
        file_path = f"{base_url}/save_to_csv"
        # Provide a link for the user to download the file
        st.success("Data extraction complete. Click the link below to download the CSV.")
        st.download_button(label="Download CSV", data=requests.get(file_path).content, file_name=file_name, mime='text/csv')
    else:
        st.error("Failed to extract data or connect to the FastAPI server.")
