import requests
from bs4 import BeautifulSoup
import csv
import os
import streamlit as st
# Function to check if scraping is allowed on a website
def is_scraping_allowed(url):
    try:
        # Checking robots.txt for the URL
        robots_url = url.rstrip("/") + "/robots.txt"
        response = requests.get(robots_url)

        if response.status_code == 200:
            if "Disallow: /" in response.text:
                return False
            return True
        else:
            return True
    except Exception as e:
        return True

# Function to scrape the website and extract content
def scrape_website(url):
    if not is_scraping_allowed(url):
        st.error("Scraping is disallowed on this site.")
        return

    try:
        # Send GET request to the webpage
        response = requests.get(url)
        
        if response.status_code != 200:
            st.error(f"Failed to retrieve webpage. Status code: {response.status_code}")
            return

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting headings
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        headings_text = [heading.get_text(strip=True) for heading in headings]

        # Extracting paragraphs
        paragraphs = soup.find_all('p')
        paragraphs_text = [para.get_text(strip=True) for para in paragraphs]

        # Extracting links
        links = soup.find_all('a', href=True)
        links_list = [link['href'] for link in links]

        # Extracting image URLs
        images = soup.find_all('img', src=True)
        images_list = [image['src'] for image in images]

        # Save the data to a CSV file
        save_to_csv(headings_text, paragraphs_text, links_list, images_list)

        return headings_text, paragraphs_text, links_list, images_list

    except Exception as e:
        st.error(f"Error during scraping: {e}")
        return

# Function to save the data into a CSV file
def save_to_csv(headings, paragraphs, links, images):
    filename = 'scraped_data.csv'

    # Check if file exists, if so, append data
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write the header row if it's a new file
            writer.writerow(['Heading', 'Paragraph', 'Link', 'Image URL'])

        # Write the data to the CSV file
        for heading, paragraph, link, image in zip(headings, paragraphs, links, images):
            writer.writerow([heading, paragraph, link, image])
# Streamlit UI setup
st.title("Web Scraper with Streamlit")
# Input for URL
url = st.text_input("Enter the URL to scrape:")

if url:
    # Scrape the website and get the results
    headings, paragraphs, links, images = scrape_website(url)
    if headings:
        st.subheader("Headings")
        st.write(headings)
    if paragraphs:
        st.subheader("Paragraphs")
        st.write(paragraphs)
    if links:
        st.subheader("Links")
        st.write(links)
    if images:
        st.subheader("Image URLs")
        st.write(images)
    st.write(f"Data saved to 'scraped_data.csv'")

