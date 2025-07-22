"""
Migration script to add language and voice_input fields to ChatbotQuery model
"""

from app import create_app
from app.models.models import db, ChatbotQuery
from sqlalchemy import Column, String, Boolean

def run_migration():
    """Add new columns to ChatbotQuery table"""
    app = create_app()
    
    with app.app_context():
        # Check if columns already exist
        inspector = db.inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('chatbot_query')]
        
        # Add language column if it doesn't exist
        if 'language' not in columns:
            print("Adding 'language' column to ChatbotQuery table...")
            db.engine.execute('ALTER TABLE chatbot_query ADD COLUMN language VARCHAR(10) DEFAULT "en"')
            print("Added 'language' column successfully")
        else:
            print("'language' column already exists")
        
        # Add voice_input column if it doesn't exist
        if 'voice_input' not in columns:
            print("Adding 'voice_input' column to ChatbotQuery table...")
            db.engine.execute('ALTER TABLE chatbot_query ADD COLUMN voice_input BOOLEAN DEFAULT 0')
            print("Added 'voice_input' column successfully")
        else:
            print("'voice_input' column already exists")
        
        print("Migration completed successfully")

if __name__ == "__main__":
    run_migration()