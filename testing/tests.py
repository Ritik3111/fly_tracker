import unittest
import json
import pandas as pd
from bs4 import BeautifulSoup
from fly_tracker import Scraper
from unittest.mock import Mock, patch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class TestPriceScraper(unittest.TestCase):
    def setUp(self):
        self.PriceScraper = Scraper.PriceScraper('New York', 'Boston', 100, '12 May')
        self.expected_df = pd.DataFrame({'src':['New York','New York','New York'],
                                                    "dest":['Boston','Boston','Boston'],
                                                    "Price": [100,104,107]})
        f = open("test_source_page.html", "r")
        self.mock_page_source = f.read()
        f.close()
        self.expected_soup = BeautifulSoup(self.mock_page_source,'html.parser')

    def test_preprocess(self):
        self.PriceScraper.preprocess()
        self.assertEqual(self.PriceScraper.src, 'New-York')
        self.assertEqual(self.PriceScraper.dest, 'Boston')
    
    @patch('pandas.DataFrame')
    def test_create_df(self,mock_dataframe):
        mock_json_data = [
            {"src": 'New York',"dest": 'Boston',"Price": 100},
            {"src": 'New York',"dest": 'Boston',"Price": 104},
            {"src": 'New York',"dest": 'Boston',"Price": 107}
                     ]
        
        mock_dataframe.return_value = self.expected_df
        df = self.PriceScraper.create_df(mock_json_data)
        pd.testing.assert_frame_equal(df, self.expected_df)
        mock_dataframe.assert_called_once_with(mock_json_data)

    @patch.object(Scraper.PriceScraper, 'parser')
    def test_parser(self, mock_parser):
        expected_data = [{
            "Source": "Delhi",
            "Departure Time": "10:00",
            "Destination": "Mumbai",
            "Arrival Time": "12:00",
            "Date": "2022-05-01",
            "Price": "100",
            "Airline": "Air India",
            "Timestamp": "2023-03-31 00:00:00.000000"
        }]
        mock_parser.return_value = expected_data

        soup = self.expected_soup
        data = self.PriceScraper.parser(soup)

        self.assertEqual(data, expected_data)
        mock_parser.assert_called_once_with(soup)


    @patch('bs4.BeautifulSoup',autospec=True)
    def test_soupify(self,mock_soup):
        mock_soup.return_value = self.expected_soup
        soup = self.PriceScraper.soupify(self.mock_page_source)
        self.assertEqual(soup, self.expected_soup)
        #mock_soup.assert_called_once_with(self.mock_page_source,features='html.parser')

    @patch('selenium.webdriver.Chrome',autospec=True)
    def test_get_page(self, mock_driver):
        #mock_driver.Chrome.return_value = mock_driver
        mock_driver.page_source = self.mock_page_source
        mock_element = Mock()
        mock_element.click.return_value = None
        mock_element.send_keys.return_value = None
        mock_driver.find_element.return_value = mock_element

        options = Options()
        options.add_argument('--window-size=1920,1200')
        options.add_argument('--headless')
        mock_driver.return_value.options = options

        page_source = self.PriceScraper.get_page()

        mock_driver.get.assert_called_once_with(f'https://www.google.com/travel/flights/non-stop-flights-from-{self.PriceScraper.src}-to-{self.PriceScraper.dest}.html')
        mock_driver.find_element.assert_called()
        mock_driver.execute_script.assert_called()
        mock_driver.quit.assert_called()

        self.assertEqual(page_source, self.mock_page_source)


if __name__ == '__main__':
    unittest.main()