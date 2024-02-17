import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = "mysecretkey"
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.sqlite3")
    DEBUG = True