#pragma once
#include "User.h"
class Instructor :
    public User
{

public:
    //Constructor
    Instructor(string first, string last, int id);

    //Methods
    string search_course(string search);
    void print_schedule();
    void print_classlist();

    //Destructor
    ~Instructor();
};

