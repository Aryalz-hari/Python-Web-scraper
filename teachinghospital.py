import requests
from bs4 import BeautifulSoup
import csv

URL = "https://en.wikipedia.org/wiki/List_of_hospitals_in_Nepal"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.0.0 Safari/537.36"
}

# Fetch page
response = requests.get(URL, headers=headers)
if response.status_code != 200:
    print(f"Failed to fetch page: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Find all wikitable tables
all_tables = soup.find_all("table", class_="wikitable")

# Identify the teaching hospitals table by checking for "TU Teaching Hospital"
teaching_table = None
for table in all_tables:
    if table.find("a", string=lambda text: text and "TU Teaching Hospital" in text):
        teaching_table = table
        break

if not teaching_table:
    print("Error: Could not find the teaching hospital table.")
    exit()

# Extract teaching hospital data
hospitals = []
for row in teaching_table.find_all("tr")[1:]:  # skip header
    cols = row.find_all("td")
    if len(cols) >= 3:
        name = cols[0].get_text(strip=True)
        city = cols[1].get_text(strip=True)
        province = cols[2].get_text(strip=True)
        description = cols[3].get_text(strip=True) if len(cols) > 3 else ""
        # Get the Wikipedia link if available
        link_tag = cols[0].find("a")
        url = f"https://en.wikipedia.org{link_tag['href']}" if link_tag else ""
        hospitals.append({
            "Hospital": name,
            "Wikipedia URL": url,
            "City": city,
            "Province": province,
            "Description": description
        })

# Save to CSV
with open("teaching_hospitals.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Hospital", "Wikipedia URL", "City", "Province", "Description"])
    writer.writeheader()
    for hosp in hospitals:
        writer.writerow(hosp)

print(f"Scraped {len(hospitals)} teaching hospitals. Saved to 'teaching_hospitals.csv'.")
