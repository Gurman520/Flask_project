import datetime
import sqlalchemy
from sqlalchemy import orm, Table, Column, ForeignKey
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash

Articles_user_table = Table("Articles_user_table", SqlAlchemyBase.metadata,
                            Column('article_id', ForeignKey('article.id')),
                            Column('user_id', ForeignKey('user.id')))

Article_to_tags = Table('Article_to_tags', SqlAlchemyBase.metadata,
                        Column('article_id', ForeignKey('article.id')),
                        Column('tag_id', ForeignKey('tag.id')))


class Tag(SqlAlchemyBase):
    __tablename__ = 'tag'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String)


class Article(SqlAlchemyBase):
    __tablename__ = 'article'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('user.id'))
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    create_data = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    status = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    tags = orm.relation("Tag", secondary="Article_to_tags", backref="article")
    user = orm.relation('User')


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    access_level = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    country = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    sex = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    vk = sqlalchemy.Column(sqlalchemy.String)
    GitHub = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
