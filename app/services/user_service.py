from app.database.models.models import Users
from app.database.user_repository import UserRepository
from app import logging
def register_user(email, roles, password):
    response, Message = False, ''
    repo = UserRepository(Users)
    try:
        if repo.get_by_email(email):
            Message = 'Email already exists!'
            response = False
        else:
            new_user = Users(email=email, username=email, role = roles)
            new_user.set_password(password)
            response, record = repo.create_record(new_user)
    except Exception as e:
        logging.error(f'An error occurred when attempting to register user: {e}')
        response = False
        Message = 'Some error occurred; please contact the administrator'
    
    return response, Message
def get_user_by_email(email):
    response = None
    try:
        repo = UserRepository(Users)
        response = repo.get_by_email(email)
    except Exception as e:
        logging.error(f'An error occurred when attempting get user by email: {e}')
    return response