from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

from routes.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

from routes.users import users as users_blueprint
app.register_blueprint(users_blueprint, url_prefix='/api/users')

from routes.payment import payment as payment_blueprint
app.register_blueprint(payment_blueprint, url_prefix='/api/payment')

if __name__ == "__main__":
    app.run(debug=True))
