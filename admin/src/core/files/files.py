from datetime import timedelta

from flask import current_app
from minio import S3Error
from sqlalchemy.sql import func
from core.database import db


class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.BigInteger, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    isLink = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, server_default=func.now())
    updatedAt = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now())
    members = db.relationship(
        'Member', secondary='member_files', back_populates='files', lazy='dynamic')
    horses = db.relationship(
        'Horse', secondary='horse_files', back_populates='files', lazy='dynamic')
    jya = db.relationship('Jya', secondary='jya_files',
                          back_populates='files', lazy='dynamic')

    def get_show_data(self):
        """
                Obtiene los datos para mostrar del archivo.

                Returns:
                    dict: Un diccionario con los datos del archivo.
        """
        try:
            url = self.get_presigned_url() if not self.isLink else self.url
            return {
                'id': self.id,
                'url': url,
                "real_url": self.url,
                'title': self.title,
                'type': self.type
            }
        except S3Error as e:
            return {
                'id': self.id,
                'url': None,
                'title': self.title,
                'type': self.type
            }

    def get_presigned_url(self):
        """
                Obtiene una URL pre-firmada para el archivo.

                Returns:
                    str: La URL pre-firmada.
        """
        client = current_app.storage.client
        return client.presigned_get_object(current_app.config.get("STORAGE_BUCKET"), self.url,
                                           expires=timedelta(days=1))
