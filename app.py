from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer, primary_key=True)
    specialization_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    user=db.Column(db.String(50), nullable=False)
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
    doctor_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
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
    id = db.Column(db.Integer, primar_key=True)
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
    age = db.Column(db.Integer, nullable)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=True)

    appointments = db.relationship('Appointment', backref='patient', lazy=True)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
