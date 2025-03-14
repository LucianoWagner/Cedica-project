from core.database import db

horse_rider_association = db.Table("horse_rider_association",
                                   db.Column("member_id", db.BigInteger, db.ForeignKey(
                                       "members.id"), primary_key=True),
                                   db.Column("horse_id", db.BigInteger, db.ForeignKey("horses.id"), primary_key=True))
