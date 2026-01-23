import requests
from bs4 import BeautifulSoup
import csv

URL = "https://en.wikipedia.org/wiki/List_of_hospitals_in_Nepal"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.0.0 Safari/537.36"
}

response = requests.get(URL, headers=headers)
if response.status_code != 200:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Find all tables and print their classes to debug
tables = soup.find_all("table")
print(f"Found {len(tables)} tables on the page.")
for i, t in enumerate(tables):
    print(f"Table {i}: {t.get('class')}")

# Once you see which table is correct, we target it
table = soup.find("table", class_="wikitable sortable")  # simpler selector

if not table:
    print("Error: Could not find the hospital table.")
    exit()

hospitals = []

for row in table.find_all("tr")[1:]:  # skip header
    cols = row.find_all("td")
    if len(cols) >= 4:
        name = cols[0].get_text(strip=True)
        city = cols[1].get_text(strip=True)
        province = cols[2].get_text(strip=True)
        description = cols[3].get_text(strip=True)
        
        hospitals.append({
            "Hospital": name,
            "City": city,
            "Province": province,
            "Description": description
        })

with open("nepal_hospitals.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Hospital", "City", "Province", "Description"])
    writer.writeheader()
    for hosp in hospitals:
        writer.writerow(hosp)

print(f"Scraped {len(hospitals)} hospitals. Saved to 'nepal_hospitals.csv'.")
