from app.database.base_repository import BaseRepository
from app import logging, db

class UserRepository(BaseRepository):
     def get_by_email(self, email):
        response = None
        logging.debug(f'Attempting to get user by email: {email}')
        try:
           response = self.model.query.filter_by(email=email).first()
        except Exception as e:
            logging.error(f'An error occurred when attempting to get user by email: {e}')
        return response