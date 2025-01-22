from app import logging
from app.database.base_repository import BaseRepository
from app.database.models.models import Themes, DynamicPageContent
from datetime import datetime, timedelta
from app.dto import ThemesDto, DynamicContent

def create_new_dynamic_content(dnc:DynamicContent):
    logging.info(f'Entered create dynamic content method with')
    isSuccess, record = False, None
    try:
        repo = BaseRepository(DynamicPageContent)
        if dnc is not None:
            new_content = DynamicPageContent(blog_id=dnc.promotion_id, how_to_enter_html=dnc.how_to_enter, prizes_html=dnc.prizes, block1_html=dnc.block1, block2_html=dnc.block2, rules_html=dnc.rules)
            isSuccess, record = repo.create_record(new_content)
    except Exception as e:
        logging.error(f'An error occurred when attempting to create a new dynamic content record; {e}')
    response = record.to_dict() if record else None
    return isSuccess, response
def create_new_theme_content(theme:ThemesDto):
    logging.info(f'Entered create themes method with ')
    isSuccess, record = False, None
    try:
        repo = BaseRepository(Themes)
        if theme is not None:
            new_content = Themes(name=theme.theme_name, primary_color=theme.primary, secondary_color=theme.secondary, background_color=theme.background, font_family=theme.font, font_size=theme.font_size, dpc_id=theme.dpc_id)
            isSuccess, record = repo.create_record(new_content)
    except Exception as e:
        logging.error(f'An error occurred when attempting to create a new theme record; {e}')
    response = record.to_dict() if record else None
    return isSuccess, response
def update_dynamic_content(dnc: DynamicContent):
    logging.info(f'Entered update dnc method with {vars(dnc)} ')
    isSuccess = False
    try:
        promotions_repo = BaseRepository(DynamicPageContent)
        id = int(dnc.dnc_id) if dnc.dnc_id.isdecimal() else None
        if id is not None and int(id) > 0:
            # TODO:: update with the save file component, we should remove existing file and save the new ones
            # and update promo file columns with the names of the new files
            
            update_obj = DynamicPageContent(id=dnc.dnc_id, blog_id=dnc.promotion_id, how_to_enter_html=dnc.how_to_enter, prizes_html=dnc.prizes, block1_html=dnc.block1, block2_html=dnc.block2, rules_html=dnc.rules).to_dict()
            del update_obj['id']
            logging.info(f'object with updates: {update_obj}')
            isSuccess = promotions_repo.update_record(int(dnc.dnc_id),**update_obj)
        else:
            isSuccess, record = create_new_dynamic_content(dnc)
    except Exception as e:
        logging.error(f'An error occurred when attempting to update a DNC; {e}')
    return isSuccess

def update_theme(theme: ThemesDto):
    logging.info(f'Entered update theme method with {vars(theme)}')
    isSuccess = False
    try:
        promotions_repo = BaseRepository(Themes)
        id = int(theme.theme_id) if theme.theme_id.isdecimal() else None
        if id is not None and int(id) > 0:
            # TODO:: update with the save file component, we should remove existing file and save the new ones
            # and update promo file columns with the names of the new files
            update_obj = Themes(id=theme.theme_id, name=theme.theme_name, primary_color=theme.primary, secondary_color=theme.secondary, background_color = theme.background, font_family=theme.font, font_size=theme.font_size, dpc_id=theme.dpc_id).to_dict()
            del update_obj['id']
            logging.info(f'object with updates: {update_obj}')
            isSuccess = promotions_repo.update_record(int(theme.theme_id),**update_obj)
        else:
            isSuccess, record = create_new_theme_content(theme)
    except Exception as e:
        logging.error(f'An error occurred when attempting to update a Promotion; {e}')
    return isSuccess