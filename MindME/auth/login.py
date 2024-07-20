from database.db_operations import get_user, get_admin
import bcrypt


def login_user(username, password):
    user = get_user(username)
    if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return True
    return False


def login_admin(name, password):
    admin = get_admin(name)
    if admin and bcrypt.checkpw(
        password.encode("utf-8"), admin.password.encode("utf-8")
    ):
        return True
    return False
