from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, Group, db, Role
from .utils import generate_group_code
from .forms import CreateGroupForm, AddUserForm
from werkzeug.security import generate_password_hash


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

    return render_template('authentication/create_group.html', form=form)  # Pass the form to the template

@adminbp.route('/manage_groups', methods=['GET'])
@login_required
def manage_groups():
    # Allow access to admins and group admins
    if current_user.role not in ['admin', 'group_admin']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    # Admins can see all groups, group admins can only see their own group
    if current_user.role == 'admin':
        groups = Group.query.all()
    else:
        # Assuming each group admin is assigned to a specific group
        groups = Group.query.filter_by(id=current_user.group_id).all()

    return render_template('authentication/manage_groups.html', groups=groups)

@adminbp.route('/manage_users/<int:group_id>', methods=['GET', 'POST'])
@login_required
def manage_users(group_id):
    # Allow access to admins and group-level roles
    if current_user.role not in ['admin', 'group_admin', 'accountant']:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    # Filter users by the specified group ID
    users = User.query.filter_by(group_id=group_id).all()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_role = request.form.get('role')
        user = User.query.get(user_id)
        if user:
            user.role = new_role
            db.session.commit()
            flash(f'Role updated to {new_role} for user {user.username}.', 'success')
        else:
            flash('User not found.', 'danger')

    return render_template('authentication/manage_users.html', users=users)


@adminbp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    # Ensure that only group admins can access this page
    if current_user.role != 'group_admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    form = AddUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data
        group_id = current_user.group_id  # Set group_id to the group admin's group_id

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('admin.add_user'))

        # Create new user
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password),
            name=name,
            role='user',  # Default role
            group_id=group_id
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully.', 'success')
        return redirect(url_for('admin.manage_users', group_id=group_id))

    return render_template('authentication/add_user.html', form=form)