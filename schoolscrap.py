import requests
from bs4 import BeautifulSoup
from csv import writer
import os
import time

BASE_URL = "https://edusanjal.com"
START_PAGE = 1
END_PAGE = 5

CSV_FILE = "schools.csv"
file_exists = os.path.isfile(CSV_FILE)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

with open(CSV_FILE, "a", encoding="utf-8", newline="") as f:
    csv_writer = writer(f)

    if not file_exists:
        csv_writer.writerow([
            "SchoolName",
            "Link",
            "Accreditation",
            "Level",
            "Address"
        ])

    for page in range(START_PAGE, END_PAGE + 1):
        url = f"{BASE_URL}/school?page={page}"

        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.encoding = "utf-8"

            print(f"Page {page} → Status {response.status_code}")

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            cards = soup.select("div.overflow-hidden.bg-white.rounded-sm.shadow-xl")

            if not cards:
                print(f"No cards found on page {page}")
                continue

            for card in cards:

                # Link (skip image anchor automatically)
                link_tag = card.select_one("a[href^='/school/']")
                link = BASE_URL + link_tag["href"] if link_tag else "N/A"

                # ✅ School Name (FINAL FIX)
                name_tag = card.select_one("a.text-xl span")
                SchoolName = name_tag.get_text(strip=True) if name_tag else "N/A"

                # Accreditation
                acc_li = card.find("li", title="Accreditation")
                Accreditation = (
                    acc_li.find("a").get_text(strip=True)
                    if acc_li and acc_li.find("a")
                    else "N/A"
                )

                # Level
                level_li = card.find("li", title="Level")
                Level = (
                    level_li.find("span", class_="ml-2").get_text(strip=True)
                    if level_li else "N/A"
                )

                # Address
                address_li = card.find("li", title="Address")
                Address = (
                    address_li.get_text(strip=True)
                    if address_li else "N/A"
                )

                csv_writer.writerow([
                    SchoolName,
                    link,
                    Accreditation,
                    Level,
                    Address
                ])

            print(f"Page {page} scraped successfully")
            time.sleep(1.2)

        except requests.exceptions.RequestException as e:
            print(f"Error on page {page}: {e}")
            time.sleep(5)

print("Scraping completed successfully!")
