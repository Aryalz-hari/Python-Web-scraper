import requests
from bs4 import BeautifulSoup
import csv
import time

# Base URL of the listings
BASE_URL = "https://www.nepalphonebook.com/listing-category/dental-clinics/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

# CSV file to save results
CSV_FILE = "dental_clinics.csv"

def get_clinic_details(clinic_url):
    """Scrape individual clinic page for phone and website."""
    try:
        res = requests.get(clinic_url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        
        phone_tag = soup.find("li", class_="lp-listing-phone")
        phone = phone_tag.get_text(strip=True) if phone_tag else ""
        
        website_tag = soup.find("li", class_="lp-user-web")
        website = website_tag.find("a")["href"] if website_tag else ""
        
        return phone, website
    except Exception as e:
        print(f"Error fetching {clinic_url}: {e}")
        return "", ""

def scrape_listings():
    """Loop through listing pages and get all clinics."""
    page = 1
    all_data = []

    while True:
        url = f"{BASE_URL}?page={page}"
        print(f"Scraping page {page}...")
        res = requests.get(url, headers=HEADERS)
        if res.status_code != 200:
            print("No more pages or failed to load page.")
            break

        soup = BeautifulSoup(res.text, "html.parser")
        listings = soup.find_all("div", class_="list_own_col_gt")
        if not listings:
            print("No listings found on this page.")
            break

        for listing in listings:
            name_tag = listing.find("p", class_="lp_list_title").find("a")
            name = name_tag.text.strip()
            detail_link = name_tag["href"]

            location_tag = listing.find("p", class_="lp_list_address")
            location = location_tag.text.strip() if location_tag else ""

            # Get phone and website from detail page
            phone, website = get_clinic_details(detail_link)

            all_data.append({
                "Name": name,
                "Location": location,
                "Detail Link": detail_link,
                "Phone": phone,
                "Website": website
            })

            # Be polite to server
            time.sleep(0.5)

        page += 1
        # Optional: limit pages for testing
        if page > 3:
            break

    # Save to CSV
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Location", "Detail Link", "Phone", "Website"])
        writer.writeheader()
        writer.writerows(all_data)

    print(f"Scraping completed! Data saved to {CSV_FILE}")

if __name__ == "__main__":
    scrape_listings()
