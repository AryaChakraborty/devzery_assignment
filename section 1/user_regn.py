from flask import Flask, request, jsonify, session, redirect, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Flask app secret key
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# SQLAlchemy for database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use your preferred database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Bcrypt for password hashing
bcrypt = Bcrypt(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create tables within the application context
with app.app_context():
    db.create_all()

# health check route
@app.route('/')
def health_check():
    return jsonify(message='Server is up and running.')
# Registration endpoint
@app.route('/register', methods=['POST'])
def register():
    # email, username and password
    data = request.get_json()
    
    # Check if the email or username already exists
    existing_user = User.query.filter((User.email == data['email']) | (User.username == data['username'])).first()
    if existing_user:
        return jsonify(message='Email or username already exists. Choose a different one.'), 400

    # Hash the password and create a new user
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(message='Registration successful. You can now log in.')

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    # email and password
    
    # Check if the user is already logged in
    if 'user_id' in session:
        return jsonify(message='Already logged in.')
    
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        # Store user information in the session
        session['user_id'] = user.id
        return jsonify(message='Login successful.')
    else:
        return jsonify(message='Invalid credentials.')

# Logout endpoint
@app.route('/logout', methods=['GET'])
def logout():
    # Clear the session to log out the user
    session.clear()
    return jsonify(message='Logout successful.')

# Profile endpoint
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # Check if the user is logged in
    user_id = session.get('user_id')
    print(user_id)
    if user_id is None:
        return jsonify(message='Not logged in. Please log in.'), 401

    # Retrieve user information from the database
    user = User.query.get(user_id)
    if user:
        if request.method == 'GET':
            # Retrieve user information
            user_profile = {
                'my_profile': {
                    'username': user.username,
                    'email': user.email
                },
                'other_profiles': []
            }

            # Retrieve information about other users
            other_users = User.query.filter(User.id != user.id).all()
            for other_user in other_users:
                user_profile['other_profiles'].append({
                    'username': other_user.username,
                    'email': other_user.email
                })

            return jsonify(user_profile)
        elif request.method == 'POST':
            # Update user profile
            data = request.get_json()
            if 'username' in data:
                user.username = data.get('username', user.username)
            if 'email' in data:
                user.email = data.get('email', user.email)
            db.session.commit()
            return jsonify(message='Profile updated successfully.')
    else:
        return jsonify(message='User not found.'), 404


if __name__ == '__main__':
    # Run the application
    app.run(debug=True)
