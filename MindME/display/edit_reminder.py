from datetime import date
import streamlit as st
from database.db_operations import update_reminder, Session, Reminder


def edit_reminder(reminder_id):
    session = Session()
    reminder = session.get(Reminder, reminder_id)
    if reminder is not None and reminder is Reminder:
        st.title("Edit Reminder")
        title = st.text_input("Title", value=reminder.title)
        description = st.text_area("Description", value=reminder.description)
        due_date = st.date_input("Due Date", value=reminder.due_date)
        due_time = st.time_input("Due Time", value=reminder.due_time)
        if st.button("Update Reminder") and isinstance(due_date, date):
            update_reminder(reminder_id, title, description, due_date, due_time)
            st.success("Reminder updated successfully.")
    else:
        st.error("Reminder not found.")
