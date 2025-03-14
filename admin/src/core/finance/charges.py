from sqlalchemy import func
from core.database import db


class Charge(db.Model):
    __tablename__ = "charges"

    id = db.Column(db.BigInteger, primary_key=True)
    member_id = db.Column(db.BigInteger, db.ForeignKey('members.id'))
    jya_id = db.Column(db.BigInteger, db.ForeignKey('jya.id'))
    date = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    observations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now())

    member = db.relationship("Member", back_populates="charges")
    jya = db.relationship("Jya", back_populates="charges")
