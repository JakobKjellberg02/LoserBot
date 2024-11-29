from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import re

class PlayerStats:
    """ Class to store player stats """
    kda = None
    place = None
    profile_image_url = None

class OPGGScraper:
    """ Class to get data legit from op.gg because riot doesn't want to give a key """
    def __init__(self, headless: bool = True):
        self.chrome_options = Options() # Chrome options
        if headless:
            self.chrome_options.add_argument("--headless=new") # Open chrome headless
            
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36' # We need this otherwise op will reject our friendly request
        self.chrome_options.add_argument(f'user-agent={self.user_agent}')
        self.driver = None
        
    def start_driver(self):
        """ Start Selenium WebDriver """
        if not self.driver:
            self.driver = webdriver.Chrome(options=self.chrome_options)

    def close_driver(self):
        """ Close Selenium WebDriver """
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def use_regex(self, input_text):
        """ Use a regular expression to separate the username and its unique identifier """
        pattern = re.compile(r"^(.*)#([A-Za-z0-9]+)$", re.IGNORECASE)
        match = pattern.match(input_text)
        if match:
            return match.group(1), match.group(2)
        else:
            return None, None  
        
    def get_kda(self, username: str):
        """ This Is Where the Fun Begins """
        try:
            if not self.driver:
                self.start_driver()
            first_part, second_part = self.use_regex(username) # Extract username and identifier with regex
            formatted_username = first_part.replace(" ", "%20") # Format with op standard
            url = f"https://www.op.gg/summoners/eune/{formatted_username}-{second_part}"
            self.driver.get(url)
            parent_div = self.driver.find_element(By.CLASS_NAME, "css-1jxewmm.ek41ybw0")
            child_divs = parent_div.find_elements(By.CLASS_NAME, "css-j7qwjs.ery81n90")

            if not child_divs:
                return None
            
            stats_div = child_divs[0]
            stats = PlayerStats()
            try:
                """ Stats """
                kda_div = stats_div.find_element(By.CLASS_NAME, "kda-stats")
                kda_spans = kda_div.find_elements(By.TAG_NAME, "span")
                stats.kda = "/".join(span.text.strip() for span in kda_spans if span.text.strip())
            except NoSuchElementException:
                print(f"KDA stats not found for user: {username}")
            
            try:
                """ Score badge """
                scorebadge_div = stats_div.find_element(By.CLASS_NAME, "sub")
                game_contain = scorebadge_div.find_element(By.CLASS_NAME, "game-tags__scroll-container")
                gametags_div = game_contain.find_element(By.CLASS_NAME, "game-tags")
                scorebadge_div = gametags_div.find_element(By.CLASS_NAME, "OPScoreBadge.css-1mkftr3.e1tb8p1o0")
                score_div = scorebadge_div.find_element(By.TAG_NAME, "div")
                stats.place = score_div.text
            except NoSuchElementException:
                print(f"Place stats not found for user: {username}")
                return None


            try:
                """ Image """
                champion_link = child_divs[0].find_element(By.CLASS_NAME, "champion")
                img_element = champion_link.find_element(By.TAG_NAME, "img")
                stats.profile_image_url = img_element.get_attribute("src")
            except NoSuchElementException:
                print(f"Profile image not found for user: {username}")
                return None
            
            return stats
        except Exception as e:
            print(f"Error extracting KDA: {str(e)}")
            return None
    
    # Context management methods to automatically handle the driver lifecycle
    def __enter__(self):
        """ Start the driver when entering the context """
        self.start_driver()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ close the driver when entering the context """
        self.close_driver()
            