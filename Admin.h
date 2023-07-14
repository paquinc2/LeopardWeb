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
    string search_course(int CRN);
    string search_roster(int CRN);
    void add_course();
    void remove_course();
    void add_user();
    void remove_user(int ID);
    void add_student();
    void remove_student(int ID);
    void print_roster();
    void print_courses();

    //Destructor
    ~Admin();
};

