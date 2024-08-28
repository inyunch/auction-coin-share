from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, Group, db, Role, Game, Boss, Item
from .utils import generate_group_code
from .forms import GroupForm, AdminAddUserForm, GroupAdminAddUserForm, GameForm, BossForm, ItemForm
from .decorators import role_required
from werkzeug.security import generate_password_hash
from wtforms.fields import SelectField
from wtforms.validators import DataRequired



adminbp = Blueprint('admin', __name__)

@adminbp.route('/add_group', methods=['GET', 'POST'])
@login_required
def add_group():
    form = GroupForm()
    form.game.choices = [(game.id, game.name) for game in Game.query.all()]

    if form.validate_on_submit():
        new_group = Group(
            name=form.name.data,
            code=generate_group_code(),  # Automatically generate the group code
            game_id=form.game.data
        )
        db.session.add(new_group)
        db.session.commit()
        flash('Group added successfully!', 'success')
        return redirect(url_for('admin.manage_groups'))

    return render_template('authentication/add_group.html', form=form)

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
@role_required('group_admin', 'admin')
def add_user():
    if current_user.role == 'admin':
        form = AdminAddUserForm()
        form.group_id.choices = [(group.id, group.name) for group in Group.query.all()]
    else:
        form = GroupAdminAddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        name = form.name.data

        # Determine the group_id based on the role
        if current_user.role == 'group_admin':
            group_id = current_user.group_id
        else:
            group_id = form.group_id.data

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
            role='user',
            group_id=group_id
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('admin.manage_users', group_id=group_id))

    return render_template('authentication/add_user.html', form=form)

@adminbp.route('/manage_games', methods=['GET'])
@login_required
def manage_games():
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    # Query all games
    games = Game.query.all()
    return render_template('game_info/manage_games.html', games=games)


@adminbp.route('/add_game', methods=['GET', 'POST'])
@login_required
def add_game():
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    form = GameForm()
    if form.validate_on_submit():
        new_game = Game(name=form.name.data)
        db.session.add(new_game)
        db.session.commit()
        flash('Game added successfully!', 'success')
        return redirect(url_for('admin.manage_games'))

    return render_template('game_info/add_game.html', form=form)


@adminbp.route('/manage_bosses/<int:game_id>', methods=['GET', 'POST'])
@login_required
def manage_bosses(game_id):
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    game = Game.query.get_or_404(game_id)
    bosses = Boss.query.filter_by(game_id=game.id).all()

    form = BossForm()
    if form.validate_on_submit():
        new_boss = Boss(name=form.name.data, category=form.category.data, game_id=game_id)
        db.session.add(new_boss)
        db.session.commit()
        flash('Boss added successfully!', 'success')
        return redirect(url_for('admin.manage_bosses', game_id=game_id))

    return render_template('game_info/manage_bosses.html', game=game, bosses=bosses, form=form)

@adminbp.route('/manage_items/<int:game_id>', methods=['GET', 'POST'])
@login_required
def manage_items(game_id):
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    game = Game.query.get_or_404(game_id)
    items = Item.query.filter_by(game_id=game.id).all()

    form = ItemForm()
    # form.boss.choices = [(boss.id, boss.name) for boss in Boss.query.filter_by(game_id=game_id).all()]

    if form.validate_on_submit():
        new_item = Item(
            name=form.name.data,
            category=form.category.data,
            subcategory=form.subcategory.data,
            game_id=game_id,
            # boss_id=form.boss.data if form.boss.data else None
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully!', 'success')
        return redirect(url_for('admin.manage_items', game_id=game_id))

    return render_template('game_info/manage_items.html', game=game, items=items, form=form)