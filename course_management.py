from flask import Flask
from flask_migrate import Migrate
import config
from exts import db, mail
from blueprints.user import bp as user_bp
from models import UserModel

print('hello word')