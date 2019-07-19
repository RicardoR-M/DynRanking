from flask import render_template, flash, request, url_for, redirect
from flask_login import login_user, logout_user, login_required

from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User
from . import auth_blueprint


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, False)
            nextg = request.args.get('next')
            if nextg is None or not nextg.startswith('/'):
                nextg = url_for('index.index')
            return redirect(nextg)
        flash('Invalid username or password')
    return render_template('auth/login.html', form=form)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
# @login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Se registro correctamente!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))
