from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import pandas as pd
from fly_tracker.Scraper import PriceScraper

class Notifier:
    """
    Notifier class that sends email notification with the scraped data
    """

    def __init__(self, email:str, data:pd.DataFrame, scraper:PriceScraper):
        # Define the email sender and recipient
        self.sender = "pandaritik39@gmail.com"
        self.recipient = email
        self.df = data
        self.src = scraper.src
        self.dest = scraper.dest
        self.date = scraper.date
        # Define the HTML template
        # pylint: disable=R0801
        self.html_template = '''
        <html>
        <head>
        <style>
            /* Define table styles */
            table {{
            font-family: arial, sans-serif;
            border-collapse: collapse;
            width: 100%;
            }}

            td, th {{
            border: 1px solid #dddddd;
            text-align: left;
            padding: 8px;
            }}

            tr:nth-child(even) {{
            background-color: #dddddd;
            }}
        </style>
        </head>
        <body>

        <h2>Flight Data</h2>

        {table}

        </body>
        </html>
        '''

    def send_mail(self,msg:MIMEMultipart):
        """
        Create email body and send scraped flight fare data

        Args:
            msg (MIMEMultipart): Email to be sent
        """

        # Send the message using the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.sender, "dwycyikmmvtjllzw")
        text = msg.as_string()
        server.sendmail(self.sender, self.recipient, text)
        server.quit()
    def create_message(self):
        """
        Create a message object and set the subject and body

        Returns:
            MIMEMultipart: Email Content
        """
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg['Subject'] = f"FLY_TRACKER: {self.src} to {self.dest} on {self.date} fares"
        body = f"This is an email notification from fly-tracker with fares for your {self.src} to {self.dest} route on {self.date}"  # noqa: E501
        msg.attach(MIMEText(body, 'plain'))

        # Convert the dataframe to an HTML table
        flight_data_html = self.df.to_html(index=False, classes='table table-striped')

        # Insert the table into the HTML template
        html = self.html_template.format(table=flight_data_html)

        body = MIMEText(html, 'html')
        msg.attach(body)
        return msg
