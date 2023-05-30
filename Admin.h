#pragma once
#include "User.h"
#include "Student.h"
class Admin :
    public User
{

public:
    //Constructor
    Admin(string first, string last, int id);

    //Methods
    string search_course(string search);
    string search_roster(string search);
    void add_course(string course);
    void remove_course(string course);
    void add_user();
    void remove_user(int id);
    void add_student();
    void remove_student(int id);
    void print_roster();
    void print_courses();

    //Destructor
    ~Admin();
};

