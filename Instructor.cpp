#include "Instructor.h"
#include <iostream>

using std::cout;

//Constructor
Instructor::Instructor(string first, string last, int id) : User(first, last, id) {

}

//Methods
string Instructor::search_course(string search) {
	cout << "Instructor search_course called\n";
	return search;
}
void Instructor::print_schedule() {
	cout << "Instructor print_schedule called\n";
}
void Instructor::print_classlist() {
	cout << "Instructor print_classlist called\n";
}

//Destructor
Instructor::~Instructor() {

}