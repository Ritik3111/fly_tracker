import argparse
import schedule
import time
from datetime import datetime, timedelta
from datetime import datetime
from fly_tracker.Scraper import PriceScraper
from Notifier import Notifier

parser = argparse.ArgumentParser()

parser.add_argument('--src')
parser.add_argument('--dest')
parser.add_argument('--price')
parser.add_argument('--date')
parser.add_argument('--email')

args = parser.parse_args()

start_date = datetime.now()
print("Program started at:", start_date)

def main():
    """
    Main Function
    """
    try:
        # Schedule the function to run at 12:00 am and 12:00 pm
        schedule.every().day.at("00:00").do(script)
        schedule.every().day.at("12:00").do(script)

        # Run the scheduled jobs indefinitely
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Notification Service stopped")

if __name__ == "__main__":
    main()
    
def script():
    """
    Caller Function that is scheduled to run periodically
    """
    scraper = PriceScraper(args.src,args.dest,args.price,args.date)
    page = scraper.get_page()
    soup = scraper.soupify(page)
    parsed_page = scraper.parser(soup)
    df = scraper.create_df(parsed_page)
    timestamp = datetime.now()
    df.to_csv(f'Results_{timestamp}.csv')
    notifier = Notifier(args.email,df,scraper)
    message = notifier.create_message()
    notifier.send_mail(message)
