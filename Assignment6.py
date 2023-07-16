import sqlite3
##################################################################################
####################### Creating Classes #########################################
##################################################################################
# Note: changed time to military time
class Course:
    def __init__(self, course_CRN, course_title, course_dept, course_startTime, course_endTime, course_days, course_semester, course_years, course_credits):
        self.course_CRN = course_CRN
        self.course_title = course_title
        self.course_dept = course_dept
        self.course_startTime = course_startTime
        self.course_endTime = course_endTime
        self.course_days = course_days
        self.course_semester = course_semester
        self.course_years = course_years
        self.course_credits = course_credits
        self.instructor = instructor

class Schedule:
    def __init__(self, db_connection):
        self.db_connection = db_connection

class User:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def authenticate(self, username, password):
        # This method is implemented by the subclasses
        raise NotImplementedError("Subclasses must implement the authenticate method.")

    def search_courses(self, params):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT CRN, TITLE, INSTRUCTOR "
                       "FROM COURSES "
                       "WHERE CRN LIKE ? OR TITLE LIKE ? OR DEPT LIKE ? " 
                       "OR STARTTIME = ? OR ENDTIME = ? OR DAYS LIKE ? "
                       "OR SEMESTER LIKE ? OR YEAR = ? OR CREDITS = ? "
                       "OR INSTRUCTOR LIKE ?",
                       (f"%{params}%", f"%{params}%", f"%{params}%", f"%{params}%", 
                        f"%{params}%", f"%{params}%", f"%{params}%", f"%{params}%",
                        f"%{params}%", f"%{params}%"))
        results = cursor.fetchall()
        return results

class Admin(User):
    def authenticate(self, username, password):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT ID, NAME, SURNAME FROM ADMIN WHERE USERNAME = ? AND PASSWORD = ?",
                       (username, password))
        admin_data = cursor.fetchone()
        if admin_data:
            admin_id = admin_data[0]
            admin_name = admin_data[1]
            self.user_type = "ADMIN"
            self.user_data = (admin_id, admin_name)
            return True
        return False

    def add_course(self, course):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO COURSES (CRN, TITLE, DEPT, STARTTIME, ENDTIME, DAYS, SEMESTER, YEAR, CREDITS, INSTRUCTOR) "
               "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
               (course.course_CRN, course.course_title, course.course_dept, course.course_startTime, course.course_endTime, course.course_days, course.course_semester, course.course_years, course.course_credits, course.instructor))
        self.db_connection.commit()

    def remove_course(self, course_CRN):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM COURSES WHERE CRN = ?", (course_CRN))
        self.db_connection.commit()

class Instructor(User):
    def authenticate(self, username, password):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT ID, NAME, SURNAME FROM INSTRUCTOR WHERE USERNAME = ? AND PASSWORD = ?",
                       (username, password))
        instructor_data = cursor.fetchone()
        if instructor_data:
            instructor_id, instructor_name = instructor_data
            self.user_type = "INSTRUCTOR"
            self.user_data = (instructor_id, instructor_name)
            return True
        return False

    def print_roster(self, instructor_name):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT CRN, TITLE, INSTRUCTOR "
                       "FROM COURSES "
                       "WHERE INSTRUCTOR = ?",
                       (instructor_id))
        roster = cursor.fetchall()
        for course in roster:
            print(f"Course CRN: {course[0]}")
            print(f"Course Title: {course[1]}")
            print(f"Instructor: {course[2]}")
            print()

class Student(User):
    def authenticate(self, username, password):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT ID, NAME, SURNAME FROM STUDENT WHERE USERNAME = ? AND PASSWORD = ?",
                       (username, password))
        student_data = cursor.fetchone()
        if student_data:
            student_id, student_name = student_data
            self.user_type = "STUDENT"
            self.user_data = (student_id, student_name)
            return True
        return False

##################################################################################
####################### Menu Functions ###########################################
##################################################################################
def display_menu(user_type):
    print("MENU:")

    if user_type == "ADMIN":
        print("1. Add/Remove course from semester schedule")
        print("2. Search for course(s)")
        print("3. Add/Remove Instructor from the system")
        print("4. Add/Remove Student from the system")
        print("5. Add/Remove Course to system")
        print("6. Exit")
    if user_type == "INSTRUCTOR":
        print("1. Add course to semester schedule")
        print("2. Search for course(s)")
        print("3. Print course roster")
    if user_type == "STUDENT":
        print("1. Add course to semester schedule")
        print("2. Search for course(s)")
        print("3. Search all courses")

# Creating database and connecting to it
db_connection = sqlite3.connect("assignment5.db")

# Creating tables
cursor = db_connection.cursor()
##################################################################################
####################### Creating Tables ##########################################
##################################################################################

# Creating Courses table
cursor.execute("DROP TABLE IF EXISTS COURSES")
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
               "INSTRUCTOR INTEGER)")

cursor.execute("INSERT INTO COURSES VALUES(33946, 'ADVANCED DIGITAL CIRCUIT DESIGN', 'BSEE', 800, 930, 'WEDNESDAY, FRIDAY', 'SUMMER', 2023, 4, 1);")
cursor.execute("INSERT INTO COURSES VALUES(33950, 'APPLIED PROGRAMMING CONCEPTS', 'BSCO', 800, 950, 'TUESDAY, THURSDAY', 'SUMMER', 2023, 3, 2);")
cursor.execute("INSERT INTO COURSES VALUES(33817, 'ALGORITHMS', 'BSCS', 1100, 1220, 'MONDAY, WEDNESDAY', 'SUMMER', 2023, 4, 3);")
cursor.execute("INSERT INTO COURSES VALUES(33955, 'COMPUTER NETWORKS', 'BSCO', 1230, 1320, 'MONDAY, WEDNESDAY', 'SUMMER', 2023, 4, 4);")
cursor.execute("INSERT INTO COURSES VALUES(33959, 'SIGNALS AND SYSTEMS', 'BSEE', 1300, 1450, 'TUESDAY, THURSDAY', 'SUMMER', 2023, 4, 5);")


