import streamlit as st
from database.db_operations import (
    Session,
    Reminder,
    delete_reminder as dreminder,
)


def show_reminder(reminder):
    st.subheader(reminder.title)
    st.write(reminder.description)
    st.write(f"Due: {reminder.due_date} at {reminder.due_time}")
    st.write(
        f"Last updated: {reminder.latest_update_date} at {reminder.latest_update_time}"
    )


def delete_reminder(reminder):
    dreminder(reminder.id)
    st.success("Reminder deleted successfully.")
    st.rerun()


def show_reminders(user_id):
    session = Session()
    reminders = session.query(Reminder).filter_by(user_id=user_id).all()
    st.subheader("Your Reminders")
    if len(reminders) > 0:
        for reminder in reminders:
            col1, col2 = st.columns([4, 1])
            with col1:
                show_reminder(reminder)

            with col2:
                if st.button("Delete"):
                    delete_reminder(reminder)
    else:
        st.write(
            "You have no reminders.\nCreate one through the 'Create Reminder' button."
        )
