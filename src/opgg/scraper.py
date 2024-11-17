from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import re

class OPGGScraper:
    def __init__(self, headless: bool = True):
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless=new")
            
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        self.chrome_options.add_argument(f'user-agent={self.user_agent}')
        self.driver = None
        
    def start_driver(self):
        if not self.driver:
            self.driver = webdriver.Chrome(options=self.chrome_options)

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def use_regex(self, input_text):
        pattern = re.compile(r"^(.*)#([A-Za-z0-9]+)$", re.IGNORECASE)
        match = pattern.match(input_text)
        if match:
            return match.group(1), match.group(2)
        else:
            return None, None  
        
    def get_kda(self, username: str):
        try:
            if not self.driver:
                self.start_driver()
            first_part, second_part = self.use_regex(username)
            formatted_username = first_part.replace(" ", "%20")
            url = f"https://www.op.gg/summoners/eune/{formatted_username}-{second_part}"
            self.driver.get(url)
            parent_div = self.driver.find_element(By.CLASS_NAME, "css-1jxewmm.e14wvufv0")
            child_divs = parent_div.find_elements(By.CLASS_NAME, "css-j7qwjs.e1c5dkji0")

            if not child_divs:
                return None
                
            kda_div = child_divs[0].find_element(By.CLASS_NAME, "kda-stats")
            kda_spans = kda_div.find_elements(By.TAG_NAME, "span")

            kda_text = ""
            
            for span in kda_spans:
                text = span.text.strip()
                if text:
                    kda_text += text + "/"  
            kda_text = kda_text.rstrip("/")
            return kda_text
        except NoSuchElementException:
            return None
        except Exception as e:
            print(f"Error extracting KDA: {str(e)}")
            return None
    
    def get_picture(self, username: str):
        try:
            if not self.driver:
                self.start_driver()
            first_part, second_part = self.use_regex(username)
            formatted_username = first_part.replace(" ", "%20")
            url = f"https://www.op.gg/summoners/eune/{formatted_username}-{second_part}"
            self.driver.get(url)
            parent_div = self.driver.find_element(By.CLASS_NAME, "css-1jxewmm.e14wvufv0")
            child_divs = parent_div.find_elements(By.CLASS_NAME, "css-j7qwjs.e1c5dkji0")

            if not child_divs:
                return None
                
            main_div = child_divs[0].find_element(By.CLASS_NAME, "main")
            info_div = main_div.find_element(By.CLASS_NAME, "info")
            img_element = info_div.find_element(By.TAG_NAME, "img")
            img_url = img_element.get_attribute("src")
            return img_url
        except NoSuchElementException:
            return None
        except Exception as e:
            print(f"Error extracting image: {str(e)}")
            return None
    
    def __enter__(self):
        self.start_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_driver()
            