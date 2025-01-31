class Config(object):
    DEBUG = False
    TESTING = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db' 
    # SECRET_KEY = "secret"
    
class DevelopmentConfig(Config): 
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///music.db' 
    SECRET_KEY = "qwerty12345###"
    SECURITY_PASSWORD_SALT = "qwerty12345@#$"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    CACHE_REDIS_URL=  'redis://localhost:6379/2'
    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 250
    