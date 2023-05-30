#include "User.h"
#include <iostream>

using std::cout;

//Construtor
User::User(string first, string last, int id) {
	firstname = first;
	lastname = last;
	user_id = id;
}

//Setters
void User::set_firstname(string first) {
	firstname = first;
}
void User::set_lastname(string last) {
	lastname = last;
}
void User::set_ID(int id) {
	user_id = id;
}
//Getters
string User::get_firstname() {
	return firstname;
}
string User::get_lastname() {
	return lastname;
}
int User::get_ID() {
	return user_id;
}
//Print
void User::user_info() {
	cout << "This user's name is " << firstname << " " << lastname << " and their User ID is " << user_id << "\n";
}

//Destructor
User::~User() {

}