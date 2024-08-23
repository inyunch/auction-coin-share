from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, Group, db, Role
from .utils import generate_group_code
from .models import Group, db, Role
from .forms import CreateGroupForm


adminbp = Blueprint('admin', __name__)

@adminbp.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    if current_user.role != Role.ADMIN:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    form = CreateGroupForm()  # Create an instance of the form

    if form.validate_on_submit():
        name = form.name.data
        code = generate_group_code()
        new_group = Group(name=name, code=code)
        db.session.add(new_group)
        db.session.commit()
        flash(f'Group {name} created with code {code}', 'success')
        return redirect(url_for('admin.manage_groups'))

    return render_template('create_group.html', form=form)  # Pass the form to the template

@adminbp.route('/manage_groups')
@login_required
def manage_groups():
    if current_user.role != Role.ADMIN:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    groups = Group.query.all()
    return render_template('manage_groups.html', groups=groups)

@adminbp.route('/manage_users')
@login_required
def manage_users():
    if current_user.role != Role.ADMIN:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    users = User.query.all()
    return render_template('manage_users.html', users=users)

@adminbp.route('/assign_role/<int:user_id>', methods=['POST'])
@login_required
def assign_role(user_id):
    if current_user.role != Role.ADMIN:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)
    role = request.form.get('role')
    if role in [Role.ADMIN, Role.ACCOUNTANT, Role.USER]:
        user.role = role
        db.session.commit()
        flash(f'Role {role} assigned to {user.username}', 'success')
    else:
        flash('Invalid role', 'danger')
    return redirect(url_for('admin.manage_users'))
