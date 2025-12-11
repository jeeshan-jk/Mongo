from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['student_db']
students = db['students']

# Display stats
print(f'✓ Total students in MongoDB: {students.count_documents({})}')
print('\nFirst 5 students:')
for s in students.find().limit(5):
    print(f"  - {s['Name']} ({s['USN']}) - Grade: {s['Grade']}")
