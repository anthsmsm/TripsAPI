from decouple import config
class Config:
    SECRET_KEY=config('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig
}