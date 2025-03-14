from core.database import db

member_file_association = db.Table("member_files",
                                   db.Column("member_id", db.BigInteger, db.ForeignKey(
                                       "members.id"), primary_key=True),
                                   db.Column("file_id", db.BigInteger, db.ForeignKey("files.id"), primary_key=True))
