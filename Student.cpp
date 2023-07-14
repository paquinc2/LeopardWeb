#include "Student.h"
#include <iostream>

using std::cout;

//Constructor
Student::Student(string first, string last, int id) : User(first, last, id) {

}

//Methods
string Student::search_course(int CRN) {
	cout << "Student search_course called\n";
	return "Course name";
}
void Student::add_course(int CRN) {
	cout << "Student add_course called\n";
}
void Student::remove_course(int CRN) {
	cout << "Student remove_course called\n";
}
void Student::print_schedule() {
	cout << "Student print_schedule called\n";
}

//Destructor
Student::~Student() {

}