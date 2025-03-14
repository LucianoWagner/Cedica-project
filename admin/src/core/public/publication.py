from core.database import db
from sqlalchemy.sql import func


class Publication(db.Model):
    __tablename__ = 'publications'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    publication_date = db.Column(db.DateTime, nullable=True, default=None)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=func.now(), onupdate=func.now())
    title = db.Column(db.String(150), nullable=False)
    summary = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey(
        'users.id'), nullable=False)
    status = db.Column(db.Enum('Borrador', 'Archivada',
                       'Publicada', name='publication_status'), nullable=False)
    user = db.relationship('User', back_populates='publications')

    # def to dict
    def to_dict(self):
        return {
            "id": self.id,
            "publication_date": self.publication_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "title": self.title,
            "summary": self.summary,
            "content": self.content,
            "user_id": self.user_id,
            "status": self.status
        }
