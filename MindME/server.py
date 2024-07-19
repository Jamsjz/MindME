import smtplib
import schedule
import time
from datetime import datetime
from flask import Flask
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import Reminder, User
import json
import pytz

app = Flask(__name__)

# Load config
with open("config.json") as config_file:
    config = json.load(config_file)

# Database setup
DATABASE_URI = f"postgresql://{config['database']['user']}:{config['database']['password']}@{config['database']['host']}:{config['database']['port']}/{config['database']['dbname']}"
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Email setup
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = config["eserver"]["email"]
PASSWORD = config["eserver"]["password"]


def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL, to_email, text)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")


def check_reminders():
    current_time = datetime.now(pytz.utc)
    reminders = session.query(Reminder).all()

    for reminder in reminders:
        reminder_time = datetime.combine(reminder.due_date, reminder.due_time).replace(
            tzinfo=pytz.utc
        )
        if reminder_time <= current_time:
            user = session.query(User).filter_by(id=reminder.user_id).first()
            if user:
                email_subject = "Reminder: " + reminder.title
                email_body = f"Description: {reminder.description}\nDue Date: {reminder.due_date} {reminder.due_time}"
                send_email(user.email, email_subject, email_body)
                session.delete(reminder)
                session.commit()
                print(
                    f"Sent reminder email to {user.email} and deleted reminder with ID {reminder.id}"
                )


@app.route("/")
def index():
    return "Reminder Email Server is running."


def run_scheduler():
    schedule.every(1).minutes.do(check_reminders)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_scheduler()
