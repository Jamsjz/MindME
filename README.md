# MindME

MindME is a Web Application for managing your reminders.

It is a simple web application that allows you to create, edit and delete reminders.

Each User has an account:

Users:

- username --> unique
- password --> hashed, min length 8, must contain at least one number, one uppercase letter, one lowercase letter and one special character
- email --> unique + validated

The user are able to create a new account or login with their existing account.

This app uses postgresql as database with alchemysql for the ORM The credentials are stored in a config.json file.
This app uses streamlit for the frontend.


The reminders are stored in a table -> reminders
Reminders:
- id --> primary key, unique
- title
- description
- due_date
- due_time
- date_created
- time_created
- latest_update_date
- latest_update_time
- user_id --> foreign key to users table

## Installation
### VENV
Create a virtual environment and install the dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
```

### Dependencies
Install the dependencies:
```bash
pip install -r requirements.txt
```

### Database
Create the database:
```bash
createdb mindme
```

### Config
Copy the config.json.example to MineME/config.json and fill in the values.


## Dependencies

Install the dependencies:

- postgresql
- streamlit
- alchemysql
- flask
