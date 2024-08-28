from . import db
from datetime import datetime, date
from flask_login import UserMixin


class Role:
    ADMIN = 'admin'  # Website-wide admin
    GROUP_ADMIN = 'group_admin'  # Admin within a specific group
    ACCOUNTANT = 'accountant'  # Accountant within a group
    USER = 'user'  # Normal user within a group

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default=Role.USER)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), nullable=False, unique=True)
    users = db.relationship('User', backref='group', lazy=True)

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Server(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)

class Boss(db.Model):
    __tablename__ = 'bosses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False, default='boss')  # Default category

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    boss_id = db.Column(db.Integer, db.ForeignKey('bosses.id'), nullable=True)  # Optional relationship
    category = db.Column(db.String(50), nullable=False)  # Item category
    subcategory = db.Column(db.String(50), nullable=True)  # Optional subcategory
    # boss = db.relationship('Boss', backref='items', lazy=True)

# class Event(db.Model):
#     __tablename__ = 'events'
#     id = db.Column(Integer, primary_key=True)
#     boss_id = db.Column(Integer, ForeignKey('bosses.id'), nullable=False)
#     date = db.Column(DateTime, nullable=False)
#     time = db.Column(DateTime, nullable=False)
#     proof_image = db.Column(String(400), nullable=False)
#     boss = relationship('Boss', backref='events', lazy=True)
#     items = relationship('Item', backref='event', lazy=True)
#     users = relationship('User', secondary=event_users, backref='events', lazy='dynamic')

class Listing(db.Model):
    __tablename__ = 'listings'
    id = db.Column(db.Integer, primary_key = True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    title = db.Column(db.String(80), nullable = False)
    starting_bid = db.Column(db.Float, nullable = False)
    current_bid = db.Column(db.Float, nullable = False)
    total_bids = db.Column(db.Integer, nullable = False)
    brand = db.Column(db.String(20), nullable = False)
    cpu = db.Column(db.String(10), nullable = False)
    ram_gb = db.Column(db.String(10), nullable = False)
    storage_gb = db.Column(db.String(10), nullable = False)
    description = db.Column(db.String(200), nullable = False)
    condition = db.Column(db.String(10), nullable = False)
    status = db.Column(db.String(10), nullable = False)
    image_url = db.Column(db.String(400), nullable = False)
    end_date = db.Column(db.DateTime, nullable = False)
    seller = db.Column(db.String(15), nullable = False)

    # Relationship to call listing.reviews
    reviews = db.relationship('Review', backref='listingreviews')
    # Relationship to call listing.bids
    bids = db.relationship('Bid', backref='listingbids')

    def set_review(self, review):
        self.reviews.append(review)

class Review(db.Model):
    __tablename__ = 'reviews' 
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80), nullable = False)
    feedback = db.Column(db.String(400), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.now())

    #Foreign Keys
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    listing = db.Column(db.Integer, db.ForeignKey('listings.id'))

    def __repr__(self):
        debug_string = 'User: {}, Title: {}, Feedback: {}'
        debug_string.format(self.user, self.title, self.feedback)
        return debug_string

class WatchListItem(db.Model):
    __tablename__ = 'watchlistitems'
    id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default = datetime.now())

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))

class Bid(db.Model):
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Float, nullable = False)
    bid_date = db.Column(db.DateTime, default = datetime.now())
    bid_status = db.Column(db.String(80), nullable = False)

    # Foreign Keys 
    bidder_name = db.Column(db.String(100), db.ForeignKey('users.name'))
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))
