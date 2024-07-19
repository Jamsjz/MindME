import streamlit as st
from database.db_operations import Session, Reminder


def show_reminders(user_id):
    session = Session()
    reminders = session.query(Reminder).filter_by(user_id=user_id).all()
    session.close()
    st.title("Your Reminders")
    for reminder in reminders:
        st.subheader(reminder.title)
        st.write(reminder.description)
        st.write(f"Due: {reminder.due_date} at {reminder.due_time}")
        st.write(
            f"Last updated: {reminder.latest_update_date} at {reminder.latest_update_time}"
        )
