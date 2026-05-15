from datetime import datetime
from sqlalchemy import or_
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms.auth_forms import RegistrationForm, LoginForm
from app.models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/voice')
def voice():
    return render_template('voice.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.lower().strip(),
            role='user',
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = LoginForm()
    if form.validate_on_submit():
        credential = form.email_or_username.data.strip()
        user = User.query.filter(
            or_(User.email == credential.lower(), User.username == credential)
        ).first()

        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember.data)
            user.last_login = datetime.utcnow()
            db.session.commit()

            next_page = request.args.get('next')
            if user.role == 'admin':
                return redirect(next_page or url_for('admin.dashboard'))

            return redirect(next_page or url_for('dashboard.index'))

        flash('Invalid credentials or account is inactive.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/forgot-password')
def forgot_password():
    return render_template('auth/forgot_password.html')
