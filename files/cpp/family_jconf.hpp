#include <deque>
#include <string>
#include "children_jconf.hpp"

class family_jconf
{
public:
	string husband;
	string wife;
	vector<children_jconf> children;
	bool house;
	vector<string> hobbies;
	
	family_jconf(char * family_json);
	~family_jconf();
	char * create_json();
	
}