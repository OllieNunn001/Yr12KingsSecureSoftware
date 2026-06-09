from database.data import load_users, save_users
from classes.Error import AccessError,InputError


def authorise_user(session_token, csrf_token):
    """Authorises user IFF a valid session token exsist"""
    # TODO: Implement session token validation
    if not isinstance(session_token, str) or session_token.strip() == "":
        raise AccessError("Invalid session token")
    # TODO: Implement CSRF token validation
    if not isinstance(csrf_token, str) or csrf_token.strip() == "":
        raise AccessError("Invalid CSRF token")
    # TODO: Check both tokens match a valid user session
    user_dict = load_users()
    for user in user_dict.values():
        if user.session_token == session_token:
            return True
    raise AccessError("Invalid session token")


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
