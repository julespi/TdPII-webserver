import os


class Development:
    # Configuracion general para el desarrollo, en caso
    # de ser necesario, cada developer debiera tener una
    # clase propia
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'asdasdKMASDbgbfpAPS_)()'
    SESSION_COOKIE_NAME = 'TdPII_cookie'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:''@localhost/g20_tdp2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
