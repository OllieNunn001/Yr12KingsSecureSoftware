from classes.User import User
from classes.Error import InputError, AccessError
from database.data import load_users, save_users
import re

def auth_register_user(email, password, name):
    """Service func - registers and stores user on backend"""

    user_dict = load_users()
    # TODO: Implement input validation for email, password, and name
    
    # Check if email already exists
    if email in user_dict:
        raise InputError("Email already exists")

    # TODO: Implement password strength requirements (length, complexity)

    if len(password) < 8:
        raise InputError("Password must be at least 8 characters long")
    
    if password.isdigit() or password.isalpha():
        raise InputError("Password must have both letters and numbers")
    
    # Register the user
    new_user_instance = User(email, name, password)
    user_dict[email] = new_user_instance

    # init user session
    session_token = new_user_instance.initiate_user_session()
    # TODO: Generate and return CSRF token
    save_users(user_dict)

    return session_token

def auth_login_user(email, password):
    """Service func - logins user if valid email & password"""
    # TODO: Implement input validation for email and password
    
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
