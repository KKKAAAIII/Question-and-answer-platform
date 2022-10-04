from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, flash
from exts import mail, db
from flask_mail import Message
# when generate model script, remember to import the new model, and ensure the code will run inside the app.py
from models import EmailCaptchaModel, UserModel
from datetime import datetime
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

import string
import random

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        print(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect('/')
            elif not user:
                flash('the email if not registered')
                return redirect(url_for('user.login'))
            else:
                flash('the password is not correct')
                return redirect(url_for('user.login'))
        else:
            flash('the format of the password or the email address is not correct')
            return redirect(url_for('user.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = generate_password_hash(form.password.data)

            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))  # login view func under the user file
        else:
            return redirect(url_for('user.register'))


@bp.route('/logout')
def logout():
    # clear all the data in the session
    session.clear()
    return redirect(url_for('user.login'))

@bp.route('/captcha', methods=['POST'])
def get_captcha():
    # GET, POST
    # when use get: http://127.0.0.1:5000/user/captcha?email= email address
    # email = request.args.get('email')
    # When use post
    email = request.form.get('email')
    if email:
        # create random captcha
        letters = string.ascii_letters + string.digits
        captcha = ''.join(random.sample(letters, 4))

        # create the message you want to send
        message = Message(
            subject='QAA verification code',
            recipients=[email],
            body='Your verification code is ' + captcha
            # sender = already set in config
        )

        # check the existence of the captcha and email
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        # save the email and verification code into the database
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()

        # send the message
        mail.send(message)
        # code:200 means process request successfully
        return jsonify({'code': 200})
    else:
        # code:400 means fail to process request
        return jsonify({'code': 400, 'message': 'fail to provide email address'})
