from flask import Blueprint, render_template, request, redirect, url_for, flash 
from auction.models import Listing
from sqlalchemy import or_
from flask_login import login_required, current_user
from .models import db, User, Group
from .forms import GroupForm
from .utils import generate_group_code

# Create main blueprint
mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    listings = Listing.query.filter_by(status='Active').all()
    return render_template('index.html', listings=listings)

@mainbp.route('/search')
def search():
    #get the search string from request
    if request.args['search']:
        item = "%" + request.args['search'] + '%'
    #use filter and like function to search for matching item
        listing = Listing.query.filter(
            or_(
                Listing.title.like(item),
                Listing.cpu.like(item),
                Listing.brand.like(item),
                Listing.ram_gb.like(item),
                Listing.storage_gb.like(item)
            ), Listing.status=='Active'
        )
        # Search result message 
        resultMessage = "{0} results matching '{1}'".format(listing.count(), request.args['search'])
        flash (resultMessage)
        return render_template('index.html', listings=listing)
    else:
        return redirect(url_for('main.index'))

@mainbp.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    if current_user.role != Role.ADMIN:
        abort(403)
    form = GroupForm()
    if form.validate_on_submit():
        code = generate_group_code()
        new_group = Group(name=form.name.data, code=code)
        db.session.add(new_group)
        db.session.commit()
        flash(f'Group {new_group.name} created with code {new_group.code}', 'success')
        return redirect(url_for('manage_groups'))
    return render_template('create_group.html', form=form)

@mainbp.route('/assign_role/<int:user_id>', methods=['POST'])
@login_required
def assign_role(user_id):
    if current_user.role != Role.ADMIN:
        abort(403)
    user = User.query.get_or_404(user_id)
    role = request.form.get('role')
    if role in [Role.ADMIN, Role.ACCOUNTANT_GROUP_ADMIN, Role.USER]:
        user.role = role
        db.session.commit()
        flash(f'Role {role} assigned to {user.username}', 'success')
    else:
        flash('Invalid role', 'danger')
    return redirect(url_for('manage_users'))