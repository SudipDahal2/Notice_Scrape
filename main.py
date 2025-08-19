import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import pytz
from test import scrape_notices  # Assuming scrape_notices is your scraping function

# Load environment variables
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
STATE_FILE = "last_notice.json"  # File to store the last processed notice

def send_email(subject, body, to_email):
    msg = MIMEText(body, "html")
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print(f"Email sent at {datetime.now(pytz.UTC)}")
        return True
    except Exception as e:
        print(f"Email failed: {e}")
        return False

def load_last_notice():
    """Load the last processed notice from a file."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return None

def save_last_notice(notice):
    """Save the latest notice to a file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(notice, f)

def check_and_notify():
    try:
        notices = scrape_notices()
        if not notices:
            print(f"No notices found at {datetime.now(pytz.UTC)}")
            return

        latest_notice = notices[0]  # Assume newest first
        last_notice = load_last_notice()

        # Check if the latest notice is new
        notice_identifier = latest_notice['title'] + latest_notice['notice_link']  # Unique identifier
        if last_notice and last_notice.get('identifier') == notice_identifier:
            print(f"No new notices at {datetime.now(pytz.UTC)}")
            return

        # New notice detected, send email
        current_time = datetime.now(pytz.UTC).strftime("%I:%M %p UTC on %B %d, %Y")
        subject = f"New Notice: {latest_notice['title']}"
        body = f"""
        <h1>New Notice Detected</h1>
        <p><strong>Title:</strong> {latest_notice['title']}</p>
        <p><strong>Link:</strong> <a href="{latest_notice['notice_link']}">{latest_notice['notice_link']}</a></p>
        <p><strong>File:</strong> {latest_notice['file_link'] or 'No file'}</p>
        <p>Detected at {current_time}.</p>
        """
        if send_email(subject, body, EMAIL_USER):
            # Save the new notice as the last processed one
            save_last_notice({
                'identifier': notice_identifier,
                'title': latest_notice['title'],
                'notice_link': latest_notice['notice_link']
            })
        print(f"Check completed at {datetime.now(pytz.UTC)}")

    except Exception as e:
        print(f"Error in check_and_notify: {e}")

if __name__ == "__main__":
    print("Running notice checker...")
    check_and_notify()
