from flask import Blueprint, request, jsonify, render_template, send_from_directory, flash, redirect, url_for, session, current_app, Response
from jinja2 import Template
import logging
import os
from app.services.promotion_service import get_all_promotions, create_new_promotion, update_record, get_promotion, dto_to_promo
from app.services.promotion_winners_service import get_promotion_winners, get_promotion_participants, get_all_user_promotions, get_winner_badge
from datetime import datetime, timedelta
from app import logging
from app.services.file_service import does_tempalte_exist, export_db, process_import_db
from app.services.user_service import register_user, get_user_by_email
from app.database.models.models import Users
from flask_login import login_user, logout_user, login_required, current_user
from app.error_handlers import role_required
# logging.basicConfig(level=logging.DEBUG, filename='logs/debug.log', format='%(asctime)s %(levelname)s %(name)s : %(message)s')

promotions_bp = Blueprint('promotions', __name__)
admin_bp = Blueprint('admin', __name__)
index_bp = Blueprint('main', __name__)

@index_bp.route('/image/<path:filename>')
def serve_files(filename):
    logging.debug('serve_files route')
    directory = os.path.join(os.getcwd(), 'uploads')
    logging.debug(f'image directory: {directory} and file: {filename}')
    if os.path.exists(os.path.join(directory, filename)):
        logging.error('image file not found')
        return send_from_directory(directory, filename)
    else:
        logging.debug(f"returning default image {os.path.join(os.getcwd(), 'static', 'images'), 'image-not-found.png'}")
        return send_from_directory(os.path.join(os.getcwd(),'app', 'static', 'images'), 'image-not-found.png')

@index_bp.route('/')
def index():
    logging.info('entered route')
    url_template = Template("/blog/{{ id }}")
    currentPromotions, expiredPromotions, upcomingPromotions = get_all_promotions(url_template)   
    all = upcomingPromotions + currentPromotions
    logging.info(f"testing what exists{vars(all[0])}")
    return render_template('index.html', blogPosts = all[:6])

@promotions_bp.route('/', methods=['GET'])
def promotions():
    logging.debug('Entered promotions route')
    url_template = Template("/promotions/{{ id }}")
    currentPromotions, expiredPromotions, upcomingPromotions = get_all_promotions(url_template)    
    # logging.info(vars(currentPromotions[0]))
    return render_template('promotions.html', upcomingPromotionsWithURLs=upcomingPromotions, activePromotionsWithURLs=currentPromotions, inactivePromotionsWithURLs=expiredPromotions)
@promotions_bp.route('/<id>', methods=['GET'])
def get_promotion_by_id(id):
    logging.info(f'entered the get promotion endpoint for id: {id}')
    user_message = ''
    active_promotion = False
    promo, dpc, theme = get_promotion(id)
    if promo is None:
        return render_template('404.html'),404
    logging.info(f'promo from service: {vars(promo)}')
    active_promotion = promo.endDate > datetime.today().date()
    winner_data = {'status': False, 'data': None}
    if not active_promotion:
        user_message = 'Sorry, this promotion has ended. Please visit our promotions page to view the active promotions.'
        winner_data = get_promotion_winners(promo.promo_id)
        if not winner_data:
            winner_data = {'status': False, 'data': None}
    if promo.startDate > datetime.today().date():
        user_message= 'Sorry, this promotion has ended. Please visit our promotions page to view the active promotions.'
        active_promotion = False
        
    logging.info(f'is promotion accepting entries? {active_promotion} winner: {winner_data}')
    if dpc is None or dpc.dnc_id is None or dpc.dnc_id == 0:
        template_exists, template = does_tempalte_exist(promo.promo_name)
        if template_exists:
            return render_template(template, 
                           errors=[], 
                           acceptingEntries=active_promotion, 
                           message=user_message, 
                           winner_data = winner_data,
                           dynamic_content= {
                               'promotionForm':template,
                               'promotion_info':dto_to_promo(promo)},
                           form_data={
                            'title': request.form.get('title', ''),
                            'fname': request.form.get('fname', ''),
                            'lname': request.form.get('lname', ''),
                            'email': request.form.get('email', ''),
                            'phone': request.form.get('phone', ''),
                            })
        else:
            return render_template('404.html'),404
    logging.info(f'fetched data: {vars(promo)} and {vars(dpc)} and {vars(theme)}')
    return render_template('dynamic_promotion.html', promotion=promo, content=dpc, theme=theme, winner_data = winner_data, acceptingEntries=active_promotion)
@promotions_bp.route('/user-submissions')
def user_submissions():
    logging.info('entered user submission route')
    email = session.get('email', '')
    submissions = get_all_user_promotions(email=email)
    logging.info(f'email: {email}, info: {submissions}')
    return render_template('user_promotion_submissions.html', user_submissions=submissions)

