from sqlalchemy import create_engine
from datetime import date, datetime, time
from sqlalchemy.orm import sessionmaker
from .models import Base, User, Reminder
import json

# Load database configuration
with open("config.json") as config_file:
    config = json.load(config_file)

DATABASE_URI = f"postgresql://{config['database']['user']}:{config['database']['password']}@{config['database']['host']}:{config['database']['port']}/{config['database']['database']}"

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.create_all(engine)


def add_user(username, password, email):
    session = Session()
    user = User(username=username, password=password, email=email)
    session.add(user)
    session.commit()


def get_user(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user


def add_reminder(
    title: str, description: str, due_date: date, due_time: time, user_id: int
):
    session = Session()
    reminder = Reminder(
        title=title,
        description=description,
        due_date=due_date,
        due_time=due_time,
        date_created=datetime.now().date(),
        time_created=datetime.now().time(),
        latest_update_date=datetime.now().date(),
        latest_update_time=datetime.now().time(),
        user_id=user_id,
    )
    session.add(reminder)
    session.commit()
    session.close()

    print(f"Reminder {title} created for user {user_id}")


def update_reminder(
    reminder_id: int, title: str, description: str, due_date: date, due_time: time
):
    """Update a reminder in the database"""
    session = Session()
    reminder = session.get(Reminder, reminder_id)
    if reminder is not None and reminder is Reminder:
        reminder.title = title
        reminder.description = description
        reminder.due_date = due_date
        reminder.due_time = due_time
        reminder.latest_update_date = date.today()
        reminder.latest_update_time = datetime.now().time()
    session.commit()
    print(f"Reminder {reminder_id} updated")
    session.close()


def delete_reminder(reminder_id):
    session = Session()
    reminder = session.query(Reminder).get(reminder_id)
    if reminder:
        session.delete(reminder)
        session.commit()
        print(f"Reminder {reminder_id} deleted")
    else:
        print(f"Reminder {reminder_id} not found")
    session.close()
