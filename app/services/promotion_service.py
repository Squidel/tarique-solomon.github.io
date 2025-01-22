from app import logging
from app.database.promotions_repository import PromotionsRepository
from app.database.models.models import BlogPosts
from datetime import datetime, timedelta
from app.dto import Promotion, DynamicContent, ThemesDto
from app.services.file_service import save_file
import os
from app.app_config import UPLOADS_FOLDER


def get_upcoming_promotions(start_Date:datetime, end_date:datetime = None):
    result = None
    try:
        logging.debug(f'Entered method to get all upcoming promotions')
        promotions_repo = PromotionsRepository(BlogPosts)
        sdate = start_Date if start_Date else datetime.today()
        edate = end_date if end_date else datetime(9999, 12, 31)
        result = promotions_repo.get_promotions_within_dates(sdate, edate)
    except Exception as e:
        logging.error(f'An error occurred when attempting to get all upcoming promotions; Error: {str(e)}')
        result = None
    return result

def get_promotions(is_active:bool = True):
    result = None
    try:
        logging.debug(f'Entered method to get current promotions')
        promotions_repo = PromotionsRepository(BlogPosts)
        # yesterday = datetime.today() - timedelta(days=1)
        # start_date = datetime.combine(yesterday, datetime.time(23,59,59))
        result = promotions_repo.get_current_promotions(datetime.today()) if is_active else promotions_repo.get_promotions_expired(datetime.today())
        # result = [obj for obj in result if obj['end_date'] > datetime.today()]
    except Exception as e:
        logging.error(f'An error occurred when attempting to get current promotions; Error: {str(e)}')
        result = None
    return result
def promo_to_dto(promos, url_template):
    promotions = []
    if promos:
        for promo in promos:
            url = ''
            try:
                url =url_template.render(id=promo.id)
                logging.info(f'url template: {url}')
            except Exception as e:
                url=''
                logging.error(f'failed to render url: {e}')
            promoObj = Promotion(promo.id, promo.promotion_name, promo.start_date, promo.end_date, promo.main_picture, url, promo.abbreviation)
            promotions.append(promoObj)
    return promotions
def dto_to_promo(promo:Promotion):
    logging.info('dto conversion')
    return BlogPosts(id=promo.promo_id, abbreviation=promo.abbreviation, promotion_name = promo.promo_name, banner_image = promo.banner, upload_folder = promo.uploadFolder, start_date = promo.startDate, end_date = promo.endDate, main_picture = promo.mainPicture, is_activation=promo.is_activation)
    
def get_all_promotions(url_template):
    logging.info(f'Entered get_all_promotions method, with param: {url_template}')
    currentPromotions = promo_to_dto(get_promotions(True), url_template=url_template)
    expiredPromotions = promo_to_dto(get_promotions(False), url_template=url_template)
    upcomingPromotions = promo_to_dto(get_upcoming_promotions(datetime.today()), url_template=url_template)
    logging.info(f'Exiting get_all_promotions method')
    return currentPromotions, expiredPromotions, upcomingPromotions
def create_new_promotion(promo: Promotion):
    logging.info(f'Entered create promotions method with {vars(promo)}')
    isSuccess, record = False, None
    uploaded_paths = []
    try:
        # filePath = os.path.join(os.getcwd(), 'promotion_images')
        filePath = 'app/static/images'
        promotions_repo = PromotionsRepository(BlogPosts)
        if promo is not None:
            main_pic_name, main_pic_file_path = save_file(promo.mainPicture, filePath)
            banner_name, banner_path = save_file(promo.banner, filePath)
            uploaded_paths.append(main_pic_file_path)
            uploaded_paths.append(banner_path)
            orm = BlogPosts(abbreviation=promo.abbreviation, promotion_name = promo.promo_name, banner_image = banner_name, upload_folder = promo.uploadFolder, start_date = promo.startDate, end_date = promo.endDate, main_picture = main_pic_name, is_activation = promo.is_activation)
            # if isinstance(orm.start_date, str):
            #     orm.start_date = datetime.strptime(orm.start_date, '%Y-%m-%d').date() if orm.start_date else None
            # if isinstance(orm.end_date, str):
            #     orm.end_date = datetime.strptime(orm.end_date, '%Y-%m-%d').date() if orm.end_date else None

            logging.info(f'created orm {vars(orm)}')
            isSuccess, record = promotions_repo.create_record(orm)
            if isSuccess:
                path = os.path.join(os.path.abspath('uploads'), promo.uploadFolder)
                if not os.path.exists(path):
                    os.makedirs(path)
            logging.info(f'after calls: {isSuccess} and {vars(record)}')
    except Exception as e:
        logging.error(f'An error occurred when attempting to create a new Promotion: {e}')
        for path in uploaded_paths:
            os.remove(path)
        isSuccess, record = False, None        
    response = record.to_dict() if record else None
    return isSuccess, response
def update_record(promo: Promotion):
    logging.info(f'Entered update promotions method with {vars(promo)}')
    isSuccess = False
    try:
        filePath = 'app/static/images'
        promotions_repo = PromotionsRepository(BlogPosts)
        logging.info('created promotions repo in the update method')
        if promo is not None and int(promo.promo_id) > 0:
            logging.info('about to convert object')
            main_pic_name, main_pic_file_path = save_file(promo.mainPicture, filePath)
            banner_name, banner_path = save_file(promo.banner, filePath)
            logging.info(f'banner: {banner_name} and main: {main_pic_name}')
            promo.banner = banner_name
            promo.mainPicture = main_pic_name
            update_obj = dto_to_promo(promo).to_dict()
            del update_obj['id']
            if promo.banner is None:
                logging.info('no banner image')
                del update_obj['banner_image']
            if promo.mainPicture is None:
                del update_obj['main_picture'] 
            logging.info(f'object with updates: {update_obj}')
            isSuccess = promotions_repo.update_record(int(promo.promo_id),**update_obj)
            logging.info(f'successfully updated record: {isSuccess}')
    except Exception as e:
        logging.error(f'An error occurred when attempting to update a Promotion; {e}')
    return isSuccess
def get_promotion(id:int):
    promotions = None
    content = None
    theming = None
    try:
        filePath = os.path.join(os.getcwd(), 'promotion_images')
        promotions_repo = PromotionsRepository(BlogPosts)
        promo = promotions_repo.get_record_by_id(id)
        logging.info(f'got promotion: {vars(promo)}')
        dny = promo.dynamic_page_content
        logging.info(f'got dpc: {vars(dny[0]) if dny[0] is not None else None}')
        theme = dny[0].themes if dny and dny[0] else None
        # logging.info(f'got theme: {vars(theme[0])}')
        promotions = Promotion(promo.id, promo.promotion_name, promo.start_date, promo.end_date, promo.main_picture, None, promo.abbreviation, promo.banner_image,promo.upload_folder, is_activation=promo.is_activation)
        content = DynamicContent( dny[0].id, promo.id, dny[0].how_to_enter_html, dny[0].prizes_html, dny[0].block1_html, dny[0].block2_html, dny[0].rules_html ) if dny is not None or dny[0] is not None else None
        theming = ThemesDto(theme[0].id, theme[0].name, theme[0].primary_color,theme[0].secondary_color, theme[0].background_color, theme[0].font_family,theme[0].font_size, theme[0].dpc_id) if theme is not None or theme[0] is not None else None#theme[0].to_dict()
    except Exception as e:
        logging.error(f'Error getting promotion for id: {id} with error: {e}')
    return promotions, content, theming