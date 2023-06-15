#include <iostream>
#include <string>
#include <stdio.h>
#include "sqlite3.h"
#include "User.h"
#include "Student.h"
#include "Instructor.h"
#include "Admin.h"
#include "Database.h"

using std::cout;
using std::cin;

using namespace std;


int main(int argc, char** argv) {
	
	Database database("assignment3.db");
	database.db_script();

	string firstname;
	string lastname;
	int id;

	//User interface for selecting/naming user
	cout << "Welcome to the user creation system! Please choose the type of user you want to create.\n";
	cout << "Student - 1\nInstructor - 2\nAdmin - 3\nBasic user - 0\n\n";
	int choice;
	cin >> choice;
	cout << "Please enter the user's first name: ";
	cin >> firstname;
	cout << "Please enter the user's last name: ";
	cin >> lastname;
	cout << "Please enter the user's ID: ";
	cin >> id;

	//Basic user
	if (choice == 0) {
		User user(firstname, lastname, id);
		user.user_info();
		user.set_firstname("John");
		user.set_lastname("Doe");
		user.set_ID(654321);
		user.user_info();

		cout << "\n";
	}

	//Student
	else if (choice == 1) {
		Student student(firstname, lastname, id);
		student.user_info();
		student.search_course("Course");
		student.add_course("Course");
		student.remove_course("Course");
		student.print_schedule();

		cout << "\n";
	}

	//Instructor
	else if (choice == 2) {
		Instructor instructor(firstname, lastname, id);
		instructor.user_info();
		instructor.search_course("Search");
		instructor.print_schedule();
		instructor.print_classlist();

		cout << "\n";
	}

	//Admin
	else if (choice == 3) {

		Admin admin(firstname, lastname, id);
		admin.user_info();
		admin.search_course("Course");
		admin.search_roster("Course");
		admin.add_course("Course");
		admin.remove_course("Course");
		admin.add_user();
		admin.remove_user(1234);
		admin.add_student();
		admin.remove_student(1234);
		admin.print_roster();
		admin.print_courses();
	}

	return 0;
}

//Sources
//https://www.geeksforgeeks.org/inheritance-in-c/#