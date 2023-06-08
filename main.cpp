#include <iostream>
#include <string>
#include <stdio.h>
#include "sqlite3.h"
#include "User.h"
#include "Student.h"
#include "Instructor.h"
#include "Admin.h"

using std::cout;
using std::cin;

using namespace std;

/*************************************************************************************************
 The callback() function is invoked for each result row coming out of the evaluated SQL statement
 1st argument - the 4th argument provided by sqlite3_exec() and is typically not used
 2nd argument - number of columns in the result
 3rd argument - an array of strings containing the fields in that row
 4th argument - an array of strings containing the names of the columns
*************************************************************************************************/
static int callback(void* data, int argc, char** argv, char** azcolname)
{
	int i;

	for (i = 0; i < argc; i++)
	{
		printf("%s = %s\n", azcolname[i], argv[i] ? argv[i] : "null");
	}

	printf("\n");

	return 0;
}

int main(int argc, char** argv) {
	
	//*************************************
	// Define and open the database
	//*************************************
	sqlite3* DB;
	int exit = 0;
	exit = sqlite3_open("assignment3.db", &DB);

	if (exit) {
		std::cerr << "Error open DB " << sqlite3_errmsg(DB) << std::endl;
		return (-1);
	}
	else
		std::cout << "Opened Database Successfully!" << std::endl;

	//*************************************
	// Creating a course table
	// Time is in military time
	//*************************************

	string table = "CREATE TABLE COURSES("
	"CRN INTEGER PRIMARY KEY, "
	"TITLE TEXT NOT NULL, "
	"DEPARTMENT TEXT NOT NULL, "
	"TIME TEXT NOT NULL, "
	"DAYS TEXT NOT NULL, "
	"SEMESTER TEXT NOT NULL, "
	"YEAR INTEGER NOT NULL, "
	"CREDITS INTEGER NOT NULL); ";

	char* messageError;

	// execute the create table command
	// sqlite3_exec( pointer to database file, string for sql command, callback function (used to respond to queries, not used here), input to callback, error message address)
	exit = sqlite3_exec(DB, table.c_str(), NULL, 0, &messageError);

	if (exit != SQLITE_OK)
	{
		std::cerr << "Error Create Table" << std::endl;
		sqlite3_free(messageError);
	}
	else
		cout << "Table created Successfully" << std::endl;

	//*************************************
	// Populating courses table
	//*************************************
	string sql("INSERT INTO COURSES VALUES(1, 'ADA', 'LOVELACE', 1815);"
		"INSERT INTO PROGRAMMER VALUES(2, 'GRACE', 'HOPPER', 1906);"
		"INSERT INTO PROGRAMMER VALUES(3, 'MARY KENNETH', 'KELLER', 1913);"
		"INSERT INTO PROGRAMMER VALUES(4, 'EVELYN', 'BOYD GRANVILLE', 1924);"
		"INSERT INTO PROGRAMMER VALUES(6, 'CAROL', 'SHAW', 1955);"
	);

	// execute the command
	exit = sqlite3_exec(DB, sql.c_str(), NULL, 0, &messageError);

	if (exit != SQLITE_OK)
	{
		std::cerr << "Error Insert" << std::endl;
		sqlite3_free(messageError);
	}
	else
		std::cout << "Records created Successfully!" << std::endl;


		
	/***********************************************
    print all data in the table with SELECT * FROM
	create string with query then execute
	**********************************************/
	
	string query = "SELECT * FROM PROGRAMMER;";

	cout << endl << query << endl;		//print the string to screen

	// you need the callback function this time since there could be multiple rows in the table
	sqlite3_exec(DB, query.c_str(), callback, NULL, NULL);

	sqlite3_close(DB);
	

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