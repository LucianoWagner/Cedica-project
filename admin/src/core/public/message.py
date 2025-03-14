from core.database import db
from sqlalchemy.sql import func


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=func.now(), onupdate=func.now())
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    body = db.Column(db.String(150), nullable=True)
    status = db.Column(db.Enum('Pendiente', 'Contestada',
                       name='status'), nullable=False, default='Pendiente')
    comment = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "full_name": self.full_name,
            "email": self.email,
            "body": self.body,
            "status": self.status,
            "comment": self.comment
        }
