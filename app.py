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
    appointment_date = db.Column(db.String(20), nullable=False)   
    appointment_time = db.Column(db.String(50), nullable=False)   
    status = db.Column(db.String(20), nullable=False, default='Booked')
    treatment = db.relationship('Treatment', backref='appointment', uselist=False)

class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availabilities'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)   # 'YYYY-MM-DD'
    morning = db.Column(db.String(80), nullable=True) # text like '08:00 - 12:00'
    evening = db.Column(db.String(80), nullable=True) # text like '16:00 - 20:00'

    doctor = db.relationship('Doctor', backref='availabilities')

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
    experience = db.Column(db.String(50), nullable=True)

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

        new_patient = Patient(
            user_id=new_user.id,
            name=username,   # or request.form["name"] if you collect real name
            age=0,
            gender="Not set",
            phone="Not set",
            address="Not set"
        )
        db.session.add(new_patient)
        db.session.commit()

        return redirect(url_for('login'))
  
    return render_template('register.html') 
    
@app.route('/login', methods=["POST","GET"])
def login():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username, password=password).first()
        
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'doctor':
                return redirect(url_for('doctor_dashboard'))  
            elif user.role == 'patient':
                return redirect(url_for('patient_dashboard'))
        else:
            return "Invalid credentials! <a href='/login'>Try again</a>"
    
    return render_template('login.html')
    '''
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

    return render_template('login.html') '''


@app.route('/patient_dashboard')
def patient_dashboard():
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('login'))

    user_id = session.get('user_id')

    patient = Patient.query.filter_by(user_id=user_id).first()

    # 🔥 Auto-create patient profile if missing
    if not patient:
        user = User.query.get(user_id)
        patient = Patient(
            user_id=user.id,
            name=user.username,
            age=0,
            gender="Not set",
            phone="Not set",
            address="Not set"
        )
        db.session.add(patient)
        db.session.commit()

    # Fetch appointments (safe now because patient exists)
    appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(
        Appointment.appointment_date.desc()
    ).all()

    doctors = Doctor.query.all()

    return render_template(
        'patient_dashboard.html',
        patient=patient,
        appointments=appointments,
        doctors=doctors
    )

# Update book_appointment route - simplified for POST only
@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    patient = Patient.query.filter_by(user_id=user_id).first()
    
    if not patient:
        return "Patient profile not found! Contact admin.", 400

    doctor_id = int(request.form.get('doctor_id'))
    date = request.form.get('date')
    slot = request.form.get('slot')  # 'morning' or 'evening'
    
    # Get the availability
    avail = DoctorAvailability.query.filter_by(doctor_id=doctor_id, date=date).first()
    if not avail:
        return "Selected slot no longer available. <a href='" + url_for('patient_dashboard') + "'>Go back</a>", 400

    # Get the time based on slot
    if slot == 'morning':
        appointment_time = avail.morning
    else:
        appointment_time = avail.evening
    
    if not appointment_time:
        return "Selected slot is not available. <a href='" + url_for('patient_dashboard') + "'>Go back</a>", 400

    # Check if slot is already booked
    conflict = Appointment.query.filter_by(
        doctor_id=doctor_id,
        appointment_date=date,
        appointment_time=appointment_time,
        status='Booked'
    ).first()
    
    if conflict:
        return "This slot has already been booked. <a href='" + url_for('view_doc_availability', doctor_id=doctor_id) + "'>Choose another slot</a>", 400

    # Create appointment
    doctor = Doctor.query.get_or_404(doctor_id)
    new_apt = Appointment(
        patient_name=patient.name,
        doctor_id=doctor.id,
        patient_id=patient.id,
        appointment_date=date,
        appointment_time=appointment_time,
        status='Booked'
    )
    db.session.add(new_apt)
    db.session.commit()
    
    return redirect(url_for('patient_dashboard'))

