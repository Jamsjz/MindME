import re
from database.db_operations import add_user, get_user
import bcrypt


def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[\W_]", password):
        return False
    return True


def register_user(username, password, email):
    if get_user(username) is not None:
        return "Username already exists."
    if not validate_password(password):
        return "Password does not meet complexity requirements."
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    add_user(username, hashed_password.decode("utf-8"), email)
    return "User registered successfully."
