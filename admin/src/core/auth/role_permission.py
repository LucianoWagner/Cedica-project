from core.database import db


role_permissions_association = db.Table(
    'role_permissions',
    db.Column('role_id', db.BigInteger, db.ForeignKey(
        'roles.id'), primary_key=True),
    db.Column('permission_id', db.BigInteger, db.ForeignKey(
        'permissions.id'), primary_key=True)
)
