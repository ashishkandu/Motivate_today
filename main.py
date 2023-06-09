import smtplib
from typing import final, Tuple
import json
import logging
import sys
import ssl
from datetime import datetime
import requests
from email.message import Message

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]: %(asctime)s - %(name)s - %(message)s', datefmt='%H:%M:%S')

import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)

FILENAME: final = "credentials.json"
recipients = ['ashishkandu43@gmail.com', ]


entry = 0 # Using a list in the FILENAME which consists of multiple dictionaries, key-value pair of email and password

"""
For Gmail can use: smtp.gmail.com
For Hotmail can use: smtp.live.com
"""

# host = "smtp.mail.yahoo.com" # For yahoo mail
host = "smtp.gmail.com" # For gmail
port = 587
# port = 465 # port to use if using SMTP_SSL class

# To get weekday name from the int
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def getQuote() -> Tuple[str]:
    """Returns a tuple of (quote, author)"""
    response = requests.get('https://api.quotable.io/random')
    data: dict = response.json()
    quote: str = data.get('content')
    author: str = data.get('author')
    return (quote, author)

def get_credentials() -> Tuple[str]:
    """Get credentials from FILENAME in form of tuples (email, password)"""
    try:
        with open(FILENAME) as file:
            data: dict = json.load(file)
            logging.debug("File loaded sucessfully!")
    except FileNotFoundError:
        open(FILENAME, 'w').close()
        sys.exit("Save your credentials on credentials.json file")
    else:
        email: str = data[entry].get('email')
        password: str = data[entry].get('password')
        logging.debug("Email and password setting complete")
        return (email, password)

def send_email(from_email: str, to_email: str, password: str, message: str):
    """sends email to the to_email and returns dict if error occurs"""
    context = ssl.create_default_context()
    logging.info("Initiating connection")

    # Establishing connection
    connection = smtplib.SMTP(host=host, port=port, timeout=10)
    connection.set_debuglevel(0) # Debugging off
    logging.info("Connection establsihed")

    connection.starttls(context=context)
    logging.info("Connection secured")

    # Try establishing connection and send email
    try:
        result = connection.login(user=from_email, password=password)
        logging.debug(result)

        response = connection.sendmail(from_addr=from_email, to_addrs=to_email, msg=message)
        logging.info("Message sent")
    except Exception as e:
        logging.exception(e)
        response = {'error': e}

    finally:
        connection.close()
        logging.info('Connection closed')
        return response


if __name__ == '__main__':
    
    # Get credentials
    email, password = get_credentials()

    # Fetch quote form the API
    quote, author = getQuote()

    weekday = days[datetime.now().weekday()]

    content = f"\"{quote}\" - {author}\n\nHave a good day!\nAshish".encode('utf-8')
    
    # Formating  email
    msg = Message()
    msg['From'] = email
    # msg['To'] = ", ".join(recipients)
    msg['Subject'] = f"{weekday} Motivation!!"
    msg.set_payload(content)

    result = send_email(from_email=email, to_email=recipients, password=password, message=msg.as_string())

    # logs in case result is not empty, for any errors
    if result:
        logging.error(result)

