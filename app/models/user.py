from flask_sqlalchemy import BaseQuery
from flask_login import UserMixin

from extensions import db


class GetUserQuery(BaseQuery):
    def get_user(self, user_id):
        return self.filter_by(google_user_id=str(user_id)).first()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    query_class = GetUserQuery

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    google_user_id = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.now())

    def get_id(self):
        return self.google_user_id
