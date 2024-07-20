import streamlit as st
from display.reminders import show_reminders, show_admin_reminders, show_admin_tasks
from display.create_reminder import (
    create_reminder,
    create_admin_reminder,
    create_admin_task,
)
from auth.login import login_user, login_admin
from auth.register import register_user
from database.db_operations import get_user, get_admin


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


def get_userid(username):
    user = get_user(username)
    if user is not None:
        return user.id


def get_adminid(name):
    admin = get_admin(name)
    if admin is not None:
        return admin.id


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


def show_logged_in():
    username = st.session_state["username"]
    user_id = get_userid(username)

    options = ["Reminders", "Create Reminder"]
    st.sidebar.title("MindME")
    navigation = st.sidebar.radio("Navigation", options)

    if st.sidebar.button("Logout"):
        st.session_state.pop("username")
        st.rerun()
    elif navigation == "Reminders":
        show_reminders(user_id)
    elif navigation == "Create Reminder":
        create_reminder(user_id)


def show_admin():
    with st.form("admin_login_form"):
        name = st.text_input("Admin Name")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if login_admin(name, password):
                st.success("Logged in successfully.")
                st.session_state["admin"] = name
                st.rerun()
            else:
                st.error("Invalid credentials.")


def show_admin_logged():
    name = st.session_state["admin"]
    id = get_adminid(name)

    options = ["Reminders", "Create Reminder", "Create Task", "Tasks"]
    st.sidebar.title("MindME")
    navigation = st.sidebar.radio("Navigation", options)

    if st.sidebar.button("Logout"):
        st.session_state.pop("admin")
        st.rerun()
    elif navigation == "Reminders":
        show_admin_reminders(id)
    elif navigation == "Create Reminder":
        create_admin_reminder(id)
    elif navigation == "Create Task":
        create_admin_task(id)
    elif navigation == "Tasks":
        show_admin_tasks(id)


def home():
    if "username" in st.session_state:
        username = st.session_state["username"]
        st.title(f"Welcome {username}!")
        show_logged_in()
    elif "admin" in st.session_state:
        st.title("Admin")
        show_admin_logged()
    else:
        option = st.selectbox("Login/Register", ["Login", "Register", "Login as Admin"])
        if option == "Login":
            show_login()
        elif option == "Register":
            registered = show_register()
            if registered:
                st.success("Registered successfully. Please login.")
            else:
                st.error("Registration failed.")
        elif option == "Login as Admin":
            show_admin()


if __name__ == "__main__":
    home()
