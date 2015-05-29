#pragma once
using namespace std;
#include <map>
#include "ext_string.h"
class Dict
{
public:
	Dict(void);
	~Dict(void);
	static Dict *SharedInstance();
	void FiveTupleConvertIndex(string sip,string dip,u_short sport,u_short dport,byte prototype);
	int SetFiveTupleMap(string sip,string dip,u_short sport,u_short dport,byte prototype);
private:
	static Dict *_instance;
	byte *dictindex;
	map<byte[13],int> fivetuplemap;
	map<byte[13],int>::iterator fivetupleit;
};