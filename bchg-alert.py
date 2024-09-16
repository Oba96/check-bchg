import requests
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Configuration
URL = "https://www.bchg.co.uk/our-properties/renting-with-bchg/"  # URL to monitor
EMAIL_FROM = "jjuniormvila@gmail.com"  # Sender email
EMAIL_TO = "jjuniormvila@gmail.com"    # Recipient email
EMAIL_PASSWORD = "crqecwoxsuzlcofn"    # Email password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Get the hash of the web page content
def get_page_hash(url):
    response = requests.get(url)
    content = response.text
    return hashlib.md5(content.encode('utf-8')).hexdigest()

# Send an email notification
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
    # Path to the last_hash.txt file
    last_hash_file = "last_hash.txt"

    # Ensure the file exists or create it if missing
    if not os.path.exists(last_hash_file):
        with open(last_hash_file, "w") as file:
            file.write("")  # Write an empty string to create the file

    # Read the last known hash
    with open(last_hash_file, "r") as file:
        last_hash = file.read().strip()

    # Get the current hash of the web page
    current_hash = get_page_hash(URL)
    print(f"Current hash: {current_hash}")
    print(f"Last hash: {last_hash}")
    # Compare hashes to check for updates
    if current_hash != last_hash:
        send_email("Website Update Alert", f"The page at {URL} has been updated.")
        # Save the new hash to the file
        with open(last_hash_file, "w") as file:
            file.write(current_hash)
        return 1  # Return exit code 1 to indicate change
    else:
        send_email("Website No Change Alert", f"No changes detected on the page at {URL}.")
        return 0  # Return exit code 0 to indicate no change

if __name__ == "__main__":
    print("Fetching page...")
    exit(main())  # Exit with 1 if updated, 0 if not
