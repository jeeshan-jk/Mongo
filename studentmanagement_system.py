from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select database and collection
db = client["student_db"]
students = db["students"]

# ---- CREATE ----
def add_student():
    name = input("Enter student name: ")
    roll = input("Enter roll number: ")
    grade = input("Enter grade: ")

    students.insert_one({
        "name": name,
        "roll": roll,
        "grade": grade
    })
    print("Student record added successfully!")

# ---- READ ----
def show_students():
    print("\n--- Student Records ---")
    for s in students.find():
        print(s)

def search_student():
    roll = input("Enter roll number to search: ")
    student = students.find_one({"roll": roll})
    print("Result:", student)

# ---- UPDATE ----
def update_student():
    roll = input("Enter roll number to update: ")
    new_grade = input("Enter new grade: ")

    students.update_one(
        {"roll": roll},
        {"$set": {"grade": new_grade}}
    )
    print("Student record updated!")

# ---- DELETE ----
def delete_student():
    roll = input("Enter roll number to delete: ")
    students.delete_one({"roll": roll})
    print("Student record deleted!")

# ---- MENU LOOP ----
while True:
    print("\n--- Student Database Management ---")
    print("1. Add Student")
    print("2. Show All Students")
    print("3. Search Student")
    print("4. Update Student Grade")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        show_students()
    elif choice == "3":
        search_student()
    elif choice == "4":
        update_student()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        print("Exiting program...")
        break
    else:
        print("Invalid choice! Try again.")
