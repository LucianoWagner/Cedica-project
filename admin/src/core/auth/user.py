from core.database import db
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    alias = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text)
    role_id = db.Column(db.BigInteger, db.ForeignKey(
        'roles.id'), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    member_id = db.Column(db.BigInteger, db.ForeignKey(
        'members.id'), nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(
        db.DateTime, server_default=func.now(), onupdate=func.now())
    publications = db.relationship('Publication', back_populates='user')

    def __init__(self, email, alias, password, role_id, member_id, is_approved):
        """
                Inicializa una instancia de User.

                Args:
                    email (str): El correo electrónico del usuario.
                    alias (str): El alias del usuario.
                    password (str): La contraseña del usuario.
                    role_id (int): El ID del rol del usuario.
                    member_id (int): El ID del miembro asociado al usuario.
        """
        self.email = email
        self.alias = alias
        self.password = password
        self.role_id = role_id
        self.member_id = member_id
        self.active = True
        self.is_approved = is_approved

    def __repr__(self):
        """
                Representación en cadena del usuario.

                Returns:
                    str: El correo electrónico del usuario.
        """
        return '<User %r>' % self.email
