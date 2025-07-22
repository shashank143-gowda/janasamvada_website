from app import create_app
from app.models.models import db, User
from datetime import datetime

app = create_app()

def create_new_admin():
    with app.app_context():
        # Create a new admin user with a different username
        new_admin_username = 'superadmin'
        
        # Check if this admin already exists
        existing_admin = User.query.filter_by(username=new_admin_username).first()
        if existing_admin:
            print(f"Admin user '{new_admin_username}' already exists!")
            print(f"Username: {existing_admin.username}")
            print(f"Email: {existing_admin.email}")
            
            # Reset password
            password = 'Admin123'
            existing_admin.set_password(password)
            existing_admin.role = 'admin'  # Ensure role is set to admin
            db.session.commit()
            
            print(f"Password has been reset to: {password}")
            return
        
        # Create new admin user
        new_admin = User(
            username=new_admin_username,
            email='superadmin@jansamvaad.org',
            phone='9876543210',
            village='Admin Village',
            district='Admin District',
            state='Admin State',
            reward_points=1000,
            role='admin',  # Explicitly set role to admin
            last_login=datetime.utcnow(),
            created_at=datetime.utcnow()
        )
        
        password = 'Admin123'
        new_admin.set_password(password)
        
        db.session.add(new_admin)
        db.session.commit()
        
        print(f"New admin user '{new_admin_username}' created successfully!")
        print("\nAdmin Credentials:")
        print(f"Username: {new_admin_username}")
        print(f"Email: superadmin@jansamvaad.org")
        print(f"Password: {password}")
        print("\nPlease try logging in with these credentials.")

if __name__ == '__main__':
    create_new_admin()