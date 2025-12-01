from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import render_template,request, redirect, url_for, session

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sam'

# Initialize the database
db = SQLAlchemy(app)

from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer, primary_key=True)
    specialization_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    username=db.Column(db.String(50), nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(128), nullable=False)
    role=db.Column(db.String(20), nullable=False)  # e.g., 'doctor', 'nurse', 'admin'
    
    #backuser = db.relationship('Appointment', back_populates='backapp')

class Department(db.Model):
    __tablename__ = 'departments'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), unique=True, nullable=False)
    description=db.Column(db.Text, nullable=True)    

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id=db.Column(db.Integer, primary_key=True)
    patient_name=db.Column(db.String(100), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    appointment_date=db.Column(db.DateTime, nullable=False)
    appointment_time=db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='booked')  # e.g., 'scheduled', 'completed', 'canceled'

    treatment = db.relationship('Treatment', backref='appointment', uselist=False)

class Treatment(db.Model):
    __tablename__ = 'treatments'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    #backtreat = db.relationship('Appointment', backref = 'backapp')

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    availability = db.Column(db.String(100), nullable=True)  # e.g., 'Mon-Fri 9am-5pm'

    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=True)

    appointments = db.relationship('Appointment', backref='patient', lazy=True)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["POST","GET"])
def register():
    if request.method== "POST":
        username  = request.form["username"]
        password = request.form["password"]
        print(username,password)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already taken! <a href='/register'>Try another</a>"

        new_user = User(username = username, email = f"{username}@hospital.com", password = password, role ="patient")
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
  
    return render_template('register.html') 
    
@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        username  = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()
        if existing_user and existing_user.password == password and existing_user.role == "patient":
            session['existing_user'] = existing_user.username
            session['id'] = existing_user.id
            session['role'] = existing_user.role
            return redirect(url_for('patient_dashboard'))

        elif existing_user and existing_user.password == password and existing_user.role == "doctor":
            session['existing_user'] = existing_user.username
            session['id'] = existing_user.id
            session['role'] = existing_user.role
            return redirect(url_for('doctor_dashboard'))

        if existing_user and existing_user.password == password and existing_user.role == "admin":
            session['existing_user'] = existing_user.username
            session['id'] = existing_user.id
            session['role'] = existing_user.role
            return redirect(url_for('admin_dashboard'))
        return "Username doesn't exist! <a href='/login'>Try another</a>"

    return render_template('login.html') 

@app.route('/patient_dashboard')
def patient_dashboard():
    return "Welcome to the Patient Dashboard!" 

@app.route('/doctor_dashboard')
def doctor_dashboard():
    user_id = session.get("id")
    
    # Find doctor by linked user_id
    doctor = Doctor.query.filter_by(user_id=user_id).first()

    return render_template('doctor_dashboard.html') 

@app.route('/admin_dashboard')
def admin_dashboard():
    doctors = Doctor.query.all()
    patients = Patient.query.all()
    appointments = Appointment.query.all()
    
    # Pass them to the template
    return render_template('admin_dashboard.html', 
                         doctors=doctors, 
                         patients=patients, 
                         appointments=appointments)
    return render_template('admin_dashboard.html')  

@app.route('/admin_dashboard/createdoc', methods=["GET","POST"])
def createdoc():
    if request.method == "POST":
        Username = request.form["name"]
        specialization = request.form["specialization"]
        phone = request.form["phone"]
        availability = request.form.get("availability", "Not specified")
        
        existing_user = User.query.filter_by(username=Username).first()
        if existing_user:
            return "Doctor already exist! <a href='/admin_dashboard/createdoc'>Try another</a>"


        new_user = User(
            username=Username,
            email=f"{Username}@hospital.com",
            password="doctor123",
            role="doctor"
        )
        db.session.add(new_user)
        db.session.flush()   # <-- assigns new_user.id without committing

        # now new_user.id is available
        new_doctor = Doctor(
            user_id=new_user.id,
            name=Username,
            specialization=specialization,
            phone=phone,
            availability=request.form.get("availability", "Not specified")
        )




        #new_doctor = Doctor(user_id=22, name=Username, specialization=specialization, phone=phone)
        db.session.add(new_doctor)
        db.session.commit()

        return redirect(url_for('admin_dashboard'))
    return render_template('createdoc.html') 

from flask import flash  # if you want to use flash messages

@app.route('/delete_doctor/<int:doctor_id>')
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    # optionally get linked user and delete it too
    user = User.query.get(doctor.user_id)

    db.session.delete(doctor)
    if user:
        db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))



@app.route('/logout')
def logout():
    session.pop('existing_user', None)
    return redirect(url_for('index'))


if __name__ == '__main__':

    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username='admin').first()
    
    
        if not admin:
            admin_user = User(
                username='admin',
                email='admin@hospital.com',
                password='admin123',  # Change this in production!
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
    app.run(debug=True)