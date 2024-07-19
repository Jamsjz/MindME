from datetime import date
import streamlit as st
from database.db_operations import add_reminder


def create_reminder(user_id):
    st.title("Create a New Reminder")
    title = st.text_input("Title")
    description = st.text_area("Description")
    due_date = st.date_input("Due Date")
    due_time = st.time_input("Due Time")
    if st.button("Create Reminder"):
        if isinstance(due_date, date):
            add_reminder(title, description, due_date, due_time, user_id)
            st.success("Reminder created successfully.")
