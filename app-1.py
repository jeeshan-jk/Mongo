from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import pandas as pd
import os

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["student_db"]
students_collection = db["students"]

# Function to load CSV data into MongoDB (one-time import)
def import_csv_to_mongodb():
    CSV_FILE = 'student_data (1).csv'
    if os.path.exists(CSV_FILE):
        # Check if data already imported
        if students_collection.count_documents({}) == 0:
            df = pd.read_csv(CSV_FILE)
            # Add Grade column if not exists
            if 'Grade' not in df.columns:
                df['Grade'] = 'Not Assigned'
            # Convert to dict and insert into MongoDB
            records = df.to_dict('records')
            if records:
                students_collection.insert_many(records)
                print(f"Imported {len(records)} students from CSV to MongoDB")

# Import CSV data when app starts
import_csv_to_mongodb()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/students', methods=['GET'])
def get_students():
    student_list = []
    for student in students_collection.find():
        student['_id'] = str(student['_id'])
        student_list.append(student)
    return jsonify(student_list)

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    
    # Check if USN already exists
    if students_collection.find_one({"USN": data['roll']}):
        return jsonify({"error": "Student with this USN already exists"}), 400
    
    new_student = {
        'Name': data['name'],
        'USN': data['roll'],
        'Grade': data['grade']
    }
    result = students_collection.insert_one(new_student)
    return jsonify({"message": "Student added successfully!", "id": str(result.inserted_id)}), 201

@app.route('/api/students/<roll>', methods=['GET'])
def search_student(roll):
    student = students_collection.find_one({"USN": roll})
    if student:
        student['_id'] = str(student['_id'])
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route('/api/students/<roll>', methods=['PUT'])
def update_student(roll):
    data = request.json
    result = students_collection.update_one(
        {"USN": roll},
        {"$set": {"Grade": data['grade']}}
    )
    if result.matched_count:
        return jsonify({"message": "Student updated successfully!"})
    return jsonify({"error": "Student not found"}), 404

@app.route('/api/students/<roll>', methods=['DELETE'])
def delete_student(roll):
    result = students_collection.delete_one({"USN": roll})
    if result.deleted_count:
        return jsonify({"message": "Student deleted successfully!"})
    return jsonify({"error": "Student not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
