from flask import Flask,session, jsonify, render_template,request
import pymysql

app = Flask(__name__)
# Set the secret key to a random value
app.secret_key = 'your_secret_key_here'
# 数据库连接配置
db_config = {
    'host': '1.94.97.29',
    'port': 13306,
    'user': 'root',  # 替换为你的数据库用户名
    'password': '123456',  # 替换为你的数据库密码
    'database': 'hospital_db'
}

# 创建数据库连接
def get_db_connection():
    conn = pymysql.connect(**db_config)
    return conn

# 获取所有病人信息的API
@app.route('/patients', methods=['GET'])
def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Patient')
    columns = [col[0] for col in cursor.description]
    patients = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(patients)

@app.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Patient WHERE PatientID = %s', (patient_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        columns = [col[0] for col in cursor.description]
        patient = dict(zip(columns, row))
        return jsonify(patient)
    else:
        return jsonify({"message": "Patient not found"}), 404

# API to get all wards
@app.route('/wards', methods=['GET'])
def get_wards():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Ward')
    columns = [col[0] for col in cursor.description]
    wards = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(wards)

# API to get a single ward
@app.route('/wards/<int:ward_id>', methods=['GET'])
def get_ward(ward_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Ward WHERE WardID = %s', (ward_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        columns = [col[0] for col in cursor.description]
        ward = dict(zip(columns, row))
        return jsonify(ward)
    else:
        return jsonify({"message": "Ward not found"}), 404

# API to update a ward
@app.route('/wards/<int:ward_id>', methods=['PUT'])
def update_ward(ward_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    cursor.execute('''
        UPDATE Ward
        SET Location = %s, RoomTypeCode = %s, FeeStandard = %s, Status = %s
        WHERE WardID = %s
    ''', (data['Location'], data['RoomTypeCode'], data['FeeStandard'], data['Status'], ward_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Ward updated successfully"})


# API to get all admissions
@app.route('/admissions', methods=['GET'])
def get_admissions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM AdmissionRecord')
    columns = [col[0] for col in cursor.description]
    admissions = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(admissions)

# API to get a single admission
@app.route('/admissions/<int:admission_id>', methods=['GET'])
def get_admission(admission_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM AdmissionRecord WHERE AdmissionID = %s', (admission_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        columns = [col[0] for col in cursor.description]
        admission = dict(zip(columns, row))
        return jsonify(admission)
    else:
        return jsonify({"message": "Admission record not found"}), 404

# API to delete an admission
@app.route('/admissions/<int:admission_id>', methods=['DELETE'])
def delete_admission(admission_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM AdmissionRecord WHERE AdmissionID = %s', (admission_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Admission deleted successfully"})

# API to add a new admission
@app.route('/admissions', methods=['POST'])
def add_admission():
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    cursor.execute('''
        INSERT INTO AdmissionRecord (PatientID, WardID, BedID, AdmissionDate, ExpectedDischargeDate, DischargeDate)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (data['PatientID'], data['WardID'], data['BedID'], data['AdmissionDate'], data['ExpectedDischargeDate'], data['DischargeDate']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Admission added successfully"}), 201

# API to update an admission
@app.route('/admissions/<int:admission_id>', methods=['PUT'])
def update_admission(admission_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    cursor.execute('''
        UPDATE AdmissionRecord
        SET PatientID = %s, WardID = %s, BedID = %s, AdmissionDate = %s, ExpectedDischargeDate = %s, DischargeDate = %s
        WHERE AdmissionID = %s
    ''', (data['PatientID'], data['WardID'], data['BedID'], data['AdmissionDate'], data['ExpectedDischargeDate'], data['DischargeDate'], admission_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Admission record updated successfully"})

# API to get all bills
@app.route('/bills', methods=['GET'])
def get_bills():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Bill')
    columns = [col[0] for col in cursor.description]
    bills = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(bills)

# API to get a single bill
@app.route('/bills/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Bill WHERE BillID = %s', (bill_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        columns = [col[0] for col in cursor.description]
        bill = dict(zip(columns, row))
        return jsonify(bill)
    else:
        return jsonify({"message": "Bill not found"}), 404

# API to update a bill
@app.route('/bills/<int:bill_id>', methods=['PUT'])
def update_bill(bill_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    cursor.execute('''
        UPDATE Bill
        SET AdmissionID = %s, AmountPayable = %s, AmountPaid = %s, PaymentDate = %s, PaymentStatus = %s
        WHERE BillID = %s
    ''', (data['AdmissionID'], data['AmountPayable'], data['AmountPaid'], data['PaymentDate'], data['PaymentStatus'], bill_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Bill updated successfully"})

# API to add a new bill
@app.route('/bills', methods=['POST'])
def add_bill():
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    cursor.execute('''
        INSERT INTO Bill (AdmissionID, AmountPayable, AmountPaid, PaymentDate, PaymentStatus)
        VALUES (%s, %s, %s, %s, %s)
    ''', (data['AdmissionID'], data['AmountPayable'], data['AmountPaid'], data['PaymentDate'], data['PaymentStatus']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Bill added successfully"}), 201


# API to delete a bill
@app.route('/bills/<int:bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Bill WHERE BillID = %s', (bill_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Bill deleted successfully"})


# API to get all doctors
@app.route('/doctors', methods=['GET'])
def get_doctors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Doctor')
    columns = [col[0] for col in cursor.description]
    doctors = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(doctors)

# API to get a single doctor
@app.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Doctor WHERE DoctorID = %s', (doctor_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        columns = [col[0] for col in cursor.description]
        doctor = dict(zip(columns, row))
        return jsonify(doctor)
    else:
        return jsonify({"message": "Doctor not found"}), 404

# API to add a new doctor
@app.route('/doctors', methods=['POST'])
def add_doctor():
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    cursor.execute('''
        INSERT INTO Doctor (Name, Gender, Department, Position, Username, Password)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (data['Name'], data['Gender'], data['Department'], data['Position'], data['Username'], data['Password']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Doctor added successfully"}), 201

# API to update a doctor
@app.route('/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    cursor.execute('''
        UPDATE Doctor
        SET Name = %s, Gender = %s, Department = %s, Position = %s, Username = %s, Password = %s
        WHERE DoctorID = %s
    ''', (data['Name'], data['Gender'], data['Department'], data['Position'], data['Username'], data['Password'], doctor_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Doctor updated successfully"})

# API to delete a doctor
@app.route('/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Doctor WHERE DoctorID = %s', (doctor_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Doctor deleted successfully"})

# 获取所有治疗记录的API
@app.route('/treatments', methods=['GET'])
def get_treatments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM TreatmentRecord')
    columns = [col[0] for col in cursor.description]
    treatments = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(treatments)

# 获取单个治疗记录的API
@app.route('/treatments/<int:treatment_id>', methods=['GET'])
def get_treatment(treatment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM TreatmentRecord WHERE TreatmentID = %s', (treatment_id,))
    columns = [col[0] for col in cursor.description]
    treatment = dict(zip(columns, cursor.fetchone())) if cursor.fetchone() else None
    cursor.close()
    conn.close()
    if treatment:
        return jsonify(treatment)
    else:
        return jsonify({"message": "Treatment record not found"}), 404

# 渲染首页
@app.route('/')
def index():
    return render_template('index.html')  # 渲染index.html


@app.route('/billsi')
def billsi():
    return render_template('bills.html')  # 渲染index.html

@app.route('/wardsi')
def wardsi():
    return render_template('wards.html')  # 渲染index.html

@app.route('/doctorsi')
def doctorsi():
    return render_template('doctors.html')  # 渲染index.html

@app.route('/admissionsi')
def admissionsi():
    return render_template('admissions.html')  # 渲染index.html

@app.route('/patientsi')
def patientsi():
    return render_template('patients.html')  # 渲染index.html

# API to update a patient
@app.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.json
    cursor.execute('''
        UPDATE Patient
        SET Name = %s, Gender = %s, Age = %s, Address = %s
        WHERE PatientID = %s
    ''', (data['Name'], data['Gender'], data['Age'], data['Address'], patient_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Patient updated successfully"})

    return conn



# API to handle doctor login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    session['username'] = username
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Doctor WHERE Username = %s AND Password = %s', (username, password))
    doctor = cursor.fetchone()
    cursor.close()
    conn.close()

    if doctor:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 401

# Route to render exit.html with doctor information
@app.route('/exit.html')
def exit_html():
    username = session.get('username')
    print("session:"+username)
    if not username:
        return jsonify({"message": "Unauthorized"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Doctor WHERE Username = %s', (username,))
    doctor = cursor.fetchone()
    cursor.close()
    conn.close()

    if doctor:
        columns = [col[0] for col in cursor.description]
        doctor_info = dict(zip(columns, doctor))
        return render_template('exit.html', doctor=doctor_info)
    else:
        return jsonify({"message": "Doctor not found"}), 404



# Render the login page
@app.route('/login')
def login_page():
    return render_template('login.html')





@app.route('/doctor_info', methods=['GET'])
def doctor_info():
    username = session.get('username')
    if not username:
        return jsonify({"message": "Unauthorized"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Doctor WHERE Username = %s', (username,))
    doctor = cursor.fetchone()
    cursor.close()
    conn.close()

    if doctor:
        columns = [col[0] for col in cursor.description]
        doctor_info = dict(zip(columns, doctor))
        return jsonify(doctor_info)
    else:
        return jsonify({"message": "Doctor not found"}), 404

@app.route('/update_doctor2', methods=['PUT'])
def update_doctor2():
    username = session.get('username')
    if not username:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Doctor
        SET Gender = %s, Department = %s, Position = %s
        WHERE Username = %s
    ''', (data['Gender'], data['Department'], data['Position'], username))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Doctor information updated successfully"})



@app.route('/solve.html')
def solve_html():
    return render_template('solve.html')  # 渲染index.html


from datetime import datetime

@app.route('/submit_record', methods=['POST'])
def submit_record():
    data = request.json
    patient_data = data.get('patient')
    record_data = data.get('record')
    admission_data = data.get('admission')
    username = session.get('username')

    if not username:
        return jsonify({"message": "Unauthorized"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert patient information
    cursor.execute('''
        INSERT INTO Patient (Name, Gender, Age, Address)
        VALUES (%s, %s, %s, %s)
    ''', (patient_data['Name'], patient_data['Gender'], patient_data['Age'], patient_data['Address']))
    patient_id = cursor.lastrowid

    # Get doctor ID
    cursor.execute('SELECT DoctorID FROM Doctor WHERE Username = %s', (username,))
    doctor_id = cursor.fetchone()[0]

    # Insert medical record
    cursor.execute('''
        INSERT INTO MedicalRecords (doctor_id, patient_id, symptom_record, treatment_plan)
        VALUES (%s, %s, %s, %s)
    ''', (doctor_id, patient_id, record_data['symptom_record'], record_data['treatment_plan']))

    # Convert datetime values to the correct format
    admission_date = datetime.strptime(admission_data['AdmissionDate'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
    expected_discharge_date = datetime.strptime(admission_data['ExpectedDischargeDate'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')

    # Insert admission record
    cursor.execute('''
        INSERT INTO AdmissionRecord (PatientID, WardID, BedID, AdmissionDate, ExpectedDischargeDate)
        VALUES (%s, %s, %s, %s, %s)
    ''', (patient_id, admission_data['WardID'], admission_data['BedID'], admission_date, expected_discharge_date))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Record submitted successfully"})

@app.route('/medical_records', methods=['GET'])
def get_medical_records():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            p.Name as patient_name,
            mr.symptom_record,
            mr.treatment_plan,
            ar.WardID as ward_id,
            ar.BedID as bed_id,
            ar.AdmissionDate as admission_date,
            ar.ExpectedDischargeDate as expected_discharge_date
        FROM MedicalRecords mr
        JOIN Patient p ON mr.patient_id = p.PatientID
        LEFT JOIN AdmissionRecord ar ON mr.patient_id = ar.PatientID
    ''')
    columns = [col[0] for col in cursor.description]
    records = [dict(zip(columns, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(records)

@app.route('/nurse')
def nurse():
    return render_template('nurse.html')  # 渲染index.html



if __name__ == '__main__':
    app.run(debug=True, port=5057)