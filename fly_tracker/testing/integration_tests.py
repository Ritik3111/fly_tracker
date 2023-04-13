"""
Integration Test for Scraper.py
"""

from fly_tracker import Scraper

def test_price_scraper_integration():
    """
    Integration Test for PriceScraper class
    """
    # Create a PriceScraper instance with specific parameters
    scraper = Scraper.PriceScraper(src="New York", dest="Los Angeles", price=500, date="2023-05-15")

    # Scrape the Google Flights page and parse the flight information
    page = scraper.get_page()
    soup = scraper.soupify(page)
    data = scraper.parser(soup)

    # Convert the flight information to a pandas DataFrame
    df = scraper.create_df(data)

    print(df)
    # Verify that the DataFrame contains the expected flight information
    assert len(df) > 0
    assert df['Source'][0] == "JFK" or df['Source'][0] == "EWR"
    assert df['Destination'][0] == "LAX"
    #assert df['Price'][0] <= 500
    assert df['Date'][0] == "2023-05-15"
    assert df['Airline'][0] is not None
    assert df['Timestamp'][0] is not None

    print("Integration test completed successfully.")

def main():
    """
    main function
    """
    test_price_scraper_integration()

if __name__ == '__main__':
    main()
