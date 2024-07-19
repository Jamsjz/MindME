from sqlalchemy import create_engine
from datetime import date, datetime, time
from sqlalchemy.orm import sessionmaker
from models import Reminder

DATABASE_URL = "postgresql://j:j@localhost:5432/mindme"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


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
