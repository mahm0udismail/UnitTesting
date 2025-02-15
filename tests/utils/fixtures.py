import pytest
from app import app, db

@pytest.fixture(scope="session")
def test_client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

    with app.test_client() as client:
        with app.app_context():
            db.session.rollback()
        yield client
