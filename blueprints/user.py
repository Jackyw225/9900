import json
import re
from flask import Blueprint, render_template, jsonify, redirect
from exts import mail, db
from flask_mail import Message
from flask import request
import random
import string
from models import UserModel, CaptchaModel
from werkzeug.security import generate_password_hash

bp = Blueprint('user', __name__, url_prefix='/user')

def check_register_data(data):
    email = vaild_email(data)
    captcha = validate_captcha(data)
    if email + captcha == 0:
        return 0
    elif not email:
        return email
    else:
        return captcha


def vaild_email(data):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    email = data['email']
    user = UserModel.query.filter_by(email=email).first()
    if user:
        return 'User already exists'
    if re.match(pattern, email):
        return 0
    else:
        return 'Invalid email'


def validate_captcha(data):
    captcha = data['captcha']
    email = data['email']
    captcha_model = CaptchaModel.query.filter_by(email=email, captcha=captcha).first()
    if not captcha_model:
        return 'captcha wrong'
    else:
        return 0

@bp.route('/login')
def login():
    return jsonify({'code': 500, 'message': 'check', 'data': ''})


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register1.html')
    else: ## post
        data = request.json
        check = check_register_data(data)
        if check == 0:
            email = data['email']
            name = data['email']
            password = data['password']
            user_info = UserModel(email=email, name=name, password=password)
            db.session.add(user_info)
            db.session.commit()
            return jsonify({'code': 200, 'message': '', 'data': ''})
        else:
            return jsonify({'code': 500, 'message': check, 'data': ''})



@bp.route('/register/captcha')
def captcha():
    email = request.args.get('email')
    source = string.digits * 6
    captcha = random.sample(source, 6)
    captcha = ''.join(captcha)
    message = Message(
        subject='Your captcha',
        recipients=[email],
        body='This is your captcha: ' + captcha
    )
    db_captcha = CaptchaModel(email=email, captcha=captcha)
    db.session.add(db_captcha)
    db.session.commit()
    mail.send(message)
    return jsonify({'code': 200, 'message': '', 'data': ''})
