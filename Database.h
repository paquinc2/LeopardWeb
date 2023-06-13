#pragma once
class Database
{

protected:
	const char* db_name;

public:
	
	//Constructor
	Database(const char* db);

	//Methods
	int db_script();
};

