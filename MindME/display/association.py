import streamlit as st
from database.db_operations import Session, AdminTask, User
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def associate_users_with_task(task_id, selected_usernames):
    logger.info(f"Associating users for task {task_id}")
    logger.info(f"Selected usernames: {selected_usernames}")
    session = Session()
    try:
        task = session.query(AdminTask).filter_by(id=task_id).one()
        logger.info(
            f"Current users for task {task_id}: {[user.username for user in task.users]}"
        )

        # Clear existing associations
        task.users.clear()
        logger.info(f"Cleared existing associations for task {task_id}")

        # Add new associations
        for username in selected_usernames:
            user = session.query(User).filter_by(username=username).one()
            if user not in task.users:
                task.users.append(user)
                logger.info(f"Added user {username} to task {task_id}")

        session.commit()
        logger.info(f"Successfully associated users for task {task_id}")
        logger.info(
            f"New users for task {task_id}: {[user.username for user in task.users]}"
        )
        return True
    except Exception as e:
        logger.error(f"An error occurred while associating users: {str(e)}")
        session.rollback()
        return False
    finally:
        session.close()


def get_current_associations(task_id):
    session = Session()
    try:
        task = session.query(AdminTask).filter_by(id=task_id).one()
        return [user.username for user in task.users]
    finally:
        session.close()


def show_associate_users_form(task_id):
    logger.info(f"Displaying associate users form for task {task_id}")

    st.subheader("Associate Users")

    session = Session()
    all_users = session.query(User).all()
    session.close()

    selected_usernames = handle_user_selection(task_id, all_users)

    if st.button("Associate Selected Users", key=f"associate_button_{task_id}"):
        logger.info(f"Associate button clicked for task {task_id}")
        logger.info(f"Selected usernames: {selected_usernames}")
        if associate_users_with_task(task_id, selected_usernames):
            st.success("Users associated successfully.")
            st.write(f"Associated users: {get_current_associations(task_id)}")
            # Force a rerun of the app
            st.rerun()
        else:
            st.error("Failed to associate users. Please try again.")
            st.write(f"Current associations: {get_current_associations(task_id)}")


def handle_user_selection(task_id, all_users):
    user_selection_key = f"user_selection_{task_id}"

    if user_selection_key not in st.session_state:
        st.session_state[user_selection_key] = get_current_associations(task_id)

    select_all = st.checkbox("Select All Users", key=f"select_all_{task_id}")

    if select_all:
        selected_usernames = [user.username for user in all_users]
    else:
        selected_usernames = st.multiselect(
            "Select Users to Associate",
            options=[user.username for user in all_users],
            default=st.session_state[user_selection_key],
            key=f"multiselect_{task_id}",
        )

    logger.info(f"Selected usernames: {selected_usernames}")
    st.session_state[user_selection_key] = selected_usernames
    return selected_usernames


def display_current_associations(task_id):
    st.write("Currently associated users:")
    current_associations = get_current_associations(task_id)
    for username in current_associations:
        st.write(f"- {username}")


def show_associate_users(task_id):
    logger.info(f"Showing associate users form for task {task_id}")
    st.write(
        f"Current session state for task {task_id}: {st.session_state.get(f'user_selection_{task_id}', 'Not set')}"
    )
    show_associate_users_form(task_id)


def show_admin_task(task_id):
    session = Session()
    try:
        task = session.query(AdminTask).filter_by(id=task_id).one()
        st.subheader(task.title)
        st.write(task.description)
        st.write(f"Due: {task.due_date} at {task.due_time}")

        st.write("Associated Users:")
        if task.users:
            user_data = [
                {"Username": user.username, "Email": user.email} for user in task.users
            ]
            st.table(user_data)
        else:
            st.write("No users associated with this task.")
    finally:
        session.close()
