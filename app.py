from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database file location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database extension
db = SQLAlchemy(app)

# Define the User Model (Database Schema with correct Capitalization)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False) # admin, doctor, receptionist

    def __repr__(self):
        return f'<User {self.email} - {self.role}>'

@app.route('/')
def home():
    return "<h1>Hospital Management System Server is Running!</h1>"

if __name__ == '__main__':
    app.run(debug=True)