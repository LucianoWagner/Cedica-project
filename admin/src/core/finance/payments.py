from sqlalchemy import func

from core.database import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.BigInteger, primary_key=True)
    member_id = db.Column(db.BigInteger, db.ForeignKey('members.id'))
    amount = db.Column(db.Numeric, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now())

    member = db.relationship("Member", back_populates="payments")
