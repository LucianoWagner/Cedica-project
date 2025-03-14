import datetime

from flask import current_app
from flask.globals import app_ctx
from minio import S3Error
from sqlalchemy.sql import func

from core.database import db
from core.files import generate_presigned_url


class Horse(db.Model):
    __tablename__ = 'horses'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    sex = db.Column(db.Text, nullable=False)
    race = db.Column(db.Text, nullable=False)
    fur = db.Column(db.Text, nullable=False)
    origin = db.Column(db.Enum('Compra', 'Donacion',
                       name='horse_origin'), nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False)
    headquarter = db.Column(db.Text, nullable=False)
    jya_type = db.Column(
        db.Enum('Hipoterapia', 'Monta Terapéutica', 'Deporte Ecuestre', 'Adaptado', 'Actividades Recreativas',
                'Equitación', name='jya_type'), nullable=False)
    createdAt = db.Column(db.DateTime, default=func.now())
    updatedAt = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    trainers = db.relationship('Member', secondary='horse_trainer_association', back_populates='trained_horses',
                               lazy='dynamic')
    riders = db.relationship('Member', secondary='horse_rider_association', back_populates='ridden_horses',
                             lazy='dynamic')
    files = db.relationship('File', secondary='horse_files',
                            back_populates='horses', lazy='dynamic')

    def to_dict(self):
        """
               Convierte el objeto Horse a un diccionario.

               Returns:
                   dict: Diccionario con los datos del caballo.
        """
        # Initialize MinIO client
        minio_client = current_app.storage.client

        def format_date(date):
            """
                        Formatea una fecha a 'dd/mm/yyyy'.

                        Args:
                            date (datetime): La fecha a formatear.

                        Returns:
                            str: La fecha formateada.
            """
            return date.strftime('%d/%m/%Y') if date else None

        # Build the dictionary
        horse_dict = {
            'id': self.id,
            'name': self.name,
            'birth_date': format_date(self.birth_date),
            'sex': self.sex,
            'race': self.race,
            'fur': self.fur,
            'origin': self.origin,
            'entry_date': format_date(self.entry_date),
            'headquarter': self.headquarter,
            'jya_type': self.jya_type,
            'trainers': [{'id': trainer.id, 'name': trainer.person.name, 'surname': trainer.person.surname}
                         for trainer in self.trainers],
            'riders': [{'id': rider.id, 'name': rider.person.name, 'surname': rider.person.surname}
                       for rider in self.riders],
            'files': []
        }

        # Generate presigned URLs for each file
        for file in self.files:
            try:
                url = generate_presigned_url(
                    file.url) if not file.isLink else file.url
                horse_dict['files'].append({
                    'id': file.id,
                    'url': url,
                    "real_url": file.url,
                    'title': file.title,
                    'type': file.type
                })
            except S3Error as e:
                current_app.logger.error(
                    f"Error generating presigned URL for file {file.url}: {e}")

        return horse_dict
