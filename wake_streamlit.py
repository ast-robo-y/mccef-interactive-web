import os

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


def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:
        print(f"Opening Streamlit app: {STREAMLIT_URL}")
        driver.get(STREAMLIT_URL)

        wait = WebDriverWait(driver, 30)

        try:
            button = wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(., 'Yes, get this app back up!')]"
                    )
                )
            )

            print("Wake-up button found. Clicking...")
            button.click()

            wait.until(
                EC.invisibility_of_element_located(
                    (
                        By.XPATH,
                        "//button[contains(., 'Yes, get this app back up')]"
                    )
                )
            )

            print("Wake-up button disappeared.")

        except TimeoutException:
            print(
                "No wake-up button detected, "
                "or it did not disappear in time."
            )

    finally:
        driver.quit()
        print("Finished.")


if __name__ == "__main__":
    main()