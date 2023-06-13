#include "Database.h"
#include "sqlite3.h"
#include <iostream>

using std::cout;
using std::cin;

using namespace std;

Database::Database(const char* db) {
	db_name = db;
}

/*************************************************************************************************
 The callback() function is invoked for each result row coming out of the evaluated SQL statement
 1st argument - the 4th argument provided by sqlite3_exec() and is typically not used
 2nd argument - number of columns in the result
 3rd argument - an array of strings containing the fields in that row
 4th argument - an array of strings containing the names of the columns
*************************************************************************************************/
int callback(void* data, int argc, char** argv, char** azcolname) {
	int i;

	for (i = 0; i < argc; i++)
	{
		printf("%s = %s\n", azcolname[i], argv[i] ? argv[i] : "null");
	}

	printf("\n");

	return 0;
}

int Database::db_script() {

		//*************************************
		// Define and open the database
		//*************************************
		sqlite3* DB;
		int exit = 0;
		exit = sqlite3_open(db_name, &DB);

		if (exit) {
			std::cerr << "Error open DB " << sqlite3_errmsg(DB) << std::endl;
			return (-1);
		}
		else
			std::cout << "Opened Database Successfully!" << std::endl;

		//*************************************
		// Creating a course table
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
		string sql("INSERT INTO COURSES VALUES(33946, 'ADVANCED DIGITAL CIRCUIT DESIGN', 'ELECTRICAL ENGINEERING', '8:00 AM - 9:20 AM', 'WEDNESDAY, FRIDAY', 'SUMMER', 2023, 4);"
			"INSERT INTO COURSES VALUES(33950, 'APPLIED PROGRAMMING CONCEPTS', 'ELECTRICAL ENGINEERING', '8:00 AM - 9:50 AM', 'TUESDAY, THURSDAY', 'SUMMER', 2023, 3);"
			"INSERT INTO COURSES VALUES(33817, 'ALGORITHMS', 'COMPUTER SCIENCE', '11:00 AM - 12:20 PM', 'MONDAY, WEDNESDAY', 'SUMMER', 2023, 4);"
			"INSERT INTO COURSES VALUES(33955, 'COMPUTER NETWORKS', 'ELECTRICAL ENGINEERING', '12:30 PM - 1:50 PM', 'MONDAY, WEDNESDAY', 'SUMMER', 2023, 4);"
			"INSERT INTO COURSES VALUES(33959, 'SIGNALS AND SYSTEMS', 'ELECTRICAL ENGINEERING', '1:00 PM - 2:50 PM', 'TUESDAY, THURSDAY', 'SUMMER', 2023, 4);"
		);

		exit = sqlite3_exec(DB, sql.c_str(), NULL, 0, &messageError);

		if (exit != SQLITE_OK)
		{
			std::cerr << "Error Insert" << std::endl;
			sqlite3_free(messageError);
		}
		else
			std::cout << "Records created Successfully!" << std::endl;

		//*************************************
		// Removing an instructor
		//*************************************
		sql = "DELETE FROM INSTRUCTOR WHERE ID = 20006;";
		exit = sqlite3_exec(DB, sql.c_str(), NULL, 0, &messageError);

		if (exit != SQLITE_OK) {
			std::cerr << "Error DELETE" << std::endl;
			sqlite3_free(messageError);
		}
		else
			std::cout << "Record deleted Successfully!" << std::endl;

		//*************************************
        // Adding two students
        //*************************************
		sql = ("INSERT INTO STUDENT VALUES(10011, 'Dylan', 'OBrien', 2024, 'BSCO', 'obriend7');"
			"INSERT INTO STUDENT VALUES(10012, 'Collin', 'Paquin', 2024, 'BSCO', 'paquinc');"
		);

		exit = sqlite3_exec(DB, sql.c_str(), NULL, 0, &messageError);

		if (exit != SQLITE_OK)
		{
			std::cerr << "Error Insert" << std::endl;
			sqlite3_free(messageError);
		}
		else
			std::cout << "Records created Successfully!" << std::endl;

		//*************************************
        // Modifying Admin
        //*************************************

		sql = "UPDATE ADMIN SET TITLE = 'Vice-President' WHERE NAME = 'Vera';";
		exit = sqlite3_exec(DB, sql.c_str(), NULL, 0, &messageError);

		if (exit != SQLITE_OK)
		{
			std::cerr << "Error Update" << std::endl;
			sqlite3_free(messageError);
		}
		else
			std::cout << "Records updated Successfully!" << std::endl;

		/***********************************************
		print all data in the table with SELECT * FROM
		create string with query then execute
		**********************************************/

		string query = "SELECT * FROM STUDENT;";
		cout << endl << query << endl;		//print the string to screen
		// you need the callback function this time since there could be multiple rows in the table
		sqlite3_exec(DB, query.c_str(), callback, NULL, NULL);

		query = "SELECT * FROM INSTRUCTOR;";
		cout << endl << query << endl;		//print the string to screen
		sqlite3_exec(DB, query.c_str(), callback, NULL, NULL);

		query = "SELECT * FROM ADMIN;";
		cout << endl << query << endl;		//print the string to screen
		sqlite3_exec(DB, query.c_str(), callback, NULL, NULL);

		query = "SELECT * FROM COURSES;";
		cout << endl << query << endl;		//print the string to screen
		sqlite3_exec(DB, query.c_str(), callback, NULL, NULL);

		sqlite3_close(DB);
}
