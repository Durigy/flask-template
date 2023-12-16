from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables from .env file
env_file_path = '.env'
load_dotenv()

app = Flask(__name__)

# secret_key_setting
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# database_setting
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI") if os.getenv("SQLALCHEMY_DATABASE_URI") else ''


# debug_setting
app.config['DEBUG'] = True if os.getenv("DEBUG") == ("True" or True) else False

# https_setting
app.config['HTTPS'] = True if os.getenv("HTTPS") == ("True" or True) else False

# remember_me_cookie_setting
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=int(os.getenv("REMEMBER_COOKIE_DURATION") if os.getenv("REMEMBER_COOKIE_DURATION") else 1))

# sqlalchemy_modifications_setting
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True if os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS") == ("True" or True) else False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

bcrypt = Bcrypt(app)

from . import routes