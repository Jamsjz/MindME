import streamlit as st
from display.reminders import show_reminders
from display.create_reminder import create_reminder
from auth.login import login_user
from auth.register import register_user
from database.db_operations import get_user


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
        st.experimental_rerun()
    elif navigation == "Reminders":
        show_reminders(user_id)
    elif navigation == "Create Reminder":
        create_reminder(user_id)


def home():
    if "username" in st.session_state:
        username = st.session_state["username"]
        st.title(f"Welcome {username}!")
        show_logged_in()
    else:
        option = st.selectbox("Login/Register", ["Login", "Register"])
        if option == "Login":
            show_login()
        elif option == "Register":
            if show_register():
                st.success("Registered successfully. Please login.")
                show_login()


if __name__ == "__main__":
    home()
