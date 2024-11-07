from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Initialize the SQLite database and create tables for courses, students, and student-course associations
def init_db():
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()
    # Create the courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id TEXT PRIMARY KEY,
            course_name TEXT NOT NULL
        )
    ''')
    
    # Create the student table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            student_name TEXT NOT NULL
        )
    ''')
    
    # Create an association table for students and courses
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_courses (
            student_id TEXT,
            course_id TEXT,
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(course_id) REFERENCES courses(course_id),
            PRIMARY KEY (student_id, course_id)
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database tables
init_db()

@app.route('/addCourse', methods=['POST'])
def add_course():
    try:
        data = request.get_json()
        course_name = data.get('course_name', '')
        course_id = data.get('course_id', '')
        
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
        existing_course = cursor.fetchone()
        
        if not existing_course:
            cursor.execute("INSERT INTO courses (course_id, course_name) VALUES (?, ?)", (course_id, course_name))
            conn.commit()
            response = {
                'status_code': '200',
                'message': 'Course added successfully'
            }
        else:
            response = {
                'status_code': '409',
                'message': 'Course with this ID already exists'
            }
        
        conn.close()
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'status_code': '503',
            'message': 'Internal Server Error'
        }), 503

@app.route('/getCourses', methods=['POST'])
def get_courses():
    try:
        data = request.get_json()
        student_id = data.get('student_id', '')
        
        # Query to get all course names for a given student
        conn = sqlite3.connect('courses.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT courses.course_name 
            FROM courses 
            INNER JOIN student_courses ON courses.course_id = student_courses.course_id 
            WHERE student_courses.student_id = ?
        ''', (student_id,))
        
        courses_taken = cursor.fetchall()
        course_names = [course[0] for course in courses_taken]  # Extract course names from the result
        
        if course_names:
            response = {
                'status_code': '200',
                'courses': course_names
            }
        else:
            response = {
                'status_code': '404',
                'message': 'No courses found for the given student ID'
            }
        
        conn.close()
        return jsonify(response)
    
    except Exception as e:
        return jsonify({
            'status_code': '503',
            'message': 'Internal Server Error'
        }), 503

if __name__ == '__main__':
    app.run(debug=True)
