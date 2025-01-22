from app.database.base_repository import BaseRepository
from app import logging, db
from sqlalchemy import and_, desc, asc
from app.database.models.models import Themes, DynamicPageContent

class PromotionsRepository(BaseRepository):
    def get_promotions_within_dates(self, start_date_var, end_date_var):
        records = None
        try:
            logging.debug(f'Attempting to get promotions between date range')
            records = self.model.query.filter(and_(self.model.start_date > start_date_var, self.model.end_date < end_date_var)).all()
        except Exception as e:
            logging.error(f'An error occurred when attempting to get promotions between date ranges; Error: {str(e)}')
            records = None
        return records
    
    def get_current_promotions(self, current_date):
        records = None
        try:
            logging.debug(f'Attempting to get current promotions')
            records = self.model.query.filter(and_(self.model.start_date <= current_date, self.model.end_date >= current_date)).all()
        except Exception as e:
            logging.error(f'An error occurred when attempting to get current promotions ; Error: {str(e)}')
            records = None
        return records
    
    def get_promotions_expired(self, current_date):
        records = None
        try:
            logging.debug(f'Attempting to get promotions expired')
            records = self.model.query.filter(self.model.end_date < current_date).all()
        except Exception as e:
            logging.error(f'An error occurred when attempting to get expired promotions; Error: {str(e)}')
            records = None
        return records
    def get_record_by_id(self, id):
        record = None
        try:
            record = self.model.query.filter_by(id=id).options(db.joinedload(self.model.dynamic_page_content).joinedload(DynamicPageContent.themes)).first()
        except Exception as e:
            logging.error(f'error getting promotion by id in the overridden method: {e}')
        return record
    
class PromotionSubmissionRepository(BaseRepository):
    def get_submissions_by_promotions(self, promo_id):
        record = None
        try:
            record = self.model.query.filter_by(promotion_id=promo_id).options(db.joinedload(self.model.promotions_submission_references)).all()
        except Exception as e:
            logging.error(f'error getting promotion submission: {e}')
        return record
class BadgeRepository(BaseRepository):
    def get_badge_by_winner_id(self, winner_id):
        record = None
        try:
            record = self.model.query.filter_by(winner_id=winner_id).first()
        except Exception as e:
            logging.error(f'an error occurred in the badge repository attempting to get badge by winner id: {e}')
        return record