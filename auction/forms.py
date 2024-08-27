from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, IntegerField, DecimalField, SelectField, DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm



class CreateGroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired()])
    submit = SubmitField('Create Group')
class AddUserForm(FlaskForm):
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