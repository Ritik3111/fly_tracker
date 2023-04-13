import argparse
from datetime import datetime
from fly_tracker.Scraper import PriceScraper

parser = argparse.ArgumentParser()

parser.add_argument('--src')
parser.add_argument('--dest')
parser.add_argument('--price')
parser.add_argument('--date')

args = parser.parse_args()

def main():
    """
    Main Function
    """
    scraper = PriceScraper(args.src,args.dest,args.price,args.date)
    page = scraper.get_page()
    soup = scraper.soupify(page)
    parsed_page = scraper.parser(soup)
    df = scraper.create_df(parsed_page)
    timestamp = datetime.now()
    df.to_csv(f'Results_{timestamp}.csv')

if __name__ == "__main__":
    main()
        