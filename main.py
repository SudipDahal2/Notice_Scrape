import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from datetime import datetime
from test import scrape_notices  # Assuming scrape_notices is your scraping function

# Load environment variables
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_email(subject, body, to_email):
    msg = MIMEText(body, "html")
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print(f"Email sent at {datetime.now()}")
    except Exception as e:
        print(f"Email failed: {e}")

def check_and_notify():
    notices = scrape_notices()
    if notices:
        latest_notice = notices[0]  # Assume newest first; adjust to [-1] if oldest first
        current_time = datetime.now().strftime("%I:%M %p %z on %B %d, %Y")
        subject = f"New Notice: {latest_notice['title']}"
        body = f"""
        <h1>New Notice Detected</h1>
        <p><strong>Title:</strong> {latest_notice['title']}</p>
        <p><strong>Link:</strong> <a href="{latest_notice['notice_link']}">{latest_notice['notice_link']}</a></p>
        <p><strong>File:</strong> {latest_notice['file_link'] or 'No file'}</p>
        <p>Detected at {current_time}.</p>
        """
        send_email(subject, body, EMAIL_USER)
    
    print(f"Check completed at {datetime.now()}")

if __name__ == "__main__":
    print("Running notice checker...")
    check_and_notify()