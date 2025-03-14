from core.database import db
from sqlalchemy.sql import func

from core.files import generate_presigned_url


class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.BigInteger, primary_key=True)
    person_id = db.Column(db.BigInteger, db.ForeignKey(
        'people.id'), nullable=False)
    email = db.Column(db.Text, nullable=False)
    locality = db.Column(db.Text, nullable=False)
    profession = db.Column(db.Text, nullable=False)
    job_position = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    medical_insurance = db.Column(db.Text, nullable=False)
    insurance_number = db.Column(db.Text, nullable=False)
    job_condition = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    createdAt = db.Column(db.DateTime, server_default=func.now())
    updatedAt = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now())
    user = db.relationship('User', backref='member', uselist=False)
    files = db.relationship('File', secondary='member_files',
                            back_populates='members', lazy='dynamic')
    trained_horses = db.relationship('Horse', secondary='horse_trainer_association', back_populates='trainers',
                                     lazy='dynamic')
    ridden_horses = db.relationship('Horse', secondary='horse_rider_association', back_populates='riders',
                                    lazy='dynamic')
    payments = db.relationship('Payment', back_populates='member')
    charges = db.relationship('Charge', back_populates='member')
    jyas = db.relationship(
        'Jya', secondary='jya_professional_association', back_populates='professionals')

    def to_dict(self):
        """
                Convierte el objeto Member a un diccionario.

                Returns:
                    dict: Diccionario con los datos del miembro.
        """
        horse_dict = {
            "id": self.id,
            "email": self.email,
            "locality": self.locality,
            "profession": self.profession,
            "job_position": self.job_position,
            "start_date": self.start_date.strftime('%d/%m/%Y') if self.start_date else None,
            "end_date": self.end_date.strftime('%d/%m/%Y') if self.end_date else None,
            "medical_insurance": self.medical_insurance,
            "insurance_number": self.insurance_number,
            "job_condition": self.job_condition,
            "active": 1 if self.active else 0,
            "createdAt": self.createdAt.strftime('%d/%m/%Y %H:%M:%S'),
            "updatedAt": self.updatedAt.strftime('%d/%m/%Y %H:%M:%S'),
            "name": self.person.name,
            "surname": self.person.surname,
            "dni": self.person.dni,
            "address": self.person.address,
            "telephone": self.person.telephone,
            "emergency_contact": self.person.emergency_contact,
            "files": []
        }

        for file in self.files:
            url = generate_presigned_url(
                file.url) if not file.isLink else file.url
            horse_dict['files'].append(file.get_show_data())

        return horse_dict
