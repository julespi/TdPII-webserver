import os


class DevJulian:
    # General Config
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'asdasdKMASDbgbfpAPS_)()'
    SESSION_COOKIE_NAME = 'TdPII_cookie'
    SQLALCHEMY_DATABASE_URI = 'mysql://usuario:asdasd@localhost/g20_tdp2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevMarcos:
    # General Config
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'asdasdKMASDbgbfpAPS_)()'
    SESSION_COOKIE_NAME = 'TdPII_cookie'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:''@localhost/g20_tdp2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    