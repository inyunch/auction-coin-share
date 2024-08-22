from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'iab207assesment3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction.sqlite'
    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Initialize other components
    Bootstrap(app)
    login_manager = LoginManager()
    login_manager.login_view = 'authentication.login'
    login_manager.init_app(app)

    # Import and register blueprints
    from auction.views import mainbp
    from auction.listings import listingbp
    from auction.auth import authenticationbp
    app.register_blueprint(mainbp)
    app.register_blueprint(listingbp)
    app.register_blueprint(authenticationbp)

    # Error handlers
    @app.errorhandler(404)
    def invalid_route(e):
        return render_template('404.html')

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('500.html')

    return app

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auction.sqlite'
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
#
# print('Flask app is set up correctly to recognize the `db` command')