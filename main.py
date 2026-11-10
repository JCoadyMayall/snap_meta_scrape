from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class Scraper:
    def __init__(self):
        self.driver = Driver(uc=True) # Starts Chrome browser in Undetected-Chromedriver (UC) mode


    def open_browser(self):
        """
        Opens Chrome browser using Driver.
        """
        self.driver.get("https://www.marvelsnapzone.com/tier-list/")

    def get_shadow_root(self):
        """
        Identifies the shadow root when cookies pop-up appears.
        :return: ShadowRoot object
        """
        host = (WebDriverWait(self.driver, 10).
                until(EC.presence_of_element_located((By.CSS_SELECTOR, "#cmpwrapper"))))
        shadow_root = host.shadow_root
        return shadow_root
    time.sleep(4)


    def accept_cookies(self, shadow_root):
        """
        Accepts the shadow_root object returned by get_shadow_root method and
        finds and clicks the "accept" button on cookies pop-up.
        """
        cookies_button = (WebDriverWait(self.driver, 10).
                          until((lambda d: shadow_root.
                                 find_element(By.CSS_SELECTOR, "a.cmpboxbtnyes"))))
        self.driver.execute_script("arguments[0].click();", cookies_button)


    def click_deck_link(self):
        """
        Locates the link to the top deck on the tier list and clicks it.
        """
        deck_link = (WebDriverWait(self.driver, 10).
                     until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[4]/main/div[2]/article/div"
                                                                       "/figure/table/tbody/tr[1]/td[2]/a"))))

        self.driver.execute_script("arguments[0].click();", deck_link)


    def bypass_captcha(self):
        """
        Bypasses the Cloudflare captcha after the deck link is clicked.
        """
        self.driver.uc_gui_click_captcha()


    def get_deck_code(self):
        """
        Locates the div containing the deck code.
        :return: Deck code string
        """
        deck_code_box = (WebDriverWait(self.driver, 10).
                            until(EC.visibility_of_element_located((By.CLASS_NAME, "msz-code"))))
        deck_code = deck_code_box.get_attribute('innerHTML')
        return deck_code


    def store_deck_code(self, deck_code):
        """
        Saves deck code to .txt file.
        :param deck_code: Retrieved via get_deck_code method.
        """
        with open('deck_code.txt', 'w') as file:
            file.write(deck_code)

    def close(self):
        self.driver.quit()



if __name__ == "__main__":
    scraper = Scraper()
    scraper.open_browser()
    scraper.accept_cookies(shadow_root=scraper.get_shadow_root())
    scraper.click_deck_link()
    scraper.store_deck_code(deck_code=scraper.get_deck_code())
    scraper.close()