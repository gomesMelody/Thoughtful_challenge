from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

from scripts.utils import parse_date
class SeleniumConn:
    """
    Class to connect and interact with a website using selenium.

    The class is initialized with a headless chrome options, so the browser
    won't be visible when running the script.

    Attributes:
        driver (webdriver): The selenium webdriver instance.
    """

    def __init__(self):
        """
        Initialize the class with a headless chrome options.
        """
        options = Options()
        options.add_argument('--headless=new')
        self.driver = webdriver.Chrome(options=options)

    def connect(self, url: str) -> None:
        """
        Connect to the specified url with the selenium webdriver.

        Args:
            url (str): The url to connect to.
        """
        # Use the selenium webdriver to navigate to the specified url
        self.driver.get(url)
        

    def search_for_phrase(self, phrase: str) -> None:
        """
        Search for a given phrase on the website.

        This function searches for the phrase on the website by clicking on the
        magnify icon and submitting the search bar with the given phrase.

        Args:
            phrase (str): The phrase to search for.
        """
        # Get the magnify icon element
        search_element = self.driver.find_element(By.XPATH, "//button[@data-element='search-button']")

        # Click on the magnify icon to open the search bar
        search_element.click()

        # Wait a bit for the search bar to open
        time.sleep(1)

        # Get the search bar element
        search_element = self.driver.find_element(By.NAME, "q")

        # Send the phrase to the search bar
        search_element.send_keys(phrase)

        # Submit the search bar
        search_element.submit()

    def iterate_news_by_month(self, month: int, year: int) -> list:
        """
        Iterate over the news on the current page by month.

        This function iterates over the news on the current page and extracts 
        the ones that match the given month and year. It also downloads the 
        corresponding images and stores them in the "images" directory.

        Args:
            month (int): The month to extract news for.
            year (int): The year to extract news for.

        Returns:
            A list of dictionaries containing the extracted news. Each dictionary
            contains the following keys:
                - title (str): The title of the news.
                - date (datetime.date): The date of the news.
                - category (str): The category of the news.
                - description (str): The description of the news.
                - image (str): The filename of the image associated with the news.
        """
        # get element search-results-module-results-menu with xpath
        tt = self.driver.find_element(By.CLASS_NAME, "search-results-module-results-menu")
        news_list = tt.find_elements(By.TAG_NAME, "li")
        valid_news = []
        for news in news_list:
            text_date = news.find_element(By.CLASS_NAME, "promo-timestamp").text
            date = parse_date(text_date)
            if date.month == month and date.year == year:
                # download the image
                image = news.find_element(By.CLASS_NAME, "image")
                image_url = image.get_attribute('srcset')
                image_filename = f"{date.strftime('%Y-%m-%d')}-{news.find_element(By.CLASS_NAME, 'promo-title').text}.jpg"
                open(f"images/{image_filename}", 'wb').write(image.screenshot_as_png)

                # extract the news information
                valid_news.append({
                    #  'news_element' : news,
                     'title': news.find_element(By.CLASS_NAME, "promo-title").text,
                     'date': date,
                     'category': news.find_element(By.CLASS_NAME, "promo-category").text,
                     'description': news.find_element(By.CLASS_NAME, "promo-description").text,
                     'image': image_filename
                    })

        return valid_news

    def close(self):
        """
        Close the selenium webdriver.

        This method is used to close the selenium webdriver after it has finished
        executing. It is typically called at the end of the script.
        """
        # Close the selenium webdriver
        self.driver.close()

