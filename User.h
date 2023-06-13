#pragma once
#include <string>
using std::string;

class User
{

protected:
	//Attributes
	string firstname;
	string lastname;
	int user_id;


public:
	//Constructor
	User(string first, string last, int id);

	//Setters
	void set_firstname(string first);
	void set_lastname(string last);
	void set_ID(int id);
	//Getters
	string get_firstname();
	string get_lastname();
	int get_ID();
	//Print
	void user_info();

	//Destructor
	~User();

};

