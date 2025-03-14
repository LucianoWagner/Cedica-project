from core.database import db
from core.finance import Payment


def create_payment(**kwargs):
    new_payment = Payment(**kwargs)
    db.session.add(new_payment)
    db.session.commit()
    return new_payment
