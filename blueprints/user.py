from flask import Blueprint, render_template
from exts import mail
from flask_mail import Message

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login')
def login():
    pass


@bp.route('/register')
def register():
    return render_template('register.html')

@bp.route('/mail')
def mail_test():
    message = Message(
        subject='测试邮件',
        recipients=['zhenjiew@126.com'],  # 替换为接收者的邮箱地址
        body='这是一封来自 Flask-Mail 的测试邮件！'
    )
    mail.send(message)
    return 'success'
