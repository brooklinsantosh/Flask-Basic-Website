import re

def validate_email(email: str)-> bool:
    """Returns true if the email doesn't maintain the criteria"""
    pattern = r'^[\w\.-]+@[a-zA-Z]+\.[a-zA-Z]+$'
    return re.match(pattern, email) is None

def validate_password(password: str)-> bool:
    """Returns true if the password doesn't maintain the criteria"""
    # Check for at least 1 uppercase letter
    if not re.search(r'[A-Z]', password):
        return True
    # Check for at least 1 lowercase letter
    if not re.search(r'[a-z]', password):
        return True
    # # Check for at least 1 digit
    # if not re.search(r'\d', password):
    #     return True
    # # Check for at least 1 special character
    # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
    #     return True
    return False

