import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from fastapi import FastAPI, Response
from typing import List
from fastapi.responses import FileResponse

# Initialize FastAPI app
app = FastAPI()

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
        
        contact_sections = clinic_soup.find_all('a', href=lambda href: href and href.startswith('tel:'))
        for contact_section in contact_sections:
            phone_number = contact_section['href'].replace('tel:', '').replace('&nbsp;', '').replace(' ', '').strip()
            if phone_number.isdigit() and len(phone_number) == 10:
                contact_numbers.append(phone_number)

        address_sections = clinic_soup.find_all('div', class_='qld__contact-details__col')
        for section in address_sections:
            address_tag = section.find('p')
            if address_tag and 'office hours' not in address_tag.text.lower():
                address_lines = list(address_tag.stripped_strings)
                if any(keyword in address_lines[0].lower() for keyword in ['st', 'street', 'blvd', 'hwy', 'road', 'rd']):
                    address = ", ".join(address_lines)
                    break

        contact = ", ".join(contact_numbers) if contact_numbers else None
        print(address)
        return contact, address

    except Exception as e:
        print(f"Error scraping {clinic_url}: {e}")
        return None, None

# Define FastAPI route to trigger scraping and save to CSV
@app.get("/save_to_csv", response_class=FileResponse)
def save_to_csv():
    try:
        response = requests.get(main_url)
        soup = BeautifulSoup(response.content, "html.parser")
        content_container = soup.find('div', id='content_container_138603_138603')

        hospital_list = []

        for h2 in content_container.find_all('h2'):
            letter = h2.text.strip()
            ul = h2.find_next('ul')
            
            if ul:
                for li in ul.find_all('li'):
                    a_tag = li.find('a')
                    clinic_name = a_tag.text.strip()
                    clinic_url = a_tag['href'] if a_tag and 'href' in a_tag.attrs else None

                    contact, address = None, None
                    if clinic_url:
                        contact, address = get_clinic_details(clinic_url)
                        time.sleep(1)  # Delay to avoid overwhelming the server

                    hospital_list.append({
                        "Letter": letter,
                        "Clinic/Hospital Name": clinic_name,
                        "Link": clinic_url,
                        "Contact Number": contact,
                        "Address": address
                    })
            print(f"Letter {letter} done!! ")

        # Save data to CSV
        df = pd.DataFrame(hospital_list)
        file_path = "queensland_clinics_detailed.csv"
        df.to_csv(file_path, index=False)

        # Return the CSV file as a response for download
        return FileResponse(file_path, media_type='text/csv', filename="queensland_clinics_detailed.csv")
    
    except Exception as e:
        return {"error": str(e)}
