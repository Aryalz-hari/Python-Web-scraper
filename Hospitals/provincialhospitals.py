import requests
from bs4 import BeautifulSoup
import csv

URL = "https://en.wikipedia.org/wiki/List_of_hospitals_in_Nepal"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.0.0 Safari/537.36"
}

# Fetch the page
response = requests.get(URL, headers=headers)
if response.status_code != 200:
    print(f"Failed to fetch page: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Find all wikitable tables
all_tables = soup.find_all("table", class_="wikitable")

# Identify the provincial hospital table by checking for "Mechi Provincial Hospital"
provincial_table = None
for table in all_tables:
    if table.find("a", string=lambda text: text and "Mechi Provincial Hospital" in text):
        provincial_table = table
        break

if not provincial_table:
    print("Error: Could not find the provincial hospital table.")
    exit()

# Extract provincial hospital data
hospitals = []
for row in provincial_table.find_all("tr")[1:]:  # skip header
    cols = row.find_all("td")
    if len(cols) >= 3:
        name = cols[0].get_text(strip=True)
        city = cols[1].get_text(strip=True)
        province = cols[2].get_text(strip=True)
        description = cols[3].get_text(strip=True) if len(cols) > 3 else ""
        hospitals.append({
            "Hospital": name,
            "City": city,
            "Province": province,
            "Description": description
        })

# Save to CSV
with open("provincial_hospitals.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Hospital", "City", "Province", "Description"])
    writer.writeheader()
    for hosp in hospitals:
        writer.writerow(hosp)

print(f"Scraped {len(hospitals)} provincial hospitals. Saved to 'provincial_hospitals.csv'.")
