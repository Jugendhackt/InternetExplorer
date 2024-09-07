from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class browser:
    def __init__(self) -> None:
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def loadWebsite(self, url: str) -> str:
        self.browser.get(url)
        return str(self.browser.page_source)
    
    def click_element(self, x_path: str) -> bool:
        try: self.browser.find_element(By.XPATH, x_path).click(); return True
        except: return False
    
    def type_text(self, x_path: str, text: str, submit: bool) -> bool:
        try: 
            input_element = self.browser.find_element(By.XPATH, x_path); input_element.send_keys(text); 
            if submit: input_element.send_keys(Keys.ENTER)
            return True
        except: return False
    
    def getContent(self) -> str: return str(self.browser.page_source)

    def xpath_exists(self, xpath: str) -> bool:
        try: self.browser.find_element(By.XPATH, xpath); return True
        except: return False





if __name__ == "__main__":
    driver = browser()
    print(driver.loadWebsite("https://eventfully.ugolis.de"))