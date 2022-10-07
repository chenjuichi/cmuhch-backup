#import os

#myKey=os.urandom(16).hex()
#print(myKey)

class Config:
    #CSRF_ENABLED = True
    SECRET_KEY = 'bf294d4ad47d241ea4047d39cbb6a993'     #from myKey, just once
    DEBUG = True
    TESTING = True

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
