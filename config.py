import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback-secret-key-change-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration with debug mode and local SQLite database."""
    DEBUG = True
    TESTING = False
    _db_url = os.environ.get("DATABASE_URL")
    if _db_url and _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    elif not _db_url:
        _db_url = f"sqlite:///{os.path.join(basedir, 'tasks_dev.db')}"
    SQLALCHEMY_DATABASE_URI = _db_url


class TestingConfig(Config):
    """Testing configuration with isolated in-memory SQLite database."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration with strict environment variable bindings and Vercel compatibility."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "taskflow-prod-secret-fallback-key-2026"
    _db_url = os.environ.get("DATABASE_URL")
    if _db_url and _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    elif not _db_url:
        if os.environ.get("VERCEL"):
            _db_url = "sqlite:////tmp/tasks.db"
        else:
            _db_url = f"sqlite:///{os.path.join(basedir, 'tasks_dev.db')}"
    SQLALCHEMY_DATABASE_URI = _db_url


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
