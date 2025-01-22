import os
from app import logging
import app.templates
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