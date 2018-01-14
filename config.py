
class Config:
    SECRET_KEY = "d89ryr0989gygVSDGVGYGVGYGAV7W89hgshjvs"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_ACCESS = ['access']
    

class DevelopmentConfig(Config):
    RESTPLUS_VALIDATE = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:7910@localhost/api"


class TestingConfig(Config):
    RESTPLUS_VALIDATE = False
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:7910@localhost/test_api"
    

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "database uri"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
