from database.db_operations import get_user
import bcrypt


def login_user(username, password):
    user = get_user(username)
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return True
    return False
