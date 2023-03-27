from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
from bs4 import BeautifulSoup
import pandas as pd
import datetime


class PriceScraper():
    def __init__(self,src:str,dest:str,price:int,date:str) -> None:
        self.src = src
        self.dest = dest
        self.price = price
        self.date = date

        return 


    def get_page(self):

        # Open a headless chrome browser
        options = Options()
        options.add_argument('--window-size=1920,1200')
        #options.add_argument("--headless")
        service = Service(executable_path='chromedriver_mac64')
        driver = webdriver.Chrome(service=service,options=options)

        url = 'https://www.google.com/travel/flights/non-stop-flights-from-new-york-to-boston.html'
        driver.get(url)

        driver.find_element(By.XPATH,'//*[@class="dvO2xc k0gFV"]').click()
        tt = driver.find_element(By.XPATH,'//*[@class="A8nfpe yRXJAe iWO5td"]')
        tt.find_element(By.XPATH,'//*[@class="Akxp3 Lxea9c"]').find_element(By.XPATH,'//*[@class="uT1UOd"]').click()

        date_box = driver.find_element(By.XPATH,'//*[@class="RKk3r eoY5cb j0Ppje"]')
        date_box.clear()
        date_box.send_keys('May 15')

        ## wait
        driver.implicitly_wait(5)
        date_box.send_keys(Keys.ENTER)

        driver.refresh()

        return driver.page_source


    def soupify(self,page) -> BeautifulSoup:
        soup = BeautifulSoup(soup)
        return soup

    def parser(self,soup:BeautifulSoup) -> list[dict]:
        flights = soup.find_all(class_='pIav2d')
        data = []

        for flight in flights:
            dep_time = flight.find(class_='wtdjmc YMlIz ogfYpf tPgKwe').text
            dep_city = flight.find(class_='G2WY5c sSHqwe ogfYpf tPgKwe').text
            arr_time = flight.find(class_='XWcVob YMlIz ogfYpf tPgKwe').text
            arr_city = flight.find(class_='c8rWCd sSHqwe ogfYpf tPgKwe').text
            price = flight.find(class_=re.compile('YMlIz FpEdX')).text
            airline = flight.find(class_='h1fkLb').span.text
            timestamp = datetime.datetime.now()

            info = {
                "Source": dep_city,
                "Departure Time": dep_time,
                "Destination": arr_city,
                "Arrival Time": arr_time,
                "Price": price,
                "Airline": airline,
                "Timestamp": timestamp
            }
            
            data.append(info)
        
        return data

    def create_df(self,data:list[dict]) -> pd.DataFrame:
        df = pd.DataFrame(data)
        return df