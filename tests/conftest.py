import pytest
from app import create_app, db
from app.models import Task
from config import TestingConfig


@pytest.fixture
def app():
    """Create and configure a clean Flask application instance for each test."""
    application = create_app(TestingConfig)

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the application to make HTTP requests."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test CLI runner for testing Flask CLI commands."""
    return app.test_cli_runner()


@pytest.fixture
def sample_task(app):
    """Fixture providing a persisted sample Task model instance."""
    with app.app_context():
        task = Task(title="Sample Task for Testing", done=False)
        db.session.add(task)
        db.session.commit()
        # Refresh to attach attributes
        task_id = task.id
    return task_id
