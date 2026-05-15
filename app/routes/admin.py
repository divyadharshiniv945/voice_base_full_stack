from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from app.decorators.auth import admin_required, active_required
from app.models.user import User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
@active_required
@admin_required
def dashboard():
    users = User.query.order_by(User.created_at.desc()).limit(5).all()
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    return render_template('admin/dashboard.html', users=users, total_users=total_users, active_users=active_users)


@admin_bp.route('/users')
@login_required
@active_required
@admin_required
def users():
    search = request.args.get('search', '').strip()
    page = request.args.get('page', 1, type=int)
    query = User.query.order_by(User.created_at.desc())

    if search:
        query = query.filter(or_(User.username.contains(search), User.email.contains(search)))

    pagination = query.paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/users.html', pagination=pagination, search=search)


@admin_bp.route('/users/<int:user_id>/role', methods=['POST'])
@login_required
@active_required
@admin_required
def change_role(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot change your own role.', 'warning')
        return redirect(url_for('admin.users'))

    user.role = 'admin' if user.role == 'user' else 'user'
    db.session.commit()
    flash('User role updated successfully.', 'success')
    return redirect(url_for('admin.users', search=request.args.get('search', '')))


@admin_bp.route('/users/<int:user_id>/status', methods=['POST'])
@login_required
@active_required
@admin_required
def toggle_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot change your own account status.', 'warning')
        return redirect(url_for('admin.users'))

    user.is_active = not user.is_active
    db.session.commit()
    flash('Account status updated.', 'success')
    return redirect(url_for('admin.users', search=request.args.get('search', '')))


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@active_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot remove yourself from the system.', 'warning')
        return redirect(url_for('admin.users'))

    db.session.delete(user)
    db.session.commit()
    flash('User removed successfully.', 'success')
    return redirect(url_for('admin.users', search=request.args.get('search', '')))
