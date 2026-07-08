from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-hospital-key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    check_in_status = db.Column(db.Boolean, default=True)

# 1. Update Root Route to route active sessions directly to dashboards
@app.route('/')
def home():
    if 'user_id' in session:
        if session['user_role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif session['user_role'] == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif session['user_role'] == 'receptionist':
            return redirect(url_for('receptionist_dashboard'))
    return "<h1>Hospital Management System Server is Running!</h1><a href='/login'>Go to Login</a>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        hashed_pw = generate_password_hash(password, method='scrypt')
        new_user = User(email=email, password_hash=hashed_pw, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# 2. Update Login Route to land users in their proper environments
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['user_role'] = user.role
            return redirect(url_for('home'))
        else:
            return "<h3>Invalid email or password!</h3>"
    return render_template('login.html')

# 3. Day 5: Secured Dashboard Routes
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['user_role'] != 'admin':
        return "<h3>Access Denied: You do not have Admin permissions.</h3>", 403
    return render_template('admin_dashboard.html')

@app.route('/doctor/dashboard')
def doctor_dashboard():
    if 'user_id' not in session or session['user_role'] != 'doctor':
        return "<h3>Access Denied: You do not have Doctor permissions.</h3>", 403
    return render_template('doctor_dashboard.html')

@app.route('/receptionist/dashboard')
def receptionist_dashboard():
    if 'user_id' not in session or session['user_role'] != 'receptionist':
        return "<h3>Access Denied: You do not have Receptionist permissions.</h3>", 403
    return render_template('receptionist_dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)