from flask import Blueprint, request, session, flash, url_for
from app.dto import Promotion, APIResponse, conver_json_to_class, create_objects_from_form_data
from app.services.promotion_service import create_new_promotion, update_record
from app.services.dynamic_content_service import create_new_dynamic_content, create_new_theme_content, update_dynamic_content, update_theme
from app.services.promotion_winners_service import generate_promotion_winner, submit_promotion,create_winner_badge
from app.services.file_service import process_import_db
from app import logging
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_user, logout_user, login_required, current_user
from app.error_handlers import role_required

api_bp = Blueprint('api', __name__)

@api_bp.route('/promotion/create', methods=['POST'])
def create():
    response = APIResponse()
    response.data = None
    response.message = 'Unable to create a new promotion'
    response.status_code = 400
    logging.info(f'new create request {request.form} files? {request.files}')
    try:
        promotion, dynamic_content, theme = create_objects_from_form_data(request.form, request.files)
        if promotion is not None:
            isSuccess, record = create_new_promotion(promotion)
            if isSuccess:
                logging.info(f"successfully created promotion: {record} with id{record['id']}")
                response.data = record
                response.message = 'partially created new promotion'
                response.status_code = 202
                dynamic_content.promotion_id = record['id']
                logging.info(f'updating dynamic content with promotion: {vars(dynamic_content)}')
                dyn_Success, dyn = create_new_dynamic_content(dynamic_content)
                logging.info(f'created dyn: {dyn_Success}, {dyn}')
                if dyn_Success:
                    response.data = record
                    response.message = 'partially created new promotion'
                    response.status_code = 202
                    theme.dpc_id = dyn['id']
                    theme_Success, theme_record = create_new_theme_content(theme)
                    if theme_Success:                        
                        response.data = record
                        response.message = 'Successfully created new promotion'
                        response.status_code = 201
    except Exception as e:
        logging.error(f'An error occurred when attempting to call the create promotion endpoint: {vars(e)}')
        response.data = None
        response.message ='An error occurred when attempting to create the promotion; Please contact the administrator'
        response.status_code = 500
    return response.make_response()
@api_bp.route('/promotion/modify', methods=['PUT'])
def modify():
    response = APIResponse()
    try:
        promotion, dynamic_content, theme = create_objects_from_form_data(request.form, request.files)
        if promotion is not None:
            isSuccess = update_record(promotion)
            if isSuccess:
                logging.info(f'successfully updated promotion:  with id{promotion.promo_id}')
                response.data = None
                response.message = 'partially updated promotion'
                response.status_code = 202
                # dynamic_content.promotion_id = record['id']
                logging.info(f'updating dynamic content with promotion: {vars(dynamic_content)}')
                dyn_Success = update_dynamic_content(dynamic_content)
                logging.info(f'created dyn: {dyn_Success}')
                if dyn_Success:
                    response.data = None
                    response.message = 'partially updated promotion'
                    response.status_code = 202
                    # theme.dpc_id = dyn['id']
                    theme_Success = update_theme(theme)
                    if theme_Success:                        
                        response.data = None
                        response.message = 'Successfully updated promotion'
                        response.status_code = 201
    except Exception as e:
        logging.error(f'An error occurred when attempting to call the update promotion endpoint: {vars(e)}')
        response.data = None
        response.message ='An error occurred when attempting to update the promotion; Please contact the administrator'
        response.status_code = 500
    return response.make_response()

@api_bp.route('/promotion/select-winners', methods=['POST'])
def select_winner():
    response = APIResponse()
    response.data = None
    response.message = 'Unable to create a new promotion'
    response.status_code = 400
    logging.info(f'new select winner method')
    try:
        data = request.get_json()
        logging.info(f'json result from request: {data}')
        promotion_id = data['id']
        promotion_winner_count = data['num_of_winners']
        if generate_promotion_winner(promotion_id, promotion_winner_count):
            response.data = None
            response.message = 'Winners selected for promotion'
            response.status_code = 200
        else:
            response.data = None
            response.message = 'No winners generated; check if winners already exists'
            response.status_code = 400
    except Exception as e:
        logging.error(f'An error has occurred when attempting to select winners; {e}')
    return response.make_response()
@api_bp.route('/promotion/submit', methods=['POST'])
def submit():
    logging.info('entered the promotion submission api')
    response = APIResponse()
    response.data = None
    response.message = 'Unable to create a new promotion'
    response.status_code = 400
    try:
        success, errors, message = submit_promotion(request)
        logging.info(f'after service call: {success} {errors} {message}')
        if errors:
            flash('Failed to submi', 'warning')
            logging.info(f'some errors were returned: {errors}')
            response.message = errors
            response.status_code = 400
        elif success:
            email = request.form.get('email')
            session['email'] = email
            response.status_code = 200
            message['guidelines']=f"{url_for('promotions.get_promotion_by_id', id=message['id'])}#accordionFooter"
            message['submissions']=f"{url_for('promotions.user_submission_email', email=email)}"
            response.message = render_template('email_template.html', message=message)
        
    except Exception as e:
         logging.error(f'An error has occurred when attempting to submit; {e}')
    return response.make_response()
@api_bp.route('/promotion/archive', methods=['POST'])
def archive():
    logging.info('entered the promotion archive api')
    response = APIResponse()
    response.data = None
    response.message = 'Unable to archive submission'
    response.status_code = 400
    try:
        logging.info('attempting to archive entry')
        data = request.get_json()
        logging.info(f'json data: {data}')
        if archive_entry(data['entryId']) :
            response.message = 'entry archived'
            response.status_code = 200
    except Exception as e:
        logging.error(f'Error when attempting to archive entry: {e}')
        response.message='Please contact adminstrator'
        response.status_code = 500
    return response.make_response()

@api_bp.route('/promotion/set-badge', methods=['POST'])
def set_winner_badge():
    logging.info('entered the set winner badge api')
    response = APIResponse()
    response.data = None
    response.message = 'Unable to set winner badge'
    response.status_code = 400
    try:
        logging.info('attempting to set winner badge')
        data = request.get_json()
        winner_id = data.get('winner_id')
        badge_name = data.get('badge_name', '')  # Default to an empty string if not provided
        badge_desc = data.get('badge_desc', '')
        logging.info(f'json data: {data}')
        if create_winner_badge(winner_id, badge_name, badge_desc):
            response.message = 'winner badge set'
            response.status_code = 200
    except Exception as e:
        logging.error(f'Error when attempting to set winner badge: {e}')
        response.message='Please contact adminstrator'
        response.status_code = 500
    return response.make_response()
@api_bp.route('/import', methods=['Post'])
@role_required('admin,manage')
@login_required
def import_database():
    response = APIResponse()
    file = request.files['file']
    result = process_import_db(file)
    if result:
        response.message = 'winner badge set'
        response.status_code = 200
    else:
        response.message='Please contact adminstrator'
        response.status_code = 500
    return response.make_response()