from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id=db.Column(d.Integer, pimary_key=True)
    specialization_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    user=db.Column(db.String(50), nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(128), nullable=False)
    role=db.Column(db.String(20), nullable=False)  # e.g., 'doctor', 'nurse', 'admin'
    
    backuser = db.relationship('Appointment', back_populates='backapp')

class Department(db.Model):
    __tablename__ = 'departments'
    id=db.Column(d.Integer, primary_key=True)
    name=db.Column(db.String(100), unique=True, nullable=False)
    description=db.Column(db.text, nullable=True)    

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id=db.Column(db.Integer, primary_key=True)
    patient_name=db.Column(db.String(100), nullable=False)
    doctor_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    appointment_date=db.Column(db.DateTime, nullable=False)
    appointment_time=db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='booked')  # e.g., 'scheduled', 'completed', 'canceled'
    backapp = d.relationship('User', back_populates = 'backuser')