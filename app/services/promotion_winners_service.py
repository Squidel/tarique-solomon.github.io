from app.database.promotions_repository import PromotionSubmissionRepository, BaseRepository, PromotionsRepository, BadgeRepository
from app import logging, db
from app.database.models.models import FormSubmissions, SelectedSubmissions,  BlogPosts,  Badges
import random, uuid, os
from app.helper_funcs import validate_form_data, send_email
from datetime import datetime
from app.services.file_service import save_file
from app.app_config import WINNER_RATIO
def generate_promotion_winner(promo_id, winner_count):
    response = False
    # if no promotion winners were already selected
    repo = BaseRepository(SelectedSubmissions)
    winners = repo.get_all_records()
    logging.info(f'wwinners: {winners} first: {vars(winners[0])}')
    if any(item.promotion_id == int(promo_id) for item in winners):
        logging.info('some winners already exists')
        return False
    participants = get_promotion_participants(promo_id=promo_id)
    if participants:
        # logging.info(f'participants: {participants}')
        winners = select_top_random_submissions(participants=participants, num_winners=int(winner_count))
        logging.info(f'top n winners: {winners}')
        for winner in winners:
            logging.info(f'about to save winner to db: {vars(winner)}')
            orm = SelectedSubmissions(promotion_winner_id=str(uuid.uuid4()),promotion_id=promo_id, reference_number=winner.promotions_submission_references[0].reference_number)
            response, record = repo.create_record(orm)
            if response:
                create_winner_badge(record.promotion_winner_id, 'default', 'default badge generated when generating a winner')
    return response
def get_promotion_participants(promo_id):
    logging.info(f'attempting to get participant information for promotion: {promo_id}')
    response = None
    try:
        repo = PromotionSubmissionRepository(FormSubmissions)
        response = repo.get_submissions_by_promotions(promo_id)        
        # logging.info(f'submissions: {response}')
    except Exception as e:
        logging.error(f'An error occurred when attempting to get participants for promotion: {promo_id}; with error {e}')
    return response

def select_top_random_submissions(participants, num_winners):
    logging.info(f'slicing submissions list by: {num_winners}')
    winner_count = num_winners * WINNER_RATIO
    participants_copy = participants.copy()
    random.shuffle(participants_copy)
    winners = participants_copy[:winner_count]
    return winners
def get_promotion_winners(promotion_id):
    response = {'status': False, 'data': None}
    try:
        repo = PromotionsRepository(SelectedSubmissions)
        winners = repo.get_promotion_winners(promotion_id)
        logging.info(f'wwinners: {winners}, first object: {vars(winners[0])}')
        winner_obj = [{'full_name': f"{item.promotions_submission_references.form_submission.first_name} {item.promotions_submission_references.form_submission.last_name}", "reference_number":f"{item.reference_number}", "image":f"{item.promotions_submission_references.form_submission.image}", "email":f"{item.promotions_submission_references.form_submission.email_addr}", "mobile":f"{item.promotions_submission_references.form_submission.phone_num}", "badge":get_winner_badge(item.promotion_winner_id), "id":f"{item.promotion_winner_id}"} for item in winners ]
        logging.info(f'winner object: {winner_obj}')
        # Initialize dictionary to store winners in three draws
        winners_sorted_and_split = {
            'first_draw': [],
            'second_draw': [],
            'third_draw': []
        }
        test = []
        if WINNER_RATIO:
            test = split_array(winner_obj, WINNER_RATIO)
        if test:
            winners_sorted_and_split['first_draw'] = test[0]
            winners_sorted_and_split['second_draw'] = test[1]

        # # Distribute winners every 6 iterations
        # for i, winner in enumerate(winner_obj):
        #     if i % 18 < 6:
        #         winners_sorted_and_split['first_draw'].append(winner)
        #     elif i % 18 < 12:
        #         winners_sorted_and_split['second_draw'].append(winner)
        #     else:
        #         winners_sorted_and_split['third_draw'].append(winner)

        logging.info(f"Sorted and Split: {winners_sorted_and_split}")
        response['status'] = True
        response['data'] = winners_sorted_and_split
    except Exception as e:
        logging.error(f'Failed to get promotion winners: {e}')
    return response
