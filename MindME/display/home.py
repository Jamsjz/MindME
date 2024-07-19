import streamlit as st
from display.reminders import show_reminders
from display.create_reminder import create_reminder
from display.edit_reminder import edit_reminder
from display.delete_reminder import delete_reminder_view
from auth.login import login_user
from auth.register import register_user
from database.db_operations import get_user


def show_login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.success("Logged in successfully.")
            st.session_state["username"] = username
            return True
        else:
            st.error("Invalid credentials.")
            return False


def get_userid(username):
    user = get_user(username)


def show_register():
    st.title("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        message = register_user(username, password, email)
        if "successfully" in message:
            st.success(message)
        else:
            st.error(message)


def show_logged_in():
    if st.session_state.username is None:
        main()
    else:
        username = st.session_state.username

        options = ["Home", "Create Reminder"]
        st.sidebar.title("MindME")
        navigation = st.sidebar.radio("Navigation", options)
        if st.sidebar.button("Logout"):
            st.session_state.user_id = None
        elif navigation == "Reminders":
            show_reminders(user_id)
        elif navigation == "Create Reminder":
            create_reminder(user_id)
        elif navigation == "Edit Reminder":
            reminder_id = st.sidebar.text_input("Reminder ID")
            if reminder_id:
                edit_reminder(reminder_id)
        elif navigation == "Delete Reminder":
            delete_reminder_view()


def main():
    if "username" not in st.session_state:
        option = st.selectbox("Login/Register", ["Login", "Register"])
        logged_in = show_login()
        if option == "Login" and logged_in:
            show_logged_in()

        elif logged_in and option == "Register":
            show_register()
        elif option == "Register":
            show_register()

    else:
        main()


if __name__ == "__main__":
    main()
