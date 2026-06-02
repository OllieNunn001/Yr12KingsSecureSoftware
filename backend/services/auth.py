from classes.User import User
from classes.Error import InputError, AccessError
from database.data import load_users, save_users
import re

def auth_register_user(email, password, name):
    """Service func - registers and stores user on backend"""

    user_dict = load_users()
    # TODO: Implement input validation for email, password, and name

    if not isinstance(email, str) or not isinstance(password, str) or not isinstance(name, str):
        raise InputError("Email, password, and name must be strings")

    # Trim and normalise email
    email = email.strip()
    if email == "":
        raise InputError("Email cannot be empty")
    

    # Validate email format: must have local@domain.tld
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        raise InputError("Invalid email format")
    
    if email[0] == "@":
        raise InputError("Invalid email format")

    name = name.strip()
    if name == "":
        raise InputError("Name cannot be empty")
    
    if len(name) < 2 or len(name) > 50: # Name length requirement
        raise InputError("Name must be between 2 and 50 characters long")
    
    
    # Check if email already exists
    email = email.lower() # Normalise email to lowercase for uniqueness
    if email in user_dict:
        raise InputError("Email already exists")

    # Password strength checks
    if not check_password_strength(password):
        raise InputError("Password does not meet strength requirements")
    
    # Register the user
    new_user_instance = User(email, name, password)
    user_dict[email] = new_user_instance

    # init user session
    session_token = new_user_instance.initiate_user_session()
    # TODO: Generate and return CSRF token
    #csrf_token = 
    save_users(user_dict)

    return session_token

def auth_login_user(email, password):
    """Service func - logins user if valid email & password"""
    # TODO: Implement input validation for email and password

    email = email.strip()
    if email == "":
        raise InputError("Email and password cannot be empty")
    
    # Validate email format: must have local@domain.tld
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        raise InputError("Invalid email format")

    # validate user if in database
    user_dict = load_users()
    if email not in user_dict or not user_dict[email].verify_password(password):
        raise AccessError("Invalid email or password")

    session_token = user_dict[email].initiate_user_session()
    # TODO: Generate and return CSRF token
    save_users(user_dict)

    return session_token

def auth_logout_user(session_token):
    """Service func - revokes a user session via token"""
    user_dict = load_users()
    for user in user_dict.values():
        if user.session_token == session_token:
            user.revoke_user_session()

    save_users(user_dict)

def check_password_strength(password):
    """Helper func - checks password strength requirements"""
    password = password.strip()
    if len(password) < 8: # Minimum length requirement
        return False
    if len(password) > 60: # Limit to prevent DoS with extremely long passwords
        return False
    if re.search(r"\s", password): # No whitespace allowed
        return False
    # Require at least one uppercase, one lowercase, one digit, one special char
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[^A-Za-z0-9]", password):
        return False
    return True