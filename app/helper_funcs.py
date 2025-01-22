import os, logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from dotenv import load_dotenv
from app.app_config import ALLOWED_EXTENSIONS
from app import db
from flask import render_template
from datetime import datetime
import bleach, re
from app.database.base_repository import BaseRepository
from app.database.models.models import BlogPosts

logging.basicConfig(filename='logs/app.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


# Load environment variables from .env file
load_dotenv()

def send_email(recipient_email, promotion_abbreviation, message):
    logging.info("Entered send_email function")
    cursor = None
    server = None
    
    try:
        # Set up the SMTP server
        smtp_server = 'mail.876promotions.com'
        smtp_port = 465

        # Retrieve the sender email password from environment variables
        sender_password = os.environ.get('SENDER_EMAIL_PASSWORD')

        # Retrieve the promotion name based on the promotion abbreviation
        repo = BaseRepository(BlogPosts)
        result = [promo for promo in repo.get_all_records() if promo.abbreviation.strip() == promotion_abbreviation.strip]
        promotion_name = result[0] if result else ''

        # Create a MIME message
        msg = MIMEMultipart('alternative')
        msg['From'] =  formataddr(('876Promotions', 'info@876promotions.com'))
        msg['To'] = recipient_email
        #msg['Bcc'] = 'info@876promotions.com'
        msg['Subject'] = f'Your submission details for the {promotion_name} promotion'

        # Render the HTML template
        html_content = render_template('email_template.html', message=message)

        # Create the MIME parts for both text and HTML content
        text_part = MIMEText('', 'plain')
        html_part = MIMEText(html_content, 'html')

        # Attach the MIME parts to the message
        msg.attach(text_part)
        msg.attach(html_part)

        # Start the SMTP connection
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login('info@876promotions.com', sender_password)

        # Send the email
        server.sendmail('info@876promotions.com', recipient_email, msg.as_string())
        logging.info('Email sent successfully!')

    except Exception as e:
        logging.exception('An error occurred while sending the email: %s', str(e))

    finally:
        logging.info("Exiting send_email function")




# def generateRefNum(table, id):
#     logging.info("Entered generateRefNum function")
#     cursor = None
#     try:
#         # Obtain the latest Reference Number
#         cursor = db.cursor()
#         cursor.execute('SELECT abbreviation FROM Promotion_Names WHERE id = %s;', (id))
#         abbreviation = str(cursor.fetchone()[0])

#         query = f"""
#                 SELECT reference_number FROM {table} 
#                 WHERE reference_number LIKE '%{abbreviation}%'
#                 ORDER BY reference_number DESC 
#                 LIMIT 1;"""
#         cursor.execute(query)
#         result = cursor.fetchone()
#         lastRefNum = result[0] if result else None

#         # Create the new Reference Number
#         if lastRefNum:
#             suffix = lastRefNum.split(abbreviation)[1]
#             suffix = int(suffix) + 1
#             suffix_padded = str(suffix).zfill(6)
#             newRefNum = abbreviation + suffix_padded
#         else:
#             newRefNum = abbreviation + '000000'

#         return (newRefNum, abbreviation)
    
#     except Exception as e:
#         logging.exception(f"Error generating reference number: {str(e)}")

#     finally:
#         if cursor:
#             cursor.close()
#         logging.info("Exiting generateRefNum function")


def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions


# def getUpcomingPromotions():
#     logging.info("Entered getUpcomingPromotions function")
#     current_date = datetime.now().date()
#     cursor = None
#     response = []

#     try:
#         cursor = db.cursor()
#         cursor.execute('SELECT * FROM Promotion_Names WHERE start_date > %s ORDER BY id DESC;', (current_date,))
#         response = cursor.fetchall()
#         logging.info(f"Response: {response}")
    
#     except Exception as e:
#         logging.error(f"Error retrieving upcoming promotions: {str(e)}")
    
#     finally:
#         if cursor:
#             cursor.close()
#         logging.info("Exiting getUpcomingPromotions function")
#         return response
    

# def getActivePromotions():
#     logging.info("Entered getActivePromotions function")
#     current_date = datetime.now().date()
#     cursor = None
#     response = []

#     try:
#         cursor = db.cursor()
#         cursor.execute('SELECT * FROM Promotion_Names WHERE (start_date < %s OR start_date = %s) AND (end_date > %s OR end_date = %s) ORDER BY id DESC;', (current_date, current_date, current_date, current_date))
#         response = cursor.fetchall()
    
#     except Exception as e:
#         logging.error(f"Error retrieving active promotions: {str(e)}")
    
#     finally:
#         if cursor:
#             cursor.close()
#         logging.info("Exiting getActivePromotions function")
#         return response
        

# def getInactivePromotions():
#     logging.info("Entered getInactivePromotions function")
#     current_date = datetime.now().date()
#     cursor = None
#     response = []

#     try:
#         cursor = db.cursor()
#         cursor.execute('SELECT * FROM Promotion_Names WHERE end_date < %s ORDER BY id DESC;', (current_date))
#         response = cursor.fetchall()
    
#     except Exception as e:
#         logging.error(f"Error retrieving inactive promotions: {str(e)}")
    
#     finally:
#         if cursor:
#             cursor.close()
#         logging.info("Exiting getInactivePromotions function")
#         return response
    

# def getWinnersbyPromotion(id):
#     logging.info("Entered getWinnersbyPromotion function")
#     cursor = None
#     response = {'status': False, 'data': None}

#     try:
#         cursor = db.cursor()
#         query = """
#             SELECT pfs.id, pfs.first_name, pfs.last_name, psr.reference_number, pw.date_selected, pfs.image 
#             FROM Promotion_Winners pw 
#             INNER JOIN Promotions_Submission_References psr ON pw.reference_number = psr.reference_number 
#             INNER JOIN Promotions_Form_Submissions pfs ON psr.form_submission_id = pfs.id 
#             WHERE pw.promotion_id = %s;
#         """
#         cursor.execute(query, (id,))
#         winner_data = cursor.fetchall()
#         logging.info(winner_data)

#         # Sort the winners by the date_created (index 4)
#         winners_sorted = sorted(winner_data, key=lambda x: x[4])

#         # Initialize dictionary to store winners in three draws
#         winners_sorted_and_split = {
#             'first_draw': [],
#             'second_draw': [],
#             'third_draw': []
#         }

#         # Distribute winners every 6 iterations
#         for i, winner in enumerate(winners_sorted):
#             if i % 18 < 6:
#                 winners_sorted_and_split['first_draw'].append(winner)
#             elif i % 18 < 12:
#                 winners_sorted_and_split['second_draw'].append(winner)
#             else:
#                 winners_sorted_and_split['third_draw'].append(winner)

#         logging.info(f"Sorted and Split: {winners_sorted_and_split}")
#         response['status'] = True
#         response['data'] = winners_sorted_and_split

#     except Exception as e:
#         logging.error(f"An error occurred when retrieving the winners from the database: {str(e)}")

#     finally:
#         if cursor:
#             cursor.close()
        
#         logging.info("Exiting getWinnersbyPromotion function")
#         return response



# def getAllEntries(id):
#     logging.info("Entered getAllEntries function")
#     cursor = None
#     response = {'status': False, 'data': None}

#     try:
#         cursor = db.cursor()
#         query = "SELECT * FROM Promotions_Form_Submissions WHERE promotion_id = %s;"
#         cursor.execute(query, id)
#         participants = cursor.fetchall()
        
#         if participants and len(participants) > 0:
#             # Sort participants by full name (first name + last name)
#             participants_sorted = sorted(participants, key=lambda x: (x[2] + " " + x[3]))
#             response['status'] = True
#             response['data'] = participants_sorted

#     except Exception as e:
#         logging.error(f"An error occured when retrieving the participants from the database: {str(e)}")

#     finally:
#         if cursor:
#             cursor.close()
        
#         logging.info("Exiting getAllEntries function")
#         return response
    

# def archiveInvalidEntry(id):
#     logging.info("Entered archiveInvalidEntry function")
#     cursor = None
#     response = {'status': False, 'message': None}

#     try:
#         db.autocommit(False)
#         cursor = db.cursor()

#         query = """
#             INSERT INTO Invalid_Promotions_Submission_References (id, form_submission_id, reference_number, date_created)
#             SELECT id, form_submission_id, reference_number, date_created
#             FROM Promotions_Submission_References
#             WHERE form_submission_id = %s;
#         """
#         cursor.execute(query, (id,))

#         query = "DELETE FROM Promotions_Submission_References WHERE form_submission_id = %s;"
#         cursor.execute(query, (id,))

#         query = """
#             INSERT INTO Invalid_Promotions_Form_Submissions (id, promotion_id, title, first_name, last_name, email_addr, phone_num, image)
#             SELECT id, promotion_id, title, first_name, last_name, email_addr, phone_num, image
#             FROM Promotions_Form_Submissions
#             WHERE id = %s;
#         """
#         cursor.execute(query, (id,))

#         query = "DELETE FROM Promotions_Form_Submissions WHERE id = %s;"
#         cursor.execute(query, (id,))

#         db.commit()        
#         response['status'] = True
#         response['message'] = "Record successfully removed from the pool of valid entries."

#     except Exception as e:
#         db.rollback()
#         response['status'] = False
#         response['message'] = "An error occured when attempting to remove the invalid entry."
#         logging.error(f"An error occured when attempting to remove the invalid entry: {str(e)}")

#     finally:
#         if cursor:
#             cursor.close()
        
#         db.autocommit(True)
#         logging.info("Exiting archiveInvalidEntry function")
#         return response


# def isAcceptingEntries(id):
#     logging.info("Entered isAcceptingEntries function")
#     current_date = datetime.now().date()
#     cursor = None
#     response = (False, '')

#     try:
#         cursor = db.cursor()
#         cursor.execute('SELECT start_date, end_date FROM Promotion_Names WHERE id = %s;', (id))
#         result = cursor.fetchone()

#         if result:
#             start_date, end_date = result[0], result[1]
#             if start_date > current_date:
#                 response = (False, 'Submissions are disabled! This promotion has not yet started.')

#             elif start_date <= current_date and end_date >= current_date:
#                 response = (True, '')
            
#             else:
#                 response = (False, 'Sorry, this promotion has ended. Please visit our promotions page to view the active promotions.')
    
#     except Exception as e:
#         logging.error(f"Error: {str(e)}")
    
#     finally:
#         if cursor:
#             cursor.close()
#         logging.info("Exiting isAcceptingEntries function")
#         return response
    

# def get_PromotionInfobyID(id):
#     logging.info("Entered get_PromotionInfobyID function")
#     cursor = None
#     response = ({'id' : id, 'abbreviation' : '', 'promotion_name': '', 'start_date' : '', 'end_date' : '', 'main_picture' : '', 'banner_image' : '', 'upload_folder' : ''}, False)

#     try:
#         cursor = db.cursor()
#         cursor.execute('SELECT abbreviation, promotion_name, start_date , end_date , main_picture , banner_image , upload_folder FROM Promotion_Names WHERE id = %s;', (id))
#         result = cursor.fetchone()

#         if result:
#             response = ({'id' : id, 'abbreviation' : result[0], 'promotion_name': result[1], 'start_date' : result[2], 'end_date' : result[3], 'main_picture' : result[4], 'banner_image' : result[5], 'upload_folder' : result[6]}, True)
    
#     except Exception as e:
#         logging.error(f"Error: {str(e)}")
    
#     finally:
#         if cursor:
#             cursor.close()
#         logging.info("Exiting get_PromotionInfobyID function")
#         return response

# #Security Enforcement
# def get_ValidBlogPosts():
#     logging.info("Entered get_ValidBlogPosts function")
#     cursor = None
#     response = []

#     try:
#         cursor = db.cursor()
#         cursor.execute('SELECT promotion_name FROM Promotion_Names')
#         result = cursor.fetchall()

#         if result:
#             response = [row[0] for row in result]
    
#     except Exception as e:
#         logging.error(f"Error: {str(e)}")
    
#     finally:
#         if cursor:
#             cursor.close()
#         logging.info("Exiting get_ValidBlogPosts function")
#         return response

# def selectTable_Forms(id):
#     cursor = db.cursor()
#     cursor.execute('SELECT promotion_name FROM Promotion_Names WHERE id = %s;', (id))
#     promotion_name = cursor.fetchone()[0]
#     cursor.close()

#     # Validate the promotion name
#     valid_promotions = get_ValidBlogPosts()
#     if promotion_name not in valid_promotions:
#         raise ValueError(f'Invalid promotion name: {promotion_name}')

#     promotionName = promotion_name.replace(" ", "") + '_Forms'
#     return promotionName

# def selectTable_Submissions(id):
#     cursor = db.cursor()
#     cursor.execute('SELECT promotion_name FROM Promotion_Names WHERE id = %s;', (id))
#     promotion_name = cursor.fetchone()[0]
#     cursor.close()

#     # Validate the table name
#     valid_promotions = get_ValidBlogPosts()
#     if promotion_name not in valid_promotions:
#         raise ValueError(f'Invalid table name: {promotion_name}')

#     tableName = promotion_name.replace(" ", "") + '_Submissions'
#     return tableName

# def select_htmlTemplate(id):
#     logging.info("Entered select_htmlTemplate function")
#     cursor = None
#     response = ''

#     try:
#         cursor = db.cursor()
#         cursor.execute('SELECT promotion_name FROM Promotion_Names WHERE id = %s;', (id))
#         result = cursor.fetchone()

#         if result:
#             promotion_name = result[0]
#             # Validate the table name
#             valid_promotions = get_ValidBlogPosts()
#             if promotion_name not in valid_promotions:
#                 raise ValueError(f'Invalid promotion name: {promotion_name}')

#             response = promotion_name.replace(" ", "") + '.html'
    
#     except Exception as e:
#         logging.error(f"Error getting HTML template: {str(e)}")
    
#     finally:
#         if cursor:
#             cursor.close()
#         logging.info("Exiting select_htmlTemplate function")
#         return response



def validate_form_data(request):
    errors = []
    MAX_FILE = 10 * 1024 * 1024

    title = request.form.get('title')
    firstName = request.form.get('fname')
    lastName = request.form.get('lname')
    emailAddr = request.form.get('email')
    phoneNum = request.form.get('phone')
    file = request.files['purchasePhoto']
    promo_id = request.form.get('promotion_id')
    
    s_firstName = ''
    s_lastName = ''
    s_phoneNum = ''
    s_emailAddr = ''

    # Perform server-side validation
    if not (title and firstName and lastName and emailAddr and phoneNum and file):
        errors.append({'message': 'Please fill in all fields.'})

    if firstName.strip():
        s_firstName = bleach.clean(firstName.strip())
        if not re.match(r'^[a-zA-Z-]+$', s_firstName):
            errors.append({'message': 'Please enter a valid first name.', 'field': 'fname'})
    else:
        errors.append({'message': 'Please enter a valid first name.', 'field': 'fname'})

    if lastName.strip():
        s_lastName = bleach.clean(lastName.strip())
        if not re.match(r'^[a-zA-Z-]+$', s_lastName):
            errors.append({'message': 'Please enter a valid last name.', 'field': 'lname'})
    else:
        errors.append({'message': 'Please enter a valid last name.', 'field': 'lname'})

    if phoneNum:
        s_phoneNum = bleach.clean(phoneNum.strip())
        if len(s_phoneNum) != 10 or not s_phoneNum.isdigit():
            errors.append({'message': 'Please enter a 10-digit phone number without any brackets, dashes, or spaces.', 'field': 'phone'})
    else:
        s_phoneNum = ""
        errors.append({'message': 'Please enter a 10-digit phone number without any brackets, dashes, or spaces.', 'field': 'phone'})

    if emailAddr:
        s_emailAddr = bleach.clean(emailAddr.strip())
        if '@' not in s_emailAddr or '.' not in s_emailAddr:
            errors.append({'message': 'Please enter a valid email address.', 'field': 'email'})
    else:
        s_emailAddr = ""
        errors.append({'message': 'Please enter a valid email address.', 'field': 'email'})

    if not file:
        errors.append({'message': 'Please upload a photo.', 'field': 'upload'})

    if file:
        if file.content_length > MAX_FILE:
            errors.append({'message': 'File size exceeds the maximum allowed size of 5MB', 'field': 'upload'})
        
        if not allowed_file(file.filename, ALLOWED_EXTENSIONS):
            errors.append({'message': 'Invalid File Type | Please ensure that the file ends with png, jpg, jpeg, gif, jfif or heic', 'field': 'upload'})

    return errors, {
        'title': title,
        'firstName': s_firstName,
        'lastName': s_lastName,
        'emailAddr': s_emailAddr,
        'phoneNum': s_phoneNum,
        'file': file,
        'promo_id':promo_id
    }