# Creating Course_Schedule table --> will grab rows from Courses table
cursor.execute("DROP TABLE IF EXISTS COURSE_SCHEDULE")
cursor.execute("CREATE TABLE IF NOT EXISTS COURSE_SCHEDULE ("
               "CRN INTEGER PRIMARY KEY NOT NULL,"
               "TITLE TEXT NOT NULL,"
               "DEPT TEXT NOT NULL,"
               "STARTTIME INTEGER NOT NULL,"
               "ENDTIME INTEGER NOT NULL,"
               "DAYS TEXT NOT NULL,"
               "SEMESTER TEXT NOT NULL,"
               "YEAR INTEGER NOT NULL,"
               "CREDITS INTEGER NOT NULL,"
               "INSTRUCTOR INTEGER)")

# Creating Admin table
cursor.execute("DROP TABLE IF EXISTS ADMIN")
cursor.execute("CREATE TABLE IF NOT EXISTS ADMIN ("
               "ID INTEGER PRIMARY KEY NOT NULL,"
               "NAME TEXT NOT NULL,"
               "SURNAME TEXT NOT NULL,"
               "TITLE TEXT NOT NULL,"
               "OFFICE TEXT NOT NULL,"
               "EMAIL TEXT NOT NULL,"
               "USERNAME TEXT NOT NULL,"
               "PASSWORD TEXT NOT NULL)")

# Inserting into Admin
cursor.execute("INSERT INTO ADMIN VALUES(1, 'Test', 'Admin', 'President', 'Dobbs 210', 'tadmin12', 'testadmin', 'test123')")

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

    choice = input("Enter your choice: ")

    # Add/remove course from semester schedule
    if choice == "1":
        ar = input("Select (1) if you want to ADD a course or (2) if you want to REMOVE a course: ")
        if ar == "1":
            course_CRN = input("Enter the CRN of the course you want to add to the semesester schedule: ")
            cursor.execute("INSERT INTO COURSE_SCHEDULE SELECT * FROM COURSES WHERE COURSES.CRN = ?",
                            (course_CRN,))
            db_connection.commit()
            print("Course successfully added")
        elif ar == "2":
            course_CRN = input("Enter the CRN of the course you want to remove from the semesester schedule: ")
            cursor.execute("DELETE FROM COURSE_SCHEDULE WHERE CRN = ?",
                            (course_CRN,))
            db_connection.commit()
            print("Course successfully removed")
        else:
            print("Invalid choice")

    # Search for courses
    elif choice == "2":
        search_query = input("Enter a field to search courses by (Any parameter): ")
        print(user.search_courses(search_query))

    # Add/remove instructor
    elif choice == "3" and user.user_type == "ADMIN":
        instructor_id = input("Enter the instructor ID: ")
        instructor_name = input("Enter the instructor name: ")
        username = input("Enter the instructor username: ")
        password = input("Enter the instructor password: ")
        cursor.execute("INSERT INTO Instructor (instructor_id, instructor_name, username, password) "
                       "VALUES (?, ?, ?, ?)",
                       (instructor_id, instructor_name, username, password))
        db_connection.commit()
        print("Instructor added to the system.")

    # Add/remove student
    elif choice == "4" and user.user_type == "ADMIN":
        print("add/remove student")

    # Add/remove course
    elif choice == "5" and user.user_type == "ADMIN":
        ar = input("Select (1) if you want to ADD a course or (2) if you want to REMOVE a course: ")
        if ar == 1:
            course_CRN = input("Input the course CRN: ")
            course_title = input("Input course name: ")
            course_dept = input("Enter the department abbreviation the course belongs to: ")
            course_startTime = input("Enter the start time of the course in military time, represented as an integer: ")
            course_endTime = input("Enter the end time of the course in military time, represented as an integer: ")
            course_days = input("Enter the days this course is taught on separated by commas: ")
            course_semester = input("Enter the semester this course is taught in: ")
            course_years = input("Enter the year that this semester is taught: ")
            course_credits = input("Enter the number of credits this course is worth: ")
            course_instructor = input("Enter the ID or Name of the instructor who teaches this course: ")

            cursor.execute("INSERT INTO COURSES (CRN, TITLE, DEPT, STARTTIME, ENDTIME, DAYS, SEMESTER, YEAR, CREDITS, INSTRUCTOR) " 
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (course_CRN, course_title, course_dept, course_startTime, 
                            course_endTime, course_days, course_semester, course_years, course_credits, course_instructor))
            db_connection.commit()
        elif ar == 2:
            course_CRN = input("Enter the CRN of the course you would like to remove from the system: ")
            cursor.execute("DELETE FROM COURSES WHERE CRN = ?", (course_CRN,))
            db_connection.commit()
        else:
            print("Invalid choice")
        
    elif choice == "4" and user.user_type == "INSTRUCTOR":
        instructor_name = input("Enter the instructor name to print the roster: ")
        instructor.print_roster(instructor_name)

    elif choice == "5" and user.user_type == "STUDENT":
        params = input("Enter the search parameters: ")
        results = student.search_courses(params)
        for course in results:
            print(f"Course CRN: {course[0]}")
            print(f"Course Name: {course[1]}")
            print(f"Instructor: {course[2]}")
            print()

    elif choice == "6":
        break

    else:
        print("Invalid choice. Please try again.")

# Closing the database connection
db_connection.close()
