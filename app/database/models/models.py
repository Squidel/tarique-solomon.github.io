from typing import List, Optional

from sqlalchemy import CHAR, Column, Date, DateTime, ForeignKeyConstraint, Index, TEXT, text, Boolean
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship, class_mapper
from sqlalchemy.orm.base import Mapped
from app import db
from sqlalchemy import inspect
from app import logging
from datetime import datetime, date
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

Base = declarative_base()
bcrypt = Bcrypt()

class BaseModel():
    def get_primary_key(self):
        inspector = inspect(self)
        columns = inspector.mapper.columns 
        col_name = [c.description for c in columns if c.primary_key]
        logging.warning(f'primary key: {col_name}')
        if col_name and len(col_name) > 0:
            return getattr(self, col_name[0])
        return None
    
    def to_dict(self):        
        response = {}
        if hasattr(self, '_flagged_attr'):
            for key in self._flagged_attr:
                if hasattr(self, key):
                    value = getattr(self, key)
                    if isinstance(value, datetime.datetime):
                        response[key] = value.strftime("%Y-%m-%d")
                    elif key == '_sa_instance_state':
                        pass
                    elif isinstance(value, BaseModel):
                        response[key] = value.to_dict()
                    elif (isinstance(value, list) and all(isinstance(item, BaseModel) for item in value)):
                        serialized_obj = [val.to_dict() for val in value]
                        response[key] = serialized_obj
                    else:
                        response[key] = value
               
        else:
            columns = [col.key for col in class_mapper(self.__class__).columns]
            response = {col: getattr(self, col) for col in columns}
        logging.info(f'converted object: {response}')
        return response





class BlogPosts(db.Model, BaseModel):
    __tablename__ = 'blog_posts'
    
    def __init__(
        self,
        start_date: Optional[str | date] = None,
        end_date: Optional[str | date] = None,
        **kwargs
    ):
        """
        Initializes a BlogPosts instance, casting date fields if necessary.
        """
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        self.start_date = start_date

        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        self.end_date = end_date

        super().__init__(**kwargs)
    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        if isinstance(value, str):
            self._start_date = datetime.strptime(value, '%Y-%m-%d').date()
        elif isinstance(value, datetime.date):
            self._start_date = value
        else:
            self._start_date = None

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        if isinstance(value, str):
            self._end_date = datetime.strptime(value, '%Y-%m-%d').date()
        elif isinstance(value, datetime.date):
            self._end_date = value
        else:
            self._end_date = None

    id = mapped_column(INTEGER(11), primary_key=True)
    abbreviation = mapped_column(TEXT(10), nullable=False)
    promotion_name = mapped_column(TEXT(255), nullable=False)
    banner_image = mapped_column(TEXT(255), nullable=False)
    upload_folder = mapped_column(TEXT(255), nullable=False)
    start_date = mapped_column(Date)
    end_date = mapped_column(Date)
    main_picture = mapped_column(TEXT(255))
    is_activation = mapped_column(Boolean, nullable=False, default=False)
    feedback_url = mapped_column(TEXT(255), nullable=True, default=None)

    dynamic_page_content: Mapped[List['DynamicPageContent']] = relationship('DynamicPageContent', uselist=True, back_populates='promotion')
    form_submissions: Mapped[List['FormSubmissions']] = relationship('FormSubmissions', uselist=True, back_populates='promotion')
    selected_submissions: Mapped[List['SelectedSubmissions']] = relationship('SelectedSubmissions', uselist=True, back_populates='promotion')


