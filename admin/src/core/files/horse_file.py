from core.database import db

horse_file_association = db.Table("horse_files",
                                  db.Column("horse_id", db.BigInteger, db.ForeignKey(
                                      "horses.id"), primary_key=True),
                                  db.Column("file_id", db.BigInteger, db.ForeignKey("files.id"), primary_key=True))
