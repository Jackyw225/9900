from flask import Blueprint, render_template, jsonify, redirect
from exts import mail, db
from flask_mail import Message
from flask import request
import random
import string
from models import UserModel, CaptchaModel
from form import RegisterForm
from werkzeug.security import generate_password_hash

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login')
def login():
    pass


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(register.form)
        if form.validate():
            email = form.email.data
            name = form.name.data
            password = form.password.data
            user_info = UserModel(email=email, name=name, password=generate_password_hash(password))
            db.session.add(user_info)
            db.session.commit()
            return redirect('user/login')
        else:
            return 'fail'



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
