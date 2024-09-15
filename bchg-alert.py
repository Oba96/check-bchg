import requests
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Configuration
URL = "https://www.bchg.co.uk/our-properties/renting-with-bchg/"
EMAIL_FROM = "jjuniormvila@gmail.com"
EMAIL_TO = "jjuniormvila@gmail.com"
EMAIL_PASSWORD = "crqecwoxsuzlcofn"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
LAST_HASH_FILE = "last_hash.txt"

def get_page_hash(url):
    response = requests.get(url)
    content = response.text
    return hashlib.md5(content.encode('utf-8')).hexdigest()

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
    # Read the last known hash
    if os.path.exists(LAST_HASH_FILE):
        with open(LAST_HASH_FILE, "r") as file:
            last_hash = file.read().strip()
    else:
        last_hash = ""

    # Get the current hash of the web page
    current_hash = get_page_hash(URL)

    # Compare hashes to check for updates
    if current_hash != last_hash:
        send_email("Website Update Alert", f"The page at {URL} has been updated.")
        with open(LAST_HASH_FILE, "w") as file:
            file.write(current_hash)
        # Optionally, commit changes if needed
    else:
        send_email("Website No Change Alert", f"No changes detected on the page at {URL}.")

if __name__ == "__main__":
    main()
