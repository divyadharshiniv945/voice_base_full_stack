from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.decorators.auth import active_required
from app.forms.profile_forms import ProfileForm, PasswordForm
from app.utils.helpers import save_profile_image
from app.models.user import User


dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
@active_required
def index():
    return render_template('dashboard/user_dashboard.html', user=current_user)


@dashboard_bp.route('/dashboard/profile', methods=['GET', 'POST'])
@login_required
@active_required
def profile():
    form = ProfileForm(obj=current_user)
    password_form = PasswordForm()

    if form.validate_on_submit():
        new_username = form.username.data.strip()
        new_email = form.email.data.lower().strip()

        existing_user = User.query.filter(User.email == new_email, User.id != current_user.id).first()
        existing_username = User.query.filter(User.username == new_username, User.id != current_user.id).first()

        if existing_user:
            flash('This email is already in use by another account.', 'warning')
        elif existing_username:
            flash('This username is already taken.', 'warning')
        else:
            current_user.username = new_username
            current_user.email = new_email
            image = form.profile_image.data
            if image:
                image_name = save_profile_image(image)
                if image_name:
                    current_user.profile_image = image_name
            db.session.commit()
            flash('Your profile has been updated.', 'success')
            return redirect(url_for('dashboard.profile'))

    return render_template('dashboard/profile.html', form=form, password_form=password_form, user=current_user)


@dashboard_bp.route('/dashboard/password', methods=['POST'])
@login_required
@active_required
def change_password():
    password_form = PasswordForm()
    form = ProfileForm(obj=current_user)

    if password_form.validate_on_submit():
        if not current_user.check_password(password_form.current_password.data):
            flash('Current password is incorrect.', 'danger')
        else:
            current_user.set_password(password_form.new_password.data)
            db.session.commit()
            flash('Password updated successfully.', 'success')
            return redirect(url_for('dashboard.profile'))

    return render_template('dashboard/profile.html', form=form, password_form=password_form, user=current_user)


@dashboard_bp.route('/dashboard/voice')
@login_required
@active_required
def voice():
    return render_template('dashboard/voice.html', user=current_user)
