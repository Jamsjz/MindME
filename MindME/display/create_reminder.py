from datetime import date
import streamlit as st
from database.db_operations import add_reminder, add_admin_reminder, add_admin_task


def create_reminder(user_id):
    st.title("Create a New Reminder")
    title = st.text_input("Title")
    description = st.text_area("Description")
    due_date = st.date_input("Due Date", min_value=date.today())
    due_time = st.time_input("Due Time", step=60)
    if st.button("Create Reminder"):
        if isinstance(due_date, date):
            add_reminder(title, description, due_date, due_time, user_id)
            st.success("Reminder created successfully.")
            st.rerun()


def create_admin_reminder(user_id):
    st.title("Create a New Reminder")
    title = st.text_input("Title")
    description = st.text_area("Description")
    due_date = st.date_input("Due Date", min_value=date.today())
    due_time = st.time_input("Due Time", step=60)
    if st.button("Create Reminder"):
        if isinstance(due_date, date):
            add_admin_reminder(title, description, due_date, due_time, user_id)
            st.success("Reminder created successfully.")
            st.rerun()


def create_admin_task(id):
    st.title("Create a New Task")
    title = st.text_input("Title")
    description = st.text_area("Description")
    due_date = st.date_input("Due Date", min_value=date.today())
    due_time = st.time_input("Due Time", step=60)
    if st.button("Create Task"):
        if isinstance(due_date, date):
            add_admin_task(title, description, due_date, due_time, id)
            st.success("Reminder created successfully.")
            st.rerun()
