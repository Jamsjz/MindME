from sqlalchemy import Column, Integer, String, Text, ForeignKey, Time, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)


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

    user = relationship("User", back_populates="reminders")


User.reminders = relationship("Reminder", order_by=Reminder.id, back_populates="user")
