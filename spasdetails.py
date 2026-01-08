from playwright.sync_api import sync_playwright
import csv
import time
import random

URL = "https://www.tripadvisor.com/Search?q=Spas&geo=293889&offset=0"
OUTPUT_FILE = "tripadvisor_spas_name_location.csv"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,   # MUST be false for TripAdvisor
        slow_mo=150
    )

    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )

    page = context.new_page()
    page.goto(URL, timeout=60000)

    # Human-like wait + scroll
    time.sleep(5)
    page.mouse.wheel(0, 800)
    time.sleep(5)

    # Wait for cards
    page.wait_for_selector('[data-test-attribute="location-results-card"]', timeout=60000)

    cards = page.query_selector_all('[data-test-attribute="location-results-card"]')
    print(f"Found {len(cards)} spas on first page")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Location"])

        for card in cards:
            # Spa Name
            name_el = card.query_selector('a[href*="Attraction_Review"]')
            name = name_el.inner_text().strip() if name_el else "N/A"

            # Location (e.g. Kathmandu, Nepal)
            location_el = card.query_selector('div.biGQs._P.VImYz.xARtZ.ZNjnF')
            location = location_el.inner_text().strip() if location_el else "N/A"

            writer.writerow([name, location])
            print(f"Saved: {name} | {location}")

            # Small random delay per item
            time.sleep(random.uniform(0.8, 1.5))

    time.sleep(5)
    browser.close()

print("\n First-page spa names & locations saved to tripadvisor_spas_name_location.csv")
