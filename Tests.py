import unittest
from unittest.mock import patch
import sqlite3
from Assignment6 import Admin, Course, Instructor, Student, Schedule

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
                       "INSTRUCTOR INTEGER)")
        cursor.execute("INSERT INTO COURSES VALUES(33946, 'ADVANCED DIGITAL CIRCUIT DESIGN', 'BSEE', 800, 930, 'WEDNESDAY, FRIDAY', 'SUMMER', 2023, 4, 1);")
        cursor.execute("INSERT INTO COURSES VALUES(33950, 'APPLIED PROGRAMMING CONCEPTS', 'BSCO', 800, 950, 'TUESDAY, THURSDAY', 'SUMMER', 2023, 3, 2);")

        # Create instances of Admin, Instructor, and Student for testing
        cls.admin = Admin(db_connection)
        cls.instructor = Instructor(db_connection)
        cls.student = Student(db_connection)

    @classmethod
    def tearDownClass(cls):
        # Close the database connection
        db_connection.close()

    def test_add_remove_course(self):
        # Test adding a course to the semester schedule (admin)
        course = Course(33946, 'ADVANCED DIGITAL CIRCUIT DESIGN', 'BSEE', 800, 930, 'WEDNESDAY, FRIDAY', 'SUMMER', 2023, 4)
        self.admin.add_course(course)
        # Retrieve the added course from the schedule
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM COURSE_SCHEDULE WHERE CRN = ?", (course.course_CRN,))
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], course.course_CRN)

        # Test removing a course from the semester schedule (admin)
        self.admin.remove_course(course.course_CRN)
        # Retrieve the removed course from the schedule
        cursor.execute("SELECT * FROM COURSE_SCHEDULE WHERE CRN = ?", (course.course_CRN,))
        result = cursor.fetchone()
        self.assertIsNone(result)

    @patch('builtins.print')
    def test_print_roster(self, mock_print):
        # Test printing course roster (instructor)
        instructor_name = "John Doe"
        self.instructor.print_roster(instructor_name)
        mock_print.assert_called_with(f"Course CRN: 33946\nCourse Title: ADVANCED DIGITAL CIRCUIT DESIGN\nInstructor: {instructor_name}\n\n")

    def test_login_logout(self):
        # Test user authentication
        self.assertTrue(self.admin.authenticate('testadmin', 'test123'))
        self.assertTrue(self.instructor.authenticate('instructor_username', 'instructor_password'))
        self.assertTrue(self.student.authenticate('student_username', 'student_password'))

        # Test user logout (not implemented in the provided code)
        self.assertRaises(NotImplementedError, self.admin.logout)

    def test_search_all_courses(self):
        # Test searching all courses (all users)
        expected_results = [(33946, 'ADVANCED DIGITAL CIRCUIT DESIGN', 'John Doe')]
        results = self.student.search_courses("")
        self.assertEqual(results, expected_results)

    def test_search_courses_by_parameters(self):
        # Test searching courses by parameters (all users)
        expected_results = [(33946, 'ADVANCED DIGITAL CIRCUIT DESIGN', 'John Doe')]
        results = self.student.search_courses("CIRCUIT")
        self.assertEqual(results, expected_results)

if __name__ == '__main__':
    unittest.main()
