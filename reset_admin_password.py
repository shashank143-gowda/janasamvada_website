from app import create_app
from app.models.models import db, User

app = create_app()

def reset_admin_password():
    with app.app_context():
        # Find admin user
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("Admin user does not exist!")
            return
        
        # Reset password
        new_password = 'admin123'
        admin.set_password(new_password)
        
        # Update role to make sure it's set to admin
        admin.role = 'admin'
        
        db.session.commit()
        
        print("Admin password has been reset successfully!")
        print("\nNew Admin Credentials:")
        print("Username: admin")
        print(f"Password: {new_password}")
        print("\nPlease try logging in with these credentials.")

if __name__ == '__main__':
    reset_admin_password()