def submit_promotion(submission):
    response, errors, message = False, None, None
    saved_path = None
    logging.info('entered into the submit promotion method')
    try:
        db.session.begin()
        promo_repo = BaseRepository(BlogPosts)        
        # validate submission (get values from submission)
        logging.info(f'submission: {submission.form}')
        errors, validated_data = validate_form_data(submission)
        if not errors:
            logging.info(f'no errors: {validated_data}')
            promo = promo_repo.get_record_by_id(validated_data['promo_id'])
            logging.info(f'got promotion: {promo}')
            if promo.end_date > datetime.today().date():
                abbrv = promo.abbreviation
                #generate refNumber
                reference_number = '3423423423'#generate_ref(id, abbrv)
                logging.info(f'generated reference number')
                # save submission
                generated_guid = str(uuid.uuid4())
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                formatted_datetime = datetime.strptime(timestamp, '%Y%m%d%H%M%S').strftime('%Y-%m-%d %H:%M:%S')
                filename, original_extension = os.path.splitext(validated_data['file'].filename)
                filename = f"{reference_number}_{timestamp}{original_extension}"
                path =os.path.join(os.path.abspath('uploads'), promo.upload_folder, filename)
                logging.info(f'about to save file: {path}')
                name, saved_path = save_file(validated_data['file'],'', path)
                if name:                
                    logging.info(f'saved file')
                    submission_repo = BaseRepository(FormSubmissions)
                    submission_orm = FormSubmissions(id=generated_guid, promotion_id = promo.id, title=validated_data['title'], first_name=validated_data['firstName'], last_name=validated_data['lastName'], email_addr=validated_data['emailAddr'], phone_num=validated_data['phoneNum'], image=filename)
                    isSaved, record = submission_repo.create_record_without_commit(submission_orm)
                    if isSaved:
                        logging.info(f'saved submission')
                        if isSaved:
                            db.session.commit()
                            logging.info('saved reference')
                            response = True
                            email_obj = {
                            'message' : {
                                'reference_number': reference_number,
                                'date_created': formatted_datetime,
                                'name': validated_data['firstName'] + ' ' + validated_data['lastName'],
                                'feedback': promo.feedback_url if promo and promo.feedback_url else '',
                                'id':promo.id
                            },

                            'participantEmail' : validated_data['emailAddr'],
                            'promoAbbr' : abbrv  
                            }
                            message = email_obj['message']
                            if all(data is not None for data in [email_obj['participantEmail'], email_obj['message'], abbrv]):
                                send_email(email_obj['participantEmail'], abbrv, email_obj['message'])
                            else:
                                logging.info("Required data not available for email")
                            
                        else:
                            db.session.rollback()
                            os.remove(saved_path)
                else:
                    raise Exception('File not saved')
            else:
                errors= "Promotion already closed"
    except Exception as e:
        logging.error(f'An error occurred when attempting to submit submission: {e}')
        try:
            os.remove(saved_path)
        except Exception as ie:
            logging.error(f'failed to remove uploaded file: {ie}')
        db.session.rollback()
    finally:
        logging.info('closing the session')
        db.session.close()
    logging.info(f'exiting submission service method: {response} {errors} {message}')
    return response, errors, message
    
def get_all_user_promotions(email):
    logging.info(f'Entered method to get all user promotions!')
    response = None
    try:
        logging.info(f'entered try block')
        repo = BaseRepository(FormSubmissions)
        promo_sub_list = [item for item in repo.get_all_records() if item.email_addr.strip() == email.strip()]
        logging.info(f'user submissions: {promo_sub_list}')
        promo_sub_set = set(promo_sub_list)
        promotion_map = {}
        for promo_sub in promo_sub_set:
            promo_name = promo_sub.promotion.promotion_name  # The unique promotion name
            image = promo_sub.image  # The image for submission details
            full_name = f"{promo_sub.first_name} {promo_sub.last_name}"  # Full name of the person

            if promo_name not in promotion_map:
                # Initialize the promotion entry if it's not already in the dictionary
                promotion_map[promo_name] = {
                    'promotion': promo_name,
                    'full_name': full_name,
                    'submissions': []  # To store the list of submissions
                }

            # Add submission details, ensuring the image is unique
            # We'll check if the image is already in the submission details to avoid duplicates
            if image not in [submission['submission_details'] for submission in promotion_map[promo_name]['submissions']]:
                promotion_map[promo_name]['submissions'].append({                    
                    'submission_details': promo_sub.promotion.upload_folder + image,
                    'date_created':promo_sub.promotions_submission_references[0].date_created if promo_sub.promotions_submission_references and promo_sub.promotions_submission_references[0] else 'N/A'
                })
        response = list(promotion_map.values())
    except Exception as e:
        logging.error(f'An exception occurred when attempting to get user for {email}; error: {e}')
    return response
def split_array(arr, n):
    # Calculate the size of each part
    k, m = divmod(len(arr), n)
    
    # Split array into n parts
    return [arr[i * k + min(i, m): (i + 1) * k + min(i + 1, m)] for i in range(n)]
def create_winner_badge(winner_id:str, badge_name:str, badge_desc:str=None):
    response = False
    repo = BadgeRepository(Badges)
    try:
        record = repo.get_badge_by_winner_id(winner_id=winner_id)
        if record is None:
            badge = Badges(badge_name=badge_name, badge_description=badge_desc, winner_id=winner_id)
            success, record = repo.create_record(badge)
            response = success
        else:
            updatedObj = record.to_dict()
            id = record.id
            del updatedObj['id']
            updatedObj['badge_name'] = badge_name
            response = repo.update_record(id, **updatedObj)
    except Exception as e:
        logging.error(f'An error occurred when attempting to create a badge for the user: {e}')
    return response
def get_winner_badge(winner_id:str):
    response = 'default'
    try:
        repo = BadgeRepository(Badges)
        record = repo.get_badge_by_winner_id(winner_id=winner_id)
        if record:
            logging.info('got winner badges')
            response = record.badge_name if record and record.badge_name else 'default'
    except Exception as e:
        logging.error(f'An error occurred when attempting to get the winner badge {e}')
    return response
    