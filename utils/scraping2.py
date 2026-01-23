import requests
from bs4 import BeautifulSoup
from csv import writer
import os
import re

# Function to detect Nepali characters
def is_nepali(text):
    return bool(re.search(r'[\u0900-\u097F]', text))

# CSV setup
csv_file = 'data5.csv'
file_exists = os.path.isfile(csv_file)

with open(csv_file, 'a', encoding='utf-8', newline='') as f:
    csv_writer = writer(f)
    
    # Write header if file doesn't exist
    if not file_exists:
        csv_writer.writerow(['CompanyName', 'Address', 'AddressLang', 'Phone', 'Email', 'Link'])
    
    # Loop through pages (change range if site has more/less pages)
    for i in range(1, 59):
        url = f"https://www.sahakariakhabar.com/cooperative-directory?page={i}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'  # Important for Nepali text
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Select all posts on page
        posts = soup.find_all('div', class_='col-lg-9 col-md-8')
        
        for post in posts:
            post_content = post.find('div', class_='post-content')
            if not post_content:
                continue
            
            # Company Name and link
            title_tag = post_content.find('h2').find('a')
            CompanyName = title_tag.get_text(strip=True) if title_tag else "N/A"
            link = title_tag['href'] if title_tag else "N/A"
            
            # Extract paragraph info
            info_lines = post_content.find('p').get_text("\n", strip=True).split("\n") if post_content.find('p') else []
            
            Address = Phone = Email = "N/A"
            
            for line in info_lines:
                line = line.strip()
                if "Address" in line or "ठेगाना" in line:
                    Address = re.sub(r"(Address|ठेगाना)\s*:\s*", "", line).strip()
                elif "Phone" in line or "फोन" in line:
                    Phone = re.sub(r"(Phone|फोन)\s*:\s*", "", line).strip()
                elif "Email" in line or "इमेल" in line:
                    Email = re.sub(r"(Email|इमेल)\s*:\s*", "", line).strip()
            
            # Detect address language
            AddressLang = "Nepali" if is_nepali(Address) else "English"
            
            # Write row to CSV
            csv_writer.writerow([CompanyName, Address, AddressLang, Phone, Email, link])
        
        print(f"Page {i} scraped successfully ✅")

print("Scraping complete! All data saved to data4.csv ✅")
