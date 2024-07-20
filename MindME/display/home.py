import streamlit as st
from display.reminders import show_reminders, show_admin_reminders, show_admin_tasks
from display.create_reminder import (
    create_reminder,
    create_admin_reminder,
    create_admin_task,
)
from auth.login import login_user, login_admin
from auth.register import register_user
from database.db_operations import get_user, get_admin, Session, User, Reminder
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Authentication and User Management Functions
def show_login():
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if login_user(username, password):
                st.success("Logged in successfully.")
                st.session_state["username"] = username
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")


def show_register():
    with st.form("register"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Register"):
            message = register_user(username, password, email)
            if "successfully" in message:
                st.success(message)
                return True
            elif "already" in message:
                st.error(message)
                return False
            else:
                st.error(message)
                return False


def show_admin_login():
    with st.form("admin_login_form"):
        name = st.text_input("Admin Name")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if login_admin(name, password):
                st.success("Logged in successfully.")
                st.session_state["admin"] = name
                st.experimental_rerun()
            else:
                st.error("Invalid credentials.")


# Database Operations
def get_userid(username):
    user = get_user(username)
    if user is not None:
        return user.id


def get_adminid(name):
    admin = get_admin(name)
    if admin is not None:
        return admin.id


def delete_user(id):
    session = Session()
    try:
        user = session.query(User).get(id)
        if user:
            reminders = session.query(Reminder).filter(Reminder.user_id == id).all()
            for reminder in reminders:
                session.delete(reminder)
            session.delete(user)
            session.commit()
            st.success("User and associated reminders deleted successfully.")
            return True
        else:
            st.error("User not found.")
            return False
    except Exception as e:
        logger.error(f"An error occurred while deleting user: {str(e)}")
        session.rollback()
        st.error("Failed to delete user. Please try again.")
        return False
    finally:
        session.close()


def show_users():
    session = Session()
    try:
        users = session.query(User).all()
        if users:
            user_data = [
                {"ID": user.id, "Username": user.username, "Email": user.email}
                for user in users
            ]
            st.table(user_data)
        else:
            st.write("No users found.")
    except Exception as e:
        logger.error(f"An error occurred while fetching users: {str(e)}")
        st.error("Failed to fetch users.")
    finally:
        session.close()


# User and Admin Views
def show_logged_in():
    username = st.session_state["username"]
    user_id = get_userid(username)
    options = ["Reminders", "Create Reminder"]
    st.sidebar.title("MindME")
    navigation = st.sidebar.radio("Navigation", options)
    if st.sidebar.button("Logout"):
        st.session_state.pop("username")
        st.experimental_rerun()
    elif navigation == "Reminders":
        show_reminders(user_id)
    elif navigation == "Create Reminder":
        create_reminder(user_id)


def show_admin_logged_in():
    admin_name = st.session_state["admin"]
    admin_id = get_adminid(admin_name)
    options = [
        "Reminders",
        "Create Reminder",
        "Create Task",
        "Tasks",
        "Delete User",
        "Add User",
    ]
    st.sidebar.title("MindME")
    navigation = st.sidebar.radio("Navigation", options)
    if st.sidebar.button("Logout"):
        st.session_state.pop("admin")
        st.experimental_rerun()
    elif navigation == "Reminders":
        show_admin_reminders(admin_id)
    elif navigation == "Create Reminder":
        create_admin_reminder(admin_id)
    elif navigation == "Create Task":
        create_admin_task(admin_id)
    elif navigation == "Tasks":
        show_admin_tasks(admin_id)
    elif navigation == "Delete User":
        show_users()
        user_id = st.number_input("User ID", min_value=1)
        user_id = int(user_id)
        if st.button("Delete User"):
            if delete_user(user_id):
                st.success("User deleted successfully.")
                st.experimental_rerun()
            else:
                st.error("Failed to delete user.")
    elif navigation == "Add User":
        show_register()


# Main Application
def home():
    if "username" in st.session_state:
        st.title(f"Welcome {st.session_state['username']}!")
        show_logged_in()
    elif "admin" in st.session_state:
        st.title("Admin Dashboard")
        show_admin_logged_in()
    else:
        option = st.selectbox("Login/Register", ["Login", "Register", "Login as Admin"])
        if option == "Login":
            show_login()
        elif option == "Register":
            if show_register():
                st.success("Registered successfully. Please login.")
            else:
                st.error("Registration failed.")
        elif option == "Login as Admin":
            show_admin_login()


if __name__ == "__main__":
    home()
