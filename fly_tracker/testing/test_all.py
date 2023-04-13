"""
Unit tests for Scraper.py
"""
import unittest
import sys
from unittest.mock import Mock, patch
import pandas as pd
from bs4 import BeautifulSoup
from fly_tracker import Scraper
sys.path.append('../')
sys.path.append('./')
sys.path.append('testing/')

class TestPriceScraper(unittest.TestCase):
    """
    Unit Tests for the PriceScraper class
    Args:
        unittest (_type_): _description_
    """

    def setUp(self):
        self.PriceScraper = Scraper.PriceScraper(
            'New York', 'Boston', 100, '12 May')
        self.expected_df = pd.DataFrame(
            {
                'src': ['New York', 'New York', 'New York'],
                "dest": ['Boston', 'Boston', 'Boston'],
                "Price": [100, 104, 107]
            }
        )
        #file_path = os.path.join(os.path.join(os.getcwd(),'testing'),"test_source_page.html")
        #file = open(file_path, "r", encoding='utf-8')
        #self.mock_page_source = file.read()
        #file.close()
        self.mock_page_source = "<html> </html>"
        self.expected_soup = BeautifulSoup(
            self.mock_page_source, 'html.parser')

    def test_preprocess(self) -> None:
        """
        Test for preprocess
        """
        self.PriceScraper.preprocess()
        self.assertEqual(self.PriceScraper.src, 'New-York')
        self.assertEqual(self.PriceScraper.dest, 'Boston')

    @patch('pandas.DataFrame')
    def test_create_df(self, mock_dataframe) -> None:
        """
        Unit Test for Scraper.create_df function
        Args:
            mock_dataframe (_type_): _description_
        """
        mock_json_data = [
            {"src": 'New York', "dest": 'Boston', "Price": 100},
            {"src": 'New York', "dest": 'Boston', "Price": 104},
            {"src": 'New York', "dest": 'Boston', "Price": 107}
        ]
        mock_dataframe.return_value = self.expected_df
        df = self.PriceScraper.create_df(mock_json_data)
        pd.testing.assert_frame_equal(df, self.expected_df)
        mock_dataframe.assert_called_once_with(mock_json_data)

    @patch.object(Scraper.PriceScraper, 'parser')
    def test_parser(self, mock_parser) -> None:
        """
        Unit Test for Scraper.Parser function
        Args:
            mock_parser (MagicMock): _description_
        """
        expected_data = [{
            "Source": "New York",
            "Departure Time": "10:00",
            "Destination": "Boston",
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

    @patch('bs4.BeautifulSoup', autospec=True)
    def test_soupify(self, mock_soup):
        """
        Unit Test for Scraper.Soupify function
        Args:
            mock_soup (_type_): _description_
        """
        mock_soup.return_value = self.expected_soup
        soup = self.PriceScraper.soupify(self.mock_page_source)
        self.assertEqual(soup, self.expected_soup)
        # mock_soup.assert_called_once_with(self.mock_page_source,features='html.parser')

    @patch('selenium.webdriver.Chrome', autospec=True)
    def test_get_page(self, mock_driver):
        """
        Unit Test for Scraper.get_page function
        Args:
            mock_driver (_type_): _description_
        """
        mock_driver.page_source = self.mock_page_source
        mock_response = Mock()
        mock_response.status_code = 200
        # create a mock driver.get() method
        mock_driver.return_value.get.return_value = mock_response.status_code
        page_source = self.PriceScraper.get_page()
        self.assertIsNotNone(page_source)


if __name__ == '__main__':
    unittest.main()
