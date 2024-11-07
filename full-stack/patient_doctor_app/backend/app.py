from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
db = SQLAlchemy(app)

# Models
class Patients(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(200), nullable=False)
    disease = db.Column(db.String())
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'))
    
    def patient_to_dict(self):
        return {
            'patient_id': self.patient_id,
            'patient_name': self.patient_name,
            'disease': self.disease,
            'doctor_id' : self.doctor_id
        }

class Doctor(db.Model):
    doctor_id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(200), nullable=False)

    def doctor_to_dict(self):
        return {
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor_name
        }

def create_dummy_data():
    # Check if the data already exists
    if Doctor.query.first() or Patients.query.first():
        print("Dummy data already exists. Skipping creation.")
        return

    # Creating doctors
    doctor1 = Doctor(doctor_name="Dr. John Smith")
    doctor2 = Doctor(doctor_name="Dr. Emily Johnson")

    db.session.add_all([doctor1, doctor2])
    db.session.commit()

    # Creating patients
    patient1 = Patients(patient_name="Alice Brown", disease="Flu", doctor_id=doctor1.doctor_id)
    patient2 = Patients(patient_name="Bob White", disease="Covid-19", doctor_id=doctor2.doctor_id)
    patient3 = Patients(patient_name="Charlie Black", disease="Diabetes", doctor_id=doctor1.doctor_id)

    db.session.add_all([patient1, patient2, patient3])
    db.session.commit()
    print("Dummy data created successfully.")


# Database table creation
with app.app_context():
    data = {}
    create_dummy_data()
    db.create_all()



# Routes
@app.route('/addPatient', methods=['POST'])
def add_patient():
    data = request.json
    # Check for missing fields
    if not all(key in data for key in ['patient_name', 'patient_disease', 'doctor_id']):
        return jsonify({
            'status_code': '401',
            'message': 'Patient Information Missing'
        }), 401

    try:
        pt = Patients(
            patient_name=data['patient_name'],
            disease=data['patient_disease'],
            doctor_id=data['doctor_id']
        )
        db.session.add(pt)
        db.session.commit()
        return jsonify({
            'status_code': '201',
            'message': 'Patient Added Successfully'
        }), 201

    except Exception as e:
        print("Error:", e)
        return jsonify({
            'status_code': '503',
            'message': str(e)
        }), 503

@app.route('/addDoctor', methods=['POST'])
def add_doctor():
    data = request.json
    if 'doctor_name' not in data:
        return jsonify({
            'status_code': '401',
            'message': 'Doctor Information Missing'
        }), 401

    try:
        dt = Doctor(
            doctor_name=data['doctor_name']
        )
        db.session.add(dt)
        db.session.commit()
        return jsonify({
            'status_code': '201',
            'message': 'Doctor Added Successfully'
        }), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({
            'status_code': '503',
            'message': str(e)
        }), 503


@app.route('/getPatient/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    # Fetch the patient by ID
    pt = Patients.query.get(patient_id)
    
    # Check if patient exists
    if not pt:
        return jsonify({
            'status_code': '404',
            'message': 'Patient not found'
        }), 404

    # Return patient information
    return jsonify({
        'status_code': '200',
        'patient': pt.patient_to_dict()
    }), 200

@app.route('/getAllPatient', methods=['GET'])
def get_all_patient():
    # Fetch the patient by ID
    pt = Patients.query.all()
    
    # Check if patient exists
    if not pt:
        return jsonify({
            'status_code': '404',
            'message': 'Patient not found'
        }), 404
    patients_list = [patient.patient_to_dict() for patient in pt]
    

    # Return patient information
    return jsonify({
        'status_code': '200',
        'patient': patients_list
    }), 200


@app.route('/getAllDoctor', methods=['GET'])
def get_all_doctor():
    # Fetch the patient by ID
    pt = Doctor.query.all()
    
    # Check if patient exists
    if not pt:
        return jsonify({
            'status_code': '404',
            'message': 'Patient not found'
        }), 404
    doctor_list = [patient.doctor_to_dict() for patient in pt]
    

    # Return patient information
    return jsonify({
        'status_code': '200',
        'patient': doctor_list
    }), 200


@app.route('/getDoctor/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    dt = Doctor.query.get(doctor_id)
    if not dt:
        return jsonify({
            'status_code': '404',
            'message': 'Doctor not found'
        }), 404
    
    return jsonify({
        'status_code': '200',
        'doctor': dt.doctor_to_dict()
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
