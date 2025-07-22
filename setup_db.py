from app import create_app
from app.models.models import db, User
from datetime import datetime

app = create_app()

def setup_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin already exists
        existing_admin = User.query.filter_by(username='admin').first()
        if existing_admin:
            print("Admin user already exists!")
            print(f"Username: {existing_admin.username}")
            print(f"Email: {existing_admin.email}")
            print("Password: [Use the password you set during creation]")
            return
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@jansamvaad.org',
            phone='9876543210',
            village='Admin Village',
            district='Admin District',
            state='Admin State',
            reward_points=1000,
            role='admin',  # Explicitly set role to admin
            last_login=datetime.utcnow(),
            created_at=datetime.utcnow()
        )
        admin.set_password('Admin@123')  # Set a secure password
        
        db.session.add(admin)
        db.session.commit()
        
        print("Database initialized successfully!")
        print("Admin user created successfully!")
        print("\nAdmin Credentials:")
        print("Username: admin")
        print("Email: admin@jansamvaad.org")
        print("Password: Admin@123")
        print("\nPlease change the password after first login for security reasons.")

if __name__ == '__main__':
    setup_database()