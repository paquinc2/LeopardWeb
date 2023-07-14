#pragma once
#include "User.h"
class Student :
    public User
{

public:
    //Constructor
    Student(string first, string last, int id);

    //Methods
    string search_course(int CRN);
    void add_course(int CRN);
    void remove_course(int CRN);
    void print_schedule();

    //Destructor
    ~Student();
};

