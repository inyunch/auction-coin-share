from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, SelectMultipleField, StringField, PasswordField, IntegerField, DecimalField, SelectField, DateField, TimeField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class GroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired()])
    game = SelectField('Game', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Group')

class AdminAddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    group_id = SelectField('Group', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add User')

class GroupAdminAddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add User')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Game ID', validators=[DataRequired()])
    group_code = StringField('Group Code', validators=[DataRequired()])
    submit = SubmitField('Register')

class GameForm(FlaskForm):
    name = StringField('Game Name', validators=[DataRequired()])
    submit = SubmitField('Add Game')

class BossForm(FlaskForm):
    name = StringField('Boss Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[('world boss', 'World Boss'), ('boss', 'Boss'), ('special', 'Special'), ('other', 'Other')], validators=[DataRequired()])
    submit = SubmitField('Add Boss')
class ItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired()])
    category = SelectField('Category', choices=[('weapon', 'Weapon'), ('armor', 'Armor')], validators=[DataRequired()])
    subcategory = StringField('Subcategory')
    # boss = SelectField('Boss', coerce=int, choices=[], validators=[DataRequired()])
    submit = SubmitField('Add Item')

class EventForm(FlaskForm):
    boss = SelectField('Boss', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    items = SelectMultipleField('Items', coerce=int, validators=[DataRequired()])  # Use SelectMultipleField
    owner = SelectField('Owner', coerce=int, validators=[DataRequired()])
    users = SelectMultipleField('Joining Users', coerce=int, validators=[DataRequired()])  # Use SelectMultipleField
    proof_image = FileField('Proof Image', validators=[
        FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Create Event')

class ListingForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired('Title is required')])
    starting_bid = DecimalField('Starting Bid', validators=[InputRequired('Must enter a starting bid')], render_kw={"placeholder": "$"})
    brand = SelectField('Brand', choices=[('Apple', 'Apple'), ('Microsoft', 'Microsoft'), ('Dell', 'Dell'), ('HP', 'HP'), ('Lenovo', 'Lenovo'), ('Acer', 'Acer')])
    cpu = SelectField('CPU', choices=[('i3', 'i3'), ('i5', 'i5'), ('i7', 'i7'), ('Ryzen 3', 'Ryzen 3'), ('Ryzen 5', 'Ryzen 5'), ('Ryzen 7', 'Ryzen 7')])
    ram = SelectField('RAM', choices=[('4GB', '4GB'), ('8GB', '8GB'), ('16GB', '16GB'), ('32GB', '32GB')])
    storage = SelectField('Storage', choices=[('64GB', '64GB'), ('128GB', '128GB'), ('256GB', '256GB'), ('512GB', '512GB'), ('1TB', '1TB')])
    condition = SelectField('Condition', choices=[('Excellent', 'Excellent'), ('Good', 'Good'), ('Minor defects', 'Minor defects'), ('Used', 'Used'), ('New', 'New')])
    end_date = DateField('End Date', format='%d/%m/%Y', render_kw={"placeholder": "dd/mm/yyyy"})
    ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG', 'jpeg'}
    image_url = FileField('Image', validators=[
        FileRequired(message='Image can not be empty'), FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
    description = TextAreaField('Description', validators=[InputRequired('Description is required'), Length(min=10, max=300, message='Description is too short or too long')], render_kw={"placeholder": "Description of listing..."})
    submit = SubmitField('Post Listing')

class ReviewForm(FlaskForm):
    title = StringField('Title', [InputRequired('Title is required'), Length(min=1, max=20, message='Title is too long')], render_kw={"placeholder": "Example: Great Features!"})
    feedback = TextAreaField('Review', [InputRequired('Review is required'), Length(min=5, max=400, message='Review is too long or too short')], render_kw={"placeholder": "Example: I bought this laptop a month ago and it has been great so far!"})
    submit = SubmitField('Post Review') 

class BidForm(FlaskForm):
    bid_amount = DecimalField('', validators=[InputRequired()], render_kw={"placeholder": "Bid amount..."})
    submit = SubmitField('Place Bid')