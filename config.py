
class Config:
    SECRET_KEY = "d89ryr0989gygVSDGVGYGVGYGAV7W89hgshjvs"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:7910@localhost/yummy"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "databse uri"
    # WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "database uri"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
