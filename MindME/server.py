import smtplib
import schedule
import time as time_module
from datetime import datetime
from flask import Flask
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database.models import Reminder, User, Admin, AdminTask, AdminReminder
import json
import pytz

app = Flask(__name__)

# Load config
with open("config.json") as config_file:
    config = json.load(config_file)

# Database setup
DATABASE_URI = f"postgresql://{config['database']['user']}:{config['database']['password']}@{config['database']['host']}:{config['database']['port']}/{config['database']['database']}"
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
    reminders = session.query(Reminder).filter(Reminder.processed == False).all()
    print("got reminders")
    admin_reminders = (
        session.query(AdminReminder).filter(AdminReminder.processed == False).all()
    )
    print("got admin reminders")
    print(f"Checking {len(reminders)} reminders")
    users = session.query(User).all()

    for reminder in reminders:
        for user in users:
            email_subject = f"Reminder: {reminder.title}"
            email_body = (
                f"Description: \n {reminder.description}\nDue Date: "
                f"{reminder.due_date} {reminder.due_time}"
            )
            send_email(user.email, email_subject, email_body)
            print(f"Sent reminder email to {user.email} for reminder ID {reminder.id}")
            reminder.processed = True
            print("processed")
            session.commit()
            print("committed")

    for admin_reminder in admin_reminders:
        admin = session.get(Admin, admin_reminder.admin_id)
        if admin:
            email_subject = f"Reminder: {admin_reminder.title}"
            email_body = (
                f"Description: \n {admin_reminder.description}\nDue Date: "
                f"{admin_reminder.due_date} {admin_reminder.due_time}"
            )
            send_email(admin.email, email_subject, email_body)
            print(
                f"Sent reminder email to admin {admin.email} for reminder ID {admin_reminder.id}"
            )
            admin_reminder.processed = True
            session.commit()
        else:
            print(f"Reminder with ID {admin_reminder.id} has invalid due time or date")


def check_tasks():
    current_time = datetime.now(pytz.utc)
    tasks = session.query(AdminTask).filter(AdminTask.processed == False).all()
    print(f"Checking {len(tasks)} tasks")

    for task in tasks:
        print("checked")
        for user in task.users:
            email_subject = f"Task: {task.title}"
            email_body = (
                f"Description: \n {task.description}\nDue Date: "
                f"{task.due_date} {task.due_time}"
            )
            send_email(user.email, email_subject, email_body)
            print(f"Sent task email to user {user.email} for task ID {task.id}")

        task.processed = True
        session.commit()


@app.route("/")
def index():
    return "Reminder Email Server is running."


def run_scheduler():
    schedule.every(1).minutes.do(check_reminders)
    schedule.every(1).minutes.do(check_tasks)

    while True:
        schedule.run_pending()
        time_module.sleep(1)


if __name__ == "__main__":
    run_scheduler()
