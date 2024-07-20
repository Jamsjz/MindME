from sqlalchemy import create_engine
from datetime import date, datetime, time
from sqlalchemy.orm import sessionmaker
from .models import Base, User, Reminder, Admin, AdminReminder, AdminTask
import json
import bcrypt

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


def get_admin(name):
    session = Session()
    admin = session.query(Admin).filter_by(name=name).first()
    session.close()
    return admin


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


def add_admin_reminder(
    title: str, description: str, due_date: date, due_time: time, admin_id: int
):
    session = Session()
    reminder = AdminReminder(
        title=title,
        description=description,
        due_date=due_date,
        due_time=due_time,
        date_created=datetime.now().date(),
        time_created=datetime.now().time(),
        admin_id=admin_id,
    )
    session.add(reminder)
    session.commit()
    session.close()

    print(f"Reminder {title} created for user {admin_id}")


def add_admin_task(
    title: str, description: str, due_date: date, due_time: time, admin_id: int
):
    session = Session()
    task = AdminTask(
        title=title,
        description=description,
        due_date=due_date,
        due_time=due_time,
        date_created=datetime.now().date(),
        time_created=datetime.now().time(),
        admin_id=admin_id,
    )
    session.add(task)
    session.commit()
    session.close()

    print(f"Task {title} created for user {admin_id}")


def delete_reminder(reminder_id):
    session = Session()
    reminder = session.get(Reminder, reminder_id)
    if reminder:
        session.delete(reminder)
        session.commit()
        print(f"Reminder {reminder_id} deleted")
    else:
        print(f"Reminder {reminder_id} not found")
    session.close()


def delete_admin_reminder(reminder_id):
    session = Session()
    reminder = session.get(AdminReminder, reminder_id)
    if reminder:
        session.delete(reminder)
        session.commit()
        print(f"Reminder {reminder_id} deleted")
    else:
        print(f"Reminder {reminder_id} not found")
    session.close()


def delete_admin_task(id):
    session = Session()
    task = session.get(AdminTask, id)
    if task:
        session.delete(task)
        session.commit()
        print(f"Task {id} deleted")
    else:
        print(f"Task {id} not found")
    session.close()


def create_admin():
    session = Session()
    name = input("Enter the name of the admin: ")
    email = input("Enter the email of the admin: ")
    password = input("Enter the password of the admin: ")
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    admin = Admin(name=name, email=email, password=hashed_password)
    session.add(admin)
    session.commit()
