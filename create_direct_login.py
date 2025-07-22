from app import create_app
from app.models.models import db, User
from datetime import datetime
import os

app = create_app()

def create_direct_login_html():
    with app.app_context():
        # First, make sure admin exists with correct password
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Admin user does not exist!")
            return
        
        # Set a known password for testing
        test_password = 'admin123'
        admin.set_password(test_password)
        
        # Make sure role is set to admin
        admin.role = 'admin'
        
        db.session.commit()
        
        # Create a simple HTML file for direct login
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Direct Login</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #3498db;
            text-align: center;
        }}
        .form-group {{
            margin-bottom: 15px;
        }}
        label {{
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }}
        input {{
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }}
        button {{
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            font-size: 16px;
        }}
        button:hover {{
            background-color: #2980b9;
        }}
        .credentials {{
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
            border-left: 4px solid #3498db;
        }}
        .credentials p {{
            margin: 5px 0;
        }}
        .credentials strong {{
            color: #3498db;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Direct Admin Login</h1>
        
        <div class="credentials">
            <p><strong>Username:</strong> {admin.username}</p>
            <p><strong>Password:</strong> {test_password}</p>
        </div>
        
        <form id="login-form" method="POST" action="/auth/login">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" value="{admin.username}" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" value="{test_password}" required>
            </div>
            
            <button type="submit">Login</button>
        </form>
        
        <p style="text-align: center; margin-top: 20px;">
            This form will submit directly to the login endpoint.
        </p>
    </div>

    <script>
        document.getElementById('login-form').addEventListener('submit', function(e) {{
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            fetch('/auth/login', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/x-www-form-urlencoded',
                }},
                body: new URLSearchParams({{
                    'username': username,
                    'password': password
                }})
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.success) {{
                    alert('Login successful! Redirecting to admin dashboard...');
                    window.location.href = '/admin/dashboard';
                }} else {{
                    alert('Login failed: ' + data.message);
                }}
            }})
            .catch(error => {{
                alert('Error: ' + error);
            }});
        }});
    </script>
</body>
</html>
        """
        
        # Save the HTML file
        static_dir = os.path.join(app.root_path, 'static')
        file_path = os.path.join(static_dir, 'direct_login.html')
        
        with open(file_path, 'w') as f:
            f.write(html_content)
        
        print(f"Direct login HTML file created at: {file_path}")
        print(f"Access it at: http://127.0.0.1:5000/static/direct_login.html")
        print("\nAdmin credentials:")
        print(f"Username: {admin.username}")
        print(f"Password: {test_password}")

if __name__ == '__main__':
    create_direct_login_html()