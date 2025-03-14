from core.database import db

jya_file_association = db.Table("jya_files",
                                db.Column("jya_id", db.BigInteger, db.ForeignKey(
                                    "jya.id"), primary_key=True),
                                db.Column("file_id", db.BigInteger, db.ForeignKey("files.id"), primary_key=True))
