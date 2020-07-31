import os

from flask import Flask, Blueprint
from flask_login import current_user
from flask_cors import CORS

from extensions import db, login_manager
import auth

top_bp = Blueprint('top', __name__, url_prefix='/')


@top_bp.route('/')
def index():
    if current_user.is_authenticated:
        return (
            f"<p>Hello, {current_user.name}! ログインできてるよ"
            f"You're logged in! Email: {current_user.email}</p>"
            '<a class="button" href="/auth/logout">Logout</a>'
        )
    else:
        return '<p>Hello! ログインしてないよ</p>' \
               '<a class="button" href="/auth/login">Google Login</a>'


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.secret_key = os.environ.get('SECRET_KEY')

    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.user_loader(load_user)

    app.register_blueprint(auth.bp)
    app.register_blueprint(top_bp)

    return app


def load_user(user_id):
    from models.user import User
    return User.query.get_user(user_id)
