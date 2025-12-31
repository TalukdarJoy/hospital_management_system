# 🏥 LifeLine Hospital Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A comprehensive web-based hospital management system that digitizes and streamlines hospital operations, appointments, and medical records.

## 📹 Demo

**[Watch Video Demo](https://www.youtube.com/watch?v=qHcFzkCTDhA&t=20s)**

---

## 📖 Description

LifeLine Hospital Management System is a web-based application designed to digitize and streamline hospital operations. The system replaces traditional manual record-keeping with a unified digital platform where administrators, doctors, and patients can efficiently manage appointments, medical records, and doctor availability.

The project is built using the **Flask** web framework with **SQLite** as the database and **SQLAlchemy** as the ORM. It implements session-based authentication with role-based access control, ensuring that each user type has access only to the features relevant to them.

---

##  Key Features

### 👨‍💼 Admin Dashboard
-  View total doctors, patients, and appointments
-  Create and delete doctor accounts
-  View all hospital appointments
-  Search doctors and patients

### 👨‍⚕️ Doctor Dashboard
-  View upcoming appointments
-  Set 7-day availability using predefined time slots
-  Update patient treatments (diagnosis, prescription, medicines)
-  View complete patient medical history
-  Mark appointments as completed or cancelled

### 👤 Patient Portal
-  Self-registration and login
-  View doctors and specializations
-  Check doctor availability
-  Book appointments via clickable time slots
-  View appointment history and treatment details

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Flask** | Python web framework |
| **SQLite** | Lightweight database |
| **SQLAlchemy** | ORM for database operations |
| **Jinja2** | Template engine |
| **HTML/CSS** | Frontend design |
| **Session-based Auth** | User authentication |

---

## 📁 Project Structure
```
hospital_management/
├── app.py                      # Main application file
├── hospital.db                 # SQLite database
├── templates/                  # HTML templates
│   ├── index.html             # Landing page
│   ├── login.html             # Login page
│   ├── register.html          # Patient registration
│   ├── admin_dashboard.html   # Admin interface
│   ├── doctor_dashboard.html  # Doctor interface
│   ├── patient_dashboard.html # Patient interface
│   ├── createdoc.html         # Create doctor form
│   ├── doc_availability.html  # Set availability
│   ├── view_doc_availability.html
│   ├── update_patient.html    # Update treatment
│   ├── patient_history.html   # Medical history
│   └── treatment.html         # Treatment details
└── static/
    └── style.css              # Styling
```

---

## 🗄️ Database Design

### Models

| Model | Description |
|-------|-------------|
| **User** | Stores login credentials and roles |
| **Doctor** | Doctor profile information |
| **Patient** | Patient personal information |
| **Appointment** | Links doctors and patients with scheduling |
| **DoctorAvailability** | Stores weekly availability slots |
| **Treatment** | Stores diagnosis, prescriptions, medicines |

### Key Relationships
- 🔗 One-to-one: User ↔ Doctor/Patient
- 🔗 One-to-many: Doctor/Patient ↔ Appointments
- 🔗 One-to-one: Appointment ↔ Treatment

---

## 🚀 Getting Started

### Prerequisites
```bash
Python 3.8+
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/TalukdarJoy/hospital_management_system.git
cd hospital_management_system
```

2. **Install dependencies**
```bash
pip install flask flask-sqlalchemy
```

3. **Run the application**
```bash
python app.py
```

4. **Open in browser**
```
http://127.0.0.1:5000/
```

---

## 🔑 Default Credentials

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`

### Doctor Accounts
- Created by admin
- **Default Password:** `doctor123`

### Patient Accounts
- Self-registration available

---

## 💡 Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Separate Doctor/Patient tables** | Different attributes and responsibilities |
| **Slot-based booking system** | Prevents conflicts and typing errors |
| **DoctorAvailability table** | Efficient querying, avoids double bookings |
| **Treatment as formatted text** | Flexibility without schema changes |
| **Manual session authentication** | Demonstrates core Flask concepts |

---

## 🔧 Technical Challenges Solved

 Prevented double bookings by checking existing appointments  
 Implemented bidirectional relationships using SQLAlchemy backrefs  
 Dynamically rendered slot availability based on database queries  
 Auto-created admin account on first run for immediate usability  

---

## 📚 Learning Outcomes

This project strengthened understanding of:

-  Full-stack web development using Flask
-  Database schema design and relationships
-  Role-based access control
-  Session management and authentication
-  UI/UX design for multi-role systems
-  Debugging SQLAlchemy relationship issues

---

## 🔮 Future Improvements

- [ ] Password hashing using Werkzeug
- [ ] Email and SMS notifications
- [ ] File upload for medical reports
- [ ] Advanced search and filtering
- [ ] PDF export of medical history
- [ ] Improved security and validations
- [ ] Mobile-responsive design
- [ ] Appointment reminders
- [ ] Multi-language support

---

## AI Usage

Approximately **5%** - Used only for understanding SQLAlchemy syntax and debugging specific errors.

---

## Author

**Joy Talukdar**

- GitHub: [@TalukdarJoy](https://github.com/TalukdarJoy)
- Project: [Hospital Management System](https://github.com/TalukdarJoy/hospital_management_system)

---

## Academic Year

**2025–2026**

--

## Acknowledgments

- CS50 Harvard University for the foundation
- Flask documentation for comprehensive guides
- SQLAlchemy community for support

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

**Made with ❤️ by Joy Talukdar**

</div>
