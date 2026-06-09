from typing import Optional, Dict, Any
# TODO: Import password hashing library for secure password storage
# TODO: Import library for secure token generation

import werkzeug.security as werkzeug_security  # For password hashing and verification
import secrets  # For secure token generation

class User:
    def __init__(
        self,
        email,
        name,
        password=None,
        password_hash=None,
        session_token=None,
        # TODO: Add CSRF token parameter
        csrf_token=None,
    ):
        """Initialised new user instance."""
        self.__email = email
        self.__name = name

        # __init__() is used for creating a new User instance via cls(...) or manual instantiation
        if password:
            # Hash provided plain-text password
            self.__password = werkzeug_security.generate_password_hash(password)
        elif password_hash:
            # Load existing password hash from storage
            self.__password = password_hash
        else:
            raise ValueError("Either password or password_hash must be provided")

        self.__session_token = session_token
        # TODO: Initialize CSRF token storage
        self.__csrf_token = csrf_token
        # tokens are None - if no user-session

    # private: Generate secure hexadecimal token
    def __generate_token(self):
        # TODO: Implement cryptographically secure token generation
        return secrets.token_hex(16) # Makes a hexadeciaml token with 16 bytes
        #return "insecure_token_" + self.__email

    # public: Init user session
    def initiate_user_session(self):
        # TODO: Generate CSRF token along with session token
        self.__session_token = self.__generate_token()
        return self.__session_token  # TODO: Return CSRF token

    # public: Remove user session
    def revoke_user_session(self):
        self.__session_token = None
        # TODO: Clear CSRF token on session revocation
        self.__csrf_token = None

    # public: Verify password input
    def verify_password(self, password_input):
        # TODO: Implement secure password verification using hashing
        return werkzeug_security.check_password_hash(self.__password, password_input)

    # public: Session Token Property
    @property
    def session_token(self):
        return self.__session_token

    # TODO: Add CSRF token property getter

    # public: mail Property
    @property
    def email(self):
        return self.__email

    # public: Name Property
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @email.setter
    def email(self, new_email):
        self.__email = new_email

    # public: convert fron object -> dict
    def to_dict(self):
        return {
            "email": self.__email,
            "name": self.__name,
            "password_hash": self.__password,
            "session_token": self.__session_token,
            # TODO: Include CSRF token in dictionary
            "csrf_token": self.__csrf_token,
        }

    # public: cls() used in database/data.py to convert JSON -> in-memory user object
    @classmethod
    def from_dict(cls, data):
        return cls(
            email=data["email"],
            name=data["name"],
            password_hash=data["password_hash"],
            session_token=data.get("session_token"),
            # TODO: Load CSRF token from dictionary
            csrf_token=data.get("csrf_token"),
        )
