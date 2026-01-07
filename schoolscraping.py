import requests
from bs4 import BeautifulSoup
from csv import writer
import os
import time

BASE_URL = "https://edusanjal.com/api/v1/schools"
START_PAGE = 1
END_PAGE = 2

csv_file = "schools.csv"
file_exists = os.path.isfile(csv_file)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

with open(csv_file, "a", encoding="utf-8", newline="") as f:
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
            response = requests.get(url, headers=headers, timeout=15)
            print(response.status_code)
            response.encoding = "utf-8"

            if response.status_code != 200:
                print(f"Page {page} skipped (status {response.status_code})")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            cards = soup.find_all(
                "div",
                class_="overflow-hidden bg-white rounded-sm shadow-xl"
            )

            if not cards:
                print(f"No data found on page {page}")
                continue

            for card in cards:

                # School link
                link_tag = card.find("a", href=True)
                link = BASE_URL + link_tag["href"] if link_tag else "N/A"

                # School name
                name_tag = card.find("a", class_="text-xl")
                SchoolName = name_tag.get_text(strip=True) if name_tag else "N/A"

                # Accreditation
                acc_li = card.find("li", title="Accreditation")
                Accreditation = acc_li.get_text(strip=True) if acc_li else "N/A"

                # Level
                level_li = card.find("li", title="Level")
                Level = (
                    level_li.find("span", class_="ml-2").get_text(strip=True)
                    if level_li else "N/A"
                )

                # Address
                address_li = card.find("li", title="Address")
                Address = address_li.get_text(strip=True) if address_li else "N/A"

                csv_writer.writerow([
                    SchoolName,
                    link,
                    Accreditation,
                    Level,
                    Address
                ])

            print(f"Page {page} scraped")

            # Polite delay
            time.sleep(1.2)

        except requests.exceptions.RequestException as e:
            print(f" Error on page {page}: {e}")
            time.sleep(5)

print(" Scraping completed successfully!")
