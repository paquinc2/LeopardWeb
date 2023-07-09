import sqlite3

#####Add/remove course from semester schedule (based on course ID number).
#Assemble and print course roster (instructor).
#####Add/remove courses from the system (admin).
#Log-in, log-out (all users).
#Search all courses (all users) .
#####Search courses based on parameters (all users) – you should be able to enter the parameters such as course code, day/time, etc.
#A menu to implement the use-cases.
#####Edit classes as necessary to reflect the class diagrams


##################################################################################
####################### Creating Classes #########################################
##################################################################################
# Note: changed time to military time
class Course:
    def __init__(self, course_CRN, course_title, course_dept, course_startTime, course_endTime, course_days, course_semester, course_year, course_credits):
        self.course_CRN = course_CRN
        self.course_title = course_title
        self.course_dept = course_dept
        self.course_startTime = course_startTime
        self.course_endTime = course_endTime
        self.course_days = course_days
        self.course_semester = course_semester
        self.course_year = course_year
        self.course_credits = course_credits
        self.instructor = instructor

class User:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def authenticate(self, username, password):
        # This method is implemented by the subclasses
        raise NotImplementedError("Subclasses must implement the authenticate method.")

class Admin(User):
    def authenticate(self, username, password):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT ID, NAME, SURNAME FROM ADMIN WHERE USERNAME = ? AND PASSWORD = ?",
                       (username, password))
        admin_data = cursor.fetchone()
        if admin_data:
            admin_id, admin_name = admin_data
            self.user_type = "ADMIN"
            self.user_data = (admin_id, admin_name)
            return True
        return False

    def add_course(self, course):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO COURSES (CRN, TITLE, DEPT, STARTTIME, ENDTIME, DAYS, SEMESTER, YEAR, CREDITS, INSTRUCTOR) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (course.course_CRN, course.course_title, course.course_name, course.instructor))
        self.db_connection.commit()

    def remove_course(self, course_id):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM Courses WHERE course_id = ?", (course_id,))
        self.db_connection.commit()

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
        cursor.execute("SELECT CRN, TITLE, INSTRUCTOR "
                       "FROM COURSES "
                       "WHERE CRN LIKE ? OR TITLE LIKE ?",
                       (f"%{params}%", f"%{params}%"))
        results = cursor.fetchall()
        return results

##################################################################################
####################### Menu Functions ###########################################
##################################################################################
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
##################################################################################
####################### Creating Tables ##########################################
##################################################################################

# Creating Courses table
cursor.execute("CREATE TABLE IF NOT EXISTS COURSES ("
               "CRN INTEGER PRIMARY KEY NOT NULL,"
               "TITLE TEXT NOT NULL,"
               "DEPT TEXT NOT NULL,"
               "STARTTIME INTEGER NOT NULL,"
               "ENDTIME INTEGER NOT NULL,"
               "DAYS TEXT NOT NULL,"
               "SEMESTER TEXT NOT NULL,"
               "YEAR INTEGER NOT NULL,"
               "CREDITS INTEGER NOT NULL,"
               "INSTRUCTOR TEXT)")

# Creating Admin table
cursor.execute("CREATE TABLE IF NOT EXISTS ADMIN ("
               "ID INTEGER PRIMARY KEY NOT NULL,"
               "NAME TEXT NOT NULL,"
               "SURNAME TEXT NOT NULL,"
               "TITLE TEXT NOT NULL,"
               "OFFICE TEXT NOT NULL,"
               "EMAIL TEXT NOT NULL,"
               "USERNAME TEXT NOT NULL,"
               "PASSWORD TEXT NOT NULL)")

# Creating Instructor table
cursor.execute("CREATE TABLE IF NOT EXISTS INSTRUCTOR ("
               "ID INTEGER PRIMARY KEY NOT NULL,"
               "NAME TEXT NOT NULL,"
               "SURNAME TEXT NOT NULL,"
               "TITLE TEXT NOT NULL,"
               "HIREYEAR TEXT NOT NULL,"
               "DEPT TEXT NOT NULL,"
               "EMAIL TEXT NOT NULL,"
               "USERNAME TEXT NOT NULL,"
               "PASSWORD TEXT NOT NULL)")

# Creating Student table
cursor.execute("CREATE TABLE IF NOT EXISTS STUDENT ("
               "ID INTEGER PRIMARY KEY NOT NULL,"
               "NAME TEXT NOT NULL,"
               "SURNAME TEXT NOT NULL,"
               "GRADYEAR TEXT NOT NULL,"
               "MAJOR TEXT NOT NULL,"
               "EMAIL TEXT NOT NULL,"
               "USERNAME TEXT NOT NULL,"
               "PASSWORD TEXT NOT NULL)")

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

##################################################################################
####################### Main Menu Loop ###########################################
##################################################################################
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
