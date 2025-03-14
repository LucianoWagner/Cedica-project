from core.database import db


class Person(db.Model):
    __tablename__ = 'people'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text, nullable=False)
    dni = db.Column(db.BigInteger, nullable=False)
    address = db.Column(db.Text, nullable=False)
    telephone = db.Column(db.Text, nullable=False)
    emergency_contact = db.Column(db.Text, nullable=False)

    member = db.relationship('Member', backref='person', uselist=False)
    jya = db.relationship('Jya', backref='person', uselist=False)

    def to_dict(self):
        """
        Convierte el objeto Person a un diccionario.
        return: dict: Diccionario con los datos de la persona.
        """
        return {

            "name": self.name,
            "surname": self.surname,
            "dni": self.dni,
            "address": self.address,
            "telephone": self.telephone,
            "emergency_contact": self.emergency_contact
        }
