from app import create_app
from app.models.models import db, User
import requests

app = create_app()

def test_login():
    with app.app_context():
        # First, make sure admin exists with correct password
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Admin user does not exist!")
            return
        
        # Set a known password for testing
        test_password = 'admin123'
        admin.set_password(test_password)
        db.session.commit()
        
        print(f"Admin user prepared with password: {test_password}")
        
        # Now test if the password works with the check_password method
        if admin.check_password(test_password):
            print("Password verification works correctly with check_password method")
        else:
            print("ERROR: Password verification fails with check_password method")
        
        print("\nAdmin credentials for login:")
        print(f"Username: {admin.username}")
        print(f"Password: {test_password}")
        print("\nPlease try logging in with these credentials.")

if __name__ == '__main__':
    test_login()