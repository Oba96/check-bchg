import requests
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML

# Configuration
URL = "https://www.bchg.co.uk/our-properties/renting-with-bchg/"  # Replace with the URL of the website to monitor
EMAIL_FROM = "jjuniormvila@gmail.com"  # Replace with your email
EMAIL_TO = "jjuniormvila@gmail.com"  # Replace with recipient's email
EMAIL_PASSWORD = "crqecwoxsuzlcofn"  # Replace with your email password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def get_visible_text_hash(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract visible text from the webpage, ignoring scripts, styles, and comments
    for element in soup(['script', 'style', 'noscript']):
        element.extract()

    visible_text = soup.get_text(separator=' ', strip=True)
    return hashlib.md5(visible_text.encode('utf-8')).hexdigest()

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

def main():
    last_hash_file = "last_text_hash.txt"

    # Read the last known hash
    if os.path.exists(last_hash_file):
        with open(last_hash_file, "r") as file:
            last_hash = file.read().strip()
    else:
        last_hash = ""

    # Get the current hash of the visible text
    current_hash = get_visible_text_hash(URL)

    # Compare hashes to check for updates
    if current_hash != last_hash:
        send_email("Website Text Update Alert", f"The visible text on the page at {URL} has been updated.")
        with open(last_hash_file, "w") as file:
            file.write(current_hash)
    else:
        send_email("No Text Change Alert", f"No visible text changes detected on the page at {URL}.")

if __name__ == "__main__":
    main()
