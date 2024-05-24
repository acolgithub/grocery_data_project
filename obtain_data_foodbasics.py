from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from requests_html import HTMLSession



class FoodBasics():
        
    def __init__(self):

        self.url = "https://www.foodbasics.ca"
        self.header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
        self.options = FirefoxOptions()

        # run headless
        self.options.add_argument("--headless")

        # adjust window size
        self.options.add_argument("window-size=1920,1080")


    # get relevant stories
    def get_food_basics_deal_data(self, grocery_item: str):

        # form url with query
        url_query = self.url + "/search?filter=" + grocery_item

        # get driver
        driver = webdriver.Firefox(options=self.options)

        # go to url
        driver.get(url_query)

        try:

            # wait until privacy element is visible
            WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//div[@class="banner-actions-container"]')))

            # click not to accept cookies
            privacy_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
            privacy_button.click()

            # wait until desired elements load
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='content__head']"))
            )


        except UnboundLocalError as e:
            print(e)
            driver.quit()

        finally:

            # get brand, name, price, and unit of grocery item
            search_item_description = element.find_elements(By.XPATH, "//*[@class='head__title']")
            search_item_unit = element.find_elements(By.XPATH, "//*[@class='head__unit-details']")
            search_item_price = element.find_elements(By.XPATH, "//*[@class='pricing__sale-price promo-price'] | //*[@class='pricing__sale-price']")

            # get brand text
            search_item_description = [description.text for description in search_item_description]

            # get item unit
            search_item_unit = [unit.text for unit in search_item_unit]

            # format price
            search_item_price = [re.sub(r"\n", "", price.text) for price in search_item_price]

            driver.quit()

        # make columns   
        columns = ["description", "unit", "price"]

        driver.quit()

        # make dataframe
        df = pd.DataFrame(data=[list(row) for row in zip(search_item_description, search_item_unit, search_item_price)], columns=columns)

        return df


food_basics = FoodBasics()

t0 = time.time()
print(food_basics.get_food_basics_deal_data("milk"))
print(time.time() - t0)
