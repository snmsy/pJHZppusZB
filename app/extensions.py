from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy(
    session_options={
        'autocommit': False,
        'autoflush': False,
    }
)

login_manager = LoginManager()
