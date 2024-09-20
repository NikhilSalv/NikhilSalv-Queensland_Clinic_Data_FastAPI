import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage to scrape
url = "https://www.health.qld.gov.au/services"

# Send a request to fetch the HTML content
response = requests.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the division by its ID
content_container = soup.find('div', id='content_container_138603_138603')

# Initialize a list to hold hospital names
hospital_list = []

# Iterate over each <h2> and corresponding <ul> after it
for h2 in content_container.find_all('h2'):
    # Get the letter (A, B, C, etc.)
    letter = h2.text.strip()

    # Find the next <ul> after each <h2> and get all <li> tags inside
    ul = h2.find_next('ul')
    
    if ul:
        for li in ul.find_all('li'):
            # Extract the clinic/hospital name from <li>
            clinic_name = li.text.strip()
            if clinic_name:
                hospital_list.append([letter, clinic_name])

# Create a DataFrame to store the data
df = pd.DataFrame(hospital_list, columns=["Letter", "Clinic/Hospital Name"])

# Save to a CSV file
df.to_csv("queensland_clinics.csv", index=False)

print("Data extracted and saved to queeensland_clinics.csv")
