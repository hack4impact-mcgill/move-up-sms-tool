import os

class Config:
    APP_NAME = "Move Up Sign-Up Tool"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    DATABASE_URL = str(os.environ.get("DEV_URL"))

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    PRODUCTION = True
    DATABASE_URL = str(os.environ.get("PROD_URL"))

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
