from app import create_app
from app.models.models import db, User

app = create_app()

def check_admin():
    with app.app_context():
        user = User.query.filter_by(username='admin').first()
        if user:
            print(f'Admin exists: Yes')
            print(f'Username: {user.username}')
            print(f'Email: {user.email}')
            print(f'Role: {user.role}')
            print(f'Password hash: {user.password_hash[:20]}...')
        else:
            print('Admin user does not exist in the database.')

if __name__ == '__main__':
    check_admin()