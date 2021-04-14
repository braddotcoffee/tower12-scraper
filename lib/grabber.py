from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

TOWER12_URL = "https://tower12.com/floor-plans/"
CHROMIUM_DRIVER_PATH = "/usr/lib/chromium-browser/chromedriver"


def grab_floorplans() -> str:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("start-maximized")
    # open Browser in maximized mode
    options.add_argument("disable-infobars")
    # disabling infobars
    options.add_argument("--disable-extensions")
    # disabling extensions
    options.add_argument("--disable-gpu")
    # applicable to windows os only
    options.add_argument("--disable-dev-shm-usage")
    # overcome limited resource problems
    options.add_argument("--no-sandbox")
    # Bypass OS security model
    # wait for the element to load for 10 seconds
    browser = webdriver.Chrome(CHROMIUM_DRIVER_PATH, chrome_options=options)
    browser.get(TOWER12_URL)

    try:
        # get the unit items to ensure that page is fully loaded
        WebDriverWait(browser, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, "unit-item")
            )
        )
        return browser.page_source
    finally:
        # after 10 seconds, maybe give up?
        browser.quit()
