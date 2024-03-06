import wtforms
import re
from wtforms.validators import Email, Length, EqualTo
from models import UserModel, CaptchaModel


class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="email format erro！")])
    captcha = wtforms.StringField(validators=[Length(min=6, max=6, message="Captcha erro！")])
    name = wtforms.StringField(validators=[Length(min=3, max=20, message="Name erro")])
    password = wtforms.StringField(
        validators=[Length(min=6, max=20, message="password too long or too short, it should between 6-20")])

    # password_confirm = wtforms.StringField(validators=[EqualTo("Password not the same")])

    def check_register_data(self, data):
        email = self.vaild_email(data)
        captcha = self.vaild_email(data)
        if email and captcha:
            return True
        else:
            return False

    def vaild_email(self, data):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        email = data['email']
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message='This email has been register')
        if re.match(pattern, email):
            return True
        else:
            return False

    def validate_captcha(self, data):
        captcha = data['captcha']
        email = data['email']
        captcha_model = CaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='Captcha not right！')
        else:
            return True


def check_register_data(self, data):
    email = self.vaild_email(data)
    captcha = self.vaild_email(data)
    if email and captcha:
        return True
    else:
        return False


def vaild_email(self, data):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    email = data['email']
    user = UserModel.query.filter_by(email=email).first()
    if user:
        raise wtforms.ValidationError(message='This email has been register')
    if re.match(pattern, email):
        return True
    else:
        return False


def validate_captcha(self, data):
    captcha = data['captcha']
    email = data['email']
    captcha_model = CaptchaModel.query.filter_by(email=email, captcha=captcha).first()
    if not captcha_model:
        raise wtforms.ValidationError(message='Captcha not right！')
    else:
        return True


class DictForm(wtforms.Form):
    def __init__(self, data, *args, **kwargs):
        super(DictForm, self).__init__(*args, **kwargs)
        for key, value in data.items():
            setattr(self, key, wtforms.StringField(default=value))
