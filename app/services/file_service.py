import os
from app import logging, db
from app.app_config import Config
import io
import app.templates
from sqlalchemy import text
import sqlparse
import re

def save_file(file, root_location, path=None):
    file_name = None
    file_path = None
    upload_path = root_location
    try:
        if file is not None and file.filename != '':
            file_name = file.filename
            file_path = os.path.join(os.path.abspath(upload_path), file.filename)
            if path:
                file.save(path)
                file_path=path
            else:
                file.save(file_path)
    except Exception as e:
        logging.error(f'error saving file: {e}')
        file_name = None
        file_path = None
    logging.info(f'File saved: {file_name} and {file_path} and def path:{path}')
    return file_name, file_path

def does_tempalte_exist(promotion_name):
    does_exist, template = False, None
    try:
        template_name = promotion_name.replace(" ", "") + '.html'
        template_path = os.path.join(os.path.abspath('app/templates'), template_name)
        if os.path.exists(template_path):
            does_exist = True
            template = template_name
        logging.info(f'does template exist? {does_exist} template name: {template} attempted name: {template_name} tempalte path: {template_path}')
    except:
        logging.error(f'An error occurred when attempting to get template')
    return does_exist, template

def export_db():
    temp_file = None
    buffer = io.StringIO()
    try:
        logging.info(f"got db_path: {Config.settings}")
        engine = db.get_engine()
        
        with engine.connect() as connection:
            with connection.begin():
                for line in connection.connection.iterdump():
                    buffer.write(f"{line}\n")
        buffer.seek(0)
    except Exception as e:
        logging.error(f"An error occurred when attempting to export data: {e}")
    return buffer
def import_db(sql_file):
    isSuccess = False
    try:
        if not os.path.exists(sql_file):
            raise Exception("file doesn't exist")
        with open(sql_file, 'r', encoding='utf-8') as file:
            # sql_script = text(file.read())
            sql_script = file.read()
            sql_script = sql_script.replace("\t", "")  # Replace tab characters
            sql_script = sql_script.replace("\n", "")  # Replace new lines
            sql_script = sql_script.replace("\r", "")  # Replace carriage returns
            

        with db.engine.connect() as connection:
            with connection.begin():
                # connection.execute(sql_script)
                # isSuccess = True
                statements = sqlparse.split(sql_script)
                # statements = re.split(r';\s*(?=[^"]*(?:"[^"]*"[^"]*)*$)', sql_script)
                for statement in statements:
                    statement = statement.strip()
                    if statement:
                        try:
                            connection.execute(text(statement))
                        except Exception as e:
                            logging.error(f'error executing error: {e}')
                isSuccess = True
                
    except Exception as e:
        logging.error(f"Error occurred when attempting to import sql file: {e}")
    return isSuccess
def process_import_db(file):
    response = False
    temp_file_path = None
    logging.info('entered method to process uploaded file')
    try:
        if file.filename == '':
            raise Exception("No file selected")
        if not file.filename.endswith('.sql'):
            raise Exception("Invalid file type. Only .sql files are allowed")
        temp_file_path = os.path.join('app/tmp',  file.filename)
        temp_file_path = os.path.join(os.path.abspath('tmp'), file.filename)
        file.save(temp_file_path)
        response = import_db(temp_file_path)
        os.remove(temp_file_path)
    except Exception as e:
        logging.error(f"An error occurred when attempting to process the sql file import; {e}")
        try:
            os.remove(temp_file_path)
        except:
            logging.error(f"error trying to clean up file")
    return response
