import datetime
from playwright.sync_api import sync_playwright, TimeoutError
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys
import time

# ===================== DATA MODELS =====================
@dataclass
class Business:
    name: str = ""
    address: str = ""
    phone_number: str = ""
    reviews_average: float | None = None

    def __hash__(self):
        return hash((self.name, self.phone_number))

@dataclass
class BusinessList:
    business_list: list[Business] = field(default_factory=list)
    _seen: set = field(default_factory=set, init=False)

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    save_at = os.path.join("GMaps Data", today)
    os.makedirs(save_at, exist_ok=True)

    def add(self, business: Business):
        if hash(business) not in self._seen:
            self.business_list.append(business)
            self._seen.add(hash(business))

    def dataframe(self):
        return pd.json_normalize(asdict(b) for b in self.business_list)

    def save_csv(self, name):
        self.dataframe().to_csv(f"{self.save_at}/{name}.csv", index=False)

# ===================== MAIN =====================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int, default=100)  # default 100 listings
    args = parser.parse_args()

    if args.search:
        search_list = [args.search.strip()]
    else:
        if not os.path.exists("input.txt"):
            print("❌ Provide -s or input.txt")
            sys.exit()
        with open("input.txt") as f:
            search_list = [x.strip() for x in f if x.strip()]

    with sync_playwright() as p:
        # Use persistent context for stable scraping
        browser = p.chromium.launch_persistent_context(
            user_data_dir="./user_data",  # folder created to store profile
            headless=False,
            slow_mo=150,
            locale="en-GB"
        )
        page = browser.new_page()

        # Open Google Maps
        page.goto("https://www.google.com/maps")
        time.sleep(8)
        page.mouse.click(300, 300)  # Activate UI
        time.sleep(2)

        # Accept cookies if visible
        try:
            page.get_by_role("button", name="Accept all").click(timeout=5000)
        except:
            pass

        for search in search_list:
            print("\n🔍 Searching:", search)

            # ===== RETRY-SAFE SEARCH BOX =====
            search_box = None
            max_attempts = 5
            for attempt in range(max_attempts):
                try:
                    search_box = page.get_by_placeholder("Search Google Maps")
                    search_box.wait_for(timeout=30000)
                    search_box.click(force=True)
                    search_box.fill(search)
                    search_box.press("Enter")
                    print("✅ Search box filled successfully")
                    break
                except TimeoutError:
                    print(f"⚠️ Attempt {attempt+1}/{max_attempts} failed. Retrying in 5s...")
                    time.sleep(5)
                except Exception as e:
                    print("❌ Unexpected error:", e)
                    time.sleep(5)

            if search_box is None:
                print("❌ Could not find search box. Skipping search:", search)
                continue

            page.wait_for_timeout(5000)

            # ===== SCROLL RESULTS =====
            results_selector = 'a[href*="/maps/place"]'
            previously_counted = 0
            while True:
                cards = page.locator(results_selector)
                count = cards.count()
                if count >= args.total or count == previously_counted:
                    break
                previously_counted = count
                if count > 0:
                    cards.nth(count - 1).hover()
                page.mouse.wheel(0, 8000)
                page.wait_for_timeout(2000)

            listings = page.locator(results_selector).all()[:args.total]
            print(f"✅ Found {len(listings)} listings")

            business_list = BusinessList()

            for listing in listings:
                try:
                    listing.click()
                    page.wait_for_timeout(3000)

                    business = Business()

                    # Name
                    business.name = page.locator("h1.DUwDvf").inner_text(timeout=5000)

                    # Helper for optional fields
                    def safe_text(selector):
                        loc = page.locator(selector)
                        return loc.inner_text(timeout=2000) if loc.count() else ""

                    business.address = safe_text('button[data-item-id="address"]')
                    business.phone_number = safe_text('button[data-item-id^="phone"]')


                    # Average reviews
                    try:
                        rating = page.locator('span[role="img"]').get_attribute("aria-label")
                        business.reviews_average = float(rating.split()[0])
                    except:
                        business.reviews_average = None

                    business_list.add(business)

                except TimeoutError:
                    continue
                except Exception as e:
                    print("⚠️ Error:", e)

            filename = search.replace(" ", "_")
            business_list.save_csv(filename)
            print(f"💾 Saved: {filename}")

        browser.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("❌ Failed:", e)
