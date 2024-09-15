import requests
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Configuration
URL = "https://www.bchg.co.uk/our-properties/renting-with-bchg/"  # Replace with the URL of the website to monitor
CHECK_INTERVAL = 3600  # Check every hour
EMAIL_FROM = "jjuniormvila@gmail.com"  # Replace with your email
EMAIL_TO = "jjuniormvila@gmail.com"  # Replace with recipient's email
EMAIL_PASSWORD = "crqecwoxsuzlcofn"  # Replace with your email password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
LAST_HASH_FILE = "last_hash.txt"

def get_page_hash(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        content = response.text
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")

def main():
    if not os.path.exists(LAST_HASH_FILE):
        with open(LAST_HASH_FILE, "w") as file:
            file.write("")

    # Read the last known hash
    with open(LAST_HASH_FILE, "r") as file:
        last_hash = file.read().strip()

    # Get the current hash of the web page
    current_hash = get_page_hash(URL)
    
    if current_hash is None:
        # If there was an error fetching the page, exit
        return

    # Compare hashes to check for updates
    if current_hash != last_hash:
        send_email("Website Update Alert", f"The page at {URL} has been updated.")
        with open(LAST_HASH_FILE, "w") as file:
            file.write(current_hash)
    else:
        # Optional: Comment out if you do not want to send an email when no changes are detected
        send_email("Website No Change Alert", f"No changes detected on the page at {URL}.")

if __name__ == "__main__":
    main()
