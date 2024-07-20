import re
from database.db_operations import add_user, get_user
import bcrypt
import dns.resolver


def is_valid_email(email):
    # Basic syntax check
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False

    # Domain validation
    domain = email.split("@")[1]
    try:
        dns.resolver.resolve(domain, "MX")
        return True
    except dns.resolver.NoAnswer:
        return False
    except dns.resolver.NXDOMAIN:
        return False
    except dns.resolver.Timeout:
        return False


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
    if not is_valid_email(email):
        return "Invalid email."
    if not validate_password(password):
        return "Password does not meet complexity requirements."
    if not is_valid_email(email) and not validate_password(password):
        return "Invalid email and password."
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    add_user(username, hashed_password.decode("utf-8"), email)
    return "User registered successfully."
