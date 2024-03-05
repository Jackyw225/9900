import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import UserModel, CaptchaModel
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="email format erro！")])
    captcha = wtforms.StringField(validators=[Length(min=6, max=6, message="Captcha erro！")])
    name = wtforms.StringField(validators=[Length(min=3, max=20, message="Name erro")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="password too long or too short, it should between 6-20")])
    # password_confirm = wtforms.StringField(validators=[EqualTo("Password not the same")])

    def vaild_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message='This email has been register')

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = CaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='Captcha not right！')