@app.route('/doctor_dashboard')
def doctor_dashboard():
    # Check if user is logged in and is a doctor
    if 'user_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    
    # Find doctor by linked user_id
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    
    if not doctor:
        return "Doctor profile not found! <a href='/login'>Go back</a>"
    
    # Get upcoming appointments for this doctor
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).filter(
        Appointment.status.in_(['Booked', 'Scheduled'])
    ).all()
    
    # Get all patients assigned to this doctor (unique patients from appointments)
    patient_ids = set([apt.patient_id for apt in Appointment.query.filter_by(doctor_id=doctor.id).all()])
    patients = [Patient.query.get(pid) for pid in patient_ids]
    
    return render_template('doctor_dashboard.html', 
                         doctor=doctor, 
                         appointments=appointments,
                         patients=patients)


@app.route('/update_patient/<int:appointment_id>', methods=['GET', 'POST'])
def update_patient(appointment_id):
    # Check if user is logged in and is a doctor
    if 'user_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if request.method == 'POST':
        visit_type = request.form.get('visit_type', 'In-person')
        test_done = request.form.get('test_done', '')
        diagnosis = request.form['diagnosis']
        prescription = request.form.get('prescription', '')
        medicines = request.form.get('medicines', '')
        
        # Check if treatment already exists for this appointment
        treatment = Treatment.query.filter_by(appointment_id=appointment_id).first()
        
        # Store everything in the notes field since Treatment model doesn't have separate columns
        notes_text = f"Visit Type: {visit_type}\nTest Done: {test_done}\nPrescription: {prescription}\nMedicines: {medicines}"
        
        if treatment:
            # Update existing treatment
            treatment.diagnosis = diagnosis
            treatment.notes = notes_text
        else:
            # Create new treatment record
            new_treatment = Treatment(
                appointment_id=appointment_id,
                diagnosis=diagnosis,
                notes=notes_text
            )
            db.session.add(new_treatment)
        
        # Update appointment status to completed
        appointment.status = 'Completed'
        
        db.session.commit()
        
        return redirect(url_for('doctor_dashboard'))
    
    return render_template('update_patient.html', 
                         appointment=appointment, 
                         doctor=doctor)


# Also update view_treatment route to parse prescription:

@app.route('/patient_history/<int:patient_id>')
def patient_history(patient_id):
    # Check if user is logged in and is a doctor
    if 'user_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    patient = Patient.query.get_or_404(patient_id)
    
    # Get all completed appointments for this patient with this doctor
    appointments = Appointment.query.filter_by(
        patient_id=patient_id,
        doctor_id=doctor.id,
        status='Completed'
    ).all()
    
    # Get treatments for all these appointments
    treatments = []
    for apt in appointments:
        treatment = Treatment.query.filter_by(appointment_id=apt.id).first()
        if treatment:
            # Parse notes to extract visit_type, test_done, medicines
            notes_parts = treatment.notes.split('\n') if treatment.notes else []
            visit_type = 'In-person'
            test_done = 'N/A'
            medicines = 'N/A'
            
            for part in notes_parts:
                if 'Visit Type:' in part:
                    visit_type = part.split('Visit Type:')[1].strip()
                elif 'Test Done:' in part:
                    test_done = part.split('Test Done:')[1].strip()
                elif 'Medicines:' in part:
                    medicines = part.split('Medicines:')[1].strip()
            
            treatment.visit_type = visit_type
            treatment.test_done = test_done
            treatment.medicines = medicines
            treatments.append(treatment)
    
    return render_template('patient_history.html', 
                         patient=patient, 
                         doctor=doctor,
                         treatments=treatments)


