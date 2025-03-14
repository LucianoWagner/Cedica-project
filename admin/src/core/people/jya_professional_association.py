from core.database import db

# Tabla de asociación entre Jya y Member
jya_professional_association = db.Table('jya_professional_association',
                                        db.Column('jya_id', db.BigInteger, db.ForeignKey(
                                            'jya.id'), primary_key=True),
                                        db.Column('member_id', db.BigInteger, db.ForeignKey('members.id'),
                                                  primary_key=True)
                                        )
