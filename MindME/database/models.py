from sqlalchemy import Column, Integer, String, Text, ForeignKey, Time, Date, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

# Association table for the many-to-many relationship
task_user_association = Table(
    "task_user_association",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("admin_tasks.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # Define the relationship to Reminder
    reminders = relationship("Reminder", back_populates="user")

    # Define the many-to-many relationship to AdminTasks
    tasks = relationship(
        "AdminTask", secondary=task_user_association, back_populates="users"
    )


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    due_date = Column(Date, nullable=False)
    due_time = Column(Time, nullable=False)
    date_created = Column(
        Date, default=datetime.datetime.now(datetime.UTC), nullable=False
    )
    time_created = Column(
        Time, default=datetime.datetime.now(datetime.UTC), nullable=False
    )
    latest_update_date = Column(
        Date, default=datetime.datetime.now(datetime.UTC), nullable=False
    )
    latest_update_time = Column(
        Time, default=datetime.datetime.now(datetime.UTC), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Define the relationship to User
    user = relationship("User", back_populates="reminders")

    # Define the relationship to AdminReminder
    admin_reminders = relationship("AdminReminder", back_populates="reminder")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # Define the relationship to AdminReminder
    admin_reminders = relationship("AdminReminder", back_populates="admin")


class AdminReminder(Base):
    __tablename__ = "admin_reminders"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    due_date = Column(Date, nullable=False)
    due_time = Column(Time, nullable=False)
    date_created = Column(
        Date, default=datetime.datetime.now(datetime.UTC), nullable=False
    )
    time_created = Column(
        Time, default=datetime.datetime.now(datetime.UTC), nullable=False
    )
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)

    reminder_id = Column(Integer, ForeignKey("reminders.id"))

    # Define the relationship to Admin
    admin = relationship("Admin", back_populates="admin_reminders")

    # Define the relationship to Reminder
    reminder = relationship("Reminder", back_populates="admin_reminders")


class AdminTask(Base):
    __tablename__ = "admin_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    due_date = Column(Date, nullable=False)
    due_time = Column(Time, nullable=False)
    date_created = Column(
        Date, default=datetime.datetime.now(datetime.UTC), nullable=False
    )
    time_created = Column(
        Time, default=datetime.datetime.now(datetime.UTC), nullable=False
    )
    admin_id = Column(Integer, ForeignKey("admins.id"), nullable=False)

    # Define the many-to-many relationship to User
    users = relationship(
        "User", secondary=task_user_association, back_populates="tasks"
    )
