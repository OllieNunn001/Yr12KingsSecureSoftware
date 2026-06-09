from database.data import load_users, save_users
from classes.Error import InputError


def authorise_user(session_token, csrf_token):
    """Authorises user IFF a valid session token exsist"""
    # TODO: Implement session token validation
    
    # TODO: Implement CSRF token validation
    # TODO: Check both tokens match a valid user session
    return True  # Currently allows all requests


def map_session_token_to_email(target_session_token):
    """func mapping the session token to registered user email"""
    users_dictionary = load_users()
    for email, user_obj in users_dictionary.items():
        if user_obj.session_token == None:
            continue

        if user_obj.session_token == target_session_token:
            return email
    else:
        raise InputError(f"Session token '{target_session_token}' not found")
