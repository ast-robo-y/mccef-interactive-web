import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


STREAMLIT_URL = os.environ.get(
    "STREAMLIT_APP_URL",
    "https://mccef-interactive-web-site.streamlit.app/"
)

WAKE_BUTTON = (
    By.XPATH,
    "//button[contains(., 'Yes, get this app back up!')]"
)

def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:
        print(f"Opening {STREAMLIT_URL}")
        driver.get(STREAMLIT_URL)

        wait = WebDriverWait(driver, 30)

        try:
            button = wait.until(
                EC.element_to_be_clickable(WAKE_BUTTON)
            )

            print("App is sleeping. Clicking wake-up button...")
            button.click()

            print("Wake-up request sent.")
            print("Waiting 60 seconds for Streamlit to start...")

            time.sleep(60)

            print("Refreshing page to check app status...")
            driver.refresh()

            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script(
                    "return document.readyState"
                ) == "complete"
            )

            time.sleep(5)

            if driver.find_elements(*WAKE_BUTTON):
                print("WARNING: Wake-up button is still visible.")
                print("The app may not have started successfully.")
                print(driver.find_element(By.TAG_NAME, "body").text)

            else:
                print("Wake-up button is no longer present.")
                print("Current page content:")
                print(driver.find_element(By.TAG_NAME, "body").text[:1000])

        except TimeoutException:
            print("No wake-up button detected.")
            print("The app may already be awake.")

    finally:
        driver.quit()
        print("Finished.")


if __name__ == "__main__":
    main()