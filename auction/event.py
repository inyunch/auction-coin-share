
from werkzeug.utils import secure_filename
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Event, Boss, Item, User, db
from .forms import EventForm
from datetime import datetime


eventbp = Blueprint('event', __name__)

@eventbp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    form.boss.choices = [(boss.id, boss.name) for boss in Boss.query.all()]
    form.items.choices = [(item.id, item.name) for item in Item.query.all()]
    form.owner.choices = [(user.id, user.username) for user in User.query.filter_by(group_id=current_user.group_id).all()]
    form.users.choices = [(user.id, user.username) for user in User.query.filter_by(group_id=current_user.group_id).all()]

    if form.validate_on_submit():
        # Check the image file
        db_file_path = check_upload_file(form)

        # Combine date and time into a single datetime object
        event_datetime = datetime.combine(form.date.data, form.time.data)

        # Create a new event
        new_event = Event(
            boss_id=form.boss.data,
            group_id=current_user.group_id,  # Assign the current user's group_id
            datetime=event_datetime,  # Use the combined datetime
            proof_image=db_file_path
        )
        # Add items and users
        for item_id in form.items.data:
            item = Item.query.get(item_id)
            if item:
                new_event.items.append(item)
        for user_id in form.users.data:
            user = User.query.get(user_id)
            if user:
                new_event.users.append(user)

        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('event.manage_events'))

    return render_template('event/create_event.html', form=form)

@eventbp.route('/manage_events', methods=['GET'])
@login_required
def manage_events():
    events = Event.query.filter_by(group_id=current_user.group_id).all()  # Filter by group_id
    return render_template('event/manage_events.html', events=events)

@eventbp.route('/event_details/<int:event_id>', methods=['GET'])
@login_required
def show_event_details(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event/event_details.html', event=event)


def check_upload_file(form):
    fp = form.proof_image.data
    filename = secure_filename(fp.filename)
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/uploads', filename)
    db_upload_path = '/static/uploads/' + filename
    fp.save(upload_path)
    return db_upload_path


# def check_upload_file(form):
#   fp = form.image_url.data
#   filename = fp.filename
#   BASE_PATH = os.path.dirname(__file__)
#   upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
#   db_upload_path = '/static/img/'+ secure_filename(filename)
#   fp.save(upload_path)
#   return db_upload_path
