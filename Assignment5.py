import sqlite3

# Class representing a Course
class Course:
    def __init__(self, course_id, course_code, course_name, instructor):
        self.course_id = course_id
        self.course_code = course_code
        self.course_name = course_name
        self.instructor = instructor

# Base class representing a User
class User:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def authenticate(self, username, password):
        # This method is implemented by the subclasses
        raise NotImplementedError("Subclasses must implement the authenticate method.")

# Subclass representing an Admin
class Admin(User):
    def authenticate(self, username, password):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT admin_id, admin_name FROM Admin WHERE username = ? AND password = ?",
                       (username, password))
        admin_data = cursor.fetchone()
        if admin_data:
            admin_id, admin_name = admin_data
            self.user_type = "Admin"
            self.user_data = (admin_id, admin_name)
            return True
        return False

    def add_course(self, course):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO Courses (course_id, course_code, course_name, instructor) "
                       "VALUES (?, ?, ?, ?)",
                       (course.course_id, course.course_code, course.course_name, course.instructor))
        self.db_connection.commit()

    def remove_course(self, course_id):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM Courses WHERE course_id = ?", (course_id,))
        self.db_connection.commit()

# Subclass representing an Instructor
class Instructor(User):
    def authenticate(self, username, password):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT instructor_id, instructor_name FROM Instructor WHERE username = ? AND password = ?",
                       (username, password))
        instructor_data = cursor.fetchone()
        if instructor_data:
            instructor_id, instructor_name = instructor_data
            self.user_type = "Instructor"
            self.user_data = (instructor_id, instructor_name)
            return True
        return False

    def print_roster(self, instructor_name):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT course_code, course_name, instructor "
                       "FROM Courses "
                       "WHERE instructor = ?",
                       (instructor_name,))
        roster = cursor.fetchall()
        for course in roster:
            print(f"Course Code: {course[0]}")
            print(f"Course Name: {course[1]}")
            print(f"Instructor: {course[2]}")
            print()

# Subclass representing a Student
class Student(User):
    def authenticate(self, username, password):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT student_id, student_name FROM Student WHERE username = ? AND password = ?",
                       (username, password))
        student_data = cursor.fetchone()
        if student_data:
            student_id, student_name = student_data
            self.user_type = "Student"
            self.user_data = (student_id, student_name)
            return True
        return False

    def search_courses(self, params):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT course_code, course_name, instructor "
                       "FROM Courses "
                       "WHERE course_code LIKE ? OR course_name LIKE ?",
                       (f"%{params}%", f"%{params}%"))
        results = cursor.fetchall()
        return results

# Function to display the menu based on user type
def display_menu(user_type):
    print("MENU:")
    print("1. Add course to semester schedule")
    print("2. Remove course from semester schedule")
    if user_type == "Admin":
        print("3. Add instructor to the system")
    if user_type == "Instructor":
        print("4. Print course roster")
    if user_type == "Student":
        print("5. Search all courses")
    print("6. Exit")

# Creating database and connecting to it
db_connection = sqlite3.connect("assignment5.db")

# Creating tables
cursor = db_connection.cursor()

# Creating Admin table
cursor.execute("CREATE TABLE IF NOT EXISTS Admin ("
               "admin_id INTEGER PRIMARY KEY,"
               "admin_name TEXT,"
               "username TEXT,"
               "password TEXT)")

# Creating Courses table
cursor.execute("CREATE TABLE IF NOT EXISTS Courses ("
               "course_id INTEGER PRIMARY KEY,"
               "course_code TEXT,"
               "course_name TEXT,"
               "instructor TEXT)")

# Creating Instructor table
cursor.execute("CREATE TABLE IF NOT EXISTS Instructor ("
               "instructor_id INTEGER PRIMARY KEY,"
               "instructor_name TEXT,"
               "username TEXT,"
               "password TEXT)")

# Creating Student table
cursor.execute("CREATE TABLE IF NOT EXISTS Student ("
               "student_id INTEGER PRIMARY KEY,"
               "student_name TEXT,"
               "username TEXT,"
               "password TEXT)")

# Committing the changes
db_connection.commit()

# Creating instances of Admin, Instructor, and Student
admin = Admin(db_connection)
instructor = Instructor(db_connection)
student = Student(db_connection)

# Authenticating the user
while True:
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user = None

    # Check in the Admin table
    if admin.authenticate(username, password):
        user = admin

    # Check in the Instructor table
    elif instructor.authenticate(username, password):
        user = instructor

    # Check in the Student table
    elif student.authenticate(username, password):
        user = student

    if user:
        break

    print("Authentication failed. Please try again.")

print("Authentication successful!")
print(f"Welcome, {user.user_type} {user.user_data[1]}!")

# Main menu loop
while True:
    display_menu(user.user_type)

    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        course_id = input("Enter the course ID: ")
        course_code = input("Enter the course code: ")
        course_name = input("Enter the course name: ")
        instructor_name = input("Enter the instructor name: ")
        course = Course(course_id, course_code, course_name, instructor_name)
        admin.add_course(course)
        print("Course added to the semester schedule.")

    elif choice == "2":
        course_id = input("Enter the course ID to remove: ")
        admin.remove_course(course_id)
        print("Course removed from the semester schedule.")

    elif choice == "3" and user.user_type == "Admin":
        instructor_id = input("Enter the instructor ID: ")
        instructor_name = input("Enter the instructor name: ")
        username = input("Enter the instructor username: ")
        password = input("Enter the instructor password: ")
        cursor.execute("INSERT INTO Instructor (instructor_id, instructor_name, username, password) "
                       "VALUES (?, ?, ?, ?)",
                       (instructor_id, instructor_name, username, password))
        db_connection.commit()
        print("Instructor added to the system.")

    elif choice == "4" and user.user_type == "Instructor":
        instructor_name = input("Enter the instructor name to print the roster: ")
        instructor.print_roster(instructor_name)

    elif choice == "5" and user.user_type == "Student":
        params = input("Enter the search parameters: ")
        results = student.search_courses(params)
        for course in results:
            print(f"Course Code: {course[0]}")
            print(f"Course Name: {course[1]}")
            print(f"Instructor: {course[2]}")
            print()

    elif choice == "6":
        break

    else:
        print("Invalid choice. Please try again.")

# Closing the database connection
db_connection.close()
