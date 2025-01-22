from app import db, logging

class BaseRepository:
    def __init__(self, model) -> None:
        self.model = model
    def create_record_without_commit(self, record):
        try:
            logging.debug(f'Entered create record without commit method in repo for {self.model}')
            db.session.add(record)
            logging.debug(f'Partially created record: {vars(record)}')
            return True, record
        except Exception as e:
            logging.error(f'An Error occurred when adding a record to {self.model}; Error: {str(e)}')
            return False, None
    def create_record(self, record):
        try:
            logging.debug(f'Entered create record method in repo for {self.model}')
            db.session.add(record)
            db.session.commit()
            logging.debug(f'Successfully created record: {vars(record)}')
            return True, record
        except Exception as e:
            logging.error(f'An Error occurred when adding a record to {self.model}; Error: {str(e)}')
            return False, None
    def get_all_records(self):
        logging.debug(f'entered the get all records method in repo for: {self.model}')
        try:
            return self.model.query.all()
        except Exception as e:
            logging.error(f'Error getting all {self.model} records; Error: {str(e)}')
            return None
    def get_record_by_id(self, id):
        logging.debug(f'Entered get record by id for {self.model} with id {id}')
        try:
            return self.model.query.get(id)
        except Exception as e:
            logging.error(f'Error when fetching record: {id} from {self.model}; Error: {str(e)}')
            return None
    def update_record(self, id, **kwargs):
        logging.info(f'Entered Update record method for {self.model} for record: {id}')
        try:
            record = self.get_record_by_id(id)
            if record:
                for key, value in kwargs.items():
                    if value is not None:
                        setattr(record, key, value)
                db.session.commit()
                return True
            
            else:
                return False
        
        except Exception as e:
            logging.error(f'An Error occurred when attempting to update record: {str(e)}')
            return False
    def delete_record(self, id, record):
        logging.info(f'Entered delete record method for {id} and record:{record}')
        response = False
        try:
            record_to_delete = None
            logging.info(f'in try block')
            if not record:
                record_to_delete = self.get_record_by_id(id)
            else:
                record_to_delete = record
            logging.info(f'record to be deleted: {vars(record_to_delete)}')
            if record_to_delete:
                db.session.delete(record_to_delete)
                db.session.commit()
                response = True
        except Exception as e:
            logging.error(f'An error occurred when attempting to delete record: {e}')
        return response