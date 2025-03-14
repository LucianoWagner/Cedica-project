

from core.database import db
from sqlalchemy.sql import func


class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
