# Queensland Clinic Scraper (FAST API)

## Objectives

The primary objective of this project is to compile a comprehensive list of General Practice Clinics/Medical Centres located in Queensland, Australia. The project involves using programmatic methods to scrape data from reliable sources, extract clinic details, and present them in an organized Excel format. The collected data includes:

> Clinic Name
> Address
> Contact Number
> Website (if available)
> The result is a downloadable CSV file that contains accurate and non-duplicated information for each clinic.

## Technologies Used: 

- Python: Core programming language used for web scraping and data handling.

- FastAPI: Lightweight, high-performance web framework used to expose the scraping process via API endpoints.

- BeautifulSoup: A Python library used to extract data from HTML and XML files.

- Pandas: Data analysis library used to structure the scraped data and save it as a CSV file.

- Streamlit: Web interface framework used to provide a front-end for users to trigger the scraping process and download the result.

- Requests: A Python library used to send HTTP requests for fetching HTML content.

- Regular Expressions: Utilized to ensure the correct format of phone numbers.

## Technical Architecture

## - FastAPI Service:

The FastAPI server is responsible for running the web scraper. It exposes an endpoint (/save_to_csv) that triggers the scraping process, compiles clinic details, and saves them into a CSV file.

Data is scraped from a reliable government website, specifically from the Queensland Health Services page, by crawling through clinic details.

The scraped data is processed and validated before being saved into a CSV file.
The CSV file is then served as a downloadable file for users.

## - Streamlit Web Interface:

A Streamlit front-end interface allows users to trigger the scraping process with a button labeled Extract Data and Download CSV.
Upon clicking the button, a request is made to the FastAPI endpoint. Once the process is complete, the CSV file is made available for download.
The user interface provides feedback during the scraping process and shows a success message once the file is ready.

## How to Run the Project

### Set up FastAPI Server:

Ensure you have Python installed, and install the required dependencies:


Copy code
pip install fastapi uvicorn requests beautifulsoup4 pandas

Run the FastAPI server using uvicorn:

Copy code
uvicorn main:app --reload --port 8080

This will start the FastAPI server on http://127.0.0.1:8080.

### Set up Streamlit Server:

### - Install Streamlit:

pip install streamlit

### - Run the Streamlit app:

Copy code

streamlit run streamlit_app.py

Access the app in your browser at http://localhost:8501.


## Conclusion

This project efficiently demonstrates the ability to collect structured data from public online sources using web scraping techniques and organize it into a downloadable format. By combining FastAPI for backend scraping and Streamlit for a simple user interface, the solution provides an end-to-end pipeline for automating the data collection process. This approach could be extended to other regions or data sources, offering flexibility for future use cases.