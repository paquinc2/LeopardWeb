#include "Admin.h"
#include <iostream>

using std::cout;

//Constructor
Admin::Admin(string first, string last, int id) : User(first, last, id) {

}

//Methods
string Admin::search_course(int CRN) {
	cout << "Admin search_course called\n";
	return "Course";
}
string Admin::search_roster(int CRN) {
	cout << "Admin search_roster called\n";
	return "Course";
}
void Admin::add_course() {
	cout << "Admin add_course called\n";
}
void Admin::remove_course() {
	cout << "Admin remove_course called\n";
}
//Might just call by name instead, but this is a possible avenue
void Admin::add_user() {
	cout << "Admin add_user called\n";
}
void Admin::remove_user(int ID) {
	cout << "Admin remove_user called\n";
}
void Admin::add_student() {
	cout << "Admin add_student called\n";
}
void Admin::remove_student(int ID) {
	cout << "Admin remove_student called\n";
}
void Admin::print_roster() {
	cout << "Admin print_roster called\n";
}
void Admin::print_courses() {
	cout << "Admin print_courses called\n";
}

//Destructor
Admin::~Admin() {

}