from core.database import db
from sqlalchemy.sql import func

from core.files import generate_presigned_url


class Jya(db.Model):
    __tablename__ = 'jya'

    id = db.Column(db.BigInteger, primary_key=True)
    person_id = db.Column(db.BigInteger, db.ForeignKey(
        'people.id'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    birth_place = db.Column(db.Text)
    granted = db.Column(db.Boolean, nullable=False)
    grant_percentage = db.Column(db.Float)
    behind_payment = db.Column(db.Boolean, default=False, nullable=False)
    createdAt = db.Column(db.DateTime, default=func.now())
    updatedAt = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
    files = db.relationship('File', secondary='jya_files',
                            back_populates='jya', lazy='dynamic')
    charges = db.relationship('Charge', back_populates='jya')
    professionals = db.relationship(
        'Member', secondary='jya_professional_association', back_populates='jyas')

    def to_dict(self):
        """
                Convierte el objeto Jya a un diccionario.

                Returns:
                    dict: Diccionario con los datos del JYA.
        """
        jya_dict = {

            "age": self.age,
            "birth_date": self.birth_date.strftime('%d/%m/%Y'),
            "birth_place": self.birth_place,
            "granted": self.granted,
            "grant_percentage": self.grant_percentage,
            "behind_payment": self.behind_payment,
            "files": [],
            "professionals": [professional.id for professional in self.professionals],
            **self.person.to_dict(),

        }

        for file in self.files:
            url = generate_presigned_url(
                file.url) if not file.isLink else file.url
            jya_dict['files'].append(file.get_show_data())

        return jya_dict
