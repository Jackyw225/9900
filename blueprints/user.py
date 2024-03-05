from flask import Blueprint, render_template, jsonify
from exts import mail, db
from flask_mail import Message
from flask import request
import random
import string
from models import UserModel, CaptchaModel

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login')
def login():
    pass


@bp.route('/register')
def register():
    return render_template('register.html')


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
