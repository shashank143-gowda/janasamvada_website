from app import create_app
from app.models.models import db
import os

app = create_app()

# Create tables before the first request
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)