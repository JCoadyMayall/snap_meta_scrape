from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
    def __init__(self):
        options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(options=options)


    def open_browser(self):
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


    def accept_cookies(self, shadow_root):
        """Accepts the shadow_root object returned by get_shadow_root method and
        finds and clicks the "accept" button on cookies pop-up.
        """

        cookies_button = (WebDriverWait(self.driver, 10).
                          until((lambda d: shadow_root.
                                 find_element(By.CSS_SELECTOR, "a.cmpboxbtnyes"))))
        self.driver.execute_script("arguments[0].click();", cookies_button)





    def close(self):
        self.driver.quit()



if __name__ == "__main__":
    scraper = Scraper()
    scraper.open_browser()
    scraper.accept_cookies(shadow_root=scraper.get_shadow_root())


    # scraper.close()