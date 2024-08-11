from flask import Flask, render_template, request, redirect, url_for, flash
import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
import face_processing
import subprocess
import encode_upload






cred = credentials.Certificate("faceattendancerealtime-50d48-firebase-adminsdk-dqvrs-34b6851fed.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendancerealtime-50d48-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-50d48.appspot.com"
})

bucket = storage.bucket()
ADMIN_USERNAME = db.reference(f'Admin/id').get()
ADMIN_PASSWORD = db.reference(f'Admin/password').get()

ADMIN_USERNAME,ADMIN_PASSWORD = str(ADMIN_USERNAME),str(ADMIN_PASSWORD)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Hardcoded admin and student credentials for demonstration purposes


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            # Credentials are correct, redirect to admin page
            return redirect(url_for('admin'))
        else:

            flash('Invalid id or password',   'error')
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

#
# @app.route('/student_login', methods=['GET', 'POST'])
# def student_login():
#     if request.method == 'POST':
#         student_id = request.form.get('username')  # Assuming student ID is used as username
#         password = request.form.get('password')
#
#         # Dummy authentication (replace with your authentication logic)
#         if student_id in students and password == "password":
#             return redirect(url_for('student', student_id=student_id))
#         else:
#             flash('Invalid username or password')
#             return redirect(url_for('student_login'))
#     return render_template('student_login.html')
#
# @app.route('/student/<student_id>')
# def student(student_id):
#     student_details = students.get(student_id)
#     if student_details:
#         return render_template('student.html', student_id=student_id, student_details=student_details)
#     else:
#         flash('Student not found')
#         return redirect(url_for('student_login'))
#



@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Get form data
        student_id = request.form['student_id']
        student_name = request.form['student_name']
        branch = request.form['branch']
        academic_year = request.form['academic_year']

        # Get the file from the request
        file = request.files['image']
        student_no = student_id
        # Save the file
        file.save(f"C:/Users/gopiv/PycharmProjects/OpencvPython/FaceRecognitionRealTimeDatabase/Images/{file.filename}")
        # print(student_name,student_id,branch,academic_year,file.filename)
        current_time = datetime.now()

        # Format the date and time as a string
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        data = {
              # Use student_id as the key
                "name": student_name,
                "Major": branch,
                "starting_year": int(academic_year),  # Convert to int if needed
                "total_attendance": 0,
                "standing": "A",
                "year": 6,
                "last_attendance_time": formatted_time

        }
        data1 = {
            "id": student_id,
            "password":student_name

        }

        # Upload data to Firebase
        ref = db.reference("Students")
        ref.child(student_id).set(data)
        ref1 = db.reference("StudentAut")
        ref1.child(student_id).set(data1)

        face_operation = face_processing.detect_face(f"C:/Users/gopiv/PycharmProjects/OpencvPython/FaceRecognitionRealTimeDatabase/Images/{file.filename}")
        encode_and_upload = encode_upload.save_encodings_to_file('Images')

        flash('successfully student added!',   'error')
        return redirect(url_for('add_student'))

    return render_template('add_student.html')


@app.route('/update_student',methods=['GET', 'POST'])
def update_student():
    if request.method == 'POST':
        # Get form data
        student_id = request.form['student_id']
        data = get_student_details(student_id)
        if data:
            return render_template('update_student_details.html',student=data,id=student_id)
        else:

            flash('Invalid studentId', 'error')
            return redirect(url_for('update_student'))
    return render_template('update_student.html')

@app.route('/update_student/<student_id>', methods=['POST'])
def update_student_submit(student_id):
    updated_name = request.form['student_name']
    updated_branch = request.form['branch']
    updated_academic_year = request.form['academic_year']

    # Update student details in Firebase
    ref = db.reference('Students')
    ref.child(student_id).update({
        'name': updated_name,
        'Major': updated_branch,
        'academic_year': updated_academic_year
    })

    flash('successfully updated', 'error')
    return redirect(url_for('update_student'))


@app.route('/view')
def view():
    return render_template('view.html')

@app.route('/get_student', methods=['GET', 'POST'])
def get_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        student_details = get_student_details(student_id)
        if student_details:
            return render_template('view_by_id.html', student_details=student_details,student_id=student_id)
        else:
            flash('Invalid studentId', 'error')
            return redirect(url_for('view'))
    return render_template('get_student.html')

@app.route('/get_all_students')
def get_all_students():
    all_students = get_all_students()
    return render_template('view_all.html', all_students=all_students)

@app.route('/delete',methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        student_id = request.form['student_id']
        if student_id != "":

            if not get_student_details(student_id):
                flash('invalid studentId', 'error')
                return redirect(url_for('delete'))
            flag1 = delete_student(student_id)
            flag2 = delete_image(student_id)
            delete_login_info(student_id)

            if flag1 and flag2:
                flash('successfully deleted', 'error')
                return redirect(url_for('delete'))
    return render_template("delete.html")

@app.route('/student_login',methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form.get('student_id')
        password = request.form.get('password')
        STUDENT_USERNAME = db.reference(f'StudentAut/{username}/id').get()
        STUDENT_PASSWORD = db.reference(f'StudentAut/{username}/password').get()
        # print(username,password)
        # print(STUDENT_USERNAME,STUDENT_PASSWORD)
        STUDENT_USERNAME, STUDENT_PASSWORD = str(STUDENT_USERNAME), str(STUDENT_PASSWORD)
        if username == STUDENT_USERNAME and password == STUDENT_PASSWORD:
            student_id = username
            student_details = get_student_details(student_id)
            if student_details:
                return render_template('view_by_id.html', student_details=student_details, student_id=student_id)
            else:
                # Credentials are incorrect, show flash message
                flash('Data not found', 'error')
                return redirect(url_for('student_login'))
        else:
            # Credentials are incorrect, show flash message
            flash('Invalid username or password',   'error')
            return redirect(url_for('student_login'))
    return render_template('student_login.html')





def get_student_details(student_id):
    ref = db.reference("Students")
    student_data = ref.child(student_id).get()
    return student_data


# Function to retrieve all student details from Firebase
def get_all_students():
    ref = db.reference('Students')
    all_students = ref.get()
    return all_students

def delete_student(student_id):
    ref = db.reference('Students')  # Assuming 'students' is the root node where student data is stored
    ref.child(student_id).delete()
    return True
def delete_login_info(student_id):
    ref = db.reference('StudentAut')  # Assuming 'students' is the root node where student data is stored
    ref.child(student_id).delete()
    return True


def delete_image(student_id):
        bucket = storage.bucket()
        blob = bucket.blob(f'Images/{student_id}.png')
        blob.delete()
        file_path = f"C:\\Users\\gopiv\\PycharmProjects\\OpencvPython\\FaceRecognitionRealTimeDatabase\\Images\\{student_id}.png"
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
        encode_and_upload = encode_upload.save_encodings_to_file('Images')
        return True

if __name__ == '__main__':
    app.run(debug=True)


