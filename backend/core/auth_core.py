from database.data import load_users, save_users
from classes.Error import InputError


def authorise_user(session_token, csrf_token):
    """Authorises user IFF a valid session token exsist"""
    # TODO: Implement session token validation
    user_dict = load_users()
    if not isinstance(session_token, str):# or not isinstance(csrf_token, str):
        return False
    if session_token.strip() == "":# or csrf_token.strip() == "":
        return False
    # TODO: Implement CSRF token validation
    # 
    # TODO: Check both tokens match a valid user session
    for user in user_dict.values():
        if user.session_token == session_token:# and user.csrf_token == csrf_token:
            return True
    return False


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
