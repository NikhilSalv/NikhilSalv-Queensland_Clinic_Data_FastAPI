import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL of the main page to scrape
main_url = "https://www.health.qld.gov.au/services"

# Function to extract clinic details from the individual clinic page
def get_clinic_details(clinic_url):
    try:
        response = requests.get(clinic_url)
        clinic_soup = BeautifulSoup(response.content, "html.parser")
        
        # Initialize the details with None in case they're not found
        contact = None
        address = None
        website = None
        
        # Extract contact info (Assuming it's under a <p> or similar tag with a specific class or structure)
        # This part may need adjustment based on the actual structure of the clinic pages
        contact_section = clinic_soup.find('p', string=lambda x: x and 'Phone' in x)
        if contact_section:
            contact = contact_section.text.strip()
        
        # Extract address info (Assuming it's under a <p> or <address> tag)
        address_section = clinic_soup.find('address')
        if address_section:
            address = address_section.text.strip()

        # Extract website if it exists (Assuming it's inside an <a> tag)
        website_section = clinic_soup.find('a', href=True, string=lambda x: x and 'website' in x.lower())
        if website_section:
            website = website_section['href']
        
        return contact, address, website

    except Exception as e:
        print(f"Error scraping {clinic_url}: {e}")
        return None, None, None

# Send a request to fetch the HTML content of the main page
response = requests.get(main_url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the division by its ID
content_container = soup.find('div', id='content_container_138603_138603')

# Initialize a list to hold hospital names and details
hospital_list = []

# Iterate over each <h2> and corresponding <ul> after it
for h2 in content_container.find_all('h2'):
    # Get the letter (A, B, C, etc.)
    letter = h2.text.strip()

    # Find the next <ul> after each <h2> and get all <li> tags inside
    ul = h2.find_next('ul')
    
    if ul:
        for li in ul.find_all('li'):
            # Extract the clinic/hospital name and the URL from <a> tag
            a_tag = li.find('a')
            clinic_name = a_tag.text.strip()
            clinic_url = a_tag['href'] if a_tag and 'href' in a_tag.attrs else None

            # If a clinic URL exists, visit the link to extract contact details, address, and website
            contact, address, website = None, None, None
            if clinic_url:
                contact, address, website = get_clinic_details(clinic_url)
                time.sleep(1)  # Add delay to avoid overwhelming the server with requests

            # Append the data to the list
            print("Contact : " + contact)
            print("Adress : " + address)
            print("Website : " + website)


            hospital_list.append([letter, clinic_name, clinic_url, contact, address, website])

    print(f"Letter {letter} done !!")

# Create a DataFrame to store the data
df = pd.DataFrame(hospital_list, columns=["Letter", "Clinic/Hospital Name", "Link", "Contact Number", "Address", "Website"])

# Save to a CSV file
df.to_csv("queensland_clinics_detailed.csv", index=False)

print("Data extracted and saved to queensland_clinics_detailed.csv")
