from playwright.sync_api import sync_playwright
import csv
import time

BASE_URL = "https://www.tripadvisor.com/Search?q=Spas&geo=293889&offset={}"

OUTPUT_FILE = "tripadvisor_spas.csv"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,   # IMPORTANT: keep false for TripAdvisor
        slow_mo=120
    )

    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )

    page = context.new_page()

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Rating", "Reviews", "Mentions"])

        for offset in range(0, 90, 30):   # 0,30,60 (adjust if needed)
            print(f"\nScraping offset {offset}...")

            page.goto(BASE_URL.format(offset), timeout=60000)
            page.wait_for_selector('[data-test-attribute="location-results-card"]', timeout=60000)

            cards = page.query_selector_all('[data-test-attribute="location-results-card"]')

            print(f"Found {len(cards)} results")

            for card in cards:
                # Name
                name_el = card.query_selector('a[href*="Attraction_Review"]')
                name = name_el.inner_text().strip() if name_el else "N/A"

                # Rating
                rating_el = card.query_selector('[data-automation="bubbleRatingValue"] span')
                rating = rating_el.inner_text().strip() if rating_el else "N/A"

                # Reviews
                reviews_el = card.query_selector('[data-automation="bubbleReviewCount"] span')
                reviews = reviews_el.inner_text().strip() if reviews_el else "N/A"

                # Mentions
                mentions = "N/A"
                for div in card.query_selector_all("div"):
                    text = div.inner_text()
                    if "mentions of" in text:
                        mentions = text.strip()
                        break

                writer.writerow([name, rating, reviews, mentions])

            time.sleep(3)   

    browser.close()

print("\n✅ Data saved to tripadvisor_spas.csv")
