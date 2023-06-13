#pragma once
#include "User.h"
class Student :
    public User
{

public:
    //Constructor
    Student(string first, string last, int id);

    //Methods
    string search_course(string search);
    void add_course(string course);
    void remove_course(string course);
    void print_schedule();

    //Destructor
    ~Student();
};

