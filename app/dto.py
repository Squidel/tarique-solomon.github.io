from flask import jsonify
from app import logging

def conver_json_to_class(json, dto):
    new_obj = dto()
    for key, value in json.items():
        if hasattr(new_obj, key):
            # logging.info(f'Setting vals: {new_obj} and value: {value}')
            setattr(new_obj, key, value)
    return new_obj
def create_objects_from_form_data(form, files):
    logging.info(f'entered the conversion method {form}')
    promotion_data = {
        'promo_id': form.get('promo_id'),
        'promo_name': form.get('promo_name'),
        'startDate': form.get('startDate'),
        'endDate': form.get('endDate'),
        'mainPicture': files.get('mainPicture'),
        'url': form.get('url'),
        'abbreviation': form.get('abbreviation'),
        'banner': files.get('banner'),
        'uploadFolder': form.get('uploadFolder'),
        'is_activation': form.get('activation') == 'True'
    }

    dynamic_content_data = {
        'promotion_id': promotion_data['promo_id'],
        'how_to_enter': form.get('how_to_enter'),
        'prizes': form.get('prizes'),
        'block1': form.get('block1'),
        'block2': form.get('block2'),
        'rules': form.get('rules'),
        'dnc_id':form.get('dnc_id')
    }

    theme_data = {
        'dpc_id': dynamic_content_data['dnc_id'],
        'theme_name': form.get('theme_name'),
        'primary': form.get('primary'),
        'secondary': form.get('secondary'),
        'background': form.get('background'),
        'font': form.get('font'),
        'font_size': form.get('font_size'),
        'theme_id':form.get('theme_id')
    }
    promotion = conver_json_to_class(promotion_data, Promotion)
    logging.info(f'promotion dto: {vars(promotion)}')
    dynamic_content = conver_json_to_class(dynamic_content_data, DynamicContent)
    # logging.info(f'dynamic_content dto: {dynamic_content}')
    theme = conver_json_to_class(theme_data, ThemesDto)
    # logging.info(f'theme dto: {theme}')

    return promotion, dynamic_content, theme
class APIResponse:
    def __init__(self, data=None, message=None, status_code=200):
        self.data = data
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        """
        Convert the response object into a dictionary so it can be converted to JSON.
        """
        response = {}
        if self.data is not None:
            response['data'] = self.data
        if self.message is not None:
            response['message'] = self.message
        response['status_code'] = self.status_code
        return response

    def make_response(self):
        """
        Converts the response to a Flask Response object.
        """
        return jsonify(self.to_dict()), self.status_code
class BaseDTO:
    def is_valid_object(self):
        is_valid = True
        try:
            for attr_name in dir(self):
                attr_value = getattr(self, attr_name)
                if attr_value is None:
                    is_valid = False
        except Exception as e:
            logging.error(f'An error occurred when attempting to validate object; {e}')
        return is_valid
class Promotion(BaseDTO):
    def __init__(self, id=None, name=None, startDate=None, endDate=None, mainPicture=None, url=None, abbreviation = None, banner = None, uploadFolder = '', is_activation = False, description='') -> None:
        self.promo_id = id
        self.promo_name = name
        self.startDate = startDate
        self.endDate = endDate
        self.mainPicture = mainPicture
        self.url = url
        self.abbreviation = abbreviation
        self.banner = banner
        self.uploadFolder = uploadFolder
        self.is_activation = is_activation
        self.description = description
class DynamicContent(BaseDTO):
    def __init__(self, id=None, promotion_id=None, how_to_enter=None, prizes=None, block1=None, block2=None, rules=None):
        self.dnc_id = id
        self.promotion_id = promotion_id
        self.how_to_enter = how_to_enter
        self.prizes = prizes
        self.block1 = block1
        self.block2 = block2
        self.rules = rules
class ThemesDto(BaseDTO):
    def __init__(self, id=None, name=None, primary=None, secondary=None, background=None, font=None, font_size=None, dpc_id=None):
        self.theme_id = id
        self.theme_name = name
        self.primary = primary
        self.secondary = secondary
        self.background = background
        self.font = font
        self.font_size = font_size
        self.dpc_id = dpc_id