@app.route('/doc_availability', methods=['GET', 'POST'])
def doc_availability():
    # doctor only
    if 'user_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    doctor = Doctor.query.filter_by(user_id=user_id).first()
    if not doctor:
        return "Doctor profile not found!", 400

    # Generate next 7 dates for the form
    from datetime import date, timedelta
    today = date.today()
    dates = [(today + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    if request.method == 'POST':
        # Remove any existing availability rows for this doctor for the posted dates,
        # then insert fresh rows.
        # We'll collect posted slots and upsert into DoctorAvailability.
        for i in range(7):
            d = request.form.get(f'date_{i}')
            morning = request.form.get(f'slot1_{i}', '').strip()
            evening = request.form.get(f'slot2_{i}', '').strip()

            if not d:
                continue

            # try find existing
            existing = DoctorAvailability.query.filter_by(doctor_id=doctor.id, date=d).first()
            if existing:
                existing.morning = morning or None
                existing.evening = evening or None
            else:
                new_row = DoctorAvailability(
                    doctor_id=doctor.id,
                    date=d,
                    morning=morning or None,
                    evening=evening or None
                )
                db.session.add(new_row)

        db.session.commit()
        return redirect(url_for('doctor_dashboard'))

    # GET -> show form
    # Pre-fill slots if present
    existing_map = {a.date: a for a in DoctorAvailability.query.filter_by(doctor_id=doctor.id).all()}
    return render_template('doc_availability.html', doctor=doctor, dates=dates, existing_map=existing_map)


# Patient view of a specific doctor's availability (useable from patient dashboard)
# Accepts doctor_id parameter
# Update view_doc_availability route

@app.route('/treatment/<int:appointment_id>')
def treatment(appointment_id):
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('login'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    treatment = Treatment.query.filter_by(appointment_id=appointment_id).first()
    
    # Security: Make sure patient can only view their own appointments
    user_id = session.get('user_id')
    patient = Patient.query.filter_by(user_id=user_id).first()
    
    if appointment.patient_id != patient.id:
        return "Unauthorized access", 403
    
    # Parse treatment notes if treatment exists
    if treatment and treatment.notes:
        notes_parts = treatment.notes.split('\n')
        treatment.visit_type = 'In-person'
        treatment.test_done = 'N/A'
        treatment.medicines = 'N/A'
        treatment.prescription = 'N/A'
        
        for part in notes_parts:
            if 'Visit Type:' in part:
                treatment.visit_type = part.split('Visit Type:')[1].strip()
            elif 'Test Done:' in part:
                treatment.test_done = part.split('Test Done:')[1].strip()
            elif 'Prescription:' in part:
                treatment.prescription = part.split('Prescription:')[1].strip()
            elif 'Medicines:' in part:
                treatment.medicines = part.split('Medicines:')[1].strip()
    
    return render_template('treatment.html', 
                         appointment=appointment, 
                         treatment=treatment)
@app.route('/view_doc_availability/<int:doctor_id>')
def view_doc_availability(doctor_id):
    if 'user_id' not in session or session.get('role') != 'patient':
        return redirect(url_for('login'))
    
    doctor = Doctor.query.get_or_404(doctor_id)
    avail_rows = DoctorAvailability.query.filter_by(doctor_id=doctor.id).order_by(DoctorAvailability.date).all()

    # Build availability_list with booking status
    availability_list = []
    for r in avail_rows:
        # Check if morning slot is booked
        morning_booked = False
        if r.morning:
            morning_apt = Appointment.query.filter_by(
                doctor_id=doctor.id,
                appointment_date=r.date,
                appointment_time=r.morning,
                status='Booked'
            ).first()
            morning_booked = morning_apt is not None
        
        # Check if evening slot is booked
        evening_booked = False
        if r.evening:
            evening_apt = Appointment.query.filter_by(
                doctor_id=doctor.id,
                appointment_date=r.date,
                appointment_time=r.evening,
                status='Booked'
            ).first()
            evening_booked = evening_apt is not None
        
        availability_list.append({
            'date': r.date,
            'morning': r.morning,
            'evening': r.evening,
            'morning_booked': morning_booked,
            'evening_booked': evening_booked
        })

    return render_template('view_doc_availability.html', 
                         doctor=doctor, 
                         availability_list=availability_list)



@app.route('/mark_complete/<int:appointment_id>')
def mark_complete(appointment_id):
    # Check if user is logged in and is a doctor
    if 'user_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('login'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'Completed'
    db.session.commit()
    
    return redirect(url_for('doctor_dashboard'))


@app.route('/cancel_appointment/<int:appointment_id>')
def cancel_appointment(appointment_id):
    # Check if user is logged in and is a doctor
    if 'user_id' not in session or session.get('role') != 'doctor':
        return redirect(url_for('login'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'Cancelled'
    db.session.commit()
    
    return redirect(url_for('doctor_dashboard'))
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
        experience = request.form["experience"]
        
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
            experience=experience
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