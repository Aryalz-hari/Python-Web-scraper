from playwright.sync_api import sync_playwright
from csv import writer
import time

BASE_URL = "https://edusanjal.com"
START_PAGE = 1
END_PAGE = 1624 # change to 1624 later

with open("schools.csv", "a", encoding="utf-8", newline="") as f:
    csv_writer = writer(f)
    csv_writer.writerow([
        "SchoolName",
        "Link",
        "Accreditation",
        "Level",
        "Address"
    ])

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for page_no in range(START_PAGE, END_PAGE + 1):
            url = f"{BASE_URL}/school?page={page_no}"
            print(f"Loading page {page_no}")

            page.goto(url, timeout=60000)
            page.wait_for_selector(
                "div.overflow-hidden.bg-white.rounded-sm.shadow-xl",
                timeout=60000
            )

            cards = page.query_selector_all(
                "div.overflow-hidden.bg-white.rounded-sm.shadow-xl"
            )

            print(f"  Found {len(cards)} schools")

            for card in cards:
                # ------------------------
                # School Name
                # ------------------------
                SchoolName = card.query_selector(
                    "a.text-xl span"
                ).inner_text().strip()

                # ------------------------
                # School Link
                # ------------------------
                link = BASE_URL + card.query_selector(
                    "a.text-xl"
                ).get_attribute("href")

                # ------------------------
                # Accreditation
                # ------------------------
                acc_el = card.query_selector(
                    "li[title='Accreditation'] a"
                )
                Accreditation = acc_el.inner_text().strip() if acc_el else "N/A"

                # ------------------------
                # Level
                # ------------------------
                level_el = card.query_selector(
                    "li[title='Level'] span.ml-2"
                )
                Level = level_el.inner_text().strip() if level_el else "N/A"

                # ------------------------
                # Address
                # ------------------------
                address_el = card.query_selector(
                    "li[title='Address']"
                )
                Address = address_el.inner_text().strip() if address_el else "N/A"

                csv_writer.writerow([
                    SchoolName,
                    link,
                    Accreditation,
                    Level,
                    Address
                ])

            print(f"✅ Page {page_no} scraped")
            time.sleep(1)  # polite delay

        browser.close()

print("🎉 Scraping completed successfully!")
