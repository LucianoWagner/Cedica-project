
from core.database import db
from sqlalchemy.sql import func


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    users = db.relationship('User', backref='role', lazy="dynamic")
    permissions = db.relationship(
        'Permission', secondary='role_permissions', lazy='dynamic', backref='roles')
