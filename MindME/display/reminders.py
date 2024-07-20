import streamlit as st
from .association import (
    show_associate_users_form,
    show_admin_task,
)
from database.db_operations import (
    Session,
    Reminder,
    AdminReminder,
    AdminTask,
    delete_reminder as dreminder,
    delete_admin_reminder as dadminreminder,
)
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    st.experimental_rerun()


def show_admin_reminder(reminder):
    st.subheader(reminder.title)
    st.write(reminder.description)
    st.write(f"Due: {reminder.due_date} at {reminder.due_time}")


def delete_admin_reminder(reminder):
    dadminreminder(reminder.id)
    st.success("Reminder deleted successfully.")
    st.experimental_rerun()


def show_admin_tasks(id):
    logger.info(f"Showing admin tasks for admin id {id}")
    session = Session()
    tasks = session.query(AdminTask).filter_by(admin_id=id).all()
    session.close()

    st.subheader("Your Tasks")
    if len(tasks) > 0:
        for task in tasks:
            col1, col2 = st.columns([3, 1])
            with col1:
                show_admin_task(task.id)
            with col2:
                if st.button("Delete", key=f"delete_admin_task_{task.id}"):
                    delete_admin_task(task.id)

            show_associate_users_form(task.id)
            st.markdown("---")  # Add a separator between tasks
    else:
        st.write("You have no tasks. Create one through the 'Create Task' button.")


def delete_admin_task(task_id):
    session = Session()
    try:
        task = session.query(AdminTask).filter_by(id=task_id).one()
        session.delete(task)
        session.commit()
        st.success("Task deleted successfully.")
        st.rerun()
    except Exception as e:
        logger.error(f"An error occurred while deleting task: {str(e)}")
        session.rollback()
        st.error("Failed to delete task. Please try again.")
    finally:
        session.close()


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
                if st.button("Delete", key=f"delete_reminder_{reminder.id}"):
                    delete_reminder(reminder)
    else:
        st.write(
            "You have no reminders.\nCreate one through the 'Create Reminder' button."
        )


def show_admin_reminders(admin_id):
    session = Session()
    reminders = session.query(AdminReminder).filter_by(admin_id=admin_id).all()
    st.subheader("Your Reminders")
    if len(reminders) > 0:
        for reminder in reminders:
            col1, col2 = st.columns([4, 1])
            with col1:
                show_admin_reminder(reminder)

            with col2:
                if st.button("Delete", key=f"delete_admin_reminder_{reminder.id}"):
                    delete_admin_reminder(reminder)
    else:
        st.write(
            "You have no reminders.\nCreate one through the 'Create Reminder' button."
        )
