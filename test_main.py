import unittest
from unittest.mock import patch
import sqlite3
#from LeopardWebPython import Admin
#from LeopardWebPython import Admin
from LeopardWebPython import Admin, Course, Instructor, Student

# Create a test database and connect to it
db_connection = sqlite3.connect(":memory:")

class TestCourseSchedule(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create tables and insert test data
        cursor = db_connection.cursor()
        cursor.execute("CREATE TABLE COURSES ("
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
        cursor.execute("INSERT INTO COURSES VALUES(33946, 'ADVANCED DIGITAL CIRCUIT DESIGN', 'BSEE', 800, 930, 'WEDNESDAY, FRIDAY', 'SUMMER', 2023, 4, 'John');")
        cursor.execute("INSERT INTO COURSES VALUES(33950, 'APPLIED PROGRAMMING CONCEPTS', 'BSCO', 800, 950, 'TUESDAY, THURSDAY', 'SUMMER', 2023, 3, 'Joe');")

        cursor.execute("CREATE TABLE COURSE_SCHEDULE ("
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
        cursor.execute("INSERT INTO COURSE_SCHEDULE VALUES(33946, 'ADVANCED DIGITAL CIRCUIT DESIGN', 'BSEE', 800, 930, 'WEDNESDAY, FRIDAY', 'SUMMER', 2023, 4, 'John');")
        cursor.execute("INSERT INTO COURSE_SCHEDULE VALUES(33950, 'APPLIED PROGRAMMING CONCEPTS', 'BSCO', 800, 950, 'TUESDAY, THURSDAY', 'SUMMER', 2023, 3, 'Joe');")

        cursor.execute("CREATE TABLE ADMIN ("
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

        cursor.execute("CREATE TABLE INSTRUCTOR ("
               "ID INTEGER PRIMARY KEY NOT NULL,"
               "NAME TEXT NOT NULL,"
               "SURNAME TEXT NOT NULL,"
               "TITLE TEXT NOT NULL,"
               "HIREYEAR TEXT NOT NULL,"
               "DEPT TEXT NOT NULL,"
               "EMAIL TEXT NOT NULL,"
               "USERNAME TEXT NOT NULL,"
               "PASSWORD TEXT NOT NULL)")
        cursor.execute("INSERT INTO INSTRUCTOR VALUES(123, 'John', 'Doe', 'Prof', '2024', 'BSCO', 'jdoe12', 'johnman', 'doeman')")

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
        cursor.execute("INSERT INTO STUDENT VALUES(1234, 'Dylan', 'OBrien', '2024', 'BSCE', 'obriend7', 'dylbo', 'obrilbo')")

        # Create instances of Admin, Instructor, and Student for testing
        cls.admin = Admin(db_connection)
        cls.instructor = Instructor(db_connection)
        cls.student = Student(db_connection)

    @classmethod
    def tearDownClass(cls):
        # Close the database connection
        db_connection.close()

    # Add/remove from course_schedule (bullet 1)
    def test_add_remove_course_schedule(self):
        # Test adding a course to the semester schedule (admin)
        course = Course(33945, 'NEW TEST COURSE', 'BSEE', 800, 930, 'WEDNESDAY, FRIDAY', 'SUMMER', 2023, 4, "Bob")
        self.instructor.add_course(course)
        # Retrieve the added course from the schedule
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM COURSE_SCHEDULE WHERE CRN = ?", (course.course_CRN,))
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], course.course_CRN)

        # Test removing a course from the semester schedule (admin)
        self.instructor.remove_course(course.course_CRN)
        # Retrieve the removed course from the schedule
        cursor.execute("SELECT * FROM COURSE_SCHEDULE WHERE CRN = ?", (course.course_CRN,))
        result = cursor.fetchone()
        self.assertIsNone(result)

    # Print Course_schedule (bullet 2)
    def test_print_roster(self):
        # Test printing course roster (instructor)
        instructor_name = "John"
        #expected = (f"Course CRN: 33946\nCourse Title: ADVANCED DIGITAL CIRCUIT DESIGN\nInstructor: {instructor_name}\n\n")
        expected = (33946, "ADVANCED DIGITAL CIRCUIT DESIGN", "John")
        actual = self.instructor.print_roster(instructor_name)
        self.assertEqual(expected, actual)

    # Add/remove courses from system (bullet 3)
    def test_add_remove_course(self):
        # Test adding a course to the semester schedule (admin)
        course = Course(33945, 'NEW TEST COURSE', 'BSEE', 800, 930, 'WEDNESDAY, FRIDAY', 'SUMMER', 2023, 4, "Bob")
        self.admin.add_course(course)
        # Retrieve the added course from the schedule
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM COURSES WHERE CRN = ?", (course.course_CRN,))
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], course.course_CRN)

        # Test removing a course from the semester schedule (admin)
        self.admin.remove_course(course.course_CRN)
        # Retrieve the removed course from the schedule
        cursor.execute("SELECT * FROM COURSES WHERE CRN = ?", (course.course_CRN,))
        result = cursor.fetchone()
        self.assertIsNone(result)


    # Test login (bullet 4)
    def test_login(self):
        # Test user authentication
        self.assertTrue(self.admin.authenticate('testadmin', 'test123'))
        self.assertTrue(self.instructor.authenticate('johnman', 'doeman'))
        self.assertTrue(self.student.authenticate('dylbo', 'obrilbo'))
        self.assertFalse(self.student.authenticate('dsedrgtysero', 'rgewargweso'))


    # Search all courses (bullet 5)
    def test_search_all_courses(self):
        # Test searching all courses (all users)
        expected_results = [(33946, 'ADVANCED DIGITAL CIRCUIT DESIGN', 'John')]
        results = self.student.search_courses("ADVANCED")
        self.assertEqual(results, expected_results)

    # Search courses by parameter (bullet 6)
    def test_search_courses_by_parameters(self):
        # Test searching courses by parameters (all users)
        expected_results = [(33946, 'ADVANCED DIGITAL CIRCUIT DESIGN', 'John')]
        results = self.student.search_courses("CIRCUIT")
        self.assertEqual(results, expected_results)

if __name__ == '__main__':
    unittest.main()

'''
#db_connection = sqlite3.connect("assignment5.db")
db_connection = sqlite3.connect(":memory:")

class TestLogin(unittest.TestCase):

    def test_test(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_login(self):
        #cursor = db_connection.cursor()
        admin = Admin(db_connection)
        username = "testadmin"
        password = "test123"
        self.assertTrue(admin.authenticate(username, password), "The u p was correct")
        self.assertFalse(admin.authenticate("wrong", password), "False")
        self.assertFalse(admin.Admin.authenticate(username, "wrong"), "False")

#unittest.main()

#if __name__ == '__main__':
#    unittest.main()
'''