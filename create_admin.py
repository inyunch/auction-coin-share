from werkzeug.security import generate_password_hash
from auction import create_app, db
from auction.models import User, Role

app = create_app()

with app.app_context():
    # Check if an admin user already exists
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        # Create a new admin user
        admin_user = User(
            name = 'test_admin',
            username='admin',
            password_hash=generate_password_hash('adminpassword'),  # Use a secure password
            role=Role.ADMIN
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")