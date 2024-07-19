import streamlit as st
from database.db_operations import delete_reminder


def delete_reminder_view():
    st.title("Delete Reminder")
    reminder_id = st.text_input("Reminder ID")
    if st.button("Delete Reminder"):
        delete_reminder(reminder_id)
        st.success("Reminder deleted successfully.")
