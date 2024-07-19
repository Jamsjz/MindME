import streamlit as st
from display.home import home
from database.db_operations import create_tables

create_tables()


def main():
    st.set_page_config(page_title="MindME", page_icon="🧠", layout="wide")
    st.sidebar.title("MindME")
    home()


if __name__ == "__main__":
    main()
