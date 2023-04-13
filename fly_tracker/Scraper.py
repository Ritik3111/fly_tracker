"""
Scrapes and returns a csv file with airline price data
Returns:
    pd.Dataframe: Airfare price data between src and dest
"""
import re
import datetime
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

class PriceScraper():
    """
    Scraper class that scrapes google flights
    """

    def __init__(self, src: str, dest: str, price: int, date: str) -> None:
        self.src = src
        self.dest = dest
        self.price = price
        self.date = date

    def get_page(self):
        """
        Load dynamic chrome browser and return page source to scrape
        """
        self.preprocess()
        # Open a headless chrome browser
        options = Options()
        options.add_argument('--window-size=1920,1200')
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        url = f'https://www.google.com/travel/flights/non-stop-flights-from-{self.src}-to-{self.dest}.html'
        driver.get(url)
        driver.find_element(By.XPATH, '//*[@class="dvO2xc k0gFV"]').click()
        trip_type = driver.find_element(
            By.XPATH, '//*[@class="A8nfpe yRXJAe iWO5td"]')
        trip_type.find_element(By.XPATH, '//*[@class="Akxp3 Lxea9c"]').find_element(
            By.XPATH, '//*[@class="uT1UOd"]').click()
        date_box = driver.find_element(
            By.XPATH, '//*[@class="RKk3r eoY5cb j0Ppje"]')
        time.sleep(2)

        driver.execute_script("arguments[0].value=''", date_box)
        date_box.send_keys(self.date)
        date_box.send_keys(Keys.ENTER)
        time.sleep(2)
        return driver.page_source
    def soupify(self,page: str) -> BeautifulSoup:
        """
        Return page to scrape as a BeautifulSoup object
        Args:
            page (str): Source page
        Returns:
            BeautifulSoup: parsed bs4 object
        """
        soup = BeautifulSoup(page, features="html.parser")
        return soup
    def parser(self,soup: BeautifulSoup) -> "list[dict]":
        """
        Helper parser function that scrapes required details

        Args:
            soup (BeautifulSoup): Soup object to scrape

        Returns:
            list[dict]: list of dictionaries which store scraped flight information records
        """
        flights = soup.find_all(class_='pIav2d')
        data = []

        for flight in flights:
            dep_time = flight.find(class_='wtdjmc YMlIz ogfYpf tPgKwe').text
            dep_city = flight.find(class_='G2WY5c sSHqwe ogfYpf tPgKwe').text
            arr_time = flight.find(class_='XWcVob YMlIz ogfYpf tPgKwe').text
            arr_city = flight.find(class_='c8rWCd sSHqwe ogfYpf tPgKwe').text
            price = flight.find(class_=re.compile('YMlIz FpEdX')).text
            if price > self.price:
                continue
            airline = flight.find(class_='h1fkLb').span.text
            timestamp = datetime.datetime.now()
            info = {
                "Source": dep_city,
                "Departure Time": dep_time,
                "Destination": arr_city,
                "Arrival Time": arr_time,
                "Date": self.date,
                "Price": price,
                "Airline": airline,
                "Timestamp": timestamp
            }
            data.append(info)
        return data

    def create_df(self, data: "list[dict]") -> pd.DataFrame:
        """
        Helper function to convert data into a Pandas Dataframe

        Args:
            data (list[dict]): Flight Information data

        Returns:
            pd.DataFrame: data in the form of a pandas Dataframe
        """

        df = pd.DataFrame(data)
        return df
    def preprocess(self) -> None:
        """
        Helper Preprocessing function
        """
        self.src = self.src.replace(' ', '-')
        self.dest = self.dest.replace(' ', '-')
        