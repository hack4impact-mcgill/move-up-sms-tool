import os

class Config:
    APP_NAME = "Move Up SMS Sign-Up Tool"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"

    @property
    def DATABASE_URL(self):
        if os.getenv("FLASK_CONFIG")=='production':
            return str(os.environ.get("PROD_URL"))
        else: return str(os.environ.get("DEV_URL"))

    @property
    def QUESTIONS_URL(self):
        if os.getenv("FLASK_CONFIG")=='production':
            return str(os.environ.get("PROD_QUESTIONS_URL"))
        else: return str(os.environ.get("DEV_QUESTIONS_URL"))
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    PRODUCTION = True

config = {
    "development": DevelopmentConfig(),
    "testing": TestingConfig(),
    "production": ProductionConfig(),
    "default": DevelopmentConfig(),
}
