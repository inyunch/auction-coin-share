from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'iab207assesment3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction_dev.sqlite'
    db.init_app(app)
    migrate = Migrate(app, db)
    bootstrap = Bootstrap(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect to login page

    # Import and register blueprints
    from .views import mainbp
    from .listings import listingbp
    from .auth import authbp
    from .admin import adminbp
    app.register_blueprint(mainbp)
    app.register_blueprint(listingbp)
    # app.register_blueprint(authbp)
    app.register_blueprint(authbp, url_prefix='/auth')
    app.register_blueprint(adminbp, url_prefix='/admin')

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))