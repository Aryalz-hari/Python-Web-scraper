from playwright.sync_api import sync_playwright
from csv import writer
import time
import os

BASE_URL = "https://edusanjal.com"
START_PAGE = 1
END_PAGE = 2  # for testing

CSV_FILE = "schools_full_details.csv"
file_exists = os.path.isfile(CSV_FILE)

with open(CSV_FILE, "a", encoding="utf-8", newline="") as f:
    csv_writer = writer(f)

    if not file_exists:
        csv_writer.writerow([
            "SchoolName",
            "Link",
            "Accreditation",
            "Level",
            "Address",
            "Phone",
            "Email"
        ])

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        listing_page = browser.new_page()
        detail_page = browser.new_page()  # separate page for detail

        for page_no in range(START_PAGE, END_PAGE + 1):
            list_url = f"{BASE_URL}/school?page={page_no}"
            print(f"📄 Loading listing page {page_no}...")

            try:
                listing_page.goto(list_url, timeout=60000)
                listing_page.wait_for_selector(
                    "div.overflow-hidden.bg-white.rounded-sm.shadow-xl", timeout=60000
                )
            except Exception as e:
                print(f"⚠ Could not load listing page {page_no}: {e}")
                continue

            cards = listing_page.query_selector_all(
                "div.overflow-hidden.bg-white.rounded-sm.shadow-xl"
            )
            print(f"  Found {len(cards)} schools on page {page_no}")

            for card in cards:
                # ------------------------
                # School Name
                # ------------------------
                try:
                    SchoolName = card.query_selector(
                        "a.text-xl span.grow"
                    ).inner_text().strip()
                except:
                    SchoolName = "N/A"


                try:
                    link_path = card.query_selector("a.text-xl").get_attribute("href")
                    link = BASE_URL + link_path
                except:
                    link = "N/A"

                
                try:
                    acc_el = card.query_selector("li[title='Accreditation'] a")
                    Accreditation = acc_el.inner_text().strip() if acc_el else "N/A"
                except:
                    Accreditation = "N/A"

                
                try:
                    level_el = card.query_selector("li[title='Level'] span.ml-2")
                    Level = level_el.inner_text().strip() if level_el else "N/A"
                except:
                    Level = "N/A"

                
                try:
                    address_el = card.query_selector("li[title='Address'] span.ml-2")
                    Address = address_el.inner_text().strip() if address_el else "N/A"
                except:
                    Address = "N/A"

                
                Phone, Email = "N/A", "N/A"
                if link != "N/A":
                    try:
                        detail_page.goto(link, timeout=60000)
                        detail_page.wait_for_selector(
                            "ul.flex.flex-col.bg-gray-100", timeout=60000
                        )

                        phone_el = detail_page.query_selector("li[title='Phone'] span:nth-child(2)")
                        Phone = phone_el.inner_text().strip() if phone_el else "N/A"

                        email_el = detail_page.query_selector("li[title='Email'] span:nth-child(2)")
                        Email = email_el.inner_text().strip() if email_el else "N/A"

                    except Exception as e:
                        print(f"   ⚠ Could not load detail page: {link}")

                csv_writer.writerow([
                    SchoolName,
                    link,
                    Accreditation,
                    Level,
                    Address,
                    Phone,
                    Email
                ])
                print(f"  ✅ {SchoolName} scraped")

                time.sleep(0.8)  # polite delay per school

            print(f"✅ Page {page_no} completed\n")
            time.sleep(1.5)  # polite delay per listing page

        browser.close()

print("🎉 Scraping completed successfully!")
