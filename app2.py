import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# URL of the main page to scrape
main_url = "https://www.health.qld.gov.au/services"

# Regular expression pattern for valid Australian phone numbers
phone_pattern = re.compile(r'(?:\+?61\s?|0)?([2378]\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{0,4}|\d{3}[-.\s]?\d{3}[-.\s]?\d{4})')

# Function to extract clinic details from the individual clinic page
def get_clinic_details(clinic_url):
    try:
        response = requests.get(clinic_url)
        clinic_soup = BeautifulSoup(response.content, "html.parser")
        
        contact_numbers = []
        address = None
        
        # Extract all contact info (look for <a> tag with href containing 'tel:')
        contact_sections = clinic_soup.find_all('a', href=lambda href: href and href.startswith('tel:'))
        for contact_section in contact_sections:
            # phone_text = contact_section.text.strip()
            phone_number = contact_section['href'].replace('tel:', '').replace('&nbsp;', '').replace(' ', '').strip()
            
            # Check if the number matches a valid phone format
            # match = phone_pattern.search(phone_number)

            if phone_number.isdigit() and len(phone_number) == 10:
        
                contact_numbers.append(phone_number)
        
            # Print for debugging
            # print(contact_numbers)
            # if match:
            #     contact_numbers.append(phone_number)
            #     print(contact_numbers)

        address_sections = clinic_soup.find_all('div', class_='qld__contact-details__col')
        
        # Loop through the sections to find valid addresses and skip "Office hours" content
        for section in address_sections:
            address_tag = section.find('p')
            if address_tag and 'office hours' not in address_tag.text.lower():
                # Extract the address lines separated by <br> tags
                address_lines = list(address_tag.stripped_strings)
                
                # Check if the extracted lines contain an address-like structure
                if any(keyword in address_lines[0].lower() for keyword in ['st', 'street', 'blvd', 'hwy', 'road', 'rd']):
                    address = ", ".join(address_lines)
                    break

        contact = ", ".join(contact_numbers) if contact_numbers else None
        print(address)

        return contact, address

    except Exception as e:
        print(f"Error scraping {clinic_url}: {e}")
        return None, None

# Send a request to fetch the HTML content of the main page
response = requests.get(main_url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the division by its ID (may need to adjust this based on the actual HTML structure)
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

            # If a clinic URL exists, visit the link to extract contact details and address
            contact, address = None, None
            if clinic_url:
                contact, address = get_clinic_details(clinic_url)
                time.sleep(1)  # Add delay to avoid overwhelming the server with requests

            # Append the data to the list
            hospital_list.append([letter, clinic_name, clinic_url, contact, address])

    print(f"Letter {letter} done !!")

# Create a DataFrame to store the data
df = pd.DataFrame(hospital_list, columns=["Letter", "Clinic/Hospital Name", "Link", "Contact Number", "Address"])

# Save to a CSV file
df.to_csv("queensland_clinics_detailed.csv", index=False)

print("Data extracted and saved to queensland_clinics_detailed.csv")