@promotions_bp.route('/user-submissions/<email>')
def user_submission_email(email):
    logging.info(f'entered user submission route with email: {email}')
    submissions = get_all_user_promotions(email=email)
    logging.info(f'email: {email}, info: {submissions}')
    return render_template('user_promotion_submissions.html', user_submissions=submissions)
@promotions_bp.route('/about')
def about():    
    return render_template('about.html')
@promotions_bp.route("/contact")
def contact():    
    return render_template('contact.html')
@admin_bp.route('/create',methods=['GET'])
@role_required('admin,create')
@login_required
def create_promotion():
    return render_template('create_promotion.html')
@admin_bp.route('/edit/<id>', methods=['GET'])
@role_required('admin,create')
@login_required
def edit_promotion(id):
    logging.info(f'entered the edit promotion endpoint for id: {id}')
    promo, dpc, theme = get_promotion(id)
    logging.info(f'see promo: {vars(promo)}')
    roles = [role.strip() for role in current_user.role.split(',')]
    user_can_access = promo.abbreviation in roles or 'admin' in roles
    if not user_can_access:
        return redirect(url_for('main.index')) 
    active_promotion = promo.endDate > datetime.today().date()
    logging.info(f'fetched data for edit: {vars(promo)}')
    logging.info(f'is active promotion: {active_promotion}')
    return render_template('create_promotion.html', promotion=promo, dpc=dpc, theme=theme, is_active=active_promotion)

@admin_bp.route('/manage-entries/<id>', methods=['GET'])
@role_required('admin,manage')
@login_required
def manage_entries(id):
    logging.info(f'entered manage entries route for: {id}')
    promotion_info, dnc,theme = get_promotion(id)
    logging.info(f'got promotion info: {vars(promotion_info)}')
    participants = get_promotion_participants(id)
    winner_data= get_promotion_winners(id)

    entries = [{
        'id':f"{item.id}",
        'full_name':f"{item.first_name} {item.last_name}",
        'email':f"{item.email_addr}",
        'mobile':f"{item.phone_num}",
        'image':f"{item.image}",
        'date_entered': f"{item.promotions_submission_references[0].date_created if item.promotions_submission_references and item.promotions_submission_references[0] else 'N/A'}"
    } for item in participants]
    return render_template('manageEntries.html', promotion_info=promotion_info, entries=entries, winner_data=winner_data)
@index_bp.route('/login', methods=['GET', 'POST'])
def login():
    # register_user('tarique.solomon@jsif.org', 'admin,', 'Password')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_by_email(email)
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template('register.html', form_action=url_for('main.login'), form_name='Login')
@index_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))

@admin_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        options = request.form.getlist('options')
        roles = ','.join(options)
        logging.info(f'role options: {options} and {roles}, {request.form}')
        if not roles:
            logging.info('no roles selected')
            role_options = get_roles()
            return render_template('register.html', form_action=url_for('admin.register'), form_name='Register New User', new_user=True, options= role_options)
        success, message = register_user(email=email, roles=roles, password=password)
                
        flash(message)
        if success:            
            return redirect(url_for('main.login'))
        else:
            return redirect(url_for('admin.register'))
    role_options = get_roles()
    return render_template('register.html', form_action=url_for('admin.register'), form_name='Register New User', new_user=True, options= role_options)

@admin_bp.route('/console', methods=['GET'])
@role_required('admin,manage')
@login_required
def admin_console():
    url_template = Template("/promotion/{{ id }}")
    currentPromotions, expiredPromotions, upcomingPromotions = get_all_promotions(url_template)
    promo_arr = currentPromotions + upcomingPromotions + expiredPromotions
    promo_abbr = [{'abbrv':f"{item.abbreviation}", 'id':f"{item.promo_id}", 'winner_data': get_promotion_winners(item.promo_id) } for item in promo_arr]
    logging.info(f"promotion management: {promo_abbr[0]['winner_data']}")
    return render_template('admin_console.html', records=promo_abbr)
def get_roles():
    logging.info('getting roles')
    url_template = Template("/promotion/{{ id }}")
    currentPromotions, expiredPromotions, upcomingPromotions = get_all_promotions(url_template)
    promo_arr = currentPromotions + upcomingPromotions
    logging.info(f'promo array: {promo_arr} {vars(promo_arr[0])}')
    promo_abbr = [item.abbreviation for item in promo_arr]
    logging.info(f'promo abbre: {promo_abbr}')
    options = ['admin', 'user', 'create', 'manage'] + promo_abbr
    return options
@admin_bp.route('/export', methods=['Get'])
@role_required('admin,manage')
@login_required
def export_database():
    buffer = export_db()
    response = Response(
        buffer.getvalue(),
        mimetype="application/sql",
        headers={
            "Content-Disposition": "attachment; filename=database_export.sql"
        },
    )
    return response

# Utility function to get routes for a specific blueprint
def get_routes_for_blueprint(blueprint_name):
    routes = []
    app = current_app
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith(blueprint_name):
            routes.append({
                'endpoint': rule.endpoint,
                'url': str(rule)
            })
    return routes