import wtforms
from wtforms.validators import length, email, EqualTo
from models import EmailCaptchaModel, UserModel


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


class RegisterForm(wtforms.Form):
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirmation = wtforms.StringField(validators=[EqualTo('password')])

    def validate_captcha(self, field):
        captcha = field.data  # captcha that user entered
        input_email = self.email.data  # email that user entered
        # email and captcha recorded in the system, captcha_model.email, captcha_model.captcha
        captcha_model = EmailCaptchaModel.query.filter_by(email=input_email).first()

        if not captcha_model or captcha_model.captcha != captcha:
            raise wtforms.ValidationError('captcha is not correct')

    def validate_email(self, field):
        input_email = field.data
        user_model = UserModel.query.filter_by(email=input_email).first()
        if user_model:
            raise wtforms.ValidationError('email already exists')


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=5, max=100)])
    content = wtforms.StringField(validators=[length(min=5)])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[length(min=1)])
