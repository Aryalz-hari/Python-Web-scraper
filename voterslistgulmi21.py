# # # voterslistgulmi.py
# # from selenium import webdriver
# # from selenium.webdriver.support.ui import Select, WebDriverWait
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support import expected_conditions as EC
# # import time
# # import csv

# # # ----------------- INPUTS -----------------
# # province = "लुम्बिनी प्रदेश"
# # district = "गुल्मी"
# # municipality = "धुर्कोट गाउँपालिका"
# # ward = "6"
# # polling_center = "देवीस्थान आधारभुत विद्यालय, किमुखर्क"

# # # ----------------- SETUP -----------------
# # options = webdriver.ChromeOptions()
# # options.add_argument("--start-maximized")
# # driver = webdriver.Chrome(options=options)

# # wait = WebDriverWait(driver, 30)  # wait up to 30 sec for elements

# # # ----------------- OPEN PAGE -----------------
# # driver.get("https://election.gov.np/np/page/voter-list-db")

# # # ----------------- HELPER FUNCTION -----------------
# # def select_option_by_text(select_id, text):
# #     """Wait until the dropdown is populated, then select by visible text"""
# #     select_elem = wait.until(EC.presence_of_element_located((By.ID, select_id)))
# #     select_dropdown = Select(select_elem)

# #     # Wait until options are more than 1 (dropdown fully loaded)
# #     wait.until(lambda d: len(select_dropdown.options) > 1)

# #     select_dropdown.select_by_visible_text(text)
# #     time.sleep(2)  # small sleep to ensure next dropdown loads

# # # ----------------- SELECT FORM OPTIONS -----------------
# # select_option_by_text("province", province)
# # select_option_by_text("district", district)
# # select_option_by_text("municipality", municipality)
# # select_option_by_text("ward", ward)
# # select_option_by_text("polling_center", polling_center)

# # # ----------------- SUBMIT FORM -----------------
# # submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'खोज्नुहोस्')]")))
# # submit_btn.click()

# # # ----------------- SCRAPE DATA -----------------
# # # Wait until the table appears
# # table = wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id='voterListTable']")))

# # rows = table.find_elements(By.TAG_NAME, "tr")

# # # Save data to CSV
# # with open("voter_list.csv", "w", newline="", encoding="utf-8") as f:
# #     writer = csv.writer(f)
# #     for row in rows:
# #         cells = row.find_elements(By.TAG_NAME, "td")
# #         writer.writerow([cell.text for cell in cells])

# # print("Scraping complete! Data saved to voter_list.csv")

# # # ----------------- CLOSE DRIVER -----------------
# # driver.quit()


# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait, Select
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# # ----------------- INPUT -----------------
# province = "लुम्बिनी प्रदेश"
# district = "गुल्मी"
# municipality = "धुर्कोट गाउँपालिका"
# ward = "6"
# polling_center = "देवीस्थान आधारभुत विद्यालय, किमुखर्क"

# # ----------------- SETUP -----------------
# chrome_options = Options()
# chrome_options.add_argument("--start-maximized")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# wait = WebDriverWait(driver, 30)  # wait up to 30 sec for slow loads

# driver.get("https://election.gov.np/np/page/voter-list-db")

# # ----------------- HELPER FUNCTION -----------------
# def select_option(select_id, text):
#     """Select dropdown option by visible text, wait for options to load"""
#     select_elem = wait.until(EC.presence_of_element_located((By.ID, select_id)))
#     select_dropdown = Select(select_elem)
    
#     # Wait until more than 1 option is loaded (site is slow)
#     wait.until(lambda d: len(select_dropdown.options) > 1)
    
#     select_dropdown.select_by_visible_text(text)
#     time.sleep(2)  # small wait for next dropdown to populate

# # ----------------- SELECT DROPDOWNS -----------------
# select_option("state", province)
# select_option("district", district)
# select_option("vdc_mun", municipality)
# select_option("ward", ward)
# select_option("reg_centre", polling_center)

# # ----------------- CLICK SUBMIT -----------------
# submit_button = wait.until(EC.element_to_be_clickable((By.ID, "btnSubmit")))
# submit_button.click()

# # ----------------- SCRAP DATA -----------------
# # Wait until the results table appears
# table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

# rows = table.find_elements(By.TAG_NAME, "tr")
# voters_data = []

# for row in rows[1:]:  # skip header
#     cols = row.find_elements(By.TAG_NAME, "td")
#     voter = [col.text.strip() for col in cols]
#     voters_data.append(voter)

# # ----------------- PRINT DATA -----------------
# for v in voters_data:
#     print(v)

# # ----------------- CLOSE DRIVER -----------------
# driver.quit()

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# -------------------- CONFIG --------------------
province = "लुम्बिनी प्रदेश"
district = "गुल्मी"
municipality = "धुर्कोट गाउँपालिका"
ward = "6"
polling_center = "देवीस्थान आधारभुत विद्यालय, किमुखर्क"

URL = "https://election.gov.np/np/page/voter-list-db"

# -------------------- DRIVER SETUP --------------------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 60)  # long wait for slow JS

driver.get(URL)

# -------------------- HELPER FUNCTIONS --------------------
def wait_for_dropdown(select_id, timeout=60):
    """Wait until a dropdown has more than 1 option (ignores the default)."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        select_elem = Select(driver.find_element(By.ID, select_id))
        if len(select_elem.options) > 1:
            return select_elem
        time.sleep(1)
    raise Exception(f"Dropdown {select_id} did not populate in time.")

def select_option(select_id, visible_text):
    select_elem = wait_for_dropdown(select_id)
    select_elem.select_by_visible_text(visible_text)
    # wait a few seconds for JS to populate next dropdown
    time.sleep(2)

# -------------------- SELECT DROPDOWNS --------------------
print("Selecting dropdowns...")
select_option("state", province)
select_option("district", district)
select_option("vdc_mun", municipality)
select_option("ward", ward)
select_option("reg_centre", polling_center)

# -------------------- SUBMIT FORM --------------------
submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "btnSubmit")))
submit_btn.click()
print("Form submitted, waiting for voter table...")

# -------------------- SCRAPE TABLE --------------------
def scrape_table():
    """Scrape voter table rows and return as list of dicts."""
    voters = []

    while True:
        # wait for table
        wait.until(EC.presence_of_element_located((By.ID, "tbl_data")))

        rows = driver.find_elements(By.CSS_SELECTOR, "#tbl_data tbody tr")
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            voter = {
                "serial": cols[0].text,
                "voter_no": cols[1].text,
                "name": cols[2].text,
                "age": cols[3].text,
                "gender": cols[4].text,
                "spouse": cols[5].text,
                "parents": cols[6].text,
            }
            # optionally click the "मतदाता विवरण" button
            details_btn = cols[7].find_element(By.TAG_NAME, "button")
            # details_btn.click()
            # time.sleep(1)  # wait for modal or page to load if needed
            voters.append(voter)

        # check if "Next" button is enabled
        next_btn = driver.find_element(By.ID, "tbl_data_next")
        if "paginate_enabled" in next_btn.get_attribute("class"):
            next_btn.click()
            time.sleep(2)  # wait for table to refresh
        else:
            break

    return voters

voter_data = scrape_table()
print(f"Scraped {len(voter_data)} voters.")
for v in voter_data[:10]:  # print first 10 for example
    print(v)

driver.quit()
