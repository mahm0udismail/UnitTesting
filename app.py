from flask import Flask
from routes import init_routes
from database import init_db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = init_db(app)

init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