class Users(db.Model, BaseModel, UserMixin):
    __tablename__ = 'users'
    __table_args__ = (
        Index('email', 'email', unique=True),
        Index('username', 'username', unique=True)
    )

    id = mapped_column(INTEGER(11), primary_key=True)
    username = mapped_column(TEXT(150), nullable=False)
    email = mapped_column(TEXT(150), nullable=False)
    password = mapped_column(TEXT(200), nullable=False)
    role = mapped_column(TEXT(50), nullable=False, server_default=text("'user'"))
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class DynamicPageContent(db.Model, BaseModel):
    __tablename__ = 'dynamic_page_content'
    __table_args__ = (
        ForeignKeyConstraint(['blog_id'], ['blog_posts.id'], name='dynamic_page_content_ibfk_1'),
        Index('blog_id', 'blog_id')
    )

    id = mapped_column(INTEGER(11), primary_key=True)
    blog_id = mapped_column(INTEGER(11))
    how_to_enter_html = mapped_column(TEXT)
    prizes_html = mapped_column(TEXT)
    block1_html = mapped_column(TEXT)
    block2_html = mapped_column(TEXT)
    rules_html = mapped_column(TEXT)

    promotion: Mapped[Optional['BlogPosts']] = relationship('BlogPosts', back_populates='dynamic_page_content')
    themes: Mapped[List['Themes']] = relationship('Themes', uselist=True, back_populates='dpc')



class FormSubmissions(db.Model, BaseModel):
    __tablename__ = 'form_submissions'
    __table_args__ = (
        ForeignKeyConstraint(['blog_id'], ['blog_posts.id'], name='form_submissions_ibfk_1'),
        Index('blog_id', 'blog_id')
    )

    id = mapped_column(CHAR(36), primary_key=True)
    blog_id = mapped_column(INTEGER(11), nullable=False)
    title = mapped_column(TEXT(5), nullable=False)
    first_name = mapped_column(TEXT(50), nullable=False)
    last_name = mapped_column(TEXT(50), nullable=False)
    email_addr = mapped_column(TEXT(50), nullable=False)
    phone_num = mapped_column(TEXT(10), nullable=False)
    image = mapped_column(TEXT(255), nullable=False)

    promotion: Mapped['BlogPosts'] = relationship('BlogPosts', back_populates='form_submissions')


class Themes(db.Model, BaseModel):
    __tablename__ = 'themes'
    __table_args__ = (
        ForeignKeyConstraint(['dpc_id'], ['dynamic_page_content.id'], name='themes_ibfk_1'),
        Index('dpc_id', 'dpc_id')
    )

    id = mapped_column(INTEGER(11), primary_key=True)
    name = mapped_column(TEXT(50))
    primary_color = mapped_column(TEXT(7))
    secondary_color = mapped_column(TEXT(7))
    background_color = mapped_column(TEXT(7))
    font_family = mapped_column(TEXT(50))
    font_size = mapped_column(INTEGER(11))
    dpc_id = mapped_column(INTEGER(11))

    dpc: Mapped[Optional['DynamicPageContent']] = relationship('DynamicPageContent', back_populates='themes')


class SelectedSubmissions(db.Model, BaseModel):
    __tablename__ = 'selected_submissions'
    __table_args__ = (
        ForeignKeyConstraint(['blog_id'], ['blog_posts.id'], name='selected_submissions_ibfk_1'),
        Index('blog_id', 'blog_id')
    )

    promotion_winner_id = mapped_column(CHAR(36), primary_key=True)
    blog_id = mapped_column(INTEGER(11), nullable=False)
    reference_number = mapped_column(TEXT(20), nullable=False)
    date_selected = mapped_column(DateTime, nullable=False, server_default=text('current_timestamp()'))

    promotion: Mapped['BlogPosts'] = relationship('BlogPosts', back_populates='selected_submissions')
    badges: Mapped[List['Badges']] = relationship('Badges', uselist=True, back_populates='winner')

class Badges(db.Model, BaseModel):
    __tablename__ = 'badges'
    __table_args__ = (
        ForeignKeyConstraint(['winner_id'], ['selected_submissions.promotion_winner_id'], name='winner_badge_fk'),
        Index('promotion_winner_id_idx', 'winner_id')
    )

    id = mapped_column(INTEGER(11), primary_key=True)
    badge_name = mapped_column(TEXT(80), nullable=False)
    winner_id = mapped_column(CHAR(36), nullable=False)
    badge_description = mapped_column(TEXT(255))

    winner: Mapped['SelectedSubmissions'] = relationship('SelectedSubmissions', back_populates='badges')
