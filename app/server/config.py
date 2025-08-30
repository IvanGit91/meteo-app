import os


class LocalConfig:
    TESTING = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "postgresql://admin:admin@localhost:5433/meteorological"


class DevelopmentConfig:
    TESTING = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('POSTGRES_DB')}"


class TestingConfig:
